# AI-Slop Anti-Pattern List

## Table of Contents

- [I. Visual style](#i-visual-style)
- [II. Typography](#ii-typography)
- [III. Layout](#iii-layout)
- [IV. Content and copy](#iv-content-and-copy)
- [V. Interaction and motion](#v-interaction-and-motion)
- [VI. Color](#vi-color)
- [Self-check workflow](#self-check-workflow)
- [VII. Content density principle (positive stance)](#vii-content-density-principle-positive-stance)
- [VIII. Content anti-patterns (T-042)](#viii-content-anti-patterns-t-042)
- [IX. Anti-AI-cliché visual checklist (T-044)](#ix-anti-ai-cliché-visual-checklist-t-044)

> **A thousand no's for one yes.** Each item below is an instant tell for AI-generated work.
> Each entry names: ❌ the anti-pattern → ✅ a better alternative → 📝 the reason.

---

## I. Visual style

### 1. Purple-blue / pink-purple gradient backgrounds

- ❌ `background: linear-gradient(135deg, #667eea, #764ba2)`
- ✅ Solid low-saturation background; if a gradient is genuinely needed, use `oklch` with a narrow hue range.
- 📝 This gradient is the 2018 Stripe / Dribbble-era cliché, copied into the ground.

### 2. Rounded card + 4 px colored left-accent

- ❌ `border-left: 4px solid #6366f1; border-radius: 8px`
- ✅ Differentiate with background color shifts, a hairline bottom rule, or nothing at all (let whitespace and hierarchy do the work).
- 📝 This is over-generalized Notion / Linear knock-off. Stops differentiating anything.

### 3. AI-drawn SVG illustrations / mascots / scenes

- ❌ Inline SVG painting people, landscapes, products.
- ✅ Use a placeholder (gray box with size + text label), and ask the user for real assets.
- 📝 AI-drawn SVG has stiff lines and wrong proportions. It visibly degrades the whole piece.

### 4. Emoji overuse

- ❌ ✨ everywhere, 🚀 in headlines, 📊 as icon substitutes.
- ✅ Use emoji only when the brand explicitly uses them. Otherwise zero.
- 📝 Emoji almost always make design look frivolous or juvenile.

### 5. Unrestrained glassmorphism

- ❌ Every card getting `backdrop-filter: blur(20px)` + semi-transparent white.
- ✅ Use locally when the underlying layer is genuinely complex enough to carry the effect.
- 📝 Overused 2021 trend; usually also fails contrast.

### 6. Cool-but-meaningless 3D decor

- ❌ Floating 3D geometric shapes, abstract orbs, pseudo-3D buttons.
- ✅ Let flatness + whitespace + typographic rhythm carry the hierarchy.
- 📝 Visual noise that carries no information.

---

## II. Typography

### 7. Default-font trap

- ❌ Inter, Roboto, Arial, system-ui, Fraunces, Poppins.
- ✅ Pick a typeface with real character that matches the brand voice:
  - Editorial / narrative → GT Alpina, Tiempos, Söhne, Untitled Sans
  - Tech / tools → JetBrains Mono for accents, Suisse Int'l, Neue Haas Grotesk
  - Art / emotional → PP Editorial New, Reckless, Authentic Sans
- 📝 Inter / Roboto are "safe bets" but they have zero identity.

### 8. Weight soup

- ❌ 300 / 400 / 500 / 600 / 700 all on one page.
- ✅ Two or three weights maximum (usually Regular + Bold, Medium when needed).
- 📝 Weight chaos = visual loss of control.

### 9. Excessive script / handwriting fonts

- ❌ Pacifico or handwritten fonts for a main headline.
- ✅ Create emphasis with rhythm, scale contrast, and case — not scripts.
- 📝 Unless the brand IS handwritten, script type reads cheap.

---

## III. Layout

### 10. Hero → 3-column features → CTA → footer, universal template

- ❌ Every landing page is the same container.
- ✅ Ask "what is this page doing" first, derive the structure from that.
- 📝 Template compliance = zero differentiation.

### 11. Alternating white / pale-gray section backgrounds

- ❌ Mechanical white / pale-gray / white / pale-gray looks like a PowerPoint template.
- ✅ Use one or two background shades; mostly solid, switch only at real section breaks.
- 📝 Default AI rhythm, serves no content.

### 12. One icon per feature

- ❌ Three to six features in a row, each with its own small icon.
- ✅ Use icons only when they carry real visual differentiation. Otherwise plain text.
- 📝 Icon slop reduces information density.

### 13. Trust-marker carpet

- ❌ "1000+ customers," "ISO 27001," customer logo walls.
- ✅ Show only real, verifiable trust signals, and put them where they help.
- 📝 Fake credibility ornaments.

### 14. Every card the same size

- ❌ 3×3 grid with identical tiles.
- ✅ Size by importance (bento grid, non-uniform grid).
- 📝 Averaging = no focal point.

---

## IV. Content and copy

### 15. Placeholder names / testimonials / numbers

- ❌ "Sarah J. — CEO at TechCorp" + 5 stars.
- ✅ Leave whitespace or "[customer testimonial TK]" placeholder.
- 📝 Fabricated social proof reads cheap and breaches honesty.

### 16. Invented statistics

- ❌ "300% efficiency gain," "10x user growth."
- ✅ Only use real, supplied numbers. Otherwise omit.
- 📝 AI-invented numbers are visibly fake.

### 17. Filler paragraphs

- ❌ Every section stuffed with 3–4 sentences of description.
- ✅ Whitespace, one big line, let the visuals carry the rest.
- 📝 AI tends to "fill in"; good design tends to "say less."

### 18. Meaningless subtitles

- ❌ Main headline + a polite subtitle restating the main headline.
- ✅ If there's a subtitle, give it real information. Otherwise drop it.
- 📝 Subtitles are not a default component.

### 19. Exclamation / question-mark fever

- ❌ "Make it yours today!" / "Why wait?"
- ✅ Declarative, confident copy.
- 📝 Sales-y tone reads cheap.

---

## V. Interaction and motion

### 20. First-viewport blanket fade-in + Y-translate

- ❌ Every element animates `opacity: 0 → 1, translateY(20px → 0)` simultaneously.
- ✅ Staged intentional animation (main first, support after), or none at all.
- 📝 Default template animation with zero memorability.

### 21. Everything `hover: scale(1.05) + shadow`

- ❌ All interactive elements using the same hover feedback.
- ✅ Different levels of the hierarchy get different feedback (color shift / underline expand / inner detail reveal).
- 📝 Monotonous.

### 22. Parallax everywhere

- ❌ Every layer parallaxing.
- ✅ Use on one or two signature sections, static elsewhere.
- 📝 Poor performance + motion sickness.

## VI. Color

### 23. Saturation at the ceiling

- ❌ `#FF0000`, `#00FF00` — raw screen primaries.
- ✅ Use `oklch` in the comfortable-lightness band; reference physical print palettes.
- 📝 Default AI colors are chaotic and painful.

### 24. Infinitely expanding palette

- ❌ Every component introducing a new color.
- ✅ Strict 5 – 7 colors (primary, 3 neutrals, 2 semantic).
- 📝 Palette sprawl = brand collapse.

### 25. Dark mode ≠ straight inversion

- ❌ Flip the light theme and call it dark.
- ✅ Re-design contrast, hierarchy, and color weight for dark.
- 📝 Deeper is not darker.

### 26. Never use `scrollIntoView`

- ❌ `element.scrollIntoView({behavior: 'smooth'})`
- ✅ Compute the offset manually and use `window.scrollTo({top, behavior: 'smooth'})`.
- 📝 `scrollIntoView` breaks the parent iframe's scroll position when the output is embedded in a host. Use the manual path for stability.

---

## Self-check workflow

Before shipping any HTML:

1. Open the file.
2. Read every one of rules 1 through 26. If any match, rework.
3. Run one more grep:

   ```
   grep -E "linear-gradient|border-radius.*border-left|Inter|Roboto|🚀|✨|scrollIntoView" <file>
   ```

4. All clear → deliver.

---

## VII. Content density principle (positive stance)

Rules 1–26 say what NOT to do. Design also needs an affirmative principle.

### Every element must earn its place

Before adding anything to the page, ask:

- What task does this section perform?
- Does this icon carry real differentiation, or is it decoration?
- Is this number real, or is it here to "look professional"?

**Can't answer? Delete it.**

### Whitespace is not a problem to fix

A section that "looks empty" is not a defect — it is rhythm. The correct response is:

- ✅ Adjust the visual weight of the surrounding elements so the whitespace breathes.
- ❌ Stuff in lorem ipsum / fake numbers / generic icons.

### Icons are not default accessories

"Professional-looking" pages are often just icon stacks — and icon stacks actively reduce information. Rule:

- ✅ Add an icon when it has real semantic differentiation (status indicator, category marker).
- ❌ Decorative icons, filler icons — remove. Plain text is cleaner.

### When there's a content gap, ask the user

If you think "a customer-logo wall would add credibility" — first ask the user if they have real customer logos. If not, don't add one.

AI-invented "trust signals" are fake, and readers see through them instantly.

---

## VIII. Content anti-patterns (T-042)

> Ledger T-042. Source: tasteful-ui-skill-master (MIT). Complements rules 15–19.

Content-layer bans — each item is an instant AI-slop tell in copy or labelling:

| Anti-pattern | Example | Better alternative |
|---|---|---|
| **Fake personas as demo data** | "Sarah J. — CEO at TechCorp" | Leave `[customer TK]` or use clearly fictional placeholders |
| **`//`-kickers** | `// SOLUTION` above a section heading | Use a plain label, eyebrow, or no prefix |
| **Mono-caps filler subtitles** | `POWERFUL. FAST. RELIABLE.` | Write copy that states a real benefit |
| **Unicode-glyph decoration** | `→` or `✦` used as section decoration instead of text | Remove or replace with a real design element |
| **Robotic CTA copy** | "Authenticate Session", "Proceed to Checkout Finalization" | "Sign in", "Pay now" — the shortest action verb that works |
| **Genericized benefit headers** | "Empowering Teams", "Driving Growth" | Name the exact outcome: "Ship faster", "Cut churn" |

### Preserve — do NOT strip when refactoring existing UI

When you are editing or improving an existing product, keep these intact:

- **The identity cue** — the element (logo treatment, accent color, typeface) that makes the product recognizable.
- **The primary task** — whatever the user most needs to accomplish on this screen.
- **The real data shape** — if a component shows "Product A / $12.00 / Qty: 3", keep that shape; don't simplify to a placeholder.
- **Existing domain terminology** — if users call it an "Opportunity" not a "Lead", keep "Opportunity".

Taste guardrail: if a refactor would look more impressive in a portfolio screenshot but make the product less clear to its actual users, reject it.

---

## IX. Anti-AI-cliché visual checklist (T-044)

> Ledger T-044. Sources: atelier-main (MIT), tasteful-ui-skill-master (MIT), Bexa (MIT), 21st-frontend-design (MIT). See also `component-taste.md` and `visual-direction-tokens.md`.

Run this checklist before shipping any visual output. Each item is an immediate tell that the work is AI-generated:

### Color and gradient
- [ ] **Purple→blue gradient on white** — `linear-gradient(135deg, #667eea, #764ba2)` or any variation. (Note: atmospheric background blooms and gradient meshes as texture are OK when purposeful.)
- [ ] **Gradients on buttons, text, or small controls** — gradient fills on interactive elements read cheap. Atmospheric background blooms are the exception.
- [ ] **Rainbow gradients** as accent or text treatment.

### Layout and components
- [ ] **Equal-spacing card grids with no hierarchy** — 3×3 or 4×4 identical tiles; averaging = no focal point.
- [ ] **Colored left-border callouts on rounded containers** — `border-left: 4px solid accent; border-radius: 8px`. This is Notion/Linear knock-off that stopped differentiating anything.
- [ ] **Heavy borders on everything** — "boxy" designs where every element has a visible enclosure.

### Decoration
- [ ] **Emoji as decoration** — ✨, 🚀, 📊 as section icons or headline accents unless the brand explicitly uses them.
- [ ] **Self-drawn SVG illustrations / mascots** — stiff lines, wrong proportions. Use a sized placeholder box and ask for real assets.
- [ ] **Animate everything** — every element fading and translating in simultaneously on load.

### Hero patterns (the 3 AI hero archetypes — avoid all three by default)
- [ ] **Centered H1 + subtitle + single CTA** on a solid or gradient background — the universal AI landing-page template.
- [ ] **Stock photo + dark overlay + white text** hero.
- [ ] **Name + tagline hero with no visible benefit** — "Acme. Built for teams." with nothing concrete underneath.

### Typography
- [ ] Main font is on the forbidden list — see Section VIII in `typography-system.md` (Inter, Roboto, Space Grotesk, etc.).
