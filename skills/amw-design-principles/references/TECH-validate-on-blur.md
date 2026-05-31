---
name: TECH-validate-on-blur
category: design-principles-reference
source: clean-room write-up of common-knowledge form-UX timing ("reward early, punish late", widely documented — Konjević's "Designing Perfect Text Field", Nielsen Norman inline-validation studies); no verbatim copy
license: this file = MIT (plugin license)
also-in: "TECH-form-error-recovery.md (cites this for blur-validation timing); TECH-form-validation-patterns.md (the rule-set this times); amw-form-designer-agent (applies validation timing at build)"
---

# VALIDATE-ON-BLUR — when to fire field validation, not just how

## Table of Contents

- [What this is](#what-this-is)
- [The core timing rule](#the-core-timing-rule)
- [Reward early, punish late](#reward-early-punish-late)
- [Per-state behavior](#per-state-behavior)
- [Async validation (availability checks)](#async-validation-availability-checks)
- [Anti-patterns](#anti-patterns)
- [Cross-references](#cross-references)

## What this is

Validation correctness is *what* to check; this file is *when* to surface the result. Most form frustration is a timing bug, not a rule bug: validating on every keystroke punishes the user mid-typing ("Email is invalid" while they're still typing the `@`), while validating only on submit makes them fix a whole form at once after the fact. The right default sits between the two.

## The core timing rule

**Validate a field when the user leaves it (on `blur`), not on every keystroke and not only on submit.** Blur is the signal that the user considers the field "done" — that's the cheapest, least-annoying moment to tell them it's wrong.

## Reward early, punish late

The refinement that makes inline validation feel helpful instead of naggy:

- **Punish late** — show an error only *after* the user leaves a field (`blur`), never while they are still typing into a not-yet-errored field.
- **Reward early** — *once a field has already shown an error*, switch that field to validate on `input` (every keystroke) so the error clears the instant the value becomes valid. The user fixing a flagged field gets immediate positive feedback; they don't have to blur again to confirm the fix.

So a field's validation mode is stateful: `on-blur` until its first error, then `on-input` until it's valid again.

## Per-state behavior

| Field state | When to validate | What to show |
|---|---|---|
| Untouched, empty | never | nothing (no error on a field the user hasn't reached) |
| Focused, first entry | never (wait for blur) | nothing |
| Blurred, valid | on blur | optional success affordance (only if the form is long / high-stakes) |
| Blurred, invalid | on blur | the specific error (see [TECH-aria-invalid-describedby](TECH-aria-invalid-describedby.md) for the a11y wiring) |
| Invalid, being corrected | on input (every keystroke) | clear the error the moment it's valid |
| Submit pressed | validate ALL fields | focus the first invalid field; show an error summary for multi-error forms |

Required-vs-optional: never error an *empty optional* field. An empty *required* field errors on blur only if the user has interacted with the form (e.g., on submit), not the instant the page loads.

## Async validation (availability checks)

For checks that hit the network (username/email availability, coupon validity): debounce on `input` (~300–500 ms after the last keystroke) rather than firing per keystroke, show a pending affordance while in flight, and never block the user from continuing to the next field while the check resolves. Treat a network failure as "couldn't check," not "invalid."

## Anti-patterns

- **Keystroke-validating a pristine field** — "Invalid email" before the user finishes typing. The single most common inline-validation mistake.
- **Submit-only validation on a long form** — the user discovers six errors at once after filling everything.
- **Never clearing the error while the user fixes it** — forcing a second blur to confirm a correction. Switch to `on-input` after the first error.
- **Erroring empty untouched fields on page load** — a form that's red before the user does anything.

## Cross-references

- [TECH-form-error-recovery](TECH-form-error-recovery.md) — what the error message says and how the user recovers, once this file decides *when* to show it.
- [TECH-form-validation-patterns](TECH-form-validation-patterns.md) — the validation rules whose results this times.
- [TECH-aria-invalid-describedby](TECH-aria-invalid-describedby.md) — the accessible wiring for the error this surfaces.
- [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) — `success-pulse` on field-fix and `error-shake` on submit-fail.
