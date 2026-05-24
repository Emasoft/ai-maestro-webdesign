# Error Handling — common symptoms and fixes

## Table of Contents

- [Symptom-to-fix table](#symptom-to-fix-table)
- [Cross-references](#cross-references)

## Symptom-to-fix table

When an infographic build delivers the wrong result, route the symptom to the matching cause and fix.

| Symptom | Likely cause | Fix |
|---|---|---|
| Output looks like a SaaS landing page | Uniform card grids, generous whitespace, paragraph descriptions, no tables/arrows | Replace card grids with `bullet_panel` + `dense_table`. Add directional arrow connectors between sections. |
| Output looks like a dashboard | Data-sparse, too much empty space, body font 14–16px | Tighten to 11–13px body, 12–16px padding. Add content blocks until 8+ on portrait-medium. |
| Output looks like a slide deck | Each section is one idea surrounded by whitespace | Merge sparse sections, increase density, use mixed layouts per section. |
| "Component demo" repetition | Same component type repeated 3+ times in a row | Apply Section Variety Rule — at least 3 different component types across 4+ sections. |
| Floating-islands sections | No arrows/connectors showing how sections relate | Add labeled arrows between related sections. Use consistent color coding to signal linked concepts. |
| Playwright missing at export | `/amw-init` not run or `playwright install chromium` skipped | Run `/amw-init` to install Playwright + Chromium. |
| CDN fonts fall back to Times/Arial | Offline environment, or Google Fonts blocked | `html-export.py` defaults to spinning up a local HTTP server; confirm the host can reach `fonts.googleapis.com`. Fallback: use system-font stack and accept degraded editorial feel. |
| Fabricated stats in output | Skill guessed numbers not in the brief | Reject; regenerate using only the user's supplied data. Every non-user number is a Rule 1 violation. |
| Wrong template chosen | User intent mapped to a generic template when a playbook fits | Re-read the Template Selection table in [_template-registry](_template-registry.md); if the content type is one of the 5 playbooks (token-economics, crypto-explainer, game-overview, ecosystem, airdrop-guide), override and use the playbook template. |
| Output is light mode when user wanted dark | Wording like "whitepaper" or "report" was misread as a light-mode signal | Dark is the default. Light mode requires an explicit user request ("light background", "white background", "print-ready report"). |
| Build is interrupted mid-render (browser crash) | Playwright Chromium runaway or OOM | Re-run with `--scale 1` to reduce memory; if still failing, use the staged render mode (one component at a time via Mode A). |
| Export produces fonts as black rectangles in PDF | PDF generator hasn't subset the font | Run `bin/amw-html-export.py` with `--embed-fonts` flag; if missing, fall back to PNG export only. |

## Cross-references

- [SKILL](../SKILL.md) — parent skill
- [_template-registry](_template-registry.md) — template selection table
- [_non-negotiables](_non-negotiables.md) — enforcement rules
- [_execution-modes](_execution-modes.md) — mode workflows
