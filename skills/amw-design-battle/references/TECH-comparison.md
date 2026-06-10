# TECH-comparison — Battle card visual contract + summary template

## Table of Contents

- [1. `design-battle-card.html` — visual card](#1-design-battle-cardhtml-visual-card)
- [2. `design-battle-summary.md` — markdown table](#2-design-battle-summarymd-markdown-table)
- [3. Winner-determination algorithm (canonical)](#3-winner-determination-algorithm-canonical)
- [4. Cross-category note (when to add it)](#4-cross-category-note-when-to-add-it)
- [5. Verdict-note anti-patterns (do not emit)](#5-verdict-note-anti-patterns-do-not-emit)

**Version:** 1.0
**Status:** Canonical layout and phrasing rules for `amw-design-battle` deliverables. Load this file before emitting any battle card.

The battle card has three deliverables: an HTML visual card, a markdown summary, and a JSON record. This document specifies the contract for the first two. The JSON shape lives in the SKILL.md.

---

## 1. `design-battle-card.html` — visual card

### Layout

The card is a self-contained single HTML file. No external scripts, no external stylesheets, no remote font fetches. Inline `<style>` block. System-font fallback stack on every text element.

The card has FIVE regions stacked vertically:

```
┌─────────────────────────────────────────────────────────┐
│  HEADER                                                 │
│  - "Design Battle" title (h1)                           │
│  - Audit timestamp + rubric version (small muted)       │
├─────────────────────────────────────────────────────────┤
│  VERDICT STRIP                                          │
│  - Big result: "Side B wins 4-1 (3 ties)"               │
│  - Verdict note (one sentence)                          │
├─────────────────────────────────────────────────────────┤
│  PAIRED LABELS                                          │
│  - "Side A: <label>" left   |   "Side B: <label>" right │
├─────────────────────────────────────────────────────────┤
│  PER-DIMENSION ROWS (8 rows, one per dimension)         │
│  - Dimension name (left aligned)                        │
│  - A bar (left half, fills from center outward)         │
│  - B bar (right half, fills from center outward)        │
│  - A score + B score numerically                        │
│  - Winner marker (◀ or ▶ or "tie" or "n/a")             │
├─────────────────────────────────────────────────────────┤
│  FOOTER                                                 │
│  - Source URLs/paths for both artifacts                 │
│  - Category note (if cross-category)                    │
│  - Weighting note (if non-default)                      │
└─────────────────────────────────────────────────────────┘
```

### Paired-bar visual

Each dimension row uses the SAME row width. Both A and B bars start from a central axis and extend outward (A leftward, B rightward). Bar length = score × (half_row_width / 10). The visual gap between the two bars at the dimension's row is the dimension delta — readers can scan all 8 rows and the imbalances jump out.

When one side scores NULL on a dimension, that side's bar is rendered as a hatched/striped pattern of zero length plus a small "n/a" badge. The non-NULL side still extends from center; the row's winner is "by forfeit" labelled as such next to the winner marker.

### Colour rules

The card has TWO chromatic colours, one per side:

- **Side A:** OKLCH(60% .14 264) — a balanced blue (do NOT use green; green reads as "good", blue is neutral)
- **Side B:** OKLCH(60% .14 30) — a balanced warm orange (do NOT use red; red reads as "bad", orange is neutral)

Both colours have AA contrast against the card background (`#fafafa` light mode, `#0e0e10` dark mode — auto-detected via `prefers-color-scheme`).

Winner marker uses the winning side's colour at increased weight. Tie marker is text-only ("tie") in a neutral grey. "n/a" marker is small italic in the same neutral grey.

DO NOT use traffic-light colour coding (green = winner, red = loser). The rubric is neutral; the card must be neutral. The point is to SHOW the gap, not to declare moral judgement.

### Typography

- H1 title: 32px / 36px line-height / 600 weight
- Verdict strip headline: 24px / 28px line-height / 500 weight
- Verdict note: 14px / 20px / 400, muted colour
- Side labels: 16px / 20px / 500 weight, in each side's chromatic colour
- Dimension name: 16px / 20px / 500 weight
- Bar numeric scores: 14px / 20px / 600 weight (paired with each bar)
- Footer: 13px / 18px / 400, muted

All sizes use a 1.250 (minor-third) scale starting from a 13px base. Line-heights are explicit; do NOT use unitless line-height inheritance for the card.

### Responsive behavior

At viewport widths < 720px, the per-dimension rows collapse: the dimension name and winner marker stay full-width on top; A and B bars stack vertically rather than fanning from center. Numeric scores stay visible. The verdict strip remains at the top in either orientation.

DO NOT add a print stylesheet. The card is screen-first; users save it to PDF via the browser if needed.

### Accessibility

- All paired bars include `aria-label="Side A scored X.X on dimension Y; Side B scored Z.Z"` for screen-reader clarity.
- Winner markers include text equivalents (the markers ◀ / ▶ are decorative; the wins are also stated textually in the verdict strip and footer).
- Colour is NEVER the only signal — the textual "A wins / B wins / tie / n/a" appears next to every dimension row.
- Body text minimum contrast: 4.5:1 in both light and dark modes.
- Reduced-motion: the card MAY include a subtle bar-grow animation on initial render; honour `prefers-reduced-motion: reduce` and render bars at final length instantly when set.

---

## 2. `design-battle-summary.md` — markdown table

### Required structure

```markdown
# Design Battle: <Side A label> vs <Side B label>

**Audited:** <ISO 8601 + TZ>
**Rubric version:** 1.0

## Verdict

**<Side A | Side B | Tie>** wins overall, <X>-<Y> dimensions (<Z> ties).

<one-sentence verdict_note from JSON>

## Per-dimension scores

| Dimension     | A    | B    | Winner   | Delta |
|---------------|------|------|----------|-------|
| Palette       | 8.5  | 7.0  | A        | 1.5   |
| Typography    | 7.0  | 9.0  | B        | 2.0   |
| Rhythm        | 6.5  | 6.5  | tie      | 0.0   |
| Hierarchy     | 9.0  | 8.5  | tie      | 0.5   |
| Motion        | n/a  | 7.0  | B (forfeit) | — |
| Accessibility | 5.0  | 8.0  | B        | 3.0   |
| Consistency   | 8.0  | 7.5  | tie      | 0.5   |
| Signature     | 4.0  | 9.0  | B        | 5.0   |

## Evidence highlights

### Side A: <label>

- **<dimension where A scored highest>:** <evidence excerpt from A's grade-data>
- **<dimension where A scored lowest>:** <evidence excerpt from A's grade-data>

### Side B: <label>

- **<dimension where B scored highest>:** <evidence excerpt from B's grade-data>
- **<dimension where B scored lowest>:** <evidence excerpt from B's grade-data>

## Largest gap

The largest single-dimension gap is **<dimension>** (delta <X.X>) — <evidence A> vs <evidence B>.

## Footer

- Side A source: <URL or path>
- Side B source: <URL or path>
- Categories: <same / cross-category note>
- Weighting: <default unweighted / explicit weights>
```

### Phrasing rules for the verdict line

The verdict line in the markdown summary follows EXACT phrasing rules so the output is consumable by tooling that greps for victory state:

- `<Side A | Side B>` is the literal label (the user-supplied or default).
- `wins overall` or `ties overall` — never any other phrase ("comes out ahead", "edges out", "beats" are all forbidden — they have rhetorical bias).
- `<X>-<Y> dimensions` — wins counts. ALWAYS the winning side's count first.
- `(<Z> ties)` — tie count in parentheses.

Example: "Side B wins overall, 4-1 dimensions (3 ties)."

### Phrasing rules for verdict_note

The verdict_note is one sentence (≤200 chars) that names the most informative single observation. Templates:

- When the gap is dominated by one dimension: "The <dimension> gap (<delta>) drives the result; both sides tie on <count> other dimensions."
- When accessibility is the determining factor: "Side B's accessibility lead (delta <X>) is the structural difference; without it, the comparison would tie."
- When one side wins on signature while losing structural dimensions: "Side B has stronger signature but weaker accessibility; reader-priority dictates verdict."
- When the wins are evenly distributed: "No single dimension dominates; <side> wins on a broad spread of structural dimensions."
- When categories differ: "Categories differ (A is <category-a>, B is <category-b>); dimensional emphasis may not transfer."

NEVER use "obviously", "clearly", "vastly", "much better" — these are rhetorical filler that distort the data presentation.

---

## 3. Winner-determination algorithm (canonical)

This is the algorithm the JSON-emitter MUST follow. Any UI or tooling consuming the battle output assumes this exact logic:

```
for each dimension d in [palette, typography, rhythm, hierarchy, motion, accessibility, consistency, signature]:
  a_score = side_a.grade_data.dimensions[d].score
  b_score = side_b.grade_data.dimensions[d].score

  if a_score is NULL and b_score is NULL:
    winner[d] = "n/a"
    delta[d] = null
    note[d] = "both sides insufficient evidence"
  elif a_score is NULL:
    winner[d] = "b"
    delta[d] = null
    note[d] = "by forfeit; A is " + a_grade_data.dimensions[d].evidence
  elif b_score is NULL:
    winner[d] = "a"
    delta[d] = null
    note[d] = "by forfeit; B is " + b_grade_data.dimensions[d].evidence
  else:
    diff = abs(a_score - b_score)
    if diff <= 0.5:
      winner[d] = "tie"
      delta[d] = round(a_score - b_score, 1)
    elif a_score > b_score:
      winner[d] = "a"
      delta[d] = round(a_score - b_score, 1)
    else:
      winner[d] = "b"
      delta[d] = round(b_score - a_score, 1)

# Overall
a_wins = count of d where winner[d] == "a"
b_wins = count of d where winner[d] == "b"
ties   = count of d where winner[d] == "tie"
na     = count of d where winner[d] == "n/a"

if a_wins > b_wins:  overall = "a"
elif b_wins > a_wins: overall = "b"
else: overall = "tie"
```

The 0.5 tie threshold is canonical. Do NOT change it without bumping the rubric version.

---

## 4. Cross-category note (when to add it)

The cross-category note appears in the report-card footer and the MD summary footer when the two artifacts are in clearly different domains. Heuristic for "different category":

- Marketing landing page vs internal admin dashboard
- E-commerce product detail vs developer tool homepage
- Static documentation vs interactive single-page app
- Mobile-first PWA vs desktop-first enterprise tool

When in doubt, do NOT add the note. The default is "same category, no special note." The note exists to warn the reader that dimensional priorities (motion's relative importance, signature's relative importance, etc.) may not transfer — it does NOT alter the scoring.

---

## 5. Verdict-note anti-patterns (do not emit)

- "The clear winner is X" — forbidden. Use "X wins overall, A-B dimensions (C ties)."
- "A is much better than B" — forbidden. Use "A leads on N dimensions; B leads on M; X dimensions tie."
- "A is unequivocally superior" — forbidden. The rubric does not measure superiority; it measures eight specific dimensions.
- "B should be redesigned" — forbidden. The battle card describes, it does not prescribe.
- Numbers without units — wrong. "A scores 8.5" not "A is 8.5."

The card and summary are neutral data presentations. Verdict opinions belong in the analyst's follow-up, not in the deliverables.
