---
name: TECH-form-validation-patterns
category: form-designer-references
source: P2 enhancement for amw-form-designer-agent §9 (Skill-Decision Matrix); batch9 T-132 (clean-room from long-tail A-02)
also-in: globalCC skill `accessibility-a11y` for the `aria-live` deep dive; `zod-schema-validation` for schema authoring
---

# Form validation patterns

## Table of Contents

- [What it does](#what-it-does)
- [When to validate](#when-to-validate)
- [Debounce policy](#debounce-policy)
- [Error message phrasing](#error-message-phrasing)
- [The `aria-invalid` + `aria-describedby` contract](#the-aria-invalid--aria-describedby-contract)
- [Submit-while-invalid pattern](#submit-while-invalid-pattern)
- [Vanilla HTML+JS reference](#vanilla-htmljs-reference)
- [React + shadcn (RHF + Zod) variant](#react--shadcn-rhf--zod-variant)
- [Multi-error summary](#multi-error-summary)
- [WCAG 2.1 AA notes](#wcag-21-aa-notes)
- [Cross-references](#cross-references)

## What it does

Defines when and how the form-designer agent's `validation_rules` block manifests as user-facing feedback. Inline vs submit-time, debounce timings, message phrasing, and the ARIA wiring that makes errors perceivable to assistive tech.

## When to validate

| Validation mode | Use for | Avoid for |
|---|---|---|
| **On blur** (default for most fields) | Email, phone, URL, name, address — anything where premature error-on-keystroke creates noise | Password strength (use on-input), credit-card (use on-input with format mask) |
| **On input (every keystroke)** | Password strength meter, credit-card type detector, character counter (max-length warning) | Email/URL/phone (waits for user to finish typing) |
| **On submit only** | Confirm-password match, async server-side checks (username taken, address verified) | Required-field check (annoys the user) |
| **On change (select / radio / checkbox)** | Selectable inputs — fires on user intent, no debounce needed | Text inputs (use blur) |

The hard rule: **`onTouched` mode** — validate when the user has interacted with the field and then moved on. RHF expresses this as `mode: 'onTouched'`; plain HTML uses `addEventListener('blur', ..., {once: false})` after the first focus event.

Avoid `mode: 'onChange'` (every keystroke) — it produces 50ms of red error message on an email field that the user is still typing. Research-backed: inline-on-blur saves ~22% abandonment vs error-on-keystroke.

Use `noValidate` on the `<form>` element so the browser's default bubble-tooltip doesn't fight your inline errors:

```html
<form noValidate onsubmit="return validateAndSubmit(event)">
```

## Debounce policy

- **Blur-driven validation:** no debounce. Fires once when the field loses focus.
- **Input-driven (password meter, char counter):** debounce 150ms. Below 150ms the meter flickers; above 300ms it feels laggy.
- **Async server-side (username taken check):** debounce 400ms after the last keystroke, fire ONE request. Use `AbortController` to cancel pending requests on new keystrokes.

```js
let lastReq = null;
input.addEventListener('input', debounce(async (e) => {
  lastReq?.abort();
  lastReq = new AbortController();
  try {
    const res = await fetch(`/api/check?u=${e.target.value}`, { signal: lastReq.signal });
    const { available } = await res.json();
    setFieldStatus(input, available ? 'ok' : 'taken');
  } catch (err) {
    if (err.name !== 'AbortError') setFieldStatus(input, 'error');
  }
}, 400));
```

## Error message phrasing

The agent's `validation_rules.errorMessage` field is consumed by the renderer. Rules:

| Bad | Good | Why |
|---|---|---|
| "Invalid" | "Email must include @" | Tells user what to do |
| "Required" | "Email is required" | Names the field for context |
| "Invalid format" | "Phone must be 10 digits, e.g. 555-867-5309" | Shows valid example |
| "Error" | "Password must be at least 8 characters" | Specifies the rule |
| "Try again" | "We couldn't reach our servers. Please retry." | Distinguishes user error from system error |

Tone: present-tense, second-person, no exclamation marks. Never blame the user ("You entered an invalid email"). Avoid jargon ("Pattern mismatch" → "Phone must be digits only").

For locale-aware copy, the agent delegates to `amw-multilanguage-copywriter-agent` via main-agent (see §9 row "Locale-specific error copy").

## The `aria-invalid` + `aria-describedby` contract

The minimum viable a11y contract for any errored field:

```html
<label for="email">Email address</label>
<input
  id="email"
  name="email"
  type="email"
  autocomplete="email"
  required
  aria-required="true"
  aria-invalid="true"
  aria-describedby="email-error email-hint"
>
<p id="email-hint" class="hint">We'll never share your email.</p>
<p id="email-error" class="error" role="alert">Email must include @ and a domain.</p>
```

Rules:

- `aria-invalid="true"` MUST be set only AFTER the user has interacted (touched + blurred), not on initial render. A page that loads with every required field announced as invalid is hostile.
- `aria-describedby` accepts space-separated IDs. Always include both the hint AND the error message — the hint stays useful even after the error resolves.
- The error message element MUST be in the DOM when announced. Don't toggle `display: none` and back; toggle `hidden` or use `aria-live`. Better: keep the element rendered with empty text content; set `textContent` on error.
- `role="alert"` on the error element makes screen-readers announce immediately. Use it only for one-error-at-a-time inline errors; the multi-error summary uses `role="alert"` once on the summary container.

When the error resolves, set `aria-invalid="false"` (or remove the attribute) AND clear the error element's text. Don't leave stale text in the DOM.

## Submit-while-invalid pattern

Hard rule: **never disable the submit button while the form is invalid.**

Why: a disabled button is unreachable by screen-readers (depending on platform) and gives the user no explanation. They see "Submit (greyed out)" and don't know what's wrong.

Pattern: keep submit always enabled. On click, if form is invalid:

1. Set `aria-invalid="true"` on every invalid field.
2. Build a summary at the top of the form: "Please fix 3 errors before submitting." with anchor links to each invalid field.
3. Move focus to the summary container (which has `tabIndex="-1"` so it's programmatically focusable but not in tab order).
4. Screen-readers announce the summary via `role="alert"` or `aria-live="assertive"`.

```html
<div id="form-summary" role="alert" tabindex="-1" hidden>
  <h2>Please fix 3 errors:</h2>
  <ul>
    <li><a href="#email">Email is required</a></li>
    <li><a href="#phone">Phone must be 10 digits</a></li>
    <li><a href="#password">Password must be at least 8 characters</a></li>
  </ul>
</div>
```

```js
form.addEventListener('submit', e => {
  const invalid = form.querySelectorAll('[aria-invalid="true"]');
  if (invalid.length > 0) {
    e.preventDefault();
    const summary = document.getElementById('form-summary');
    summary.hidden = false;
    summary.querySelector('h2').textContent = `Please fix ${invalid.length} ${invalid.length === 1 ? 'error' : 'errors'}:`;
    summary.focus();
    return;
  }
  // proceed to async submit (see TECH-form-async-submit.md)
});
```

## Vanilla HTML+JS reference

```html
<form id="signup" noValidate>
  <div id="form-summary" role="alert" tabindex="-1" hidden></div>
  <label for="email">Email address</label>
  <input id="email" name="email" type="email" autocomplete="email" required
         aria-required="true" aria-describedby="email-hint email-error">
  <p id="email-hint">We'll send a verification link.</p>
  <p id="email-error" class="error" hidden></p>
  <button type="submit">Create account</button>
</form>

<script>
const form = document.getElementById('signup');
function validateField(input) {
  const err = document.getElementById(`${input.id}-error`);
  let msg = '';
  if (input.validity.valueMissing) msg = `${input.labels[0].textContent} is required.`;
  else if (input.validity.typeMismatch) msg = `${input.labels[0].textContent} must be valid.`;
  input.setAttribute('aria-invalid', msg ? 'true' : 'false');
  err.textContent = msg;
  err.hidden = !msg;
  return !msg;
}
form.querySelectorAll('input').forEach(i => i.addEventListener('blur', () => validateField(i)));
form.addEventListener('submit', e => {
  const valid = [...form.querySelectorAll('input')].every(validateField);
  if (!valid) { e.preventDefault(); /* show summary, focus it — see pattern above */ }
});
</script>
```

## React + shadcn (RHF + Zod) variant

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Form, FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage } from '@/components/ui/form';

const schema = z.object({
  email: z.string().min(1, 'Email is required').email('Email must include @ and a domain'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export function SignupForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    mode: 'onTouched',  // validate on blur after first interaction
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(submit)} noValidate>
        <FormField name="email" render={({ field, fieldState }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <input type="email" autoComplete="email" aria-invalid={!!fieldState.error} {...field} />
            </FormControl>
            <FormDescription>We'll send a verification link.</FormDescription>
            <FormMessage />
          </FormItem>
        )} />
        {/* ... */}
        <button type="submit">Create account</button>
      </form>
    </Form>
  );
}
```

shadcn's `<FormMessage />` reads `fieldState.error?.message` and wires `id` + `aria-describedby` automatically. The `mode: 'onTouched'` is the canonical setting.

## Multi-error summary

When ≥2 fields are invalid on submit, render the summary at the top of the form (see "Submit-while-invalid pattern"). Each summary item is an anchor `<a href="#fieldId">` that, when clicked, scrolls to and focuses the offending field. Screen-reader users hear the count first, then can navigate to each error in order.

For single-field errors (one input invalid), skip the summary — the inline `role="alert"` on the field's error message is enough.

## WCAG 2.1 AA notes

- **3.3.1 Error Identification (A)** — every error MUST be identified in text AND programmatically (`aria-invalid` + `aria-describedby` pointing to the message).
- **3.3.2 Labels or Instructions (A)** — every input has a `<label>` (or `aria-label` if visually labeled differently). Required fields announce required via `aria-required="true"`.
- **3.3.3 Error Suggestion (AA)** — error messages must suggest the fix. "Invalid" fails; "Email must include @" passes.
- **3.3.4 Error Prevention (AA)** — for legal/financial/data-deletion forms, provide review-and-confirm step OR allow reversal within 24h. The form-designer's `multi_step` block with a final "Review" step satisfies this for checkouts.
- **4.1.3 Status Messages (AA)** — error counts and async status (server-side validation pending) MUST use `aria-live` regions. `polite` for non-critical, `assertive` for errors that block submit.
- **2.4.3 Focus Order (A)** — focus must move to the summary container on submit-while-invalid. Visible focus ring required (`:focus-visible`).
- **1.4.3 Contrast (AA)** — error text vs background must hit 4.5:1. Most red error tokens fail on dark mode — verify both themes via `bin/amw-design-md-contrast.py` or eyeballed in DevTools.

## Cross-references

- `amw-form-designer-agent.md` §9 — invoked when the form-designer agent's YAML return contains a `validation_rules` block.
- `TECH-form-multi-step.md` — error-step-navigation pattern that uses this validation API at step transitions.
- `TECH-form-async-submit.md` — submit handling that integrates with the submit-while-invalid pattern.
- `skills/amw-design-principles/color-system.md` — `danger.foreground` / `danger.background` tokens for error styling.
- `skills/amw-shadcn-ui/docs/components/radix/field.mdx` — shadcn `FormMessage` API.
