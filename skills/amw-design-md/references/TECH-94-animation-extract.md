# TECH-94: Animation, transition, and motion extraction

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Architecture](#architecture)
- [What dev-browser captures](#what-dev-browser-captures)
- [Motion-role classification](#motion-role-classification)
- [Duration normalization](#duration-normalization)
- [Easing normalization](#easing-normalization)
- [Output schema](#output-schema)
- [Worked example](#worked-example)
- [Failure modes](#failure-modes)
- [Cross-references](#cross-references)

## What it does

Documents how `amw-design-md-extractor-agent` reads `transition-*`, `animation-*`, and `transform` properties from a live URL, classifies each by **motion role** (entry, exit, hover, focus, page-transition), and emits a normalized `motion.{role}.{duration,easing}` block under `extensions.motion` in the DESIGN.md frontmatter.

Variant 1 DESIGN.md does not specify a motion section in its core schema; motion lives in the extension namespace per [extension-sections-10-14](./extension-sections-10-14.md).

The base capture flow (DOM walk + computed-style sampling) is shared with [TECH-07-url-extraction](TECH-07-url-extraction.md); this TECH focuses on the **role classification + normalization** layer specific to motion.

## When to use

- User says: "extract DESIGN.md from <URL> with motion / animation tokens"
- User says: "I want the transition system from this site"
- Brand-researcher: extracting from a site where motion is a key brand signal (Linear, Stripe, Vercel-style sites)

## When NOT to use

- User explicitly only wants Variant 1 core tokens → skip; do not bloat frontmatter with unused extension namespace
- Site uses `prefers-reduced-motion: reduce` exclusively (no animations under any user preference) → return empty `motion: {}` + prose note
- Site uses JS-driven motion (Framer Motion, GSAP, anime.js) with no CSS transitions → out of scope for this TECH; record in `warnings`

## Architecture

```
        URL ─────► dev-browser eval ────► JSON snapshot
                                          (computed + matched rules)
                          │
                          ▼
        For each element + each :state pseudoclass:
          {selector, transition_value, animation_value, transform_value, role}
                          │
                          ▼
        Parse transition_value into transition_layers:
          { property, duration, easing, delay }
                          │
                          ▼
        Classify each layer by motion role:
          - hover: triggered on :hover
          - focus: triggered on :focus / :focus-visible
          - entry: animation-name on initial render (e.g., fadeIn)
          - exit: animation-name on removal (rare; often JS)
          - page-transition: matched on layout-root selectors
                          │
                          ▼
        Cluster durations + easings per role
                          │
                          ▼
        Emit extensions.motion.{role}.{duration,easing} entries
```

## What dev-browser captures

The extraction extends the standard JSON snapshot with a `motion` array. Because transitions and animations are state-triggered (`:hover`, `:focus`), the eval script reads the matched CSS rules — NOT just computed styles, which only reflect the current state:

```js
function captureMotion() {
  const motion = [];
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch { continue; }  // CORS skip
    if (!rules) continue;
    for (const rule of rules) {
      if (rule.type !== CSSRule.STYLE_RULE) continue;
      const s = rule.style;
      const t = s.transition || s.transitionDuration;
      const a = s.animationName;
      const tr = s.transform;
      if (!t && !a && !tr) continue;
      motion.push({
        selector: rule.selectorText,
        transition: t,
        transitionDuration: s.transitionDuration,
        transitionTimingFunction: s.transitionTimingFunction,
        transitionDelay: s.transitionDelay,
        transitionProperty: s.transitionProperty,
        animationName: a,
        animationDuration: s.animationDuration,
        animationTimingFunction: s.animationTimingFunction,
      });
    }
  }
  return motion;
}
```

CORS-restricted external stylesheets are silently skipped (the browser blocks reading their rules). Inline `<style>` and same-origin sheets cover most real sites.

## Motion-role classification

The post-processor classifies each captured rule by inspecting the selector + properties:

| Selector pattern / property | Inferred role |
|---|---|
| Selector contains `:hover` | `hover` |
| Selector contains `:focus`, `:focus-visible` | `focus` |
| `animationName` set, not `:hover`/`:focus` | `entry` (one-shot on mount) |
| Selector contains `[data-state="open"]`, `.active`, `.is-visible` | `entry` (visibility toggle) |
| Selector matches `main`, `[role="main"]`, `body.page` | `page-transition` |
| `transition-property` includes `opacity`, `transform`, transition on a button-shaped element | `hover` (likely; verify) |
| `transition-property: all` (catch-all) | `hover` (most common; flag if uncertain) |
| Default fallback | `interactive` (generic state change) |

Ambiguous classifications get tagged with a `confidence: low` marker in the captured data; the emitter notes them in prose ("Detected as hover but the selector is generic — verify intent").

## Duration normalization

CSS supports `ms` and `s` units. The post-processor:

1. Convert every duration to milliseconds.
2. Quantize to a 25ms grid (round to nearest 25). Modern systems typically use 100/150/200/300/500ms steps; the grid removes noise from `223ms` / `247ms` rounding artifacts.
3. Cluster the rounded values per role.
4. The most-frequent duration per role wins → becomes `motion.{role}.duration`.
5. Other observed durations are listed in `motion.{role}.alternates` (informational).

## Easing normalization

CSS easings come in three forms: keywords (`ease`, `ease-in`, `ease-out`, `ease-in-out`, `linear`), bezier curves (`cubic-bezier(...)`), and `steps()`. Normalization:

1. **Keywords** preserved as-is.
2. **Custom bezier curves** kept verbatim AND tagged with the nearest keyword (computed by control-point distance to the 5 keyword presets). Example: `cubic-bezier(0.4, 0, 0.2, 1)` → labeled `≈ ease-out`.
3. **`steps()`** preserved as-is; rarely appears in real-world transitions; if present, flagged as suspect because it usually indicates a sprite-sheet animation, not a UI transition.

The most-frequent easing per role wins → becomes `motion.{role}.easing`. Other observed easings appear in `motion.{role}.alternates`.

## Output schema

```yaml
extensions:
  motion:
    hover:
      duration: "150ms"
      easing: "cubic-bezier(0.4, 0, 0.2, 1)"   # ≈ ease-out
      properties: ["background-color", "transform", "box-shadow"]
      usage: "button + card hover lift; subtle color shift"
    focus:
      duration: "150ms"
      easing: "ease-out"
      properties: ["outline-color", "outline-offset"]
      usage: "focus ring fade-in"
    entry:
      duration: "300ms"
      easing: "cubic-bezier(0, 0, 0.2, 1)"     # ≈ ease-out
      properties: ["opacity", "transform"]
      usage: "modal / drawer / popover entry"
    page-transition:
      duration: "500ms"
      easing: "cubic-bezier(0.4, 0, 0.2, 1)"
      properties: ["opacity"]
      usage: "route change crossfade"
    reduced-motion:
      duration: "0ms"
      easing: "linear"
      usage: "respects prefers-reduced-motion: reduce"
```

If the site does NOT declare a `@media (prefers-reduced-motion: reduce)` block, the extractor adds `reduced-motion: { duration: "0ms" }` as a default with a `warnings` entry — every motion-using design system SHOULD ship reduced-motion support per WCAG.

## Worked example

Input: Vercel.com homepage.

dev-browser captures 31 rules with motion properties:
- 12 hover transitions on buttons/links (150ms ease-out)
- 6 focus rings on inputs/buttons (150ms ease-out)
- 8 entry animations on hero copy (300-500ms cubic-bezier)
- 3 `prefers-reduced-motion: reduce` overrides
- 2 generic `transition: all` on cards (classified as `hover`, confidence low)

Result: 4 populated motion roles + a reduced-motion entry. Prose note: "2 rules used `transition: all` — verify hover is the intended role; consider tightening the transition-property list".

## Failure modes

| Failure | Cause | Recovery |
|---|---|---|
| All motion comes from JS (Framer Motion etc.) | No CSS to extract | Return empty `extensions.motion: {}` + warning "Motion appears JS-driven; CSS extraction yielded no tokens" |
| CORS blocks external stylesheets | Cross-origin CDN-hosted CSS | Capture what's available; record skipped sheets in `warnings` |
| Mixed easings per role (no clear winner) | Site has inconsistent motion | Pick most-frequent; surface alternates in prose; suggest user pick canonical |
| `transition: all` everywhere | Common Tailwind / pre-flight default | Classify by selector role; flag ambiguity |
| `@keyframes` referenced but not parsed | Animation name without the keyframes block | Record the animation-name only; do NOT reconstruct keyframes |
| Reduced-motion override missing | Site doesn't ship a11y | Emit `reduced-motion: 0ms` default + warning |

## Cross-references

- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — base URL extraction flow
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- [TECH-86-multi-page-extract](./TECH-86-multi-page-extract.md) — when motion differs across pages, multi-page merge applies
- [TECH-91-shadow-and-elevation-extract](./TECH-91-shadow-and-elevation-extract.md) — shadows often participate in hover transitions; extract together
- [TECH-96-container-query-extract](./TECH-96-container-query-extract.md) — modern motion sometimes depends on container size; extract together for layered systems
- [extension-sections-10-14](./extension-sections-10-14.md) — where extension namespaces live in Variant 1 DESIGN.md
- `../../../bin/amw-design-md-from-url.sh` — bin script that hosts this classifier
- `../../../bin/amw-dev-browser-wrapper.sh` — browser primitive used internally
- [amw-design-md-extractor-agent](../../../agents/amw-design-md-extractor-agent.md) — the agent that owns this flow
