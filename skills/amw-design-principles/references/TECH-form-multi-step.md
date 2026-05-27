---
name: TECH-form-multi-step
category: form-designer-references
source: P2 enhancement for amw-form-designer-agent §9 (Skill-Decision Matrix); batch9 T-131 (clean-room from long-tail V-06/A-05)
also-in: globalCC skill `accessibility-a11y` for the keyboard-trap and focus-management deep dive
---

# Multi-step forms (wizards, checkout funnels)

## Table of Contents

- [What it does](#what-it-does)
- [When to use multi-step](#when-to-use-multi-step)
- [State model](#state-model)
- [Step-indicator patterns](#step-indicator-patterns)
- [Back/forward state preservation](#backforward-state-preservation)
- [Save draft / autosave](#save-draft--autosave)
- [Error-step navigation](#error-step-navigation)
- [Vanilla HTML+JS reference](#vanilla-htmljs-reference)
- [React + shadcn variant](#react--shadcn-variant)
- [WCAG 2.1 AA notes](#wcag-21-aa-notes)
- [Cross-references](#cross-references)

## What it does

Decomposes a long form into 2–6 sequential steps so the user is never staring at >7 fields at once. The form-designer agent emits `multi_step` blocks in its YAML return; this reference defines the patterns that block expands into.

## When to use multi-step

| Condition | Single page | Multi-step |
|---|---|---|
| ≤6 fields total | Yes | No |
| 7–12 fields, no logical groups | Yes (with section headings) | Optional |
| 7–12 fields, clear groups (shipping vs payment vs review) | No | Yes |
| ≥13 fields | No | Yes |
| Each step has its own validation expense (server-side OTP, address lookup) | No | Yes |
| User must commit to step 1 before step 2 makes sense (signup → onboarding) | No | Yes |

Bias: prefer a single long form scrolled vertically. Multi-step is only "better" when the user explicitly benefits from the chunking (perceived progress, lower abandonment on long flows, recoverable state).

## State model

The agent emits a JSON-shaped state envelope. The renderer keeps this in memory AND mirrors to `sessionStorage` on every field commit so a refresh restores position:

```json
{
  "currentStep": 1,
  "totalSteps": 4,
  "values": { "email": "", "name": "", "shipping": { ... } },
  "validation": { "email": null, "name": "Required" },
  "stepStatus": ["valid", "current", "untouched", "untouched"]
}
```

`stepStatus` enum: `untouched | current | valid | invalid`. Only `invalid` triggers the error-step-navigation jump (see below). `current` and `valid` may coexist with prior steps that are still editable.

## Step-indicator patterns

Two patterns. Pick by step count:

- **Linear bar (2–4 steps)** — horizontal pill row with current step highlighted, prior steps shown as `valid` (check mark), upcoming steps `untouched` (muted). Each step pill is clickable IF prior steps are valid.
- **Numbered tabs (5–6 steps)** — vertical list on desktop, collapsed into "Step 3 of 6" on mobile <640px. Tabs are clickable only for visited steps.

Hard invariant: never hide the step indicator on a small viewport. Replace it with the text fallback "Step 3 of 6" but the user must always know where they are.

```ascii
┌─────────────────────────────────────────────────────────────────┐
│   ◉ Account ─── ◉ Shipping ─── ○ Payment ─── ○ Review          │
└─────────────────────────────────────────────────────────────────┘
```

## Back/forward state preservation

- Browser `popstate`: every step transition pushes `history.pushState({step: N}, '', '?step=N')`. `popstate` reads `event.state.step` and rehydrates.
- Field values persist on every blur, not on step transition. If the user types in step 2 then navigates back to step 1 mid-keystroke, step-2 values are NOT lost.
- "Back" button on step 1 returns to the page that invoked the form (browser default). Never trap focus inside the form.

## Save draft / autosave

Autosave triggers:

- On `blur` of every field (debounced 600ms to coalesce rapid blurs).
- On step transition (synchronous, awaited).
- On `visibilitychange` to `hidden` (Page Lifecycle API) so closing the tab persists the latest values.

Persistence layers (pick by `auth` flag):

| Auth state | Layer | Lifetime |
|---|---|---|
| Anonymous | `sessionStorage` | Until tab closes |
| Anonymous + opt-in "remember me" | `localStorage` | 7 days, then auto-purge |
| Authenticated | Server-side `POST /api/draft/:formId` | Indefinite, user can resume across devices |

The agent emits a `draft_strategy` field in its YAML return so the wireframe-builder knows which layer to wire.

## Error-step navigation

When the user clicks "Submit" on the final step and a prior step has an invalid field:

1. Compute the lowest-numbered step containing an invalid field.
2. `history.replaceState({step: N})` to that step.
3. Focus the first invalid input (`querySelector('[aria-invalid="true"]')`).
4. Announce via `aria-live="assertive"` region: "Form has 2 errors. Returning to step 1 to fix them."
5. Mark steps in the indicator as `invalid` (red dot or X icon) so the user can preview which steps need attention.

Never silently dump the user back to step 1 without the announcement — screen-reader users miss the visual jump.

## Vanilla HTML+JS reference

```html
<form id="wizard" novalidate>
  <ol class="steps" role="list">
    <li aria-current="step">1. Account</li>
    <li>2. Shipping</li>
    <li>3. Payment</li>
    <li>4. Review</li>
  </ol>

  <fieldset data-step="1">
    <legend>Account details</legend>
    <label for="email">Email</label>
    <input id="email" name="email" type="email" autocomplete="email" required>
  </fieldset>
  <fieldset data-step="2" hidden> ... </fieldset>

  <div role="region" aria-live="polite" id="step-announcer"></div>

  <nav class="wizard-nav">
    <button type="button" data-action="back">Back</button>
    <button type="button" data-action="next">Continue</button>
    <button type="submit" hidden>Submit</button>
  </nav>
</form>

<script>
const form = document.getElementById('wizard');
const announcer = document.getElementById('step-announcer');
let currentStep = 1;
const totalSteps = 4;

function showStep(n) {
  form.querySelectorAll('[data-step]').forEach(fs => {
    fs.hidden = parseInt(fs.dataset.step) !== n;
  });
  form.querySelectorAll('[aria-current]').forEach(el => el.removeAttribute('aria-current'));
  form.querySelector(`.steps li:nth-child(${n})`).setAttribute('aria-current', 'step');
  announcer.textContent = `Step ${n} of ${totalSteps}`;
  const firstInput = form.querySelector(`[data-step="${n}"] input, [data-step="${n}"] select`);
  if (firstInput) firstInput.focus();
  history.pushState({step: n}, '', `?step=${n}`);
  currentStep = n;
}

form.addEventListener('click', e => {
  if (e.target.dataset.action === 'next' && currentStep < totalSteps) showStep(currentStep + 1);
  if (e.target.dataset.action === 'back' && currentStep > 1) showStep(currentStep - 1);
});

window.addEventListener('popstate', e => {
  if (e.state?.step) showStep(e.state.step);
});
</script>
```

## React + shadcn variant

```tsx
import { useState } from 'react';
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form';
import { Button } from '@/components/ui/button';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
  street: z.string().min(3),
});

export function Wizard() {
  const [step, setStep] = useState(1);
  const form = useForm({ resolver: zodResolver(schema), mode: 'onTouched' });

  const stepFields = { 1: ['email', 'name'], 2: ['street'] };
  async function next() {
    const ok = await form.trigger(stepFields[step] as any);
    if (ok) setStep(s => s + 1);
  }

  return (
    <Form {...form}>
      <ol className="flex gap-4 mb-6" role="list">
        {[1, 2].map(n => (
          <li key={n} aria-current={n === step ? 'step' : undefined}>{n}</li>
        ))}
      </ol>

      {step === 1 && (
        <FormField name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><input type="email" autoComplete="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
      )}
      {/* step 2 fields ... */}

      <div className="flex justify-between">
        {step > 1 && <Button type="button" variant="outline" onClick={() => setStep(s => s - 1)}>Back</Button>}
        {step < 2 ? <Button type="button" onClick={next}>Continue</Button>
                  : <Button type="submit">Submit</Button>}
      </div>
    </Form>
  );
}
```

RHF's `trigger(fieldNames)` validates only the current step's fields before advancing — the canonical pattern for per-step validation gating.

## WCAG 2.1 AA notes

- **Keyboard navigation (2.1.1)** — every step transition must be reachable via Tab + Enter. Mouse-only "Next" buttons fail. The clickable step pills must also be reachable via keyboard with `<button>` not `<div>`.
- **Focus management (2.4.3)** — on step transition, programmatically focus the first input of the new step. Without this, screen-reader users land on the body and re-read the page from the top.
- **Status announcements (4.1.3)** — wrap the step-change message in `aria-live="polite"` (non-interrupting) or `aria-live="assertive"` (for error-step jumps). Use `polite` by default to avoid screen-reader rudeness.
- **Page title (2.4.2)** — update `document.title` to include "Step N of M" so screen-reader users orienting via title get the position.
- **No keyboard traps (2.1.2)** — the "Back" button on step 1 must return to the prior page, not loop the user inside step 1. Browser-native back is the safest UX.
- **Focus visible (2.4.7)** — never `outline: none` on step indicators or wizard nav buttons. Use `:focus-visible` ring with sufficient contrast.
- **Form errors must be programmatically determined (3.3.1)** — see `TECH-form-validation-patterns.md` for the `aria-invalid` + `aria-describedby` contract.

## Cross-references

- `amw-form-designer-agent.md` §9 — invoked when the form-designer agent's YAML return contains a `multi_step` block.
- `TECH-form-validation-patterns.md` — defines the per-step validation rules referenced from §5 above.
- `TECH-form-async-submit.md` — defines submit-state UX referenced from the final step's submit button.
- `skills/amw-design-principles/spacing-rhythm.md` — 8pt rhythm for step-pill spacing.
- `skills/amw-design-principles/color-system.md` — danger/success token semantics for `stepStatus` colors.
