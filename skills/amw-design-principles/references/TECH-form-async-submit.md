---
name: TECH-form-async-submit
category: form-designer-references
source: P2 enhancement for amw-form-designer-agent §9 (Skill-Decision Matrix); batch9 T-133 (direct-port + clean-room from grp-06 shadcn-claude-skill MIT, grp-07 wavefront modal/dialog/toast taxonomy)
also-in: globalCC skills `react-query` and `tanstack-query` for the optimistic-mutation deep dive
---

# Async submit UX

## Table of Contents

- [What it does](#what-it-does)
- [Submit lifecycle states](#submit-lifecycle-states)
- [Optimistic UI](#optimistic-ui)
- [Loading state — inline spinner, not modal overlay](#loading-state--inline-spinner-not-modal-overlay)
- [Success state — toast vs redirect vs inline confirmation](#success-state--toast-vs-redirect-vs-inline-confirmation)
- [Retry-on-failure](#retry-on-failure)
- [Idempotency](#idempotency)
- [Vanilla HTML+JS reference](#vanilla-htmljs-reference)
- [React + shadcn variant](#react--shadcn-variant)
- [WCAG 2.1 AA notes](#wcag-21-aa-notes)
- [Cross-references](#cross-references)

## What it does

After the form passes validation (see `TECH-form-validation-patterns.md`), the submit handler fires a network request. This reference defines the four canonical states (`idle | submitting | success | error`), the UX patterns for each, and the retry / idempotency / accessibility contracts.

## Submit lifecycle states

```
idle ─submit──► submitting ─resolve──► success
                    │
                    └─reject──► error ─retry──► submitting
```

The form-designer agent emits a `submit_state_machine` block when async submit is in scope. The renderer maps each state to UI affordances.

| State | Submit button | Form fields | ARIA |
|---|---|---|---|
| `idle` | Enabled, label="Submit" | Editable | none |
| `submitting` | Disabled, label="Submitting…", spinner inline | Disabled (`fieldset[disabled]`) | `aria-busy="true"` on form |
| `success` | Hidden OR replaced with "Done" | Disabled, or form unmounts | Announce via toast/`role="status"` |
| `error` | Enabled, label="Retry" | Editable | Error announced via `role="alert"` |

## Optimistic UI

Use only when (1) success rate >95% (comments, likes, add-to-cart), (2) rollback is acceptable without data loss, (3) immediate feedback matters. Do NOT use for payment, account creation, or destructive actions (delete/transfer) — false success is confusing or fraud-adjacent.

Pattern (RHF + TanStack Query):

```tsx
const mutation = useMutation({
  mutationFn: createComment,
  onMutate: async (newComment) => {
    await queryClient.cancelQueries(['comments']);
    const prev = queryClient.getQueryData(['comments']);
    queryClient.setQueryData(['comments'], (old: Comment[]) => [...old, { ...newComment, pending: true }]);
    return { prev };
  },
  onError: (_e, _v, ctx) => {
    queryClient.setQueryData(['comments'], ctx.prev);  // rollback
    toast.error('Comment failed to post. Please retry.');
  },
  onSettled: () => queryClient.invalidateQueries(['comments']),
});
```

Render optimistic items at `opacity: 0.6` or with a "Sending…" pill so the user knows it's pending.

## Loading state — inline spinner, not modal overlay

Hard rule: **do not block the entire form with a modal overlay during submit.** The user cannot scroll up to re-read what they submitted, cancel becomes ambiguous (does it abort the request?), and screen-readers re-announce the modal title.

Instead:

- Replace the submit button's text with `Submitting…` and add an inline SVG spinner inside the button.
- Set `aria-busy="true"` on the `<form>` element.
- Wrap form fields in `<fieldset disabled>` to prevent edits during flight.
- Show a small `role="status" aria-live="polite"` element near the button: "Submitting… please wait."

Full HTML+JS implementation in the Vanilla reference below.

## Success state — toast vs redirect vs inline confirmation

Three patterns:

| Pattern | Use for | Avoid for |
|---|---|---|
| **Inline confirmation** (replace form with success in-place) | Standalone forms (contact, feedback) where user expects "Thanks, we got your message" | Multi-step flows where user must continue elsewhere |
| **Redirect** (`router.push('/thanks')`) | Post-checkout, post-onboarding — user finished a journey, starts a new one | Passive forms — full nav feels heavy |
| **Toast** (Sonner / shadcn `useToast`) | Background mutations: "Settings saved", "Comment posted" — user stays on the surface | Critical confirmations user might miss (payment receipts) |

Toast taxonomy (grp-07 shadcn modal/dialog/toast): **Modal** = caller renders + owns state, custom layout (image picker). **Dialog** = `useDialog()` singleton, imperative `dialog.confirm()`, confirmations (Delete account?). **Toast** = `useToast()` ephemeral feedback. Rule: user must act → Dialog. User just needs to know → Toast. Custom layout → Modal.

```tsx
import { useToast } from '@/components/ui/use-toast';

function onSubmit(values) {
  mutation.mutate(values, {
    onSuccess: () => toast({ title: 'Saved', description: 'Your changes are live.' }),
    onError: (err) => toast({ variant: 'destructive', title: 'Save failed', description: err.message }),
  });
}
```

## Retry-on-failure

Distinguish the failure class:

| Error class | UI |
|---|---|
| **Network** (offline, timeout) | "Can't reach our servers. [Retry]" — same idempotency key |
| **Server 5xx** | "Something went wrong on our end. [Retry]" — same idempotency key |
| **Server 4xx validation** | Inline field errors per `TECH-form-validation-patterns.md` — no retry button (user must edit) |
| **Auth 401/403** | "Session expired. [Sign in again]" — preserve form state in `sessionStorage` |
| **Rate-limit 429** | "Too many attempts. Try again in N seconds." — disable button with countdown |

Never auto-retry payment or account-creation mutations. The user must click Retry explicitly so they can abandon if the prior attempt actually succeeded server-side. For idempotent reads (drafts, options) `AbortController` + exponential backoff is fine; for mutations, manual retry only.

## Idempotency

Every mutation MUST include an idempotency key when the protocol supports it (Stripe, modern REST APIs). Generate the key ONCE per submit attempt — reuse on retries so the server can dedupe; regenerate only when the user edits and re-submits a new attempt.

```js
const idempotencyKey = crypto.randomUUID();
fetch('/api/orders', {
  method: 'POST',
  headers: { 'Idempotency-Key': idempotencyKey, 'Content-Type': 'application/json' },
  body: JSON.stringify(values),
});
```

## Vanilla HTML+JS reference

```html
<form id="contact" noValidate aria-busy="false">
  <fieldset>
    <label for="msg">Message</label>
    <textarea id="msg" name="msg" required></textarea>
    <button type="submit" id="submitBtn">
      <svg class="spinner" aria-hidden="true" hidden>...</svg>
      <span class="label">Send</span>
    </button>
    <p role="status" aria-live="polite" id="submit-status"></p>
  </fieldset>
</form>

<script>
const form = document.getElementById('contact');
const btn = document.getElementById('submitBtn');
const status = document.getElementById('submit-status');
let idempotencyKey = null;

function setSubmitting(b) {
  btn.disabled = b;
  btn.querySelector('.spinner').hidden = !b;
  if (b) btn.querySelector('.label').textContent = 'Sending…';
  form.setAttribute('aria-busy', String(b));
  form.querySelector('fieldset').disabled = b;
}

form.addEventListener('submit', async e => {
  e.preventDefault();
  if (btn.disabled) return;
  idempotencyKey ??= crypto.randomUUID();
  // validate first per TECH-form-validation-patterns.md
  setSubmitting(true);
  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Idempotency-Key': idempotencyKey, 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    if (!res.ok) throw new Error(res.status >= 500 ? 'server' : 'client');
    status.textContent = 'Sent. We will reply within 24 hours.';
    form.querySelector('fieldset').remove();
    idempotencyKey = null;
  } catch (err) {
    status.textContent = err.message === 'server'
      ? 'Server error. Click Send to retry.'
      : 'Could not send. Please check your message and try again.';
    btn.querySelector('.label').textContent = 'Retry';
  } finally {
    setSubmitting(false);
  }
});
</script>
```

## React + shadcn variant

```tsx
import { useForm } from 'react-hook-form';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { Loader2 } from 'lucide-react';

export function ContactForm() {
  const { toast } = useToast();
  const form = useForm({ mode: 'onTouched' });
  const idempotencyKey = useRef<string>();

  const mutation = useMutation({
    mutationFn: async (values: any) => {
      idempotencyKey.current ??= crypto.randomUUID();
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Idempotency-Key': idempotencyKey.current, 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      });
      if (!res.ok) throw new Error(res.status >= 500 ? 'Server error — retry' : 'Submission failed');
      return res.json();
    },
    onSuccess: () => { toast({ title: 'Sent', description: 'We will reply within 24 hours.' }); idempotencyKey.current = undefined; form.reset(); },
    onError: (err) => toast({ variant: 'destructive', title: 'Send failed', description: err.message }),
  });

  return (
    <form onSubmit={form.handleSubmit(v => mutation.mutate(v))} aria-busy={mutation.isPending} noValidate>
      <fieldset disabled={mutation.isPending}>
        <textarea {...form.register('msg', { required: true })} />
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending && <Loader2 className="animate-spin mr-2" aria-hidden="true" />}
          {mutation.isPending ? 'Sending…' : mutation.isError ? 'Retry' : 'Send'}
        </Button>
      </fieldset>
    </form>
  );
}
```

## WCAG 2.1 AA notes

- **4.1.3 Status Messages (AA)** — every state transition (submitting → success/error) MUST be announced via `aria-live` or `role="status"` / `role="alert"`. Visual spinner alone is invisible to screen-readers.
- **2.1.1 Keyboard (A)** — disabled submit during submit should still be focusable so the screen-reader can read its label. `aria-disabled="true"` keeps it tab-reachable; `disabled` does not but prevents accidental re-submit on double-Enter. Pick by priority.
- **2.4.3 Focus Order (A)** — on success, focus the confirmation heading / toast region. On error, focus the first invalid field OR the retry button.
- **3.2.2 On Input (A)** — never auto-submit on change. Submit only on explicit click/Enter.
- **2.4.7 Focus Visible (AA)** — keep `:focus-visible` ring on the submit button during loading.
- **1.4.13 Content on Hover or Focus (AA)** — toasts must be dismissible AND remain visible while hovered/focused. Sonner/shadcn satisfy this by default.
- **2.2.1 Timing Adjustable (A)** — auto-dismissing toasts MUST be ≥5s OR offer a way to extend. shadcn default 5000ms; do not shorten.

## Cross-references

- `agents/amw-form-designer-agent.md` §9 — invoked when the form-designer agent's YAML return contains a `submit_state_machine` block.
- `TECH-form-validation-patterns.md` — validation must pass before this submit path fires.
- `TECH-form-multi-step.md` — final step's submit button uses this submit-state machine.
- `skills/amw-shadcn-ui/vendor/components/base/sonner.mdx` — toast component reference.
- `skills/amw-shadcn-ui/vendor/components/radix/dialog.mdx` — Dialog vs Modal vs Toast taxonomy.
