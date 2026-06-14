# TECH-stitch-worked-examples

## Table of Contents

- [Usage](#usage)
- [Examples](#examples)
- [Scenario 1 — MCP reachable, pull tokens](#scenario-1-mcp-reachable-pull-tokens)
- [Scenario 2 — MCP absent, fallback](#scenario-2-mcp-absent-fallback)

## Usage

The skill is invoked indirectly through `amw-design-md-author-agent`, `amw-wireframe-builder-agent`, or `amw-design-extract` when those agents detect a Stitch trigger and route to this skill. There is no user-facing slash command at this scaffold stage — when the MCP becomes available a `/amw-stitch-sync` command may be added in a later wave.

A direct invocation pattern (for sub-agents already inside Phase B) looks like this in pseudocode:

```text
1. probe = call mcp__stitch__ping or mcp__stitch__list_workspaces(limit=1)
2. if probe is error:
       emit fallback line and stop
3. operation = classify_trigger(user_phrase)
4. raw = call the matching mcp__stitch__* tool
5. canonical = translate(raw, operation)
6. write canonical to project output path
7. return path
```

The canonical tool-name mapping for steps 4 and 5 lives in [TECH-stitch-design-language](./TECH-stitch-design-language.md). Edit that file, not the SKILL.md, when the upstream Stitch MCP changes its surface.

## Examples

Two illustrative scenarios — both run end-to-end, both exercise the fallback when the MCP is absent.

### Scenario 1 — MCP reachable, pull tokens

User says: "pull design tokens from stitch workspace acme-marketing into the project."

1. Skill probes. Probe returns `{ "workspaces": ["acme-marketing", "acme-internal"] }`. Success.
2. Skill classifies intent as `pull-tokens`.
3. Skill calls the documented Stitch token-read tool (canonical name in TECH-stitch-design-language.md).
4. Skill translates the returned payload to W3C tokens JSON.
5. Skill writes `<project>/design/tokens/tokens.w3c.json` and emits the path.
6. Skill reports completion with the workspace ID, the tool version, and the artifact path.

### Scenario 2 — MCP absent, fallback

User says: "pull design tokens from stitch."

1. Skill probes. Probe returns "tool not found". Fail.
2. Skill emits the fallback line.
3. Caller (likely `amw-design-md-extractor-agent`) reads the fallback line and consults [TECH-stitch-fallback-strategy](./TECH-stitch-fallback-strategy.md).
4. Caller asks the user for a URL or codebase to extract from, then routes to `amw-design-extract` or `amw-design-md-from-url.sh`.
5. The Stitch-integration skill plays no further role in this run.
