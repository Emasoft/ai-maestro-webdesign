# Design Laws and Heuristics

## Table of Contents

- [I. Gestalt's five principles (organizing the visual field)](#i-gestalts-five-principles-organizing-the-visual-field)
- [II. Fitts's Law](#ii-fittss-law)
- [III. Hick's Law](#iii-hicks-law)
- [IV. Miller's Law (7 ± 2)](#iv-millers-law-7-2)
- [V. Jakob's Law](#v-jakobs-law)
- [VI. The four dimensions of visual hierarchy](#vi-the-four-dimensions-of-visual-hierarchy)
- [VII. F-Pattern vs Z-Pattern reading](#vii-f-pattern-vs-z-pattern-reading)
- [VIII. Peak-End Rule](#viii-peak-end-rule)
- [IX. Aesthetic-Usability Effect](#ix-aesthetic-usability-effect)
- [Self-check list](#self-check-list)
- [X. Refactoring-UI atomic audit rules (T-054)](#x-refactoring-ui-atomic-audit-rules-t-054)

> These are **classic design laws** that hold across eras and styles. Violating them is like violating physics — the user experience is guaranteed to suffer.

---

## I. Gestalt's five principles (organizing the visual field)

The human brain automatically groups related information. The designer's job is to **make that automatic grouping match the information structure**.

### 1. Proximity
**Elements that are close together are perceived as a group.**

```
❌ title ──16px── desc ──16px── meta ──16px── (next block)
   All distances equal → unclear which items belong together

✅ title ──8px── desc ──16px── meta ──48px── (next block)
   Tight within a group, loose between groups
```

### 2. Similarity
**Elements with similar styling are perceived as the same kind.**

- All "clickable" items share one accent color
- All "secondary info" shares one muted gray
- **Forbidden**: one CTA is an orange button, another CTA is a blue text link (forces the user to guess)

### 3. Closure
**The brain automatically completes incomplete shapes.**

Application: you don't need to draw a closed rectangle to indicate "this is a card." A thin bottom line + left/right alignment + consistent internal padding is enough — the brain fills in the "card" boundary.

### 4. Continuity
**The eye prefers to follow smooth curves and straight lines.**

Application:
- Left-align > center-align (all text starts on the same vertical line, so scanning takes less effort)
- Avoid making important content cross obvious visual discontinuities

### 5. Figure-Ground
**Contrast = focus.**

- Bright element on a dark background → focus
- Saturated color on a neutral ground → focus
- **Rule**: at most 1 "figure"-level focus per screen; everything else is "ground"

---

## II. Fitts's Law

**Time to reach a target ∝ distance / target size**

```
T = a + b × log₂(distance / target size + 1)
```

In plain English: **the bigger the target and the shorter the distance, the easier it is to click.**

### Application

| Scenario | Heuristic |
|----------|-----------|
| Primary CTA button | Large (≥ 48px), placed at the end of the visual flow (bottom-right / bottom) |
| Secondary action | Can be smaller, but not below 32px |
| Mobile critical buttons | **At least 44×44px** hit target |
| Screen edges | **Infinitely large target** (the cursor gets stopped), so close buttons work best in the corners |
| Destructive operations | Deliberately placed far / made small to raise the cost of the action ("Delete account" hidden in a secondary menu) |

---

## III. Hick's Law

**The more choices there are, the longer the decision takes (logarithmic growth).**

```
T = b × log₂(n + 1)
```

### Application

- **1 of 3** is far faster than **1 of 7**
- Main menu items ≤ 7
- Trim every form field you can
- Too many options → switch to **progressive disclosure** (ask the core question first, then branch based on the answer)
- Apple's site has always kept ~5 nav items

### Counter-example

Amazon's homepage is crammed with options → but in practice users just use the search box and ignore the categories.

---

## IV. Miller's Law (7 ± 2)

**Short-term memory capacity: 7±2 units.**

### Application

- One group of information ≤ 5–7 items
- Phone-number grouping: 138-1234-5678 (3 groups), not 13812345678
- Nav-bar items ≤ 7
- Product feature list ≤ 5

Past that, **chunk and layer**.

---

## V. Jakob's Law

**Users spend most of their time on other sites, so they expect your site to behave like every other site.**

### Application

- Logo top-left, search box top-right, primary CTA in the hero center or top-right
- Shopping-cart icon top-right
- Hamburger icon means "menu"
- Form "submit" button at the bottom

**Breaking convention = forcing the user to relearn = friction. Don't violate this unless you have a strong brand or experience reason.**

---

## VI. The four dimensions of visual hierarchy

To make one element "stand out most," tune in this priority order:

```
1. Size     (the strongest weapon)
2. Color    (saturation + contrast)
3. Weight   (font weight)
4. Spacing  (whitespace = breathing room = importance)
5. Position (top-left / center / bottom each carry meaning)
```

**Rule**: **stack** these dimensions together (big + bold + saturated + plenty of whitespace). A combined signal is clearer than any single dimension alone.

### Counter-example (no hierarchy)

```css
/* ❌ Every piece of text is 16px Regular #333 */
/* → User doesn't know where to look */
```

### Correct example (clear hierarchy)

```css
h1    { 48px / 700 / #000 / margin-bottom: 24px }  /* most prominent */
lead  { 20px / 400 / #333 / margin-bottom: 16px }  /* next */
body  { 16px / 400 / #555 }                         /* default */
meta  { 12px / 400 / #888 }                         /* weakest */
```

---

## VII. F-Pattern vs Z-Pattern reading

### F-Pattern (long content / text-dense)

- User scans from top-left to the right → back to the left lower down → scans right again → then moves vertically
- Use for: blogs, news, email, search results
- **Design implication**: put the important information in the **first two lines + the left column**

### Z-Pattern (short content / visually driven)

- Top-left → top-right → bottom-left → bottom-right
- Use for: landing pages, posters, single-page ads
- **Design implication**:
  - Top-left = logo
  - Top-right = navigation / secondary CTA
  - Bottom-left = supporting copy
  - Bottom-right = **primary CTA** (end of the flow)

---

## VIII. Peak-End Rule

**A person's memory of an experience is determined by two moments: the peak and the last moment.**

### Application

- The first load needs a "wow" moment (hero animation, key visual)
- The completion / success page must be designed with care (Stripe's ✓ animation is the textbook example)
- The middle can be plain, but **the opening and the ending cannot be plain**

---

## IX. Aesthetic-Usability Effect

**Users perceive more attractive designs as easier to use, even when the functionality is identical.**

This is not "pretty skin beats everything"; it's that **aesthetics is a function**. Don't use "function over form" to justify ugliness.

---

## Self-check list

When making a design decision, ask yourself:

- [ ] Are related elements using proximity (placed close together)?
- [ ] Are same-kind elements using similarity (consistent styling)?
- [ ] Does the primary CTA satisfy Fitts's Law (big + easy to reach)?
- [ ] Is the number of options ≤ 7 (Hick + Miller)?
- [ ] Am I breaking Jakob (user common sense)? If so, is the reason strong enough?
- [ ] Does the visual hierarchy use at least 2–3 dimensions (size / color / weight / spacing)?
- [ ] Did I pick F-pattern vs Z-pattern correctly?
- [ ] Do the opening and ending have peak moments (Peak-End)?

---

## X. Refactoring-UI atomic audit rules (T-054)

> Ledger T-054. Source: refactoring-ui-plugin-main (MIT). Attribution: rules and patterns from *Refactoring UI* by Adam Wathan & Steve Schoger (https://refactoringui.com/).

### Button hierarchy failure modes

| Failure | Description | Fix |
|---|---|---|
| **Button Battle** | Save and Cancel both filled with brand color | Make Cancel outline or grey solid |
| **Gray Confusion** | Very light grey (200) secondary looks disabled | Use grey 400–500 or outline instead of near-white grey |
| **Red Alert** | Delete button more prominent than primary action | Make Delete text-only red; it should not compete |
| **Primary Overload** | 3+ buttons sharing the same "primary" visual weight | Choose one true primary; demote the rest |
| **Invisible Tertiary** | Text links same color as body copy | Use brand color or underline for tertiary actions |

**Button level map:** Primary = filled brand color · Secondary = grey solid or outline · Tertiary = text-only · Destructive = text red (never competing solid).

### 5-step declutter sequence

When a component looks too heavy, work through this sequence and stop as soon as clarity is achieved:

1. **Remove borders** → replace with spacing.
2. **Remove or reduce backgrounds** → use whitespace to group.
3. **Remove separators** → increase the gap between sections instead.
4. **Soften or remove shadows** → keep only for elevation (modals, dropdowns, hover states).
5. **Add back only what is needed** for hierarchy or essential clarity.

Do not skip ahead. Most clutter problems resolve at step 1 or 2.

### Shadow elevation scale (5 levels)

| Level | Use case | CSS (approximate) |
|---|---|---|
| **None** | Static text, icons, flat content | `none` |
| **Subtle** | Cards (alternative to borders) | `0 2px 4px rgba(0,0,0,0.1)` |
| **Low** | Raised cards, hover affordance on buttons | `0 4px 6px rgba(0,0,0,0.1)` |
| **Medium** | Dropdowns, popovers, tooltips | `0 10px 15px rgba(0,0,0,0.1)` |
| **High** | Modals, dialogs, drawers | `0 20px 25px rgba(0,0,0,0.15)` |

**Shadow carpet anti-pattern:** applying any non-None shadow to every card on a page. Flatten static cards; subtle shadows are acceptable as an alternative to borders, but uniform shadow-on-everything eliminates depth signal entirely.

**Black shadows rule:** never use pure `rgba(0,0,0,*)` at opacity > 0.15 without tinting toward the brand color. Harsh black shadows read cheap.

### Grey palette and hex rule

- Define **8–10 explicit grey shades** (near-white to near-black) as named design tokens.
- Assign explicit hex values; do NOT derive shades at render time with `rgba(0,0,0,0.05)` etc. — opacity-derived greys produce inconsistency across backgrounds.
- The majority of any UI surface is grey; 3–4 shades is always too few.

### Empty-state 5-part template

Every zero-content screen must answer all five in order:

1. **Illustration / icon** — relevant to the content type; never generic "404" style.
2. **Headline** — friendly, explanatory ("No reports yet", not "Empty" or "No data").
3. **Description** — one or two sentences: what this area is for, how to add content.
4. **Primary action** — a clear CTA button; the obvious next step.
5. **Secondary info** (optional) — learn-more link, template, import option.

Hide tabs, filters, and sort controls that serve no purpose without content — they create a false impression of a broken interface.
