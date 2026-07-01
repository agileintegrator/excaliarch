"""Excaliarch reader.

Lifts an Excaliarch-authored Excalidraw diagram into an ArchiMate-domain
model that an agent (or any caller) can reason over directly.

The Excaliarch labelling convention encodes an ArchiMate concept as a
closed shape whose bound text reads ``"<ArchiMate Type>:\\n<instance name>"``.
Lines and arrows between those shapes encode ArchiMate 3.1 relationships.
Free-standing text becomes diagram annotation.

Run as ``python3 reader.py <file>`` to print the model as JSON on stdout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterable

CONCEPT_SHAPE_TYPES = frozenset({"rectangle", "ellipse", "diamond"})
EDGE_SHAPE_TYPES = frozenset({"arrow", "line"})


def read_diagram(path: str | Path) -> dict[str, Any]:
    """Return the ArchiMate-domain model for the Excalidraw file at *path*."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    live = [e for e in payload.get("elements", []) if not e.get("isDeleted")]
    by_id: dict[str, dict[str, Any]] = {e["id"]: e for e in live}

    used_text_ids: set[str] = set()

    concepts = list(_extract_concepts(live, by_id, used_text_ids))
    relationships = list(_extract_relationships(live, by_id, used_text_ids))
    annotations = list(_extract_annotations(live, used_text_ids))

    return {
        "source": str(path),
        "concepts": concepts,
        "relationships": relationships,
        "annotations": annotations,
    }


def _extract_concepts(
    live: Iterable[dict[str, Any]],
    by_id: dict[str, dict[str, Any]],
    used_text_ids: set[str],
) -> Iterable[dict[str, Any]]:
    for el in live:
        if el.get("type") not in CONCEPT_SHAPE_TYPES:
            continue
        label, text_id = _bound_label(el, by_id)
        if text_id:
            used_text_ids.add(text_id)
        stereotypes, archimate_type, name = _parse_excaliarch_label(label)
        yield {
            "id": el["id"],
            "stereotypes": stereotypes,
            "archimate_type": archimate_type,
            "name": name,
            "shape": el["type"],
            "position": [_round_or_none(el.get("x")), _round_or_none(el.get("y"))],
            "size": [_round_or_none(el.get("width")), _round_or_none(el.get("height"))],
            "stroke": el.get("strokeColor"),
            "fill": el.get("backgroundColor"),
        }


def _extract_relationships(
    live: Iterable[dict[str, Any]],
    by_id: dict[str, dict[str, Any]],
    used_text_ids: set[str],
) -> Iterable[dict[str, Any]]:
    for el in live:
        if el.get("type") not in EDGE_SHAPE_TYPES:
            continue
        label, text_id = _bound_label(el, by_id)
        if text_id:
            used_text_ids.add(text_id)
        yield {
            "id": el["id"],
            "from": _endpoint_id(el.get("startBinding")),
            "to": _endpoint_id(el.get("endBinding")),
            "stroke_style": el.get("strokeStyle"),
            "stroke_width": el.get("strokeWidth"),
            "start_arrowhead": el.get("startArrowhead"),
            "end_arrowhead": el.get("endArrowhead"),
            "label": label,
            "archimate_kind": None,
        }


def _extract_annotations(
    live: Iterable[dict[str, Any]],
    used_text_ids: set[str],
) -> Iterable[dict[str, Any]]:
    for el in live:
        if el.get("type") != "text":
            continue
        if el["id"] in used_text_ids:
            continue
        if el.get("containerId"):
            continue
        body = (el.get("text") or "").strip()
        if not body:
            continue
        yield {
            "text": body,
            "position": [_round_or_none(el.get("x")), _round_or_none(el.get("y"))],
        }


def _bound_label(
    el: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
) -> tuple[str | None, str | None]:
    """Return ``(text, text_element_id)`` for the first live text bound to *el*."""
    for ref in el.get("boundElements") or ():
        if ref.get("type") != "text":
            continue
        child = by_id.get(ref.get("id"))
        if child is None or child.get("isDeleted"):
            continue
        return (child.get("text") or "").strip() or None, child["id"]
    return None, None


def _parse_excaliarch_label(
    label: str | None,
) -> tuple[list[str], str | None, str | None]:
    """Split a label into ``(stereotypes, type, name)``.

    Excaliarch labels can optionally carry one or more UML-style
    stereotypes on their own lines above the ``"<Type>: <name>"`` line —
    e.g. ``"<<OpenAPI>>\\nArtifact: TicDataOpenAPI"``. Leading ``<<…>>``
    lines are peeled off into the stereotypes list in document order;
    the remainder is split on the first ``":"`` into type and name. A
    label with no ``:`` is treated as name-only and returns
    ``type=None``. An empty or missing label returns
    ``([], None, None)``.
    """
    if not label:
        return [], None, None
    lines = label.split("\n")
    stereotypes: list[str] = []
    while lines:
        stripped = lines[0].strip()
        if (
            stripped.startswith("<<")
            and stripped.endswith(">>")
            and len(stripped) > 4
        ):
            stereotypes.append(stripped[2:-2].strip())
            lines = lines[1:]
        else:
            break
    remainder = "\n".join(lines).strip()
    if not remainder:
        return stereotypes, None, None
    head, sep, tail = remainder.partition(":")
    if not sep:
        return stereotypes, None, head.strip() or None
    return stereotypes, (head.strip() or None), (tail.strip() or None)


def _endpoint_id(binding: dict[str, Any] | None) -> str | None:
    if not binding:
        return None
    return binding.get("elementId")


def _round_or_none(value: Any) -> int | None:
    if isinstance(value, (int, float)):
        return round(value)
    return None


def _cli(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: reader.py <file.excalidraw>", file=sys.stderr)
        return 2
    model = read_diagram(argv[1])
    json.dump(model, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv))
