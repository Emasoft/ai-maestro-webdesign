---
name: TECH-aria-invalid-describedby
category: design-principles-reference
source: clean-room write-up of the W3C WAI-ARIA Authoring Practices form-error pattern (common-knowledge accessibility wiring); no verbatim copy
license: this file = MIT (plugin license)
also-in: "TECH-form-error-recovery.md (cites this as the ARIA wiring minimum); TECH-validate-on-blur.md (the timing that triggers this wiring); amw-accessibility-auditor-agent (checks this wiring on form audits); amw-form-designer-agent (emits it)"
---

# ARIA-INVALID + DESCRIBEDBY — the minimum accessible form-error wiring

## Table of Contents

- [What this is](#what-this-is)
- [The minimum wiring](#the-minimum-wiring)
- [Announcing the error when it appears](#announcing-the-error-when-it-appears)
- [Submit-fail: summary + focus management](#submit-fail-summary--focus-management)
- [Clearing the error](#clearing-the-error)
- [Anti-patterns](#anti-patterns)
- [Cross-references](#cross-references)

## What this is

A sighted user sees a red border and an error line. A screen-reader user perceives **nothing** unless the error is wired into the accessibility tree. This is the minimum wiring that makes a form error announce correctly — it is not optional polish, it is the difference between a usable and an unusable form for assistive-tech users. (WCAG 3.3.1 Error Identification, 1.3.1 Info & Relationships, 4.1.3 Status Messages.)

## The minimum wiring

When a field is invalid, three things must be true:

1. The input carries **`aria-invalid="true"`** (and `aria-invalid="false"` or the attribute removed when valid).
2. The error message element has a **stable `id`**.
3. The input's **`aria-describedby`** references that id (space-separated if it also describes a hint).

```html
<label for="email">Email</label>
<input id="email" type="email" name="email"
       aria-invalid="true"
       aria-describedby="email-hint email-error" />
<p id="email-hint" class="hint">We'll only use this for the receipt.</p>
<p id="email-error" class="error">Enter an email like name@example.com.</p>
```

When the field becomes valid, set `aria-invalid="false"` (or remove it) and drop the error id from `aria-describedby`. The hint id stays.

## Announcing the error when it appears

`aria-describedby` makes the error readable *when the field is focused* — but a screen-reader user needs to *hear* an error that appears after they blur or submit. Put the error text in a live region so it is announced on insertion:

- Per-field: give the error container `role="alert"` (implicit `aria-live="assertive"`), OR an `aria-live="polite"` region for less urgent validation.
- Insert the error **text** into the live region (an empty region that you later fill announces correctly; a region that exists only when erroring may not).

## Submit-fail: summary + focus management

On a submit that fails validation:

- Render an **error summary** at the top of the form (a list linking to each invalid field by its `id`), inside a focusable container.
- **Move focus** to the summary (or to the first invalid field) so keyboard / screen-reader users land on the problem instead of being left at the submit button.
- Each summary link targets the field's `id`; activating it focuses that field.

## Clearing the error

When the user fixes the field (see the reward-early timing in [TECH-validate-on-blur](TECH-validate-on-blur.md)): set `aria-invalid="false"`, remove the error id from `aria-describedby`, and clear/empty the live-region text so a stale error isn't re-announced.

## Anti-patterns

- **Color-only error signalling** — a red border with no `aria-invalid` and no text. Invisible to screen readers and to color-blind users (WCAG 1.4.1). Always pair an icon + text with the color.
- **Error text with no `id` / not referenced** by `aria-describedby` — the message is on screen but not associated with the field.
- **Toast-only errors** — a transient toast that vanishes; the field stays unmarked. The error must live on the field.
- **Focus left on submit** — failing validation but leaving focus on the (now-pointless) submit button.
- **`role="alert"` wrapping the whole form** — over-announces; scope live regions to the message, not the form.

## Cross-references

- [TECH-form-error-recovery](TECH-form-error-recovery.md) — the message wording + recovery flow this wiring carries.
- [TECH-validate-on-blur](TECH-validate-on-blur.md) — *when* the `aria-invalid` state flips on and off.
- `skills/amw-design-principles/color-system.md` — § II error-color contrast (so the visible signal also passes WCAG AA).
- `agents/amw-accessibility-auditor-agent.md` — audits this wiring as part of the WCAG 2.1 AA form check.
