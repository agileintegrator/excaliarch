# Excaliarch skill — TODO

Follow-ups deferred from the v1 shakedown against
`credit-market-datamart/architecture/credit-market-datamart.excalidraw`
(2026-06-05). v1 reader and SKILL.md left as-is; capture here, decide later.

## Convention gaps (settle in `excaliarch-template-guidelines.md` first)

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
- **Distribution: wrap as a plugin for marketplace install.** Anthropic's
  Agent Skill spec is cross-platform (Claude Code CLI, claude.ai web,
  Claude API, Claude apps), but Custom Skills don't auto-sync across
  surfaces — users install once per channel. To enable Claude Code
  marketplace install (`/plugin marketplace add agileintegrator/excaliarch`
  → `/plugin install excaliarch`), add a `.claude-plugin/plugin.json`
  manifest at the repo root. For claude.ai web the install today is
  "ZIP `.claude/skills/excaliarch/` and upload via Settings →
  Capabilities → Skills" (UI label varies — also surfaced as
  Customize → Skills depending on version). The user-global symlink we
  keep on Timo's Mac is now a CLI convenience, not the canonical
  distribution path.

- **Validate the skill on each surface.** SKILL.md is spec-compliant
  on paper (`name` lowercase ≤64, `description` ≤1024, helper script
  pattern matches docs) but the cross-surface install routes are
  un-tested end-to-end. First time anyone uploads to claude.ai or the
  API, confirm the reader executes in that sandbox (it uses Python
  stdlib only so should work, but "should" is doing real work in that
  sentence).

## Done

- **Stereotypes** *(2026-06-05).* Convention added to
  `excaliarch-template-guidelines.md` (new "Stereotypes (optional)"
  subsection under Naming). Reader's `_parse_excaliarch_label` now
  peels leading `<<…>>` lines off the label and emits a `stereotypes`
  list on each concept (empty when none). Verified on the
  credit-market-datamart shakedown — the three stereotyped `Artifact`
  concepts now come through with clean `archimate_type: "Artifact"`
  and the stereotype on its own field.
