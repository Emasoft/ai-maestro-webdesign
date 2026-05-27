# TECH-rubric — The 8-dimension design grading rubric

**Version:** 1.0
**Status:** Canonical scoring criteria for `amw-design-grade`. Load this file in full before every audit. Cross-dimension calibration notes appear at the end.

Every dimension scores 0-10. Letter grade is deterministic:

| Score | Grade |
|---|---|
| 9.0-10.0 | A |
| 7.0-8.9 | B |
| 5.0-6.9 | C |
| 3.0-4.9 | D |
| 0.0-2.9 | F |

NULL is a valid score when evidence is insufficient for the artifact type.

---

## 1. Palette

**What is measured:** colour-system coherence. Does the artifact use a structured ramp (OKLCH or HSL) or arbitrary hex picks? Are dark and light parity-checked? Is chromatic balance maintained (not just monochromatic + one neon)? Are semantic roles (success / warning / danger / info) consistent?

### Scoring criteria

- **9-10 (A):** Full OKLCH/HSL token ramp (≥7 steps per family); dark + light explicit and parity-tested; semantic roles defined (success/warning/danger/info) and used consistently; chromatic balance evident (≥2 chromatic hues OR an opinionated single-hue commitment); no orphan hex values in computed styles.
- **7-8 (B):** Structured ramp present (≥5 steps); one orientation (light or dark) is primary, the other adequate; semantic roles partially defined; ≤3 orphan hex values; chromatic structure visible but limited.
- **5-6 (C):** Some ramp structure (3-4 steps); single-orientation only OR dark/light differ in non-parity ways; semantic roles ad-hoc; 4-10 orphan values.
- **3-4 (D):** Two or three colours chosen ad-hoc; no ramp; semantic roles missing or wrong (red used for "primary action" without warning meaning); >10 orphan values.
- **0-2 (F):** Single colour OR uncontrolled hex sprawl OR colour choices visibly violate basic harmony (e.g. saturated red + saturated green adjacency on body copy).

### Required evidence

- Token excerpt (CSS custom properties or extracted ramp)
- Orphan-value count (computed styles that do NOT reference a token)
- Dark/light parity check result (which orientation, which gaps)

### Common pitfalls in scoring

- Do NOT confuse "lots of colours" with palette quality. Wide hue range without structure is a 3-4, not a 6.
- Do NOT reward "looks nice" without checking token reuse. The signature dimension covers identity; palette covers system.

---

## 2. Typography

**What is measured:** type-scale structure, family pairing, vertical-rhythm anchoring, optical adjustments (letter-spacing on display, line-height ratio for body, small-caps where appropriate). Reading ergonomics on body copy.

### Scoring criteria

- **9-10 (A):** Named modular scale (perfect-fourth / major-third / minor-third / golden) explicitly stated; ≥2 families paired with a justified rationale (e.g. serif display + sans body); body line-height 1.5-1.7; display line-height 1.0-1.2; letter-spacing adjustments per scale step; optical small caps / lining figures used where typographically correct.
- **7-8 (B):** Consistent scale ratio evident (≥4 sizes from a single multiplier); ≤2 families well-paired; body line-height in 1.4-1.7 range; display tightened (line-height ≤ 1.3); minor optical adjustments present.
- **5-6 (C):** 3-4 type sizes, ratio not strict; single family OR adequate pairing; line-heights present but uniform across scale (e.g. all 1.5).
- **3-4 (D):** Type sizes ad-hoc (e.g. 14, 17, 22, 31, 48 — no detectable ratio); body line-height ≤1.3 or ≥1.9; display untightened.
- **0-2 (F):** Single size used everywhere OR ≥3 families fighting for attention OR body copy in display-only typefaces.

### Required evidence

- Type-scale ratio (computed from observed sizes)
- Family pairing (font-family stack excerpts)
- Body line-height value
- Display line-height value

### Common pitfalls

- A pretty headline does not redeem unreadable body copy. Body ergonomics dominate the score.
- Do NOT score on aesthetic personality — that's the signature dimension. Typography scores on STRUCTURE.

---

## 3. Rhythm

**What is measured:** spacing-token discipline. Is there a base unit (4px / 8px / em-derived) and a documented step set? Does every observed gap, padding, and margin in computed styles reference a token, or are there orphan values? Does density vary appropriately across sections (hero vs feature row vs footer) without breaking the token system?

