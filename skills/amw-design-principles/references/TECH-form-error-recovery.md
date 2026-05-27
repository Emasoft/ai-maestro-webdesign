# TECH — Form Error Recovery Patterns

How forms surface validation errors, announce them to assistive tech, and recover the user toward a successful submission. Owned by `amw-form-designer-agent`; consumed by `amw-wireframe-builder-agent` whenever a form is rendered.

This file lives alongside the R1-shipped pair `TECH-validate-on-blur.md` (T-131) and `TECH-aria-invalid-describedby.md` (T-132) — those two cover the timing and the ARIA wiring. This file covers the **recovery flow** (what happens after the error is shown and the user is trying to fix it).

Provenance / license: composed from `wavefront` UX guidance (MIT → direct-port) and `ux-ui-mastery` accessibility writeups (no license → clean-room). The fork-discipline boundary (T-118) and announce-plan-before-coding cue (T-119) are direct-ports from `atelier` (MIT). Native browser features (T-123) are clean-room.

---

## Tokens

```css
:root {
  /* Error / success palette — read from color-system.md, do not hardcode */
  --color-error: oklch(50% 0.18 25);
  --color-error-bg: oklch(96% 0.04 25);
  --color-error-border: oklch(60% 0.16 25);
  --color-success: oklch(55% 0.15 145);

  /* Error spacing — paired with the form field spacing scale */
  --error-message-gap: 4px;       /* gap between input and inline error */
  --error-summary-gap: 16px;      /* gap between summary block and first field */
  --error-icon-size: 16px;

  /* Error focus ring — distinct from default focus to mark "field needs attention" */
  --error-outline: 2px solid var(--color-error);
  --error-outline-offset: 2px;
}
```

**Hard invariants:**
1. Inline error text must contrast ≥ 4.5:1 against its background (WCAG AA). The red-on-red anti-pattern (`#c00` text on `#fee` bg gives 3.8:1 — fails) is rejected.
2. Error icons are decorative; the error must be announced to screen readers via text (`role="alert"` or `aria-live="polite"`), never icon-only.
3. The error message names the field and the violation; "Invalid" is rejected ("Email must contain @", "Date must be after today", etc.).

---

## The four recovery strategies

### Strategy 1 — Inline-first, on-blur reveal (default for short forms ≤ 6 fields)

The R1 doctrine: validate on blur, never on keystroke (exception: live password strength). When the user leaves a field with an invalid value, the error appears inline immediately below the field, wired with `aria-invalid` + `aria-describedby` (see `TECH-aria-invalid-describedby.md`).

Recovery sequence:
1. Field gains error state on blur (`aria-invalid="true"`, error text inserted into `#field-id-error`, `aria-describedby` points at it).
2. As soon as the user re-focuses the field, the error stays visible (do not clear on focus — the user needs to see the violation while they type).
3. On the user's NEXT blur (or on submit, whichever comes first), revalidate. If valid, remove the error and announce success silently (the visual cue — error block disappears, `aria-invalid` removed — is enough; do not blast a success toast for fixing a single field).
4. On submit, all fields revalidate; any new errors that appear after submission go through Strategy 2 below.

### Strategy 2 — Submit-summary block (mandatory for forms ≥ 7 fields OR when ≥ 3 fields fail)

When the user submits and multiple fields are invalid, screen-reader users cannot navigate easily to find each inline error. Add an error summary block at the top of the form.

Structural recipe:
```html
<div id="form-errors"
     role="alert"
     aria-labelledby="form-errors-title"
     tabindex="-1"
     class="error-summary"
     hidden>
  <h2 id="form-errors-title">There are 3 errors in this form</h2>
  <ul>
    <li><a href="#email">Email must contain @</a></li>
    <li><a href="#phone">Phone must be 10 digits</a></li>
    <li><a href="#dob">Date of birth must be in the past</a></li>
  </ul>
</div>
<form noValidate>
  <!-- fields -->
</form>
```

```js
async function handleSubmit(e) {
  e.preventDefault();
  const errors = validateForm();
  const summary = document.getElementById('form-errors');
  if (errors.length === 0) { submitForm(); return; }
  renderSummary(summary, errors);
  summary.hidden = false;
  summary.focus(); // Critical — moves SR focus into the summary so it reads
  // Each <a href="#field"> in the summary lets users jump to the field
}
```

Why `tabindex="-1"` + explicit `.focus()`: when `role="alert"` content appears, some screen readers announce it but do not move focus there. Forcing focus into the summary guarantees the announcement and gives keyboard users a navigable list. `tabindex="-1"` makes it programmatically focusable without inserting it into the tab order.

Why `noValidate`: native browser validation tooltips have inconsistent ARIA wiring across browsers, and they cannot be styled. Suppress them and own the validation UX entirely (R1's T-131 doctrine; RHF's `mode: 'onTouched'` is the React Hook Form equivalent).

### Strategy 3 — Progressive disclosure (multi-step forms)

When a form is split across N steps (checkout, onboarding, signup wizard), do not validate the entire form at the end — validate each step's fields before allowing the "Next" button to advance. The user fixes errors in the context where they were entered.

