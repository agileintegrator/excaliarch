# Excaliarch skill — TODO

Follow-ups deferred from the v1 shakedown against
`credit-market-datamart/architecture/credit-market-datamart.excalidraw`
(2026-06-05). v1 reader and SKILL.md left as-is; capture here, decide later.

## Convention gaps (settle in `excaliarch-template-guidelines.md` first)

- **Stereotypes are not in the labelling convention.** Real diagrams use
  labels like `"<<OpenAPI>>\nArtifact: TicDataOpenAPI"`. The reader
  faithfully splits on the first `:`, producing
  `archimate_type = "<<OpenAPI>>\nArtifact"` — accurate but ugly. Extend
  the guidelines to specify how stereotypes are written, then teach the
  parser to peel `<<stereotype>>` into its own field on the concept.
- **No way to mark a closed shape as structural / decoration.** The
  shakedown found 14 / 24 closed shapes with no typed label — a mix of
  Groupings, visual panels, and possibly Junctions (one was an ellipse).
  Reader can't tell "intentionally untyped" from "author forgot the
  label". Add a convention for marking structural-only shapes, then split
  `decorations[]` out of `concepts[]` in the reader's output.
- **Visual key for the 12 ArchiMate 3.1 relationship types.** The
  guidelines have images but no explicit
  `(stroke_style, stroke_width, start_arrowhead, end_arrowhead) →
  archimate_kind` table. Add the table, then teach the reader to fill
  `relationships[].archimate_kind` from it. Until that table exists,
  leave `archimate_kind: null` as v1 does.

## Reader improvements (no convention change needed)

- **Emit a normalised name alongside the raw one.** Real labels contain
  visual soft-breaks (`"CreditMarketData\nmartService"`). Keep `name`
  verbatim for round-trip, add `name_normalised` with whitespace
  collapsed for downstream consumers.
- **Flag unbound relationships in the SKILL.md interpretation rules.**
  Half the relationships in the shakedown diagram had at least one
  endpoint not snapped to a shape — usually a real authoring bug. The
  reader already surfaces this via `from` / `to: null`; just tell the
  agent in `SKILL.md` to report unbound relationships back to the user
  rather than silently skip them.

## Bigger extensions

- **Writing direction (v2).** Generate an Excaliarch-conformant
  `.excalidraw` file from an ArchiMate model. Already flagged in
  `SKILL.md` under Scope.
- **Decide the user-global stub story.** The stub at
  `~/.claude/skills/excaliarch/SKILL.md` lives only on this machine
  (it's outside any repo). If we want CLI sessions on other machines to
  resolve `excaliarch` the same way, either turn the stub into a tiny
  committed installer in this repo, or accept that the canonical
  in-repo path is the only durable surface.