### Scoring criteria

- **9-10 (A):** Documented spacing tokens with named scale (e.g. 4/8/12/16/24/32/48/64); ≥95% of computed gaps/paddings/margins reference a token; density variance is intentional and aligned (hero gets the largest token, footer the smallest, no orphan steps); baseline grid alignment visible in screenshot crops.
- **7-8 (B):** Token set evident (≥5 steps); 80-95% token reuse; some density-variance discipline; a few orphan values (≤5) in non-hero sections.
- **5-6 (C):** Partial token structure (3-4 steps); 60-80% token reuse; density variance present but uncalibrated.
- **3-4 (D):** Ad-hoc gaps (14, 17, 22, 31px in arbitrary mix); <60% token reuse; no apparent density logic.
- **0-2 (F):** Random spacing everywhere; padding/margin values look transcribed from designer guess rather than a system.

### Required evidence

- Spacing-token excerpt (if a system exists)
- Orphan-value count and the orphan values themselves
- Density variance check (hero gap value vs footer gap value)

### Common pitfalls

- Generous whitespace alone is not rhythm. Discipline of step choice matters more than amount.
- The hero ALWAYS has more breathing room than the footer in a competent design. Inversion is a red flag.

---

## 4. Hierarchy

**What is measured:** can a first-time viewer identify the primary action within 1 second of seeing the artifact? Does the heading-level stack (H1 → H2 → H3) read as the page's structural outline? Are visual weights (font weight, font size, colour contrast, background fill) ordered consistently with semantic importance?

### Scoring criteria

- **9-10 (A):** Primary action visually dominant (size + colour-contrast + position above the fold); H1 unambiguous; H2 / H3 cascade cleanly; secondary actions clearly subordinate (outline button, ghost button, link); body copy is the lowest-weight element on the page (where appropriate); structure is the page's "outline read".
- **7-8 (B):** Primary action identifiable within 2 seconds; heading stack reads correctly; one or two visual-weight inconsistencies (e.g. a body-copy paragraph weight-bolder than a section heading).
- **5-6 (C):** Primary action present but competes with secondary; heading stack works but H3 occasionally outweighs H2.
- **3-4 (D):** Multiple primary actions claiming attention; flat heading hierarchy (H1 looks like H3); body copy as visually loud as the CTA.
- **0-2 (F):** No discernible primary action OR everything has the same visual weight OR the page reads as a wall of equally-emphasized elements.

### Required evidence

- Primary-action description (where on page, size, colour treatment)
- H1 / H2 / H3 sizes and weights
- Body copy size and weight

### Common pitfalls

- "Above the fold" is one factor, not the only factor. A bold CTA buried below the fold can still win hierarchy if the fold draws the eye toward it.
- Mobile and desktop hierarchies can differ; score the primary orientation the artifact targets.

---

## 5. Motion

**What is measured:** motion-token discipline and purposefulness. Are durations and easing curves documented? Do they vary intentionally (faster for hover, slower for layout, slowest for page transitions) or is everything a 300ms ease-in-out? Does motion respect `prefers-reduced-motion`? Does any animation serve a real informational purpose (state transition, attention guidance) rather than decoration?

### Scoring criteria

- **9-10 (A):** Documented motion tokens (e.g. 150ms fast / 250ms medium / 400ms slow + named easings); usage matches token semantics; `prefers-reduced-motion` honoured (no parallax, no auto-carousels, no decorative oscillation when reduced-motion is set); each animation has a stated purpose.
- **7-8 (B):** Two or three motion tokens; mostly used correctly; `prefers-reduced-motion` partially honoured; decorative motion limited.
- **5-6 (C):** One default duration applied everywhere (300ms ease-in-out); `prefers-reduced-motion` not implemented OR not tested; decorative motion present but not aggressive.
- **3-4 (D):** Motion erratic (3 different durations on similar interactions); no reduced-motion support; gratuitous parallax or auto-carousel.
- **0-2 (F):** Motion clearly hostile (forced auto-playing carousel without pause, scroll-jacked navigation, multiple competing animations); accessibility violations.

### Required evidence

