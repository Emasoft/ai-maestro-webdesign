# TECH-theme-swap — Remix algorithms (named vocabulary + OKLCH hue rotation)

## Table of Contents

- [Mode 1 — Named-vocabulary remix](#mode-1-named-vocabulary-remix)
- [Mode 2 — OKLCH hue rotation](#mode-2-oklch-hue-rotation)
- [Combined Mode 1 + Mode 2](#combined-mode-1-mode-2)
- [Render-test contract](#render-test-contract)
- [Anti-patterns (do not do)](#anti-patterns-do-not-do)
- [Versioning](#versioning)

**Version:** 1.0
**Status:** Canonical algorithms for `amw-design-remix`. Load this file before any remix run.

This document specifies the two remix modes in detail: named-vocabulary swap (Mode 1) and OKLCH hue rotation (Mode 2). The SKILL.md gives the workflow; this file gives the math, the merge rules, and the edge cases.

---

## Mode 1 — Named-vocabulary remix

### Algorithm

```
input:
  source_tokens    -- the source design's canonical token bundle
  target_style_id  -- e.g. "S-001"

step 1: load catalogue
  read skills/amw-design-system-presets/references/catalogue.md
  resolve target_style_id to its catalogue row
  if not found: fail with explicit error listing valid IDs

step 2: load preset
  read skills/amw-design-system-presets/references/<style_id>-<slug>.md
  extract:
    preset.tokens           (the Token Block section)
    preset.breaks_if_rules  (the "Breaks if" invariants list)
    preset.aesthetic_position
    preset.identity_summary
    preset.source_attribution

step 3: identify brand tokens to preserve
  brand_tokens = subset of source_tokens that meet ANY of:
    - explicitly tagged as "brand identity" in DESIGN.md frontmatter
    - the source's wordmark colour (logo SVG fill)
    - a registered/trademarked colour (user declares in input)
    - a brand font (the typeface IS the brand identity, not a generic body face)

step 4: build merged bundle
  merged = preset.tokens  (full preset baseline)
  for each token in brand_tokens:
    merged[token.key] = token.value
    record in preserved_brand_tokens log

step 5: check invariants
  warnings = []
  for each rule in preset.breaks_if_rules:
    if merged violates rule:
      warnings.append({
        "rule": rule,
        "offending_token": which token in merged triggers it,
        "recommendation": "either remove brand override OR accept exit from named preset"
      })

step 6: render-test
  inject merged into _test-skeleton.html
  emit remix-render-test.html

step 7: emit deliverables
  remix-tokens.css, remix-tokens.json, remix-render-test.html, remix-report.md
  report includes:
    - source ref
    - target style ID + identity summary
    - preserved_brand_tokens log
    - invariant warnings (with recommendations)
    - source_attribution from preset (preserved as required by amw-design-system-presets §4)
```

### Brand-token preservation rules (Mode 1 detail)

Brand identity is preserved over preset identity. Which tokens count as brand:

1. **Always brand** (preserved unconditionally):
   - Logo wordmark colour (extracted from SVG logo fill if available)
   - Logo wordmark typography (the font used in the wordmark itself, not the body font)
   - User-declared brand primary (when the user supplies a hex in the prompt)

2. **Conditionally brand** (preserve if explicitly tagged):
   - Brand secondary / accent (only if DESIGN.md frontmatter or the user's prompt tags it as brand)
   - Brand-defining motion behaviour (rare; only if the source design has signature motion documented as identity)

3. **Never brand** (always replaced by preset):
   - Body text colour (the preset's choice wins)
   - Surface / background colours (the preset's choice wins)
   - Spacing tokens (the preset's choice wins)
   - Radius tokens (the preset's choice wins)
   - Shadow tokens (the preset's choice wins)
   - Motion tokens (default; only preserved when conditional rule applies)

### Invariant violation handling

When a preserved brand token violates a preset's "breaks if" rule, the skill MUST:

1. Emit a clear warning in `remix-report.md` (do NOT silently strip the brand token; do NOT silently accept the violation).
2. State the rule verbatim.
3. Name which token causes the violation and which preset rule it breaks.
4. Offer two recommendations: (a) remove the brand override to comply with the preset; (b) accept that the artifact is "<preset> inspired" rather than the named preset.
5. Let the user decide. The skill does NOT auto-resolve.

Example warning text:

> **Invariant violation:** Swiss preset breaks if border-radius exceeds 4px. The preserved brand token `--radius-card=8px` violates this rule.
>
> Recommendations:
> - Remove the brand `--radius-card` override → artifact remains a true Swiss preset
> - Keep `--radius-card=8px` → artifact is "Swiss-inspired" but not the canonical Swiss preset; label accordingly

### Identity-defining tokens in DESIGN.md

When the source is a DESIGN.md, look for these frontmatter fields to identify brand tokens:

```yaml
brand:
  primary-color: "#FF0000"    # always preserved
  logo-font: "Custom Sans"     # always preserved
  identity-accent: "#FFD700"   # preserved if tagged
identity-tokens:
  - --color-brand-primary
  - --color-brand-secondary
```

When the source is a `designlang` extraction JSON, look for `brand.*` keys. When the source is a URL or HTML, the user MUST explicitly declare brand tokens in their prompt — the skill cannot auto-detect brand identity from a website without user guidance (auto-detection misidentifies arbitrary CTA colours as "brand").

---

## Mode 2 — OKLCH hue rotation

### Algorithm

```
input:
  source_tokens        -- the source design's canonical token bundle
  target_primary       -- the new brand primary, as hex / rgb / hsl / OKLCH
  source_primary_token -- which token in source is "primary" (optional; auto-detect if missing)

step 1: parse target_primary to OKLCH triple
  target_oklch = to_oklch(target_primary)
  target_hue = target_oklch.h

step 2: identify source primary
  if source_primary_token provided:
    source_oklch = to_oklch(source_tokens[source_primary_token])
  else:
    # Auto-detect: pick the highest-chroma chromatic token
    chromatic_tokens = filter source_tokens to those with OKLCH chroma >= 0.04
    source_primary_token = chromatic_tokens.max_by(chroma)
    source_oklch = to_oklch(source_tokens[source_primary_token])

  source_hue = source_oklch.h

step 3: compute hue delta
  delta = target_hue - source_hue  # in degrees, can be negative
  # normalise to [-180, 180] for clean reporting
  delta = ((delta + 180) mod 360) - 180

step 4: rotate every chromatic token
  rotated_tokens = {}
  clamped_log = []
  for each (key, value) in source_tokens:
    if is_color_token(key):
      o = to_oklch(value)
      if o.c >= 0.04:                    # chromatic — rotate
        new_h = (o.h + delta) mod 360
        candidate = oklch(o.l, o.c, new_h)
        # clamp into displayable gamut
        clamped = clamp_to_srgb_or_p3(candidate)
        if clamped.c < o.c:
          clamped_log.append({
            "token": key,
            "original_oklch": (o.l, o.c, new_h),
            "clamped_oklch": (clamped.l, clamped.c, clamped.h),
            "reason": "out of sRGB gamut" (or "out of P3 gamut")
          })
        rotated_tokens[key] = from_oklch(clamped)
      else:                                # neutral — preserve
        rotated_tokens[key] = value
    else:
      rotated_tokens[key] = value         # non-colour token — preserve

step 5: re-check WCAG-AA
  contrast_warnings = []
  for each pair (text_token, bg_token) where the source design pairs them:
    new_contrast = wcag_contrast(rotated_tokens[text_token], rotated_tokens[bg_token])
    if new_contrast < 4.5 and source pair was >= 4.5:
      contrast_warnings.append({
        "text": text_token,
        "background": bg_token,
        "original_contrast": ...,
        "rotated_contrast": new_contrast,
        "recommendation": "increase text lightness by X% or decrease background chroma"
      })

step 6: render-test
  inject rotated_tokens into _test-skeleton.html

step 7: emit deliverables (same shape as Mode 1)
```

### OKLCH conversion notes

The skill MUST use a tested conversion library (e.g. `culori` in JS, `coloraide` in Python, or any reputable CSS-Color-4 implementation). DO NOT roll an OKLCH conversion from scratch — the L*a*b* / OKLab math is precise and small errors cause visible drift.

Input formats the parser must accept:

- Hex: `#fff`, `#ffffff`, `#ffffffff`
- Functional rgb: `rgb(255 255 255)`, `rgb(255,255,255)`, `rgba(...)`, with optional alpha
- Functional hsl: `hsl(240 50% 50%)`, with optional alpha
- Functional oklch: `oklch(60% 0.15 240)`, with optional alpha
- Functional oklab: convert to OKLCH on the fly
- CSS named colours: only the standard CSS named colours (`black`, `white`, `red`, `currentColor` is treated as opaque grey for rotation purposes — flag in report)

Output format for rotated tokens: prefer `oklch(L% C H)` notation to preserve precision. When the source design used hex notation, also emit hex as a comment alongside for compatibility:

```css
--color-primary: oklch(60% 0.15 240); /* #3b82f6 */
```

### Gamut clamping

OKLCH is wider than sRGB. A rotation can push a colour to a triple that is not displayable in sRGB or even P3. The clamping rule:

1. Start with the rotated `(L, C, H)`.
2. If the colour fits in sRGB, use it.
3. If not, decrease chroma in 1% steps until it fits.
4. If the user specified `--gamut p3` in their prompt, clamp to P3 instead of sRGB.
5. Record the clamp in `clamped_tokens` log.

Never alter lightness or hue during clamping — the rotation's intent is preserved by adjusting only chroma. Altering L or H would silently change which colour the user sees.

### Auto-detecting source primary

When the user does not specify which source token is "primary," auto-detect with this rule:

1. Filter tokens to those with chroma ≥ 0.04 (excludes neutrals).
2. From those, prefer tokens named `--color-primary`, `--brand-primary`, `--primary`, `--accent` in that order.
3. If no name matches, pick the chromatic token with the highest chroma value.
4. If multiple tokens tie, pick the one with the median lightness.

Tell the user which token was auto-detected. Offer them the chance to override before computing the rotation.

### Neutral tokens stay neutral

A neutral token is one where OKLCH chroma < 0.04. These are visually "greyish" and do NOT carry hue identity. Rotating them produces visible tinted-grey artifacts that the user did NOT ask for. Therefore: neutral tokens are passed through unchanged.

If the source design has a deliberately-tinted neutral (e.g. a warm cream `oklch(95% 0.03 60)`), the chroma is borderline 0.04. The skill MUST surface borderline cases in the report and ask the user whether to rotate them:

> Token `--color-neutral-bg` has chroma 0.03 (borderline neutral). Rotating it produces a hue shift from cream-warm to cream-blue. Rotate this token? (y/n)

### Post-rotation WCAG check

Every pair the source design used (text on background, accent on surface, etc.) MUST be re-checked after rotation. If a contrast drops below 4.5:1 (AA body text) or 3.0:1 (large text 18pt+ or 14pt bold), warn explicitly.

Common rotation pitfalls that drop contrast:

- Rotating around to a hue with lower perceived luminance even at the same OKLCH L (e.g. pure yellow at L=80 reads brighter than pure violet at L=80; the OKLCH L is perceptually uniform but the surrounding chroma still affects perceived brightness).
- Rotating accent text on light surfaces when the new hue is lower contrast against the original background (background was not rotated because it was a neutral; accent was rotated).

Recommend lightness adjustments in the report, not automatic adjustments. The user chooses whether to nudge L on offending tokens or accept the contrast loss.

---

## Combined Mode 1 + Mode 2

When the user supplies BOTH a named style AND a new primary colour:

1. Run Mode 1 first: produce the preset's baseline token bundle.
2. Identify the preset's primary token (named `--color-primary` or equivalent in the preset).
3. Apply Mode 2 hue rotation to the preset's bundle, rotating from the preset's primary toward the user's specified primary.
4. Verify both: preset's "breaks-if" invariants AND post-rotation WCAG.
5. Report covers both swaps.

This mode is useful for "make my brand look like Swiss but with my orange instead of red." The structural Swiss vocabulary is enforced; the chromatic identity follows the user.

---

## Render-test contract

The render-test page uses `amw-design-system-presets/references/_test-skeleton.html` unmodified — only the token block at the top of the file is replaced with the remixed bundle. The test page shows the 8 standard primitives (header, hero, feature row, quote, pricing, form, footer, modal) so the user can verify the remix renders coherently across the typical component set.

Inject the remixed `--color-*`, `--font-*`, `--spacing-*`, `--radius-*`, `--shadow-*`, `--motion-*` tokens directly into the `:root` rule of the skeleton. Do NOT modify the skeleton's HTML structure; do NOT add or remove components. The skeleton is the canonical render surface; any deviation breaks parity with `amw-design-system-presets` render-tests.

---

## Anti-patterns (do not do)

- **Rotating neutrals "to make the design more chromatic"** — neutrals are neutrals for a reason. The user explicitly asked for a hue rotation; if they wanted to inject chroma into the design, they would have asked for a different remix mode.
- **Silently fixing AA failures by nudging lightness** — surface the failure; let the user decide. Auto-fixing drift opens correction loops that move further from the user's intent each iteration.
- **Inventing "brutalist-like" tokens from memory** — Mode 1 reads the catalogue. Always.
- **Mixing presets** — "make it brutalist + art deco" is two different presets. Pick one. If the user truly wants a hybrid, they need to invoke the remix twice or author a custom S-NNN preset first.
- **Stripping source_attribution** — Mode 1 outputs MUST preserve the preset's source_attribution per `amw-design-system-presets/SKILL.md` non-negotiable §4.
- **Deciding which source tokens are "brand identity" by guess** — when the source is a URL or HTML, the user MUST declare brand tokens. The skill does not auto-detect; the failure mode of auto-detection is too brand-disrespectful.
- **Returning the merged bundle without rendering the test page** — the render-test is non-optional. Without it, the user has no visual check that the remix is coherent.

---

## Versioning

Bump the version (`remix_mode_version` in the JSON) when:

- The brand-token preservation rules change.
- The gamut-clamping algorithm changes.
- The neutral-token threshold (currently chroma < 0.04) changes.
- The WCAG-check pairing logic changes.

Current version: **1.0**.
