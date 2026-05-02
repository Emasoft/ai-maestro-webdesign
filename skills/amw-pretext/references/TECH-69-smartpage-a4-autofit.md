---
name: TECH-69-smartpage-a4-autofit
category: workflow
source: pretext-skills/SKILL-17.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# SmartPage — auto-fit Markdown to one A4 page

**Category:** workflow
**Status:** stable

## What it does

The `smartpage` skill (SKILL-17) uses pretext internally to binary-search the font size (6-72 px) that fits a Markdown document onto exactly ONE A4 page (210×297 mm). Exports PDF + PNG + MD. 10 themes available (classic, warm, academic, editorial, noir, mint, ink, tech, kraft, smartisan).

## When to use

- One-pager handouts
- Recipe cards / event posters
- Any "fit this content to one printable page" task

## How it works

```
Markdown → marked.lexer() → Pretext measure → binary search 6-72 px → render → Playwright export
```

```bash
# Source: SKILL-17.md
git clone https://github.com/fxjhello/SmartPage.git
cd SmartPage && npm install
npm smartpage input.md --theme editorial --output-dir ~/Desktop
```

## Minimal example

```bash
npm smartpage file.md --theme classic
```

## Gotchas

- Playwright is the render engine — install browsers first (`npx playwright install chromium`).
- A4 is hardcoded — letter/legal sizes need fork modifications.
- Font must exist on the system; SmartPage defaults to Noto Sans SC for CJK coverage.

## Cross-references

- Related: TECH-27-auto-fit-font-size
- API reference: [TECH-27-auto-fit-font-size](TECH-27-auto-fit-font-size.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
