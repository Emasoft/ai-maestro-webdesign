# ASCII style presets and banned characters

## Table of Contents

- [Style presets (orthogonal to mode selection)](#style-presets-orthogonal-to-mode-selection)
- [Banned characters (severity-rated — enforced by validate-ascii.py)](#banned-characters-severity-rated-enforced-by-validate-asciipy)
- [Cross-references](#cross-references)

Source provenance: style presets come from `SKILLS-TO-INTEGRATE/diagrams-skills/diagram-skill-main/ASCII-STYLES.md` lines 5-155; banned characters come from `bin/amw-validate-ascii.py` lines 72-98 (`%forbidden_chars` table).

## Style presets (orthogonal to mode selection)

The mode (`diagram` / `table` / `layers` / `sequence` / freeform) picks **structure**. A style preset picks **aesthetic** — how much labeling, how many Unicode glyphs, inline vs. boxed. These are an opt-in dial; the default is `unicode` for Mode A and hand-author-as-you-go for Mode B. You can name the style explicitly in the brief ("use the clasico style") or the skill will infer it from context (target is a plain-text README → clasico; terminal screenshot for a docs site → detallado).

| Preset | Glyph set | Labels on edges | Width | Use when |
|---|---|---|---|---|
| `detallado` (detailed) | Unicode box-drawing + `> v ╭╮╰╯` | Yes (numbered `1. Request`) | Widest | Docs/review artifacts, high clarity, labelled steps |
| `unicode` | Unicode box-drawing | No | Medium | Large diagrams where label clutter dominates |
| `clasico` (classic) | Pure ASCII (`+` `-` `\|` `>` `<` `v` `^`) | Optional | Medium | READMEs, maximum compatibility, copy-paste-safe |
| `compacto` (compact) | One-line inline: `A -> B -> C` with `-+-` / `+-` fan-outs | No | Narrowest | Linear flows, single-line summaries, captions |

### Preset examples

**`detallado`** — all boxes + labels + semantic shapes (rounded for DBs):

```
+--------+  1. Request   +----------+  2. Process   +---------+
| Client |-------------->| Gateway  |-------------->| Service |
+--------+               +----------+               +---------+
                               |
                               | 3. Query
                               v
                         /----------\
                         |    DB    |
                         \----------/
```

**`unicode`** — boxes without edge labels (rendered with `+---+` here for cross-doc safety; in actual output the skill uses the `+---+` to `+---+` Unicode equivalents):

```
+--------+     +----------+     +---------+
| Client |---->| Gateway  |---->| Service |
+--------+     +----------+     +---------+
```

**`clasico`** — pure ASCII (the same as `unicode` but never substitutes Unicode box-drawing for `+ - |`):

```
+--------+     +----------+     +---------+
| Client |---->| Gateway  |---->| Service |
+--------+     +----------+     +---------+
```

**`compacto`** — inline:

```
Client -> Gateway -> Service -> DB
```

**`compacto` with fan-out:**

```
Client -> Gateway -+-> Service A -> DB-A
                   +-> Service B -> DB-B
```

The preset is orthogonal to the Mode A sub-mode: `--style clasico` + `sub-mode: layers` produces ASCII-only layered architecture; `--style detallado` + `sub-mode: sequence` produces a sequence diagram with labelled messages and Unicode lifelines. Mode B freeform wireframes usually imply `unicode` (box-drawing of a UI frame); a user explicitly asking for a "retro terminal" look wants `clasico`.

## Banned characters (severity-rated — enforced by validate-ascii.py)

The validator flags these as forbidden because they render at variable width in most monospaced fonts. They are tiered by severity so the FIX iteration loop fixes **CRITICAL first** (definitely breaks alignment for everyone), then **HIGH** (breaks on common fonts), then **MEDIUM** (may break on some fonts). The validator reports the tier in the error code (e.g. `FORBIDDEN_CHAR_CRITICAL`, `FORBIDDEN_CHAR_HIGH`, `FORBIDDEN_CHAR_MEDIUM`) — address them in that order.

### CRITICAL — will definitely break alignment

| Banned codepoint | Approx. width | Use instead |
|---|---|---|
| `U+27F6` (LONG RIGHTWARDS ARROW) | 3-4x | `-->` or `->` |
| `U+27F5` (LONG LEFTWARDS ARROW) | 3-4x | `<--` or `<-` |
| `U+27F9` (LONG RIGHTWARDS DOUBLE ARROW) | 3-4x | `==>` |
| `U+27F8` (LONG LEFTWARDS DOUBLE ARROW) | 3-4x | `<==` |
| `U+27F7` (LONG LEFT RIGHT ARROW) | 4-5x | `<->` |
| `U+27FA` (LONG LEFT RIGHT DOUBLE ARROW) | 4-5x | `<=>` |

### HIGH — likely to break alignment on common fonts

| Banned codepoint | Approx. width | Use instead |
|---|---|---|
| `U+21D2` (RIGHTWARDS DOUBLE ARROW) | 1.5-2x | `=>` |
| `U+21D0` (LEFTWARDS DOUBLE ARROW) | 1.5-2x | `<=` |
| `U+21D4` (LEFT RIGHT DOUBLE ARROW) | 2x | `<=>` |
| `U+21D1` (UPWARDS DOUBLE ARROW) | 1.5x | `^` |
| `U+21D3` (DOWNWARDS DOUBLE ARROW) | 1.5x | `v` |
| `U+21D5` (UP DOWN DOUBLE ARROW) | 1.5x | `^v` |

### MEDIUM — may break alignment on some fonts

| Banned codepoint | Approx. width | Use instead |
|---|---|---|
| `U+25B6` (BLACK RIGHT-POINTING TRIANGLE) | 1.2-1.5x | `>` |
| `U+25C0` (BLACK LEFT-POINTING TRIANGLE) | 1.2-1.5x | `<` |
| `U+25B2` (BLACK UP-POINTING TRIANGLE) | variable | `^` |
| `U+25BC` (BLACK DOWN-POINTING TRIANGLE) | variable | `v` |
| `U+21C6` (LEFTWARDS ARROW OVER RIGHTWARDS ARROW) | 2x | `<>` |
| `U+21C4` (RIGHTWARDS ARROW OVER LEFTWARDS ARROW) | 2x | `><` |

### Always-banned regardless of tier

| Banned | Why | Use instead |
|---|---|---|
| Most emoji | 2-col in terminals | `[!]` `(*)` `[x]` `[ ]` `*` |
| CJK characters | 2-col in monospaced terminals | Romanized text, or account for +1 col per char on that row |

If the user insists on including an emoji or CJK char, account for its 2-col width explicitly in the frame (the frame right-edge shifts right by 1 for each 2-col char on that row).

## Cross-references

- [SKILL](../SKILL.md) — the parent skill (Mode A / Mode B authoring).
- [SKILL](../../amw-ascii-validator/SKILL.md) — validator that enforces these bans.
- [SKILL](../../amw-ascii-sketch/SKILL.md) — plan-phase iteration skill that applies the same banned-character substitutions before emitting variants.
