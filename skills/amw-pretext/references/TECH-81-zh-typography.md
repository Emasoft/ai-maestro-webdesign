---
name: TECH-81-zh-typography
category: cjk
status: stub
---

<!--
  TECH-81-zh-typography — Chinese Web Typography (stub)
  Sibling of TECH-80-ja-typography. Placeholder for forthcoming ZH-specific rules.
-->

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [How it works — Baseline CSS](#how-it-works--baseline-css)
- [Worked examples](#worked-examples)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-81 — Chinese Web Typography (stub)

> **CJK-exception:** This file contains Chinese characters (Simplified and Traditional) as required by its subject matter. All other plugin files remain CJK-free.

**Category:** cjk
**Status:** stub — core rules pending; see TECH-80 for the sister JA technique

---

## What it does

Documents CSS rules, font-feature settings, line-break behaviour, and browser-compatibility notes for rendering Simplified Chinese (`zh-Hans`) and Traditional Chinese (`zh-Hant`) body text and headings on the web.

Many rules overlap with TECH-80 (Japanese) because both scripts share Unicode CJK blocks and similar kinsoku-equivalent constraints. This file notes the **differences** and ZH-specific patterns; read TECH-80 first for shared foundations.

---

## When to use

- Authoring or reviewing CSS for a page whose primary language is `zh-Hans` or `zh-Hant`.
- Choosing between Simplified and Traditional font families (`"Noto Sans SC"` vs `"Noto Sans TC"`).
- Diagnosing broken line-break or word-break behaviour on a Chinese page.
- Adding BudouX phrase segmentation for Chinese body text (BudouX ships a default Chinese parser alongside the Japanese one).

---

## When NOT to use

- Japanese-only projects — use TECH-80 directly.
- Mixed CJK content where the base language is Japanese — anchor to TECH-80 and treat Chinese as an override layer.
- Latin-script pages; no CJK content present.

---

## How it works — Baseline CSS

> **Stub note:** Full ZH-specific rules are forthcoming. The CSS skeleton below covers the most critical cross-browser baseline. Expand with project-specific typographic decisions.

```css
/* ── Simplified Chinese baseline ─────────────────────────── */
:lang(zh-Hans),
:lang(zh-CN) {
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.75;
  /* Suppress per-character break inside a sentence; prefer punctuation breaks */
  word-break: keep-all;
  overflow-wrap: anywhere;
  line-break: strict;          /* honour kinsoku-equivalent punctuation rules */
  font-feature-settings: "palt" 1;  /* proportional metrics — same as JA rule 4 */
}

/* ── Traditional Chinese baseline ────────────────────────── */
:lang(zh-Hant),
:lang(zh-TW),
:lang(zh-HK) {
  font-family: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
  line-height: 1.75;
  word-break: keep-all;
  overflow-wrap: anywhere;
  line-break: strict;
  font-feature-settings: "palt" 1;
}

/* ── Headings ─────────────────────────────────────────────── */
:lang(zh) h1,
:lang(zh) h2,
:lang(zh) h3 {
  text-wrap: balance;          /* same as JA rule 2; Blink 114+ / Safari 17.5+ */
  letter-spacing: 0.04em;
}
```

Key shared rules inherited from TECH-80 (apply unchanged):
- `word-break: keep-all` on any element feeding BudouX `<wbr>` output.
- `text-align: justify` suppressed on mobile card bodies (identical JP/ZH bug).
- `font-feature-settings: "palt"` for proportional kana-equivalent CJK metrics.
- Quoted-phrase nowrap: wrap `「…」` / `『…』` in `<span class="nowrap">`.

---

## Worked examples

### BudouX for Chinese

BudouX ships a default Chinese parser. Usage is identical to Japanese except for the parser constructor:

```ts
import { loadDefaultSimplifiedChineseParser } from "budoux";

const parser = loadDefaultSimplifiedChineseParser();

// Plain-text segmentation
const segments = parser.parse("今天天气非常好，适合出门散步。");
// → ["今天", "天气", "非常好，", "适合", "出门", "散步。"]

// HTML with <wbr> insertion (CSS must have word-break: keep-all)
const html = parser.translateHTMLString(
  "今天天气非常好，适合出门散步。"
);
```

For Traditional Chinese, substitute `loadDefaultTraditionalChineseParser()`.

---

## Gotchas

- **`word-break: break-all` is destructive for Chinese** — it forces breaks inside every character sequence. Use `keep-all` + `overflow-wrap: anywhere` instead.
- **`text-align: justify` on mobile** — same #1 bug as Japanese (see TECH-80 Rule 17). Suppress on cards and narrow containers.
- **Font family mismatch `zh-Hans` vs `zh-Hant`** — serving a Simplified font to a Traditional locale (or vice versa) produces visually incorrect glyphs for hundreds of characters (e.g., 碗 vs 碗 differ by regional standard). Always use `:lang(zh-Hans)` / `:lang(zh-Hant)` scoping, not a single `:lang(zh)` rule for both font stacks.
- **BudouX Chinese parser accuracy** — the default Chinese parser is trained on Simplified Chinese news corpora. Traditional Chinese results may be suboptimal; verify on representative content.
- **`font-feature-settings: "palt"` support** — full support in Noto Sans SC/TC; partial or absent in system fonts (`PingFang`, `Microsoft YaHei`). Test on target fonts before relying on it.

---

## Cross-references

- [TECH-80-ja-typography](TECH-80-ja-typography.md) — Japanese web typography; shares kinsoku, BudouX, `word-break: keep-all`, `font-feature-settings: "palt"`, justify suppression, quoted-phrase patterns. Read TECH-80 first.
- [TECH-16-cjk-keep-all](TECH-16-cjk-keep-all.md) — `word-break: keep-all` option for `prepare()` in pretext (applies to both JA and ZH measurement)
- [TECH-32-multilingual-bidi](TECH-32-multilingual-bidi.md) — multilingual and bidi text handling
- [TECH-11-set-locale](TECH-11-set-locale.md) — `setLocale('zh')` for pretext segmentation
- [_index](_index.md) — full catalog
- [../../amw-design-principles/typography-system.md](../../amw-design-principles/typography-system.md) — plugin typography tokens (pretext extends, never replaces)