- Motion-token excerpt (if any)
- Observed durations on key interactions (hover, button-press, page-transition)
- Reduced-motion media-query check result

### NULL conditions

- Static DESIGN.md without rendered interactions → score NULL unless the spec explicitly defines tokens (then partial scoring on token discipline only, capped at 6).
- Single-screen artifact with no interactive elements → NULL.

---

## 6. Accessibility

**What is measured:** WCAG 2.1 AA compliance on the audited surface. Computed contrast ratios for body and accent text on their backgrounds. Focus-state visibility. Semantic landmarks. Hit-target sizes. Reduced-motion (already counted in dimension 5, do not double-count). Form label association (when forms are present).

### Scoring criteria

- **9-10 (A):** All body/UI text passes AA (≥4.5:1 for ≤18px, ≥3:1 for ≥18px bold or ≥24px regular); focus rings ≥2px with ≥3:1 contrast; semantic landmarks (`<header>` `<main>` `<nav>` `<footer>` or ARIA equivalents) present; ≥44×44px hit targets on touch; form labels associated; alt-text on all decorative-vs-meaningful images correctly distinguished.
- **7-8 (B):** Body text passes AA; one or two accent-text contrast issues (e.g. a single secondary CTA at 4.0:1); focus rings present and visible; landmarks correct; hit targets occasionally <44px on small icons.
- **5-6 (C):** Body text borderline AA; multiple accent-text contrast failures; focus rings exist but ≤1px or low-chroma; some landmarks missing.
- **3-4 (D):** Body text fails AA in places; focus rings missing on interactive elements; landmarks largely absent; hit targets routinely <44px.
- **0-2 (F):** Body text fails AA generally; no visible focus states; no landmarks; multiple form fields without labels; meaningful images without alt text.

### Required evidence

- Body-text computed contrast ratio (with values)
- Accent / CTA contrast ratio (with values)
- Focus-state observation (existence, thickness, contrast)
- Landmark check result

### Hard caps

- Any artifact with computed body-text contrast < 4.5:1 caps at score 4 maximum (D).
- Any artifact with NO visible focus states on interactive elements caps at score 3 maximum (D).
- Any artifact with form fields missing labels caps at score 4 maximum (D).

---

## 7. Consistency

**What is measured:** repeated-pattern fidelity. Do the same component types (button, card, input, badge) look the same everywhere they appear? Are variant rules predictable (a primary button always looks like THE primary button)? Do tokens drive the styling or are there one-off overrides? Are spacing, colour, type, and motion choices consistent across the artifact?

### Scoring criteria

- **9-10 (A):** ≥95% of styled rules reference a token; no component has more than 2 visually-distinct variants without an explicit rationale (size or state, not arbitrary); spacing/colour/type/motion tokens drive computed styles uniformly across hero / feature / footer; the same button on two different pages of the artifact is pixel-identical.
- **7-8 (B):** 80-95% token reuse; ≤3 component variant inconsistencies (e.g. footer CTA padding differs from hero CTA without reason); generally uniform.
- **5-6 (C):** 60-80% token reuse; multiple variant inconsistencies; sections feel like they were styled independently.
- **3-4 (D):** <60% token reuse; component variants visibly random; hero and footer look like different sites.
- **0-2 (F):** No detectable token system; every section is its own snowflake; the same logical component appears in 4+ distinct visual forms.

### Required evidence

- Token-reuse percentage (computed-rules / token-referencing-rules)
- Variant inconsistencies (specific component, specific delta)
- Cross-section comparison (hero button vs footer button)

### Common pitfalls

- Do NOT confuse consistency with monotony. A design with disciplined variant rules (small/medium/large; primary/secondary/ghost) IS consistent.
- "Different by intent" is allowed. A pricing page hero will differ from the marketing-home hero — the question is whether the BUTTON / CARD / FORM primitives stay coherent.

---

## 8. Signature

**What is measured:** does the artifact have a recognisable identity beyond stock components? Are there opinionated choices a competing site could not replicate without copying? Is there a memorable detail (typographic pairing, colour commitment, motion personality, layout signature) the viewer carries away?

### Scoring criteria

