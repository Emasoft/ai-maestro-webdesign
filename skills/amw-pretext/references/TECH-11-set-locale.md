---
name: TECH-11-set-locale
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, use-pretext/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# setLocale() — global Intl.Segmenter locale override

**Category:** api
**Status:** stable

## What it does

`setLocale(locale?)` sets the locale used by `Intl.Segmenter` for subsequent `prepare()` calls. Affects word-break and line-break behavior globally. Call once at app startup if your content uses a non-default locale (Japanese, Thai, Arabic, etc.).

## When to use

- Multilingual apps where the OS locale is not the content language
- CJK / Thai / Arabic text that needs locale-aware segmentation
- Server-side rendering where the runtime default is wrong

## How it works

Updates the shared segmenter instance. Also implicitly clears the measurement cache because segment boundaries change.

```ts
// Source: use-pretext/SKILL.md
import { setLocale } from '@chenglou/pretext'
setLocale('ja')  // prepare() now segments Japanese with JA rules
```

## Minimal example

```ts
// Source: use-pretext/SKILL.md
setLocale('th')  // Thai: word boundaries via ICU rules
const prepared = prepare(thaiText, '16px "Noto Sans Thai"')
```

## Gotchas

- Global side effect — affects every `prepare()` after the call.
- Also clears caches; don't call in hot paths.
- Pass no argument to reset to the runtime default.

## Cross-references

- Related: TECH-10-clear-cache, TECH-34-cjk-keep-all
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
