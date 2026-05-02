---
name: amw-design-md-from-url
description: "Extract a Variant 1 DESIGN.md from a live URL by capturing the page through amw-dev-browser, reading computed styles + DOM landmarks, and emitting canonical YAML frontmatter + prose sections. Spawns amw-design-md-extractor-agent (input_type=url). Faithful transcription only — never invents tokens not present in the source."
---

# /amw-design-md-from-url

Pipe a live URL through the plugin's `amw-dev-browser` primitive and `bin/amw-design-md-from-url.sh` so a Variant 1 DESIGN.md captures the actual computed styles and meta-content of the page. This is the URL-based extraction path (peer to `/amw-design-md-from-tailwind` and `/amw-design-md-from-codebase`).

## Arguments

`$ARGUMENTS` should contain at minimum a URL. Optional flags:

- `--out <path>` — output DESIGN.md path (default: `./DESIGN.md`)
- `--wait-for-selector <css>` — instruct dev-browser to wait until the selector resolves (use for SPAs)
- `--companions css,json,inventory,prompt` — emit companion files alongside DESIGN.md
- `--no-contrast` — skip the WCAG contrast check (default: run it)

If `$ARGUMENTS` is empty or not a valid URL, ask: *"Which URL should I extract DESIGN.md from?"* and stop.

## Action

### 1. Prerequisite check

Confirm `dev-browser` is on PATH. If missing, point at `/amw-init` (step that vendors `dev-browser`).

### 2. Spawn `amw-design-md-extractor-agent`

Pass the structured input:

```yaml
input_type: "url"
url: "<the-url>"
output_path: "<--out value or ./DESIGN.md>"
companion_targets: ["<--companions list>"]
contrast_check: true | false
strict_lint: true
```

The agent runs `bin/amw-design-md-from-url.sh`, then the lint gate and contrast check, then optionally companion generation.

### 3. Surface the result

After the agent returns:

- DESIGN.md path
- Lint status (PASS / PARTIAL)
- Contrast warnings, if any
- Companion file paths
- Sidecar `<DESIGN.md>.extraction-notes.md` path if produced

If `status=partial` because of an SPA-loading-skeleton extraction, present the suggested fix (re-run with `--wait-for-selector`) and stop.

## Non-negotiables

- **dev-browser is the only browser-automation backend.** No Playwright, no Puppeteer, no Chrome DevTools MCP.
- **Respect robots.txt and X-Robots-Tag.** If the site disallows automated access, stop with an explicit message.
- **No login walls.** Public URLs only; if the URL redirects to a sign-in page, stop and ask for a public alternative.
- **Faithful transcription.** Tokens absent in the source remain `# TODO:` in the output — they are never invented.
- **Lint gate is mandatory.**

## Failure modes

- URL unreachable or timeout → agent returns `status=partial`; surface and stop.
- Site is JS-heavy SPA returning a loading skeleton → re-run suggestion with `--wait-for-selector`.
- Contrast check flags multiple failing pairs → surface as warnings; do not modify the source's design choices.

## Cross-references

- [amw-design-md-extractor-agent](agents/amw-design-md-extractor-agent.md)
- [TECH-07-url-extraction](skills/amw-design-md/references/TECH-07-url-extraction.md)
- [TECH-09-multipage-extraction](skills/amw-design-md/references/TECH-09-multipage-extraction.md)
- [SKILL](skills/amw-dev-browser/SKILL.md)
- `bin/amw-design-md-from-url.sh`
- `bin/amw-design-md-lint.sh`
- `bin/amw-design-md-contrast.py`
