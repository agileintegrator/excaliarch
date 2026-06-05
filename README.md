![excalidraw-claude-archi](images/excalidraw-claude-archi.png "Excaliarch concept logo")

# Excaliarch

Excaliarch is a set of tools and methods that use Excalidraw to create, maintain, and exploit Archimate content.

**License**: [MIT](LICENSE) — © 2025 agileintegrator. Public repository.

## Rationale and Scope

The goal of the Excaliarch is to speed up and improve the accuracy of archimate models and their resulting deployments.

Spoiler: excaliarch relies on Claude 4 sonnet to convert archimate content in excalidraw to runnable software.

Ultimately, we hope Excaliarh will cover the deloyment of any software resources or data assets that you can model in Archimate, but initially we focus on services to support data and integration products, namely:
 - physical schemas for persistent stores
 - the data that goes in the persistent stores
 - APIs

## Getting started

The fastest way to use Excaliarch today is the bundled **Agent Skill** — see [Skill](#skill) below for install routes — then ask Claude to read one of your Excalidraw files:

> *"Use the excaliarch skill on `architecture/my-diagram.excalidraw` and tell me what's in it."*

Claude lifts the diagram into an ArchiMate-domain JSON model (concepts, relationships, annotations) and answers in those terms.

For pipelines, CI, or any non-agent consumer, the parser is also a standalone Python script with no third-party dependencies:

```bash
python3 .claude/skills/excaliarch/reader.py <file.excalidraw>
```

It prints the model as JSON on stdout.

## Guidelines

See the [Excaliarch Usage Guidelines](excaliarch-template-guidelines.md) for the labelling convention and modelling notation the reader expects.

## Skill

This repo ships an Anthropic [Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) at [`.claude/skills/excaliarch/`](.claude/skills/excaliarch/). The Agent Skill spec is cross-platform, so the same `SKILL.md` + `reader.py` works on every Claude surface — though Custom Skills don't auto-sync across surfaces (Anthropic's current limitation), so you install once per channel.

**Install routes**

- **Claude Code (CLI)** — auto-discovered when a session starts in this repo. To use it from any directory, symlink once:
  ```bash
  ln -s "$PWD/.claude/skills/excaliarch" ~/.claude/skills/excaliarch
  ```
- **claude.ai web** (Pro, Max, Team, or Enterprise; code execution enabled) — ZIP the `.claude/skills/excaliarch/` directory and upload via the Skills section of your settings. The current UI surfaces this under *Settings → Capabilities → Skills* or *Customize → Skills* depending on the version you have.
- **Claude API** — upload via the [Skills API](https://platform.claude.com/docs/en/build-with-claude/skills-guide) (`/v1/skills` endpoints). The API runtime has no network access, but the reader doesn't need it.
- **Marketplace install** *(planned)* — `/plugin marketplace add agileintegrator/excaliarch` once a `.claude-plugin/plugin.json` manifest is added at the repo root.

See [SKILL.md](.claude/skills/excaliarch/SKILL.md) for trigger conditions, the labelling convention, and the JSON model schema. Known gaps and follow-ups are tracked in [TODO.md](.claude/skills/excaliarch/TODO.md). v1 is read-only; the writing direction is planned.

## Artefacts (git)

 - excalidraw source diagrams
 - rendered images
 - physical schemas (planned)
