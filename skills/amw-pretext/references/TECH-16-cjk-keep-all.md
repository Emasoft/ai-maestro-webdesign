---
name: TECH-16-cjk-keep-all
category: measure
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-13.md, SKILL-21.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# CJK keep-all word-break

**Category:** measure
**Status:** stable

## What it does

Pass `{ wordBreak: 'keep-all' }` to `prepare()` for Korean / Chinese / Japanese content that should NOT break mid-word. Mirrors CSS `word-break: keep-all` — the layout prefers to break at spaces and punctuation, keeping CJK sequences whole.

## When to use

- Korean content (spaces delimit words)
- Chinese/Japanese headlines where arbitrary mid-character breaks look wrong
- Multilingual documents that mix CJK with Latin

## How it works

Changes the internal break-opportunity rule for CJK clusters — only punctuation and whitespace remain breakable.

```ts
// Source: pretext-text-measurement/SKILL.md
const prepared = prepare(cjkText, '16px NotoSansCJK', { wordBreak: 'keep-all' })
const { height, lineCount } = layout(prepared, 300, 22)
```

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md
const prepared = prepare('新功能上线！使用请联系客服。', '16px "Noto Sans SC"', { wordBreak: 'keep-all' })
```

## Gotchas

- Without `keep-all`, CJK text can break on any character — visually jarring in Korean especially.
- Rightward of `setLocale('ja')` / `setLocale('zh')` may be required for proper segmentation.

## Cross-references

- Related: TECH-11-set-locale, TECH-32-multilingual-bidi
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
