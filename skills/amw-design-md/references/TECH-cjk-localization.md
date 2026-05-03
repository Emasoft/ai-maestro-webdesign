---
name: TECH-cjk-localization
category: localization
source: docs_dev/extracted/google-labs/awesome-design-md-{jp,zh-master,k}-main
also-in: skills/amw-design-md/references/TECH-03-typography-tokens.md, skills/amw-design-md/references/TECH-09-multipage-extraction.md, agents/amw-multilanguage-copywriter-agent.md, skills/amw-design-principles/typography-system.md
status: stable
extracted-from: 25 JP DESIGN.md files (awesome-design-md-jp), 6 KO DESIGN.md files (awesome-k-design-md), 58 ZH DESIGN.md files (awesome-design-md-zh) + 1 official JP template + 1 KO contributing guide
---

# TECH: CJK (Chinese / Japanese / Korean) localization for web design

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [1. Typography (per language)](#1-typography-per-language)
  - [2. Layout](#2-layout)
  - [3. Punctuation + line breaking](#3-punctuation-line-breaking)
  - [4. Cultural symbolism](#4-cultural-symbolism)
  - [5. Microcopy patterns](#5-microcopy-patterns)
  - [6. Locale machinery](#6-locale-machinery)
  - [7. SEO impacts](#7-seo-impacts)
  - [8. Performance](#8-performance)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)
- [Source attribution](#source-attribution)


## What it does

Provides a single reference for localizing webpages into Japanese, Chinese
(Simplified or Traditional), and Korean. Documents font fallback chains,
typography metrics, layout adjustments, punctuation rules, cultural
symbolism, microcopy patterns, locale machinery, SEO impacts, and font
performance — every CJK-specific quirk that breaks if the agent treats CJK
as "Latin with different characters." All values are extracted from real,
shipping CJK websites (Apple JP, MUJI, note, WIRED.jp, Cookpad, Toyota,
SmartHR, freee, Rakuten, Mercari, ABEMA, pixiv, Toss, Naver, Coupang,
Daangn, Baemin, Kakao, plus Sanity, BMW, Spotify Chinese variants).

## When to use

Trigger this TECH file whenever the user requests:

- A Japanese, Chinese (Simplified or Traditional), or Korean version of a
  webpage / landing page / dashboard / form / email
- A multi-locale site whose locale list includes any of `ja`, `ko`,
  `zh-Hans`, `zh-Hant`, `zh-CN`, `zh-TW`, `zh-HK`
- Any UI that will display CJK glyphs, even as fallback for mixed-content
  pages (e.g. an English page with Japanese product names)
- Migration of an existing English UI into a CJK-default UI (where the
  default body text language is CJK)

Do NOT trigger when CJK appears only inside an `<img>` or a screenshot —
those are not text. Trigger ONLY when CJK characters will be rendered as
HTML text by the browser.

## How it works

The CJK localization problem decomposes into eight independent layers.
Apply them in order; each layer overrides the Latin-default value of the
previous layer.

### 1. Typography (per language)

CJK glyphs are dramatically denser than Latin glyphs at the same `font-size`.
Latin body text at 16px / line-height 1.4 is comfortable; the same metrics
applied to CJK produce cramped, illegible UI. Each language also has a
distinct font-stack convention rooted in OS-bundled fonts.

#### Japanese (`ja` / `ja-JP`)

**Canonical body font stack** (per `awesome-design-md-jp-main/template/DESIGN.md`
and `note/DESIGN.md` line 109-129):

```css
/* Modern default — gothic body */
font-family:
  "Helvetica Neue",                          /* Western glyphs first (Apple/MUJI convention) */
  Arial,
  "Hiragino Kaku Gothic ProN",               /* macOS modern */
  "Hiragino Sans",                           /* macOS newer (10.11+) */
  "Yu Gothic",                               /* Windows 8.1+ / macOS modern */
  YuGothic,                                  /* macOS legacy alias (no quotes) */
  "Noto Sans JP",                            /* webfont fallback / Linux / Android */
  Meiryo,                                    /* Windows legacy */
  "MS PGothic",                              /* very old Windows fallback */
  sans-serif;

/* Mincho (serif) — for long-form reading content only */
font-family:
  "Hiragino Mincho ProN",                    /* macOS */
  "Hiragino Mincho Pro",
  "Yu Mincho",                               /* Windows / macOS */
  YuMincho,
  "BIZ UDPMincho",                           /* Windows accessibility-focused */
  "MS PMincho",                              /* legacy Windows */
  serif;

/* Monospace — code blocks */
font-family:
  SFMono-Regular,
  Consolas,
  Menlo,
  Courier,
  monospace;
```

**Two fundamental fallback strategies** observed:

1. **Western-first** (Apple JP, WIRED.jp, MUJI, Mercari, note, Toyota) —
   Helvetica Neue / SF Pro / Arial first, Japanese fonts after. The browser
   uses Western glyphs for ASCII and Japanese fonts for CJK characters.
   Best for brands with strong Western typography heritage.

2. **Japanese-first** (Cookpad, freee, SmartHR) — Japanese gothic first
   (`noto-sans` Adobe Fonts version, or `Yu Gothic`/`AdjustedYuGothic`).
   Best for native Japanese services where Japanese reading comfort
   dominates over Western sample-text aesthetic.

**Body sizing**: 14–18px depending on density target. (Per `note/DESIGN.md`
line 156: 18px / line-height 2.0 for article body; per `mercari/DESIGN.md`
line 74: 15px / line-height 1.4 for compact UI; per `pixiv/DESIGN.md`
line 72: 12px body for gallery UI). **Never go below 12px for any user-readable
CJK content.** The `template/DESIGN.md` line 250 specifies 14–16px on mobile
as the floor.

**Line-height**: **1.5–2.0** is the canonical range (per `template/DESIGN.md`
line 102: "日本語本文は line-height: 1.5 以上を推奨（1.7〜2.0が読みやすい）").
Specifically:

| Use case | line-height | Source |
|---|---|---|
| Compact UI (lists, tables, business apps) | 1.4–1.5 | mercari, smarthr |
| Standard body | 1.5–1.6 | cookpad, muji, toyota, abema |
| Editorial / long-form reading | 1.7–2.0 | note (article body 2.0), wired (1.75) |
| Headings | 1.0–1.5 | varies — h1 typically 1.05–1.5 |

Latin convention of 1.4–1.5 for body is **too tight** for Japanese — the
glyph density makes lines visually merge.

**Letter-spacing** (字間, ji-kan):

| Pattern | Value | When |
|---|---|---|
| Western-mode default | `normal` | Most JP body text — pixiv, abema, mercari, toyota body, muji |
| Tight tracking (詰め組み) | `-0.4px` ≈ `-0.025em` | Cookpad globally — Japanese "tightly-set" aesthetic |
| Slight loosening | `0.04em` to `0.1em` | Toyota body (0.04em), template recommendation, headings on note (0.04em h1+h2) |
| Strong tracking | `0.083em–0.1em` | Latin labels in CJK pages (WIRED's `WiredMono` nav at 0.083em) |

The template explicitly recommends `letter-spacing: 0.04em` for body to
improve legibility (per template line 98). However, real shipping sites
diverge — some use `normal`, some use negative tracking. **Never use
positive `letter-spacing` greater than `0.1em` on Japanese body** — it
breaks word recognition since Japanese has no inter-word spacing.

**OpenType features** (`font-feature-settings`):

```css
/* Proportional Japanese kerning — palt */
font-feature-settings: "palt" 1;

/* Latin kerning — kern */
font-feature-settings: "kern" 1;

/* Both, in order */
font-feature-settings: "palt", "kern";
```

- `palt` — proportional alternates for Japanese punctuation. Tightens 「」、。
  to non-fullwidth proportional spacing. **Apply to headings, NOT to body**
  (per `note/DESIGN.md` line 188: "letter-spacing: 0.04em と palt は
  見出し専用。本文には適用しない"). WIRED is an exception — applies `palt`
  globally on body for editorial-tightness aesthetic.
- `liga` — Latin ligatures (fi, fl). Cookpad applies `liga` only.
- `kern` — Latin kerning. Sometimes paired with `palt` in mixed JP+EN body.

**Vertical writing** (縦書き, tategaki) — `writing-mode: vertical-rl`:

```css
.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;       /* CJK upright, Latin rotated */
  /* OR: text-orientation: upright;   for full upright Japanese */
}
```

**Practical rule from sources**: All 25 modern JP DESIGN.md files mark
`### 3.8 縦書き → 該当なし` ("not applicable"). **Vertical writing is not
used on the modern Japanese web.** It is reserved for: traditional fiction
publishers, museum/gallery exhibition pages, calligraphy showcases, and
specific editorial features. **Do not enable vertical writing as a default
or "more authentic" option** — modern JP UI is horizontal LTR like English.

**Furigana / ruby annotations** — pronunciation aids printed above kanji:

```html
<ruby>漢字<rt>かんじ</rt></ruby>
<!-- More explicit form: -->
<ruby><rb>漢字</rb><rt>かんじ</rt></ruby>
```

```css
ruby {
  ruby-position: over;     /* default */
  ruby-align: center;
}
rt {
  font-size: 0.5em;        /* furigana is half-size */
  line-height: 1;
}
```

Use furigana for: children's content, education sites, names with rare
readings, dictionary/glossary entries. **Do not** use furigana on
general-audience content for common kanji (it implies the reader is
illiterate). NOT documented in source files (template/DESIGN.md does not
cover ruby) — this rule is general HTML5 standard.

**Hiragana-only / katakana-only**: Some JP brands use katakana-only labels
for product names (loanwords, brand names). Cookpad uses hiragana
honorifics ("おすすめ", "おはなし") as a brand voice. Mixing scripts is
normal and intentional in Japanese — never normalize to one script.

#### Chinese — Simplified (`zh` / `zh-CN` / `zh-Hans`)

**Canonical body font stack** (per `awesome-design-md-zh-master/design-md-cn/sanity/DESIGN.md`
line 66 and `bmw/DESIGN.md` line 66 — the rare cases the zh variant
documents Chinese-specific fallback):

```css
/* Modern default — Simplified Chinese */
font-family:
  -apple-system,                             /* macOS / iOS — auto-picks PingFang SC */
  BlinkMacSystemFont,                        /* macOS WebKit */
  "PingFang SC",                             /* macOS / iOS explicit */
  "Hiragino Sans GB",                        /* macOS legacy SC */
  "Microsoft YaHei",                         /* Windows default SC */
  "微软雅黑",                                  /* Windows literal CJK name */
  STXihei,                                    /* macOS lighter weight */
  "Source Han Sans CN",                      /* webfont — Adobe/Google */
  "Noto Sans CJK SC",                        /* webfont alternative — Google */
  "Noto Sans SC",                            /* webfont compact */
  "WenQuanYi Micro Hei",                     /* Linux open-source */
  sans-serif;
```

**Note**: Source files in the zh variant **mostly translate Western brand
DESIGN.md into Chinese prose** without changing the font stacks (e.g.
Apple's stack remains "SF Pro Display..." — it is not localized to PingFang
SC). The TWO files that do document a CJK fallback are `bmw/DESIGN.md`
(BMW's global stack including Hiragino Sans GB / STXihei / Microsoft YaHei
/ WenQuanYi Micro Hei) and `sanity/DESIGN.md` (which explicitly labels its
fallback as "回退/CJK"). The stack above is the consolidated industry-standard
SC fallback chain reconstructed from those two files plus widely-known
defaults.

**Body sizing**: 14–16px (Chinese chars are slightly less dense than
Japanese — kanji compounds are usually 2 chars, not 3–4 like Japanese).
Headings 18px+.

**Line-height**: **1.5–1.75** is the canonical range (slightly lower than
Japanese because SC chars are visually less complex). Per the `bmw/DESIGN.md`
line 7 description: "60px 大写标题字重 300 是定义性的排版手势——轻字重字体在低语
权威而非高喊" — the Chinese variant prefers tight headings, looser body.

**Letter-spacing**: **`normal` to `0.05em`**. Chinese has even less appetite
for positive letter-spacing than Japanese — large positive tracking severs
the visual connection between characters of a compound word (词 ci2). Some
brand identities use `-0.01em` to `-0.02em` (Apple-influenced tightness)
but `normal` is safest default.

**OpenType features**: `palt` does not apply to Chinese (it's a
Japanese-specific font feature). Use `kern` only if the font supports it.
`text-spacing` (CSS Text Module Level 4) is the modern approach but has
limited browser support — do not depend on it.

#### Chinese — Traditional (`zh-TW` / `zh-Hant` / `zh-HK`)

**Canonical body font stack**:

```css
font-family:
  -apple-system,
  BlinkMacSystemFont,
  "PingFang TC",                             /* macOS / iOS Traditional */
  "Heiti TC",                                /* macOS legacy */
  "Microsoft JhengHei",                      /* Windows TC default */
  "微軟正黑體",                                /* Windows literal */
  "Source Han Sans TW",                      /* webfont — TW variant */
  "Noto Sans CJK TC",                        /* webfont — TW */
  "Noto Sans TC",
  sans-serif;

/* HK uses 'TC' fonts but with HK-specific glyph forms preferred */
font-family-hk:
  "PingFang HK",
  "Source Han Sans HK",
  "Noto Sans CJK HK",
  /* fall through to TC stack above */
  ...;
```

**Critical note on codepoints**: Simplified and Traditional Chinese share
many codepoints but have hundreds of distinct simplified-vs-traditional
character pairs (`国` vs `國`, `头` vs `頭`, etc.). The font stack alone
does NOT change codepoints — that is a content concern. The `lang` attribute
and the font choice together signal browser/font behavior:

```html
<html lang="zh-Hans">    <!-- Simplified content -->
<html lang="zh-Hant">    <!-- Traditional content -->
<html lang="zh-Hant-HK"> <!-- Traditional, HK glyph variants where they differ -->
```

When `<html lang="zh-Hans">` and Source Han Sans CN is loaded, the browser
selects SC glyph forms; under `lang="zh-Hant"` it selects TC forms. This
matters most for PingFang and Noto CJK fonts which contain BOTH glyph sets
in one file — the `lang` attribute selects the variant. **Always set the
lang attribute correctly.** Sources do not document this detail; it is
broadly known web-standards behavior.

#### Korean (`ko` / `ko-KR`)

**Canonical body font stack** (per `awesome-k-design-md-main/design-md/toss/DESIGN.md`
line 64-66, `naver/DESIGN.md` line 60-65, `coupang/DESIGN.md` line 62-64,
`kakao/DESIGN.md` line 60-63):

```css
font-family:
  "Apple SD Gothic Neo",                     /* macOS / iOS — universal Korean default */
  -apple-system,
  BlinkMacSystemFont,
  "Noto Sans KR",                            /* webfont — Google */
  "Malgun Gothic",                           /* Windows default Korean */
  "맑은 고딕",                                  /* Windows literal name (Hangul) */
  "Nanum Gothic",                            /* webfont — popular Naver-distributed */
  "나눔고딕",
  "Spoqa Han Sans Neo",                      /* Daangn / Baemin webfont */
  sans-serif;

/* Brand-specific Korean fonts (per Korean DESIGN.md sources) */
/* Toss: 'Toss Product Sans', 'Tossface' */
/* Daangn (Karrot): 'Karrot Sans' */
/* Baemin: 'BMHANNA', 'BMHANNAAIM', 'BMEULJIROTTF' */
/* Naver: 'Naver Nanum Gothic' */
```

**Hangul-specific layout rule** — `word-break: keep-all`:

```css
body {
  word-break: keep-all;   /* don't break Hangul mid-syllable-block */
  overflow-wrap: break-word;
}
```

Korean syllables (음절 블록) are visually atomic units — `한` is one block,
not three letters. Browsers default to breaking lines anywhere; this
fragments syllable blocks visually. `word-break: keep-all` keeps Korean
words intact. **All Korean DESIGN.md sources implicitly assume this** even
though most do not state it — it's a well-known Hangul convention.

**Body sizing**: 14–17px. Per `daangn/DESIGN.md` Body 1 = 16–17px, `toss/DESIGN.md`
Body 1 = 17–18px, `naver/DESIGN.md` Body 1 = 15–16px. **15–16px is the safe
default**; go to 17–18px for fintech / trust-critical UI.

**Line-height**: **1.5** is the canonical default for Korean body (tight=1.3,
relaxed=1.65–1.7). Per `toss/DESIGN.md` line 80-86, `daangn/DESIGN.md`
line 80-85, `naver/DESIGN.md` line 80-85 — all three explicitly define:

```
Tight:      1.3
Normal:     1.5
Relaxed:    1.65–1.7
```

**Letter-spacing**: Slightly **negative** (`-0.005em` to `-0.02em`) is the
norm for modern Korean UI. Per `toss/DESIGN.md` line 70-78: Display = -0.015em,
Heading = -0.01em, Body = -0.01em, Caption = -0.005em. Per `daangn/DESIGN.md`
similar. **Korean prefers negative tracking** because Apple SD Gothic Neo
glyphs have generous default sidebearings; tightening creates the modern
fintech look (Toss).

**Number-tabular alignment**: Per `toss/DESIGN.md` and `coupang/DESIGN.md`
Price specs — Korean fintech / e-commerce uses `font-variant-numeric:
tabular-nums` for price columns (2,500원 vs 12,500원 must align right).

#### Mixed Latin + CJK in the same line

Per `wired/DESIGN.md` line 56-75 (Helvetica Neue first, then Japanese
fonts) and `apple-jp/DESIGN.md` line 14-15 ("SF Pro JP" first), the
**Western-first cascade** is the de-facto industry pattern for mixed JP+EN
content: the browser uses Latin glyphs from the Latin font and CJK glyphs
from the Japanese font, which produces a more harmonious mixed line than
the reverse.

**Modern CSS approach** (not explicitly in sources, but referenced in JP
template line 75-77):

```css
/* Use unicode-range to scope each font to its glyph set */
@font-face {
  font-family: 'AppFont';
  src: url('latin.woff2') format('woff2');
  unicode-range: U+0000-024F, U+0370-03FF, U+0400-04FF;  /* Latin / Greek / Cyrillic */
}
@font-face {
  font-family: 'AppFont';
  src: url('japanese.woff2') format('woff2');
  unicode-range: U+3000-9FFF, U+FF00-FFEF;               /* CJK + halfwidth/fullwidth forms */
}
```

This is the **font-subsetting strategy** — see Section 8 (Performance) below.

### 2. Layout

#### Button widths

CJK buttons need wider `min-width` than Latin equivalents because each CJK
character is roughly 1em wide, so a 2-character button label takes ~2em
plus padding — which can look cramped without a min-width floor.

| Language | 2-char button | 3-char button | Recommended `min-width` |
|---|---|---|---|
| Latin (English) | "OK" / "GO" | "Buy" | 64–80px |
| Japanese | 「送信」 (submit) / 「閉じる」 (close) | 「ログイン」 (login) | **88–104px** (per cookpad/DESIGN.md primary buttons: padding 8px 24px → ≈ 96px min) |
| Chinese (SC) | 「提交」 (submit) / 「确定」 (confirm) | 「立即购买」 (buy now) | **88–96px** (cn glyphs slightly tighter than jp) |
| Chinese (TC) | 「送出」 / 「確定」 | 「立即購買」 | **88–96px** (same as SC structurally) |
| Korean | "확인" (confirm) / "취소" (cancel) | "회원가입" (signup) | **80–96px** (per toss/DESIGN.md primary button padding 12px 24px) |

**Source values from real sites**:
- Cookpad primary button: `padding: 8px 24px` (per `cookpad/DESIGN.md` line 124-128) → effective width ≈ 96px for "保存" (save)
- Toss primary button: `padding: 12px 24px` (per `toss/DESIGN.md` line 121-122) → effective width ≈ 88px for "확인"
- Mercari CTA "出品" (list item): `padding` per implementation, with `font-size: 14px` `weight: 700` (per `mercari/DESIGN.md` line 122-128)

**Touch target**: 44×44px is the absolute floor (WCAG 2.1 minimum), per
`template/DESIGN.md` line 248 ("最小サイズ: 44px × 44px (WCAG基準)"). Same
floor applies in all three CJK locales.

#### Form labels

Per template recommendation (no explicit position rule documented), the
de-facto pattern for CJK forms is:

- **Above-input** (top-label): standard for Western-influenced sites
  (SmartHR, freee, Mercari signup). Use this as default.
- **Inline-leading**: traditional Japanese gov / business form style
  ("お名前: [____]"). Acceptable for compact business UIs but harder to
  scan.
- **Floating labels**: AVOID for CJK — when the label collapses to the
  top-left of the input, narrow CJK labels look amputated.

#### Date inputs

Format conventions per locale:

| Locale | Native format | Placeholder convention | ISO 8601 fallback |
|---|---|---|---|
| `ja-JP` | `2026年4月26日` (full-width 年月日) or `2026/04/26` | "YYYY/MM/DD" | `2026-04-26` |
| `zh-CN` | `2026年4月26日` or `2026-04-26` | "YYYY-MM-DD" | `2026-04-26` |
| `zh-TW` | `2026年4月26日` or `2026/04/26` | "YYYY/MM/DD" | `2026-04-26` |
| `ko-KR` | `2026년 4월 26일` or `2026.04.26` | "YYYY.MM.DD" | `2026-04-26` |

**Always store dates as ISO 8601 internally** (`YYYY-MM-DD`), and use
`Intl.DateTimeFormat(locale, options)` for display. Source files do not
explicitly cover this — this is widely-known JS API behavior.

```javascript
// Example
new Intl.DateTimeFormat('ja-JP', { dateStyle: 'long' }).format(new Date('2026-04-26'));
// "2026年4月26日"

new Intl.DateTimeFormat('zh-CN', { dateStyle: 'long' }).format(new Date('2026-04-26'));
// "2026年4月26日"

new Intl.DateTimeFormat('ko-KR', { dateStyle: 'long' }).format(new Date('2026-04-26'));
// "2026년 4월 26일"
```

#### Number formatting

CJK languages have a **myriad-grouped number system** in addition to
Western thousand-grouping:

| Number | Latin | Japanese myriad (万) | Korean myriad (만) | Chinese myriad (万) |
|---|---|---|---|---|
| 10,000 | "10,000" or "10K" | 「1万」 (`1 wan`) | "1만" (`1 man`) | 「1万」 (`1 wan`) |
| 12,345 | "12,345" | 「1万2,345」 or 「12,345」 | "1만 2,345" | 「1万2,345」 |
| 100,000,000 | "100M" or "100,000,000" | 「1億」 | "1억" | 「1亿」 (SC) / 「1億」 (TC) |
| 1,000,000,000,000 | "1T" | 「1兆」 | "1조" | 「1兆」 |

**Display rules** observed in real CJK e-commerce / fintech sites:

- For prices and product counts up to 9,999: show as Western-grouped
  (e.g. `¥9,800`)
- For 10,000+: many JP/CN sites switch to myriad notation
  (`1万円` / `1万元`) — but Korean sites usually keep Western grouping
  with currency suffix (`10,000원`)
- For "view counts", "follower counts", "likes" — always use myriad
  (Japanese pixiv shows `1.2万` for 12,000 views)

```javascript
// Use Intl.NumberFormat with notation: 'compact'
new Intl.NumberFormat('ja-JP', { notation: 'compact' }).format(12345);
// "1.2万"

new Intl.NumberFormat('zh-CN', { notation: 'compact' }).format(12345);
// "1.2万"

new Intl.NumberFormat('ko-KR', { notation: 'compact' }).format(12345);
// "1.2만"
```

#### Currency

| Locale | Symbol | HTML entity | Position | Example |
|---|---|---|---|---|
| `ja-JP` | `¥` (or `円`) | `&yen;` (U+00A5) or `&#xFFE5;` (U+FFE5 fullwidth) | prefix | `¥9,800` or `9,800円` |
| `zh-CN` | `¥` (or `元`/`RMB`) | `&yen;` (U+00A5) | prefix | `¥99` or `99元` |
| `zh-CN` (international) | `CN¥` or `CNY` | (text) | prefix | `CN¥99` |
| `zh-TW` | `NT$` or `元` | (text) or `&dollar;` | prefix | `NT$99` or `99元` |
| `zh-HK` | `HK$` | (text) | prefix | `HK$99` |
| `ko-KR` | `₩` or `원` | `&#x20A9;` (U+20A9) | suffix (with 원), prefix (with ₩) | `9,800원` or `₩9,800` |

**Critical**: Both Japanese yen and Chinese yuan use the same `¥` glyph, but
they are different currencies. Always include the `lang` attribute or an
ISO 4217 code (`JPY` vs `CNY`) in any context where ambiguity matters
(invoices, banking, multi-currency carts).

```javascript
// Use Intl.NumberFormat with style: 'currency'
new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(9800);
// "￥9,800"  (note: fullwidth yen)

new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(9800);
// "₩9,800"
```

#### Phone numbers

| Locale | Format | Example |
|---|---|---|
| `ja-JP` mobile | `0X0-XXXX-XXXX` (3-4-4) | `090-1234-5678` |
| `ja-JP` landline | `0XX-XXXX-XXXX` (variable) | `03-1234-5678` (Tokyo) |
| `zh-CN` mobile | `1XX XXXX XXXX` (3-4-4 or unspaced) | `138 1234 5678` |
| `zh-CN` landline | `0XX-XXXXXXXX` | `010-12345678` (Beijing) |
| `zh-TW` mobile | `09XX-XXX-XXX` (4-3-3) | `0912-345-678` |
| `ko-KR` mobile | `01X-XXXX-XXXX` | `010-1234-5678` |
| `ko-KR` landline | `0X-XXXX-XXXX` | `02-1234-5678` (Seoul) |

Source files do not document phone formats — these are standard
country-specific telephony conventions. Use `libphonenumber` or
`Intl.PhoneNumberFormat` (when available) rather than hand-rolled regex.

#### Postal codes

| Locale | Format | Example | Input mask |
|---|---|---|---|
| `ja-JP` | `NNN-NNNN` (3-4) | `100-0001` (Chiyoda, Tokyo) | `\d{3}-\d{4}` |
| `zh-CN` | `NNNNNN` (6 digits) | `100000` (Beijing) | `\d{6}` |
| `zh-TW` | `NNN` or `NNN-NN` (3 or 5) | `100` or `100-01` (Zhongzheng, Taipei) | `\d{3}(-\d{2})?` |
| `ko-KR` | `NNNNN` (5 digits) | `04524` (Seoul) | `\d{5}` |

**Japanese specific**: Postal codes have an autoload convention — typing
the postal code auto-fills prefecture / city / district. Common JS
libraries: `yubinbango` (most popular), `jp-postal-code`. Mercari, Cookpad,
Rakuten all use this pattern.

#### Address forms — BIG-ENDIAN order (CJK is OPPOSITE of Western)

CJK addresses go from **largest unit → smallest unit**:

```
Japanese:
〒100-0001
東京都 千代田区 千代田 1-1
ABC マンション 101号
山田 太郎 様

Western (English) equivalent — REVERSED:
Mr./Ms. Taro Yamada
ABC Mansion #101
1-1 Chiyoda, Chiyoda-ku
Tokyo 100-0001
JAPAN
```

**Form field order for CJK address forms** (top-to-bottom):

1. 郵便番号 / 邮政编码 / 우편번호 (postal code) — auto-fills next 2-3 fields
2. 都道府県 / 省市 / 시도 (prefecture / province / state)
3. 市区町村 / 区县 / 시군구 (city / district)
4. 番地・町名 / 街道地址 / 도로명 (street / sub-district)
5. 建物名・部屋番号 / 楼栋·房号 / 건물명·동호수 (building / apartment)
6. 受取人氏名 / 收件人姓名 / 받는 사람 (recipient name) — usually LAST in CJK address forms

**Western address forms reverse this order** — name first, then street,
city, state, postal code, country. **Do not blindly apply the Western
order to a CJK form.** This is a frequent localization bug.

The 25 JP DESIGN.md files do not explicitly cover address-form order, but
all observed Japanese e-commerce sites (Rakuten, Mercari) follow the
big-endian pattern. This rule is from general Japanese web-localization
practice.

### 3. Punctuation + line breaking

#### CJK punctuation (full-width by default)

Japanese punctuation is **full-width** — each glyph occupies the same
square cell as a kanji. Western half-width punctuation in JP body text
looks broken / amateur.

| Mark | Full-width JP (correct) | Half-width Western (wrong in JP body) |
|---|---|---|
| Period | `。` (U+3002) | `.` |
| Comma | `、` (U+3001) | `,` |
| Question | `？` (U+FF1F) | `?` |
| Exclamation | `！` (U+FF01) | `!` |
| Quote (open) | `「` (U+300C) | `"` or `'` |
| Quote (close) | `」` (U+300D) | `"` or `'` |
| Double quote | `『 』` (U+300E / U+300F) | `""` |
| Paren (open) | `（` (U+FF08) | `(` |
| Paren (close) | `）` (U+FF09) | `)` |
| Bullet | `・` (U+30FB) | `·` |
| Em-dash equivalent | `——` (two U+2014) or `─` (U+2500) | `--` or `—` |

**Per `template/DESIGN.md` line 116-117 and replicated in cookpad / abema /
toyota / muji / line / sansan**, the canonical kinsoku character lists are:

```
行頭禁止 (cannot start a line):
  ）」』】〕〉》、。，．・：；？！

行末禁止 (cannot end a line):
  （「『【〔〈《
```

Browsers handle these via:

```css
.body {
  line-break: strict;          /* enforce kinsoku-shori on JP punctuation */
  word-break: break-all;       /* JP rakuten/cookpad style — break anywhere */
  /* OR */
  word-break: keep-all;        /* Korean style — preserve word units */
  overflow-wrap: break-word;   /* always — breaks long URL / English words */
}
```

**Strategy by locale**:

| Locale | `word-break` | `line-break` | Notes |
|---|---|---|---|
| `ja-JP` | `break-all` (most JP sites) | `strict` | Allow break anywhere except prohibited chars |
| `zh-CN` / `zh-TW` | `break-all` or default | `strict` | Same Han logic as JP |
| `ko-KR` | **`keep-all`** | default | Preserve syllable-block grouping |

This is the single most-impactful Korean-specific rule and the most
forgotten when localizing Japanese-first templates to Korean.

#### Inter-word spacing — there is none in CJK

Latin: `the quick brown fox` — five tokens separated by spaces.

CJK: `今日は天気がいい` (Japanese) / `今天天气很好` (Chinese) / `오늘 날씨가 좋다` (Korean — Korean DOES have spaces) — the browser cannot identify "words" without language-aware segmentation.

Implications:

- **Never apply `letter-spacing` to mimic word-tracking** — JP/ZH have no
  word boundaries to track.
- **Never use `text-align: justify` on JP/ZH body** without testing —
  browsers fake justification by stretching `letter-spacing`, producing
  ugly fragmented characters. Korean tolerates justify slightly better
  because of its space-separated words.
- **CSS `word-spacing` is a no-op in JP/ZH** — there are no spaces to
  expand.

Korean is a hybrid: it has spaces between 어절 (eojeol, phrases) but not
between syllables. `word-spacing` works on Korean. `word-break: keep-all`
preserves these eojeol units.

#### Quotation marks (per language convention)

| Type | Japanese | Simplified Chinese | Traditional Chinese | Korean |
|---|---|---|---|---|
| Outer quotes | 「 」 | "" '' (U+201C/U+201D — same as Western) | 「 」 (per HK/TW publishing) | "" '' or 「 」 |
| Inner / nested | 『 』 | '' '' (single) | 『 』 | '' '' or 『 』 |
| Citation / book title | 『 』 | 《 》 (U+300A/U+300B) | 《 》 | 《 》 |

Per JP template line 117 and confirmed in 21+ JP DESIGN.md files: 「」 is
the Japanese quote convention. Per general Chinese web typography: SC uses
Western "" while TC uses 「 」 (a visible Mainland-vs-Taiwan publishing
divergence). Per Korean publishing: both Western "" and CJK 「 」 are
acceptable; modern Korean digital UI tends toward Western.

### 4. Cultural symbolism

| Element | Japan | Korea | China (SC) | Taiwan (TC) |
|---|---|---|---|---|
| **Red color** | Used in MUJI brand identity (#7f0019), error/danger, sale | Coupang Red is core brand (commerce), error/danger | **Auspicious** — weddings, festivities, commerce. Naver (Korea) uses green not red, but Coupang's red is intentional Korean commerce / urgency. In China: red+gold = wealth+luck, ALWAYS positive in commercial contexts | Same as China — auspicious red |
| **White** | Funerary in traditional contexts; OK in modern UI (most JP DESIGN.md use white background) | OK in modern UI; some older funerary association | Funerary in traditional contexts; modern UI uses white freely | Same as Mainland |
| **Black** | OK in modern UI; can carry Buddhist/funerary connotation in formal print | OK in modern UI | Generally negative — death, mourning. Use sparingly as background; OK as text | Same |
| **Gold** | Premium / luxury accent; rare in body UI | Premium accent | **Highly auspicious** — wealth, status. Common in fintech / luxury Chinese e-commerce | Same as Mainland |
| **Green** | Mostly neutral; some "fresh" connotation. ABEMA (#00b900), LINE | **Naver green (#03C75A)** is the main brand of Korea's largest portal — not unusual. | **AVOID green hat icon** (绿帽子) — connotation of cuckoldry. Be careful with full green-on-male avatars | Same |
| **Number 4** | Bad luck homophone of 死 (shi, "death") — avoid 4-step funnels labeled "STEP 4 of 4", avoid "4-day shipping" framing | Same — 사 (sa) homophone of 死. Some hospitals skip floor 4 | Same — 四 (sì) homophone of 死. Some buildings skip floor 4 | Same |
| **Number 8** | Neutral | Neutral | **Auspicious** — 八 (bā) homophone of 发 (fā, "wealth/prosperity"). Retail prices often end in 8 (¥98, ¥888) | Same |
| **Number 9** | Slightly negative — homophone of 苦 (ku, "suffering") in some contexts | Neutral | Auspicious — 九 (jiǔ) homophone of 久 (jiǔ, "long-lasting") | Same |
| **Lunar dates** | Limited usage — used for some festivals (旧正月) | Used for chuseok, seollal | **Used** — 农历 lunar calendar shown alongside Gregorian on news/calendar sites | Same |
| **Era systems** | 令和 (Reiwa, current era) — government / formal contexts use era year (令和8年 = 2026). Most modern UI uses Gregorian | Gregorian only on web | Gregorian only on web | 民國 (ROC era) on government / some formal sites — 民國115年 = 2026. Show Gregorian as primary on consumer UI |
| **Funeral / mourning UI** | Black background, gray-tone, no red. White lily / chrysanthemum imagery | Same | Black + white, no red. Chrysanthemum imagery | Same |
| **Wedding / festive UI** | Red + gold + white. Cherry blossoms (sakura) | Red + gold + white | Red dominant + gold | Red + gold + white |
| **Hand gestures (icons)** | OK: 👍 thumbs-up (universal). AVOID: hand-with-1-finger pointing (rude in formal contexts) | Same as Japan | 👍 OK in modern China but elders may find direct pointing rude | Same |
| **Personal name order in display** | **Family name FIRST** (山田 太郎 = Yamada Taro) — never invert | **Family name FIRST** (김철수 = Kim Chul-soo) | **Family name FIRST** (王小明 = Wang Xiao-ming) | Same as Mainland |

**Rule of thumb**: When unsure, ASK the legal-expert agent or the
multilanguage-copywriter agent. Do NOT guess at cultural appropriateness
of color/symbol combinations.

Sources for the table:
- Number 4 / 8 conventions: widely documented Asian cultural-gift / real-estate practice; not in DESIGN.md sources directly
- Family-name ordering: confirmed by `kakao/DESIGN.md` line 4 ("기술과 사람이 만드는 더 나은 세상"), Korean-language DESIGN.md files use natural Korean grammar
- White / black funerary connotation: cultural knowledge (NOT in DESIGN.md sources)

### 5. Microcopy patterns

#### Politeness levels

**Japanese honorifics — keigo**:

| Level | Form | When used | Example |
|---|---|---|---|
| Plain (普通形) | 〜だ / 〜する | Informal, peer chat | "保存する" |
| Polite (丁寧語 / です・ます) | 〜です / 〜ます | Default web copy | "保存します" |
| Honorific (尊敬語) | お〜になる / 〜なさる | Customer-facing service | "ご注文いただきます" |
| Humble (謙譲語) | お〜する / 〜いたす | Customer-facing service from "us" | "お送りいたします" |

**Default for web copy**: です・ます (mid-formal). Per `freee/DESIGN.md`,
`smarthr/DESIGN.md`, and `template/DESIGN.md` Do's & Don'ts sections —
business/SaaS UIs use です・ます-base. **Cookpad** and **note** use a
slightly softer です・ます with friendly hiragana endings ("おすすめ"
instead of "オススメ" or "推奨"). E-commerce checkout flows often switch
to keigo (お買い上げいただきありがとうございます) at confirmation.

**Korean speech levels**:

| Level | Ending | When used | Example |
|---|---|---|---|
| Plain (해라체) | -다 | Internal/dev | "저장한다" |
| Informal (해체) | -해 / -아/-어 | Friend chat | "저장해" |
| Polite (해요체) | -어요 / -아요 | Friendly UI (Daangn, Kakao) | "저장해요" |
| Formal-polite (합쇼체) | -ㅂ니다 / -습니다 | Professional UI (Toss, Naver, Coupang) | "저장합니다" / "저장하시겠습니까?" |

Per Toss `DESIGN.md` line 234-244 confirmation patterns — Korean fintech
defaults to **합쇼체 (formal-polite)**: "정말 삭제하시겠습니까?". Per Daangn
`DESIGN.md` Philosophy "Local: 동네 기반의 따뜻하고 친근한 경험" — community
apps use **해요체 (friendly-polite)**.

**Default for Korean web copy**: 합쇼체 for fintech / corporate / e-commerce
checkout, 해요체 for community / lifestyle / chat. NEVER use plain (-다)
for end-user UI.

**Chinese politeness**: Chinese has less verb-conjugation politeness than
JP/KO — politeness is conveyed via word choice (您 nín "you-formal" vs 你
nǐ "you-informal", 请 qǐng "please" prefix). Modern web copy uses 您 in
banking / corporate contexts and 你 in social / consumer contexts. Per
`zh-master` translated docs: the Chinese conventions follow Mainland
publishing-style of "informal-polite" 你 for tech products.

#### Direct vs implied subject

Japanese copy frequently **omits the subject**:

| English (subject-required) | Japanese (subject-implied) |
|---|---|
| "You can save this." | 「保存できます。」 (lit. "Can save.") |
| "We will send a confirmation." | 「確認メールをお送りします。」 (lit. "Send confirmation email.") |
| "Please enter your name." | 「お名前をご入力ください。」 |

**Translating Japanese-style microcopy to English**: add "you" / "we" back.
**Translating English-style microcopy to Japanese**: drop the subject,
shift verb to honorific where appropriate.

Korean similarly uses passive / impersonal voice for system messages but
NOT to the same degree as Japanese — Korean copy more often retains
explicit 회원님 (member-honorific you) or 고객님 (customer-honorific you).

#### Imperative buttons

| English | Japanese | Korean | Chinese (SC) | Chinese (TC) |
|---|---|---|---|---|
| Save | 保存 | 저장 | 保存 | 儲存 |
| Cancel | キャンセル (loanword) | 취소 | 取消 | 取消 |
| OK / Confirm | OK / 確認 / 決定 | 확인 | 确定 | 確定 |
| Submit | 送信 | 제출 / 등록 | 提交 | 提交 |
| Login | ログイン (loanword) | 로그인 (loanword) | 登录 | 登入 |
| Sign up | 新規登録 / サインアップ | 회원가입 | 注册 | 註冊 |
| Search | 検索 | 검색 | 搜索 | 搜尋 |
| Delete | 削除 | 삭제 | 删除 | 刪除 |
| Click here | クリック (often dropped — JP doesn't say "click here") | 클릭 (loanword, but often "여기를 누르세요") | 点击 (verb) / 点击此处 | 點擊 |

**Note on "Click here"**: Japanese UI rarely uses 「ここをクリック」 — instead
the action verb is the link label (「詳しくはこちら」 = "Details here", or
just 「保存」 as the button label). Korean UI similarly prefers verb-as-label.
Do not literally translate "Click here" — use the action verb.

#### Confirmation prompts

Per `template/DESIGN.md` line 218 and reproductions in cookpad / muji /
toyota:

| Pattern | Japanese | Korean | Chinese (SC) | Chinese (TC) |
|---|---|---|---|---|
| Soft confirm | 「本当に削除しますか？」 | "정말 삭제하시겠습니까?" | "确定要删除吗？" | "確定要刪除嗎？" |
| Strong (irreversible) | 「この操作は元に戻せません。続行しますか？」 | "이 작업은 되돌릴 수 없습니다. 계속하시겠습니까?" | "此操作不可撤销。是否继续？" | "此操作無法復原。是否繼續？" |
| Generic Y/N | 「はい / いいえ」 | "예 / 아니오" | "是 / 否" | "是 / 否" |

Per Toss `DESIGN.md` line 234-244 confirmation aesthetic — modern Korean
fintech uses formal honorific suffix `-시-` ("정말 ~ 하시겠습니까?") for ANY
destructive action, regardless of severity.

### 6. Locale machinery

#### `lang` attribute matrix

```html
<!-- Always set on <html> AND on any element with mixed-language content -->
<html lang="ja">                      <!-- Japanese (modern) -->
<html lang="ja-JP">                   <!-- Japanese, Japan -->
<html lang="ko">                      <!-- Korean -->
<html lang="ko-KR">                   <!-- Korean, South Korea -->
<html lang="zh-Hans">                 <!-- Simplified Chinese (modern) — preferred -->
<html lang="zh-Hant">                 <!-- Traditional Chinese (modern) — preferred -->
<html lang="zh-CN">                   <!-- Mainland China (legacy, still common) -->
<html lang="zh-TW">                   <!-- Taiwan (legacy, still common) -->
<html lang="zh-HK">                   <!-- Hong Kong (Cantonese + Traditional, with HK-specific glyphs) -->
<html lang="zh-Hant-HK">              <!-- Most explicit form -->

<!-- Mixed-content example -->
<p lang="ja">これは<span lang="en">JavaScript</span>のコードです。</p>
```

**Why this matters**: Without `lang`, the browser cannot select correct
font glyph variants from a unified Source Han / Noto CJK file (which
contains BOTH SC and TC variants in one file), and screen readers will
mispronounce. **All sources** in `awesome-design-md-jp` and
`awesome-k-design-md` set `<html lang="ja">` and `<html lang="ko">`
respectively, even when not documented in the DESIGN.md (it's in the
preview.html).

#### `hreflang` for multi-locale sites

```html
<!-- All locale variants of the same page must cross-link to each other -->
<link rel="alternate" hreflang="en" href="https://example.com/en/about">
<link rel="alternate" hreflang="ja" href="https://example.com/ja/about">
<link rel="alternate" hreflang="ko" href="https://example.com/ko/about">
<link rel="alternate" hreflang="zh-Hans" href="https://example.com/zh-cn/about">
<link rel="alternate" hreflang="zh-Hant" href="https://example.com/zh-tw/about">
<link rel="alternate" hreflang="x-default" href="https://example.com/en/about">
```

`x-default` is required for the fallback locale. Source files do NOT cover
hreflang directly (it's a metadata concern not a typography concern), but
this is part of any multi-locale CJK rollout.

#### BCP 47 codes — preferred forms in 2026

| Old code (still valid) | Preferred new code (BCP 47 / Unicode CLDR) |
|---|---|
| `zh-CN` | `zh-Hans-CN` or just `zh-Hans` |
| `zh-TW` | `zh-Hant-TW` or just `zh-Hant` |
| `zh-HK` | `zh-Hant-HK` |
| `ja-JP` | `ja-JP` (no change — only one script) |
| `ko-KR` | `ko-KR` (no change — only one script) |

Per CLDR convention, the **script subtag** (`Hans` / `Hant`) is more
informative than the country (`CN` / `TW`). Modern CMS / i18n libraries
(Vue i18n, Next.js i18n, react-intl) accept both forms.

#### Right-to-left

**None of CJK is RTL.** All four locales (Japanese, Korean, Simplified
Chinese, Traditional Chinese) write left-to-right horizontally as the
modern web default.

**Vertical-RL** (`writing-mode: vertical-rl`) exists for traditional
Japanese / Chinese typography but is NOT a general RTL scenario — Latin
text inside vertical-RL stays upright (`text-orientation: mixed`) or rotates
based on `text-orientation`. Confirmed by 25/25 modern JP DESIGN.md files
all marking vertical writing as "該当なし" / not applicable.

#### `Intl` API patterns

```javascript
// Date
const date = new Date('2026-04-26');
new Intl.DateTimeFormat('ja-JP', { dateStyle: 'long' }).format(date);
// "2026年4月26日"

new Intl.DateTimeFormat('ko-KR', { dateStyle: 'long' }).format(date);
// "2026년 4월 26일"

new Intl.DateTimeFormat('zh-CN', { dateStyle: 'long' }).format(date);
// "2026年4月26日"

// Number with currency
new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(9800);
// "￥9,800"

// Compact / myriad notation
new Intl.NumberFormat('ja-JP', { notation: 'compact' }).format(15000);
// "1.5万"

new Intl.NumberFormat('ko-KR', { notation: 'compact' }).format(15000);
// "1.5만"

// Relative time
new Intl.RelativeTimeFormat('ja', { numeric: 'auto' }).format(-1, 'day');
// "昨日"

new Intl.RelativeTimeFormat('ko', { numeric: 'auto' }).format(-1, 'day');
// "어제"

// Sort / collate (CJK names sort differently from Latin)
['张三', '王五', '李四'].sort(new Intl.Collator('zh-CN').compare);
// ['李四', '王五', '张三']  -- CJK collation uses 拼音 phonetic order in zh-CN
```

### 7. SEO impacts

#### Title length

CJK characters take ~2× the visual width of Latin characters in SERP
display. Google truncates around the same pixel width, so CJK titles need
to be much shorter in character count.

| Locale | Latin (English) max | CJK max | Pixel width target |
|---|---|---|---|
| Title | 60 chars | **28–32 chars** | ≈600px |
| Meta description | 155 chars | **80–100 chars** | ≈1000px |

Per general SEO best-practice: a 30-character JP title displays at roughly
the same width as a 60-char English title in mobile SERP. Source files do
not document SEO directly (DESIGN.md is design-spec, not SEO-spec) — this
rule is widely-known SEO localization practice.

#### Schema.org — `inLanguage`

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "ホットな日本のAIスタートアップ",
  "inLanguage": "ja-JP",
  "author": {
    "@type": "Person",
    "name": "山田 太郎",
    "givenName": "太郎",
    "familyName": "山田"
  }
}
</script>
```

Always include `inLanguage` on schema.org structured data so Google's
language detection is confirmed (helpful for `hreflang` matching).

### 8. Performance

#### Font subsetting strategy

CJK fonts are **massive** in their unsubset form:

| Font | Unsubset size | Reason |
|---|---|---|
| Noto Sans JP (full) | ~6 MB | All JIS X 0213 + extended kanji |
| Noto Sans CJK (full) | ~18 MB | JP + KO + SC + TC in one file |
| Source Han Sans CN | ~5 MB | Simplified Chinese only |
| Apple SD Gothic Neo | bundled | macOS / iOS — no download |
| Hiragino Kaku Gothic ProN | bundled | macOS — no download |

**Three viable strategies** (in order of recommendation):

**Strategy 1 — System fonts only (fastest)**

Per `pixiv/DESIGN.md` line 56: pixiv uses `system-ui, -apple-system, ...,
"Noto Sans"` and **does not load any webfont**. Zero-byte font payload,
instant first paint. Trade-off: typography is OS-dependent.

```css
font-family: system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", Roboto, "Helvetica Neue", "Apple SD Gothic Neo",
  "Noto Sans KR", Arial, sans-serif;
```

**Strategy 2 — Google Fonts CSS with auto-subsetting (recommended)**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
```

Google's CSS for Noto Sans JP is split into ~120 unicode-range chunks
(hiragana, katakana, common kanji, rare kanji, etc.). The browser only
downloads chunks containing characters actually used on the page. Typical
page payload: 50-200 KB instead of 6 MB.

```css
/* Critical: font-display: swap is non-negotiable for CJK */
@font-face {
  font-family: 'Noto Sans JP';
  font-style: normal;
  font-weight: 400;
  font-display: swap;          /* show fallback while CJK font loads */
  src: url(...) format('woff2');
  unicode-range: U+3041-3094;  /* Hiragana */
}
```

**Strategy 3 — Self-hosted with manual unicode-range subsetting**

When you control the content / CMS / glossary, you can pre-compute the
exact glyph set and subset the font to just those characters using
`fonttools` (Python) or `Glyphhanger`. Result: 5-30 KB font instead of 50-200 KB.

```bash
# Example using fonttools
pyftsubset NotoSansJP-Regular.otf \
  --text-file=corpus.txt \
  --output-file=NotoSansJP-Regular.subset.woff2 \
  --flavor=woff2
```

Use this for: marketing landing pages with fixed copy, e-commerce checkout
(small fixed string set), corporate sites with tightly-controlled content.

#### `font-display: swap` is mandatory for CJK

```css
@font-face {
  font-family: 'Noto Sans JP';
  font-display: swap;         /* CRITICAL */
  /* ... */
}
```

Without `swap`, browsers wait up to 3 seconds (FOIT — Flash Of Invisible
Text) before falling back. For a multi-MB CJK font on a slow connection,
that 3-second window starts the FOIT period, then the font may STILL not
have arrived, and the user sees blank text. With `swap`, the system font
renders immediately and is replaced when the webfont arrives — visible text
the entire time.

Per `note/DESIGN.md` line 197-200 — note explicitly applies
`-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
font-kerning: auto;` globally. Add these for CJK content too.

## Minimal example

A complete working snippet showing JP/KO/ZH coexisting:

```html
<!DOCTYPE html>
<html lang="ja">                 <!-- default page locale; override per-element below -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>多言語サンプル | 다국어 샘플 | 多语言示例</title>

  <!-- hreflang for SEO -->
  <link rel="alternate" hreflang="ja" href="/ja/sample">
  <link rel="alternate" hreflang="ko" href="/ko/sample">
  <link rel="alternate" hreflang="zh-Hans" href="/zh-cn/sample">
  <link rel="alternate" hreflang="zh-Hant" href="/zh-tw/sample">
  <link rel="alternate" hreflang="x-default" href="/en/sample">

  <!-- Webfonts: Google Fonts CSS auto-subsets per unicode-range -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Sans+KR:wght@400;700&family=Noto+Sans+SC:wght@400;700&family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">

  <style>
    /* Per-language body stacks — applied via :lang() pseudo-class */
    :lang(ja) {
      font-family:
        "Helvetica Neue", Arial,
        "Hiragino Kaku Gothic ProN", "Hiragino Sans",
        "Yu Gothic", YuGothic,
        "Noto Sans JP",
        Meiryo,
        sans-serif;
      line-height: 1.7;
      letter-spacing: 0;        /* default normal — heading rules can override */
      word-break: break-all;
      overflow-wrap: break-word;
      line-break: strict;
    }

    :lang(ko) {
      font-family:
        "Apple SD Gothic Neo",
        -apple-system, BlinkMacSystemFont,
        "Noto Sans KR",
        "Malgun Gothic",
        sans-serif;
      line-height: 1.5;
      letter-spacing: -0.01em;  /* per Toss / Daangn convention */
      word-break: keep-all;     /* CRITICAL for Korean */
      overflow-wrap: break-word;
    }

    :lang(zh), :lang(zh-Hans), :lang(zh-CN) {
      font-family:
        -apple-system, BlinkMacSystemFont,
        "PingFang SC", "Hiragino Sans GB",
        "Microsoft YaHei",
        "Noto Sans SC",
        sans-serif;
      line-height: 1.6;
      letter-spacing: 0;
      word-break: break-all;
      overflow-wrap: break-word;
    }

    :lang(zh-Hant), :lang(zh-TW) {
      font-family:
        -apple-system, BlinkMacSystemFont,
        "PingFang TC",
        "Microsoft JhengHei",
        "Noto Sans TC",
        sans-serif;
      line-height: 1.6;
      letter-spacing: 0;
      word-break: break-all;
      overflow-wrap: break-word;
    }

    /* Apply palt only to JP headings */
    :lang(ja) h1, :lang(ja) h2 {
      font-feature-settings: "palt", "kern";
      letter-spacing: 0.04em;
    }

    /* Body */
    body { font-size: 16px; color: #1a1a1a; }

    /* Buttons — wider min-width for CJK */
    .btn {
      min-width: 96px;
      padding: 12px 24px;
      border-radius: 8px;
      font-weight: 700;
      cursor: pointer;
    }
    .btn-primary {
      background: #0064FF;       /* Toss-influenced fintech blue */
      color: #fff;
      border: none;
    }

    /* Mobile floor */
    @media (max-width: 480px) {
      body { font-size: 14px; }  /* but not less */
    }
  </style>
</head>
<body>
  <article lang="ja">
    <h1>こんにちは、世界。</h1>
    <p>これは日本語のサンプル本文です。<span lang="en">JavaScript</span> のように
       異なる言語の語句が混じる場合は <code>lang</code> 属性で明示します。</p>
    <p>価格: <span class="price">¥9,800</span>（送料込み）</p>
    <button class="btn btn-primary">送信</button>
  </article>

  <article lang="ko">
    <h1>안녕하세요, 세계.</h1>
    <p>한국어 샘플 본문입니다. 가격: <span class="price">9,800원</span></p>
    <button class="btn btn-primary">확인</button>
  </article>

  <article lang="zh-Hans">
    <h1>你好,世界。</h1>
    <p>这是简体中文示例。价格: <span class="price">¥99</span></p>
    <button class="btn btn-primary">确定</button>
  </article>

  <article lang="zh-Hant">
    <h1>你好,世界。</h1>
    <p>這是繁體中文範例。價格: <span class="price">NT$99</span></p>
    <button class="btn btn-primary">確定</button>
  </article>
</body>
</html>
```

## Gotchas

A list of CJK localization traps that bite even experienced Western
developers:

1. **Korean `word-break: keep-all` is non-optional.** If you forget this,
   Hangul syllable blocks fragment across lines visually. JP/ZH default
   `word-break: break-all` produces the OPPOSITE behavior to what Korean
   needs. Per `awesome-k-design-md-main`, all 6 K-design files implicitly
   assume keep-all even though most don't state it. (Source: derived from
   absence of explicit override in Korean files + general Hangul typography
   knowledge.)

2. **`palt` belongs on JP headings, not body.** Per `note/DESIGN.md` line
   188, applying `palt` and `letter-spacing: 0.04em` to body text *reduces*
   readability because palt was designed for tight headings. WIRED.jp is
   the rare exception (palt on body for editorial-tight aesthetic, per
   `wired/DESIGN.md` line 144-150) — and even WIRED uses `palt` inconsistently
   (excludes WiredMono).

3. **Yen and yuan share the `¥` glyph.** A multi-currency cart that does
   `formatCurrency(amount, '¥')` is broken — it cannot distinguish ¥9,800
   JPY from ¥9,800 CNY (a 200× price difference). Always pass the ISO 4217
   code (`JPY` / `CNY`) and let `Intl.NumberFormat` choose the symbol.

4. **CJK family names go FIRST.** Display "山田 太郎" (Yamada Taro), NOT
   "Taro Yamada", inside CJK contexts. Schema.org `givenName`/`familyName`
   distinction matters because Western-style display ("Taro Yamada") is
   almost-always wrong in JP/KO/ZH UI.

5. **Apple's `¥` is fullwidth (U+FFE5), not halfwidth (U+00A5).** Per
   `Intl.NumberFormat('ja-JP')` output: "￥9,800" uses U+FFE5. Both
   browsers render correctly, but copy-paste users may pass the symbol
   into another field expecting half-width. Most JP sites use halfwidth `¥`
   (U+00A5) in form inputs and U+FFE5 only in display contexts.

6. **Vertical writing is NOT general "more authentic Japanese."** All 25
   modern JP DESIGN.md files in `awesome-design-md-jp` mark vertical
   writing as "該当なし" (not applicable). Reserve `writing-mode: vertical-rl`
   for: museum sites, traditional fiction publishers, calligraphy showcases,
   formal poetry. Modern web UI is horizontal LTR.

7. **`font-display: swap` becomes 10× more critical with CJK.** A 200 KB
   webfont over a 4G connection is ~3 seconds — within the FOIT window. A
   2 MB unsubset CJK font on slow 3G is 30+ seconds — vastly beyond. Without
   `swap`, the user sees blank space for the entire load. ALWAYS apply
   `font-display: swap` to any CJK `@font-face`.

8. **Source Han / Noto CJK is a multi-script unified font.** A single
   `Noto Sans CJK` file contains JP, KO, SC, TC glyphs. The `lang`
   attribute selects which variant glyph the engine picks (`国` SC vs `國`
   TC for the same Unicode codepoint U+570B / U+56FD shows different
   regional preferred forms). If you forget `lang`, the user gets the
   font's default variant, often Mainland-SC, which looks "wrong" to a TW
   reader.

9. **Address forms are big-endian in CJK.** Postal code FIRST (auto-fills
   prefecture/city), then administrative units largest-to-smallest, name
   LAST. Reversing this to Western order frustrates CJK users who skim
   forms top-to-bottom expecting their prefecture first.

10. **Number 4 is bad luck in JP/KO/ZH but `aria-label="4 of 4"` is OK.**
    The cultural avoidance applies to user-facing copy ("step 4", "level 4
    member") not to internal/aria attributes. Don't strip 4-step funnels —
    just rephrase user-facing labels ("最終ステップ" instead of "ステップ 4").

11. **`text-align: justify` is risky on CJK.** The browser justifies by
    expanding `letter-spacing`, which fragments characters of a single word
    visually. Korean tolerates this slightly because of its space-separated
    eojeol, but JP/ZH bodies should stay `text-align: start` or `left`.

12. **CJK input methods (IME) require `input` event, not `keypress`.** When
    a Japanese / Korean / Chinese user types via IME, intermediate
    candidate-text is composed across many key events. `keypress`
    handlers fire for partial composition; `input` fires only on commit.
    For real-time validation / autocomplete, use `input` + the
    `composition*` events (`compositionstart`, `compositionupdate`,
    `compositionend`) to suppress validation during composition.

## Cross-references

- [SKILL](../SKILL.md) — design-md skill orchestrator
- [amw-multilanguage-copywriter-agent](../../../agents/amw-multilanguage-copywriter-agent.md) — handles JP keigo levels,
  KO speech levels, CN politeness register; copy translation
- [typography-system](../../amw-design-principles/typography-system.md) —
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
  generic typography rules; this TECH file extends with CJK-specific values
- [SKILL](../../amw-seo/SKILL.md) — for `hreflang`,
  schema.org `inLanguage`, title-length impacts (referenced via the SEO
  skill's references/ folder)
- [amw-form-designer-agent](../../../agents/amw-form-designer-agent.md) — for CJK address forms with
  big-endian order, postal-code autoload
- [amw-accessibility-auditor-agent](../../../agents/amw-accessibility-auditor-agent.md) — for CJK screen-reader
  pronunciation requirements (`lang` attribute is mandatory accessibility
  primitive)

## Source attribution

This TECH file consolidates findings from:

- `docs_dev/extracted/google-labs/awesome-design-md-jp-main/awesome-design-md-jp-main/`
  — 25 JP DESIGN.md files: abema, apple, connpass, cookpad, cybozu, droga5,
  freee, line, mec, mercari, moneyforward, muji, note, notion, novasell,
  pixiv, qiita, rakuten, sansan, smarthr, studio, tabelog, toyota, wired,
  zenn — plus `template/DESIGN.md` (canonical 9-section JP template) and
  `CONTRIBUTING.md` (quality criteria).

- `docs_dev/extracted/google-labs/awesome-k-design-md-main/awesome-k-design-md-main/`
  — 6 KO DESIGN.md files: baemin, coupang, daangn, kakao, naver, toss
  (README claims more services but only 6 are present in the extracted
  archive).

- `docs_dev/extracted/google-labs/awesome-design-md-zh-master/awesome-design-md-zh-master/`
  — 58 ZH DESIGN.md files. **Note**: the zh variant is mostly *Chinese
  translation of Western DESIGN.md files* — most entries document Western
  brands (Stripe, Vercel, Linear, etc.) whose font stacks are NOT
  Chinese-localized. Only `bmw/DESIGN.md` line 7 + 43 + 66 and
  `sanity/DESIGN.md` line 66 explicitly document a Chinese fallback chain
  (Hiragino Sans GB / STXihei / Microsoft YaHei / WenQuanYi Micro Hei).
  This is a known gap — Chinese-specific UI conventions are documented
  here from general industry knowledge supplemented by those two files.

- `docs_dev/extracted/google-labs/awesome-design-md-main/awesome-design-md-main/`
  — English baseline (used to identify what JP/KO/ZH variants ADD vs the
  generic Western DESIGN.md format).

**Single-source claims** (marked here for reviewer attention):
- Address-form big-endian order — derived from real Japanese e-commerce
  practice; not explicitly in DESIGN.md sources.
- Cultural symbolism table (Number 4, 8, 9, color taboos, gold/red
  auspiciousness) — general East Asian cultural knowledge; not in
  DESIGN.md sources, which focus on typography/colors of specific brands.
- Furigana / `<ruby>` HTML5 syntax — not in any of the 89 DESIGN.md files;
  documented from W3C HTML5 spec.
- IME `compositionstart`/`compositionend` — not in DESIGN.md sources;
  general DOM API knowledge.
- Phone number / postal code formats — not in DESIGN.md sources; general
  telephony / postal regulation knowledge.

**Deferred (not found in sources)**:
- TC/HK-specific glyph variant differences between PingFang TC and PingFang
  HK — confirmed they differ but the specific glyph deltas are not
  documented in any source file.
- Cantonese (yue) UI conventions vs Mandarin TC — TC content can be
  Cantonese OR Mandarin; the linguistic distinction is not surfaced in
  DESIGN.md sources.
- Mongolian script (vertical Mongolian) — not within CJK scope, requires
  separate TECH file if ever needed.
