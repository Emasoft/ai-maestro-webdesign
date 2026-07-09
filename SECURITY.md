# Security Policy

`ai-maestro-webdesign` ships Claude Code skills, agents, slash commands,
one hook, and a `bin/` folder of Python/shell scripts that render SVG,
export HTML to PNG/PDF/MP4, drive browser automation via
`amw-dev-browser`, and parse/validate ASCII, HTML, SVG, and Mermaid
diagram sources. Because several of these scripts execute against
attacker-influenced input (a URL to extract design tokens from, an
uploaded HTML/SVG/Mermaid file to convert or diff), we take their
security seriously.

## Reporting a vulnerability

**Do NOT file a public GitHub issue for a vulnerability.**

Use one of these private channels instead:

1. **Preferred — GitHub Security Advisories.** Visit
   <https://github.com/Emasoft/ai-maestro-webdesign/security/advisories/new>
   and submit a private advisory. Anyone with a GitHub account can do
   this; the report is visible only to repository maintainers.
2. **Alternative — email.** Send to
   `713559+Emasoft@users.noreply.github.com` with subject
   `[security] <short description>`. Maintainer email is the
   GitHub-routed noreply address; messages reach Emasoft directly.

Please include:

- The plugin version (`cat .claude-plugin/plugin.json | jq .version`).
- The Claude Code version (`claude --version`).
- The OS + arch + Python/Node version.
- A redacted reproduction case (drop any `/Users/<name>` segments
  before submitting per the redaction convention in
  `CONTRIBUTING.md`).
- The expected vs. observed behaviour.
- Your assessment of severity (CRITICAL / MAJOR / MINOR / NIT) — your
  reasoning, not your verdict; we will reach our own conclusion but
  your reasoning saves us time.

## What we will do

| Step | Target turnaround |
|---|---|
| Acknowledge receipt | within 72 hours |
| Reproduce and triage | within 7 days |
| Develop a fix | within 30 days for CRITICAL/MAJOR; best-effort for MINOR/NIT |
| Coordinated disclosure | within 90 days of initial report (CRITICAL/MAJOR); we will work with you on the schedule |
| Credit you in the release notes | always, unless you ask not to be named |

We do not offer a bug bounty. We do offer credit, a public
acknowledgment in the release notes, and a GitHub Security Advisory
CVE if the issue warrants one.

## Scope

**In scope** (please report):

- Any path by which a `bin/` script (e.g. `amw-svg-render.py`,
  `amw-html-export.py`, `amw-diagram-ir.py`, the format
  parsers/validators) can be made to execute arbitrary shell commands,
  read/write files outside the intended output directory, or fetch a
  remote resource the caller did not request.
- Prompt-injection paths in any skill or agent instruction file that
  let untrusted content (a fetched webpage, a pasted design brief, a
  third-party DESIGN.md, an SVG/HTML file being converted) trick the
  agent into running destructive shell commands, exfiltrating local
  file contents, or silently widening its own permissions.
- Any path by which `amw-dev-browser` (the plugin's sole
  browser-automation primitive) can be driven to read local files,
  local network resources, or credentials it should not have access
  to, when only public-web browsing was requested.
- SSRF / arbitrary-URL-fetch issues in `amw-design-extract`,
  `amw-design-md-extract`, or `amw-webpage-to-diagram` (all three
  accept a user-supplied URL).
- XML/SVG parsing vulnerabilities (XXE, billion-laughs, entity
  expansion) in any script that parses SVG or HTML input
  (`amw-parse-svg-diagram.py`, `amw-html-diff.py`, etc.).
- Hardcoded secrets or credentials anywhere in the repo.
- Supply-chain issues in the plugin's declared runtime dependencies
  (`dev-browser`, `hyperframes`, the vendored `beautiful-mermaid`
  wrapper under `external/mermaid-render/`).

**Out of scope** (we welcome you to file as a feature request
instead):

- Vulnerabilities in the external tools the plugin shells out to but
  does not vendor (Playwright/Chromium, `dev-browser` CLI,
  `hyperframes`, `ffmpeg`, `cairosvg`) — please report those upstream.
  We will fast-track a version bump once a fix lands there.
- Issues in Claude Code itself — report to Anthropic.
- Theoretical issues without a working exploit path. We are happy to
  discuss those, but they go through the regular issue/discussion
  channels, not the security one.
- Output-quality issues (a generated diagram or HTML page looking
  wrong, an AI-slop pattern slipping through) — those are regular bugs,
  not security reports.

## What counts as a vulnerability vs. a bug

A vulnerability has two properties:

1. **Adversarial impact** — an attacker (via a crafted URL, a crafted
   SVG/HTML/Mermaid file, or a crafted prompt) can cause an effect a
   benign input cannot achieve.
2. **Reachable** — there is a concrete code path from an
   externally-controllable input to the impact.

If both hold, file via the security channel. If only one holds (e.g.
"this fails ungracefully but there's no attacker-controlled path to
it"), file as a regular bug.

## Disclosure policy

- We follow a **90-day coordinated-disclosure window** for
  CRITICAL/MAJOR.
- If we cannot ship a fix within 90 days, we will publish the advisory
  anyway with mitigations and recommend users disable the affected
  skill/command until a fix lands.
- If you find a fix before us, please send the patch via the security
  channel — we will integrate, credit, and release.
- If the vulnerability is being actively exploited in the wild, the
  90-day window collapses to 7 days and we will release a mitigation
  immediately even if the full fix is not ready.

## Supported versions

| Plugin version | Supported | Notes |
|---|---|---|
| `0.1.x` | ✓ active | current minor; pre-1.0, expect breaking changes between minors |
| `< 0.1` | ✗ unsupported | upgrade to the latest `0.1.x` |

`uv sync --extra dev` resolves the pinned dev toolchain; upgrading the
plugin itself is done via the Claude Code plugin manager / marketplace
update flow.

## Known design constraints (not vulnerabilities)

- Skills that use Chromium/Playwright **only for output rendering**
  (`amw-infographics/scripts/export.py`, `amw-hyperframes-bridge`, the
  HTML->PNG pipeline in `bin/amw-html-export.py`) run headless and
  render local, agent-generated HTML — they are not a general-purpose
  browsing surface. `amw-dev-browser` is the only interactive
  browsing/inspection primitive and is the one to scrutinize for
  live-page-state exposure.
- The Gemini-backed `amw-excalidraw-illustrations` skill is explicitly
  gated (documented cost, requires `$GEMINI_API_KEY`) — treat any
  report about it sending data to Google's API as expected behaviour,
  not a leak, unless the gate itself can be bypassed silently.
- PNG is output-only across the entire plugin — there is no PNG
  *parser* anywhere in `bin/`, so a malicious PNG cannot be fed back
  into the diagram-conversion pipeline as input.

If you find behaviour that *could* be considered a security boundary
but is documented above as not one, please still file via the security
channel — we may have under-promised in the docs.

## Credits

We thank every researcher who has reported responsibly. Names are
listed in `ACKNOWLEDGMENTS.md` and in the relevant release notes.
