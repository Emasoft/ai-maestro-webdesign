---
name: TECH-errors-troubleshooting
category: mermaid-render-diagnostics
source: skills/amw-mermaid-render/SKILL.md
---
## Table of Contents

- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)

## Error Handling

- `exit 2` — `external/mermaid-render/` missing. Run `/amw-init`.
- `exit 3` — `node` not on PATH. Install Node.js ≥ 22.
- `exit 1 + "Parse error on line N"` — invalid Mermaid syntax. Test it at https://mermaid.live first.
- `exit 1 + "Unknown theme"` — theme name typo. Run `bin/amw-mermaid-render.sh --list-themes`.
- `validate-ascii.py` warnings on stderr — the ASCII output has variable-width glyphs. Fix the input labels (shorten, remove CJK/emoji) and re-render.

## Troubleshooting

- **"Cannot find module 'beautiful-mermaid'"** — auto-install failed. `cd external/mermaid-render && npm install`.
- **Empty SVG output** — invalid Mermaid syntax. Test at https://mermaid.live first.
- **Fonts not rendering** — target system lacks the font; use `"Inter, system-ui, sans-serif"` or `@font-face` in host page.
- **CJK/emoji breaking ASCII alignment** — expected (double-width). Rename labels or switch to SVG.