- **9-10 (A):** Multiple opinionated commitments (specific typographic pairing, distinctive colour ramp, signature motion behavior, distinctive grid choice); a viewer shown only a component crop could identify the site; the design is unmistakable in its category.
- **7-8 (B):** Two opinionated commitments; recognisable within its category; some stock-component DNA still visible but a custom layer sits on top.
- **5-6 (C):** One opinionated commitment (e.g. a single bold colour choice); otherwise stock; the site is competent but not memorable.
- **3-4 (D):** Stock components throughout; opinion absent or limited to a logo placement; the artifact looks like any other site in its category.
- **0-2 (F):** Pure template DNA; the site is visually indistinguishable from every other site of its kind.

### Required evidence

- The opinionated commitment(s), named explicitly
- A "could a competitor replicate this in 1 hour?" test result
- The memorable detail (or NULL if none exists)

### Common pitfalls

- Do NOT confuse signature with novelty for its own sake. A well-executed Swiss-grid landing page with disciplined typography IS opinionated and scores well; a brutalist page with random misaligned elements is NOT opinionated, it is sloppy.
- A site can score 10/10 on dimensions 1-7 and 3/10 on signature if it is a perfect stock template. Stock execution is not signature.

---

## Cross-dimension calibration notes

Read these before scoring. They prevent common cross-dimension drift:

1. **Signature and consistency can conflict** — a design with a strong signature often makes opinionated breaks from default consistency (e.g. an oversized footer that breaks the rhythm but reinforces identity). Score each dimension on its own criteria; do NOT punish signature for breaking consistency or vice versa.

2. **Accessibility caps everything informally** — an artifact that scores 9-10 across dimensions 1-5,7,8 but fails AA contrast (dimension 6 score 4) is NOT a B or A design despite the high average. State this in the report-card footer. Recommend: "average mean masks an accessibility blocker; treat overall as D until contrast is fixed."

3. **Typography and rhythm are tightly coupled** — a strong type-scale ratio typically pulls rhythm along with it (line-heights compose with vertical-rhythm). Score them independently but flag when they disagree by ≥3 points (e.g. typography 9, rhythm 4) — that pattern usually means typography was specified well but the implementation is sloppy in spacing.

4. **Motion NULL is common** — static DESIGN.md files, single-screen captures, and most non-interactive artifacts get NULL on dimension 5. Treat NULL as legitimate; the overall score divides by the number of scored dimensions, not by 8.

5. **Palette and signature are independent** — a strong palette with no signature is possible (well-systematized but bland). A strong signature with mediocre palette is also possible (memorable identity but undisciplined colour). Do not let one drive the other.

6. **Hierarchy is binary-leaning** — an artifact either gets the primary action right or doesn't. The middle scores (5-7) cover "has hierarchy but one or two competitors muddy it." Pure failure is rare in modern sites; pure success requires the 1-second test.

7. **Consistency is the most token-derivative dimension** — if you measured rhythm (dimension 3) accurately by computing token-reuse percentage, your consistency score should be in the same neighborhood. A ≥3-point gap means you are measuring different things; revisit.

8. **The mean has known pathologies** — a 6.9 / C overall can mask 7-9 / 1-3 / 7-9 / 7-9 / 7-9 / 7-9 / 7-9 / 7-9 (one F dimension dragging the mean). Always print the dimension-level table; never report only the overall.

---

## NULL handling

A dimension scores NULL when:

- The artifact type cannot evidence that dimension (motion on a static spec; signature on a 200-character DESIGN.md token list).
- The audit input is incomplete (no screenshot available for visual-weight checks; no DOM available for landmark checks).

NULL is NOT a substitute for low scores. If evidence IS available but the artifact does poorly, score it 0-2. NULL means the artifact CANNOT BE EVALUATED on this dimension, not that it failed.

When computing the overall mean: sum the non-NULL scores, divide by the count of non-NULL dimensions, round to 1 decimal. State in the report-card footer: "Overall computed from N of 8 dimensions; D1, D2, ... were NULL because [reason]."

---

## Versioning

The rubric is versioned. The `design-grade-data.json` output records the `rubric_version` field so consumers can detect score-comparability across audits performed under different rubric revisions. Bump the version when:

- A dimension is added, removed, or renamed.
- A scoring boundary changes (e.g. "9-10 A" becomes "9.5-10 A").
- A hard cap (dimension 6) is added or removed.

Current version: **1.0**.