Per-step recovery sequence:
1. User fills step N, clicks "Next".
2. Validate step N's fields only. If any fail, do NOT advance; surface errors via Strategy 1 (≤ 6 fields per step is the design target) or Strategy 2 (≥ 7).
3. Step N's "Next" button gains `aria-disabled="true"` (NOT the `disabled` attribute — `aria-disabled` keeps the button focusable so the user can read why it cannot advance via the associated error summary).
4. As errors clear (per-field blur revalidation), recompute the step's overall valid state. When all fields pass, restore `aria-disabled="false"`.

The user must always be able to RETURN to previous steps without losing data. Multi-step forms persist their state to a draft store on every field change.

### Strategy 4 — Server-side error replay (after submit)

Some errors only surface server-side (email already registered, payment declined, coupon expired). The form must:

1. Receive a structured error response: `{ field: "email", code: "ALREADY_REGISTERED", message: "An account with this email already exists. Sign in instead?" }`.
2. Inject the message into the field's `#field-id-error` exactly as inline-first does.
3. Set `aria-invalid="true"` on the field.
4. Move focus to the field (the user expects to land where the problem is).
5. If the error has an actionable recovery (sign-in, contact support), the message includes a link or button to that path. The user is not left at a dead end.

Server error messages must be sanitized before injection — never `innerHTML` raw server text into the DOM. Use `textContent` or a templated structure with the message string assigned to a known text node.

---

## Announce-on-error a11y wiring (mandatory)

Every error path above relies on the same five primitives:

1. **`aria-invalid="true"`** on every field that fails. Removed when the field passes.
2. **`aria-describedby="field-id-error"`** linking the field to its error container. The container exists in the DOM (empty `<span>` until needed); we toggle text content, not existence — this avoids reflow-induced screen-reader stutter.
3. **`role="alert"` or `aria-live="polite"`** on the error summary container. `alert` is more assertive but interrupts what the SR was reading; `polite` queues. For form submit errors, `alert` is correct (the user just took an action; interrupting is appropriate). For background async errors (autosave failure), `polite` is correct.
4. **Focus management** — move focus into the summary on submit fail; move focus to the first errored field after server-side error replay; never move focus on keystroke or blur.
5. **Error icons are decorative.** `aria-hidden="true"` on the icon SVG. The text adjacent to the icon carries the meaning.

See R1's `TECH-aria-invalid-describedby.md` for the minimum-viable code snippet; this file's contribution is the recovery-flow strategy choice.

---

## Empty / loading / disabled-state edges

Forms have several non-error states that are often forgotten:

- **Empty state on first paint** — no error indicators visible; required fields are marked with a leading visual cue (asterisk or "Required" text), never with red coloring.
- **Loading state during submit** — submit button shows a spinner; all fields gain `aria-busy="true"` on the form; the form is not removed from the DOM (the user may need to retry, so the values must persist).
- **Disabled fields** — use `aria-disabled` when the user can still focus the field to read why it is disabled (e.g., a billing field disabled until the address is filled); use the native `disabled` attribute only when the field is truly skip-over (e.g., a hidden honeypot field).
- **Read-only fields** (e.g., pre-filled email from URL parameter) — `readonly` attribute, not `disabled`. Read-only fields are submitted with the form; disabled fields are not.

---

## Native browser features that replace JS — T-123 applied to forms

The plugin's general rule (native browser features over JS libs) lands on forms as:

- **`:has(:invalid)`** — style the parent label group when any descendant input is invalid. Zero JS required for the "this section has errors" cue.
  ```css
  fieldset:has(:user-invalid) { border-color: var(--color-error-border); }
  ```
  `:user-invalid` (note: not `:invalid`) only fires after the user has interacted with the field, avoiding the "everything is red on first paint" anti-pattern.
- **`inert` attribute** — when a modal form opens, set `inert` on the rest of the page. Keyboard tabbing and AT cannot reach the dimmed background. Zero JS focus-trap library needed.
- **`autocomplete` attribute** — the most underused accessibility tool. `autocomplete="email"` / `autocomplete="tel"` / `autocomplete="cc-number"` lets the OS surface saved values and lets password managers populate correctly. The autocomplete catalog has ~60 named tokens; use the specific one (`postal-code` not `zip`, `given-name` not `first-name`).
- **`enterkeyhint`** — controls the mobile virtual keyboard's enter-key label. `enterkeyhint="next"` on the second-to-last field, `enterkeyhint="send"` on the submit, `enterkeyhint="search"` on a search box.
- **Popover API** for help / hint surfaces — see `TECH-microinteractions-catalog.md` example 8. The hint surface for "what is a security code" no longer needs a tooltip library.

---

## Fork discipline (token-substitution-only edits) — T-118 applied to forms

When modifying an existing form (not building from scratch), the form-designer's edit boundary is:

