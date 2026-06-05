---
name: excaliarch
description: Read and interpret an Excaliarch-template Excalidraw file — a diagram that encodes ArchiMate 3.1 concepts and relationships using the Excaliarch "<Type>: <name>" labelling convention. Invoke when the user mentions "excaliarch", or when asked to read / interpret / summarise a .excalidraw file whose shape labels follow this convention.
---

# Excaliarch reader (v1, read-only)

Excaliarch stores ArchiMate models inside ordinary Excalidraw JSON. The
convention this skill expects:

- An ArchiMate concept is a closed shape (`rectangle`, `ellipse`, or
  `diamond`) whose bound text element reads `"<ArchiMate Type>:\n<instance
  name>"` — e.g. `"Business process:\nOrder Intake"`,
  `"App Service: API Gateway Service"`.
- A relationship is a `line` or `arrow` whose `startBinding.elementId` and
  `endBinding.elementId` point at concept shapes.
- Standalone text (a `text` element with no `containerId` and not bound by
  any shape) is diagram annotation, not part of the model.

The 12 ArchiMate 3.1 relationship types are visually distinguished by line
style and arrowhead. The canonical visual key for this repo lives in
`excaliarch-template-guidelines.md`. Use that document — not assumptions —
when classifying relationships.

## How to use

Run the bundled reader to lift a diagram into a structured model:

```bash
python3 .claude/skills/excaliarch/reader.py <path-to-file.excalidraw>
```

The reader prints a single JSON document with three arrays:

- `concepts[]` — `id`, `archimate_type`, `name`, `shape`, `position`,
  `size`, `stroke`, `fill`. `archimate_type` is the text before the first
  `:` in the bound label; `name` is what follows.
- `relationships[]` — `id`, `from`, `to` (concept ids), `stroke_style`,
  `stroke_width`, `start_arrowhead`, `end_arrowhead`, `label`,
  `archimate_kind` (left `null`; classify downstream from the styling
  fields against the guidelines).
- `annotations[]` — `text`, `position`. Standalone text only.

If a label has no `:`, `archimate_type` is `null` and the whole label
becomes `name`. If a relationship's endpoint is unbound, the corresponding
`from` / `to` is `null`.

For small diagrams, reading the file inline (Read tool) is also fine — but
prefer the reader for anything non-trivial: it skips deleted elements,
resolves bound text, and gives you the ArchiMate-level model directly.

## Interpreting the model

1. List `concepts` grouped by `archimate_type` to give the user the
   inventory of the diagram.
2. For each `relationship`, resolve `from` / `to` against the concept
   list, then classify `archimate_kind` from `stroke_style`,
   `stroke_width`, and arrowheads using the visual key in
   `excaliarch-template-guidelines.md`. If the visual key is silent or
   ambiguous for a given combination, report the raw styling fields back
   to the user rather than guessing.
3. Surface `annotations` separately — they are author commentary, not
   model content.

## Scope

v1: read-only. Writing diagrams from an ArchiMate model is a planned
extension and out of scope here.

## Example output

For a small architecture diagram, the model the reader prints looks
like this (trimmed):

```json
{
  "source": "architecture/credit-market-datamart.excalidraw",
  "concepts": [
    {
      "id": "WLPSjmoCErhICnRzcSKwl",
      "archimate_type": "App component",
      "name": "CreditMarketDatamart",
      "shape": "rectangle",
      "position": [580, 240],
      "size": [220, 80],
      "stroke": "#1971c2",
      "fill": "#a5d8ff"
    }
  ],
  "relationships": [
    {
      "id": "rel-1",
      "from": "WLPSjmoCErhICnRzcSKwl",
      "to": "AbCDeFg",
      "stroke_style": "solid",
      "stroke_width": 2,
      "start_arrowhead": null,
      "end_arrowhead": "triangle_outline",
      "label": null,
      "archimate_kind": null
    }
  ],
  "annotations": []
}
```

## Known limitations

See [TODO.md](TODO.md) alongside this file for the shakedown follow-ups
— stereotyped labels, unbound relationships, name normalisation, the
visual-key classification table that would let the reader fill
`relationships[].archimate_kind`. None of these gate v1 reading;
they shape v2.
