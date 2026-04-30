---
name: TECH-32-multilingual-bidi
category: typography
source: pretext-skills/amw-pretext-typography-skill-main/references/multilingual-typography.md
also-in: SKILL-13.md, SKILL-16.md, pretext-main-2/README.md
---

# Multilingual / bidi / emoji measurement

**Category:** typography
**Status:** stable

## What it does

Pretext's measurement handles Arabic/Hebrew (RTL), CJK, Thai, emoji (including multi-codepoint ZWJ sequences), and mixed-direction strings in a single prepared handle. The library reports ~7680/7680 accuracy across Chrome/Safari/Firefox sweeps (source: SKILL-16 / pretext-main-2 STATUS.md).

## When to use

- Any i18n UI
- Mixed-direction strings (`'AGI 春天到了. بدأت الرحلة 🚀'`)
- Emoji-dense chat, comments, social UIs

## How it works

`Intl.Segmenter` segments graphemes honoring extended pictographic sequences; Canvas `measureText` provides accurate per-segment width. The line breaker applies bidi rules from Unicode.

```ts
// Source: pretext-main-2/README.md
const prepared = prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')
const { height } = layout(prepared, 320, 20)
```

## Minimal example

```ts
// CJK + emoji + Arabic
const prepared = prepare('Hello مرحبا 🎉 新年快乐', '16px "Noto Sans"')
```

## Gotchas

- Canvas on some platforms renders ZWJ sequences (family emoji) as separate glyphs; measurement matches the render, so the "wrong looking" output is still internally consistent.
- For Korean, add `{ wordBreak: 'keep-all' }`.
- RTL shaping happens at render time (browser's Canvas) — pretext supplies widths, not glyph positioning.

## Recommended practices (source: pretext-typography-skill-main/references/multilingual-typography.md)

- Prefer realistic sample content early — do not use placeholder lorem ipsum for i18n testing.
- Test at narrow, medium, and wide widths.
- Pin a named font stack used by the actual UI.
- Use `setLocale()` when locale-sensitive line break behavior matters.
- Enable `{ whiteSpace: 'pre-wrap' }` for editors, notes, and imported plain text.

## QA checklist

- Line count does not unexpectedly jump between browsers for the target font.
- Punctuation at line edges feels natural for the active locale.
- No accidental clipping with mixed emoji or tall glyphs.
- Cursor handoff remains seamless in multi-column or obstacle layouts.
- Virtualization stays stable as content language changes.

## Cross-references

- Related: TECH-11-set-locale, TECH-16-cjk-keep-all
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