1. Replace hardcoded color / spacing / font values with token references from DESIGN.md. Allowed.
2. Wire missing ARIA attributes (`aria-invalid`, `aria-describedby`, summary block). Allowed.
3. Add the requested feature (a new field, a new validation rule). Allowed.
4. **Do NOT** alter JS event handler names, DOM structure outside the affected fields, or CSS class naming. Disallowed.
5. **Do NOT** touch backend code (form submission endpoint, validation API). Stop and return a `blocking_issues` note that the change requires backend coordination.

If a token used in the form does not exist in DESIGN.md, stop and request an extension (the announce-plan-before-coding cue, T-119: a 1–2 sentence note stating the missing token + suggested name + value + reason, then wait).

---

## Breaks-if

- The error message text is inserted via `innerHTML` rather than `textContent` / structured assignment. Server-side error replay becomes an XSS vector when an attacker registers an email containing HTML.
- The submit-summary block is rendered but never receives focus. Screen-reader users cannot find it; they fix nothing.
- `disabled` is used instead of `aria-disabled` for a field that the user might focus to read why it cannot be edited. Keyboard / SR users see the field skip in tab order and conclude it is missing.
- Validation runs on every keystroke. The form shouts at the user mid-typing — well-known 22% form abandonment increase (R1 / T-131).
- Error icons are present without the adjacent text being a complete error description. Icon-only validation fails WCAG 1.1.1 (non-text content).
- A multi-step form clears the user's earlier-step data on validation failure of a later step. The user starts over and abandons.
- The form has no native `<form>` element — the submission flow is hooked into a `<div>` with a click listener. Browser autofill, password managers, and `enter` key submit all silently break.

---

## Component examples

### Example A — Inline-first short form (contact)

```html
<form id="contact" noValidate>
  <div class="field">
    <label for="email">Email <abbr title="required">*</abbr></label>
    <input id="email"
           name="email"
           type="email"
           required
           autocomplete="email"
           enterkeyhint="next"
           aria-describedby="email-error">
    <span id="email-error" class="field-error" role="alert" aria-live="polite"></span>
  </div>
  <div class="field">
    <label for="message">Message <abbr title="required">*</abbr></label>
    <textarea id="message"
              name="message"
              required
              aria-describedby="message-error"
              enterkeyhint="send"></textarea>
    <span id="message-error" class="field-error" role="alert" aria-live="polite"></span>
  </div>
  <button type="submit">Send</button>
</form>
```

```js
function validateField(input) {
  const errorEl = document.getElementById(input.id + '-error');
  if (input.validity.valueMissing) {
    errorEl.textContent = `${input.labels[0].textContent.trim().replace('*','').trim()} is required.`;
    input.setAttribute('aria-invalid', 'true');
    return false;
  }
  if (input.validity.typeMismatch && input.type === 'email') {
    errorEl.textContent = 'Email must contain @ and a domain.';
    input.setAttribute('aria-invalid', 'true');
    return false;
  }
  errorEl.textContent = '';
  input.removeAttribute('aria-invalid');
  return true;
}

document.querySelectorAll('#contact input, #contact textarea').forEach(el => {
  el.addEventListener('blur', () => validateField(el));
});

document.getElementById('contact').addEventListener('submit', e => {
  e.preventDefault();
  const inputs = [...e.target.querySelectorAll('input, textarea')];
  const allValid = inputs.map(validateField).every(Boolean);
  if (allValid) submitForm(new FormData(e.target));
});
```

Why this composes: `noValidate` suppresses the browser's tooltips so we own the UX. Each field has a permanent error span with `role="alert"` + `aria-live="polite"`; we toggle text content, never the element's existence. Blur revalidation gives the user the "feedback after I leave the field" pattern. Submit revalidates everything (covers the case where the user submits without touching every field).

### Example B — Multi-step checkout with summary fallback

```
Step 1: Cart review     →  Step 2: Shipping  →  Step 3: Payment  →  Confirm
```

Each step has a `noValidate` form and a `Next` button. The Next button validates that step's fields:
- If 1–2 errors: inline-first (Strategy 1).
- If 3+ errors: render the summary block at the top of the step and focus it (Strategy 2).
- If the user clicks "Back" to a prior step, the summary block is cleared (errors only apply to the current step).
- On the final "Place order" submit, server-side errors come back (Strategy 4) — focus moves to the offending field, with the server message injected. The user is not bounced back to step 1.

Drafts persist after every field blur; refreshing the page reloads the user at the same step with the same values.

---

## Cross-references

- Blur-validation timing: `TECH-validate-on-blur.md` (R1 / T-131).
- ARIA wiring minimum: `TECH-aria-invalid-describedby.md` (R1 / T-132).
- Microinteractions used (success-pulse on field-fix, error-shake on submit-fail): `TECH-microinteractions-catalog.md` entries 4 and 5.
- Color tokens: `amw-design-principles/color-system.md` § II (WCAG contrast).
- Hit-target floor for form controls: `amw-design-principles/spacing-rhythm.md` § IV (44 × 44 px minimum tap target).
- AI-slop form gotchas: `amw-design-principles/ai-slop-avoid.md` § IV (content and copy) — error messages must be specific, not "Invalid input."
