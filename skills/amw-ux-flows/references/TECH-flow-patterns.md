---
name: TECH-flow-patterns
category: ux-flow
source: ux-designer-skill-main/references/16-onboarding.md (MIT, direct-port) + ux-designer-skill-main/references/14-ai-ux-patterns.md (T-149..T-156 synthesis)
also-in:
---

## Table of Contents

- [What this is](#what-this-is)
- [Pattern 1 — Onboarding wizard](#pattern-1--onboarding-wizard)
- [Pattern 2 — Sign-up + email verification](#pattern-2--sign-up--email-verification)
- [Pattern 3 — Checkout funnel](#pattern-3--checkout-funnel)
- [Pattern 4 — Password reset](#pattern-4--password-reset)
- [Pattern 5 — Error recovery](#pattern-5--error-recovery)
- [Cross-cutting principles](#cross-cutting-principles)
- [Cross-references](#cross-references)

# Flow patterns — canonical multi-screen flows with state diagrams and decision points

## What this is

Five canonical UX flow patterns that recur in nearly every webapp project: onboarding, sign-up + email verification, checkout, password reset, error recovery. For each: the state diagram, the key decision points, the screens, and the failure modes.

These patterns are the input to wireframe production. When `amw-wireframe-builder-agent` produces a multi-screen flow, the screens map onto one of these patterns. Deviating from a canonical pattern is allowed — but only with intent, and only after acknowledging the cost (users have to learn the new pattern).

Each pattern documents the **happy path**, the **decision points** (where the flow branches), and the **failure modes** (where users drop off or get stuck).

## Pattern 1 — Onboarding wizard

The 3–5 step first-run experience that brings the user from "just signed up" to "experienced first value" (the aha moment).

### State diagram

```
[Welcome]
   │
   ▼
[Step 1: profile / role]
   │
   ├─ skip ─────────────────┐
   ▼                        │
[Step 2: team / workspace]  │
   │                        │
   ├─ skip ─────────────┐   │
   ▼                    │   │
[Step 3: connect data]  │   │
   │                    │   │
   ├─ skip ──────┐      │   │
   ▼             │      │   │
[Step 4: invite] │      │   │
   │             │      │   │
   ▼             ▼      ▼   ▼
[Completion / aha moment]
```

### Key decision points

1. **Skip vs continue at every step.** Every step shows BOTH options. No mandatory tour traps.
2. **Profile collection: now vs deferred?** Default: defer everything except what's needed for routing. Collect role/team only if those determine the post-onboarding UI.
3. **Where does the wizard end?** At the aha moment, not at a "Setup complete!" celebration. The user should land on their first real task.

### Screens (minimum)

- Welcome (1 screen, 1 CTA: "Get started")
- 3–5 wizard steps (each with: progress indicator N of M, single primary CTA, Skip option, Back if Step > 1)
- Completion → land directly on the dashboard / first-task view

### Failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Forced sequence | User stuck on Step 2 because Step 2 requires data they don't have yet | Make every step skippable; persist progress |
| No progress indicator | User doesn't know how long the wizard is | Show "Step N of M" on every step |
| Celebration too early | Confetti before the user does anything meaningful | Move celebration to first real action, not wizard completion |
| Re-shown on return | Wizard appears every login | Persist completion; offer "retake tour" from Help only |
| Sign-up + wizard collision | 8 required fields total (3 in sign-up + 5 in wizard) | Reduce to 2 in sign-up + 3 in wizard; defer rest |

## Pattern 2 — Sign-up + email verification

The bridge between intent ("I want to try this") and account creation. Decision point: verify before or after first use?

### State diagram

```
[Marketing CTA: "Try free"]
   │
   ▼
[Sign-up form]
   │
   ├─ social SSO ──────────┐
   ▼                       │
[Email + password]         │
   │                       │
   ▼                       │
[Account created]          │
   │                       │
   ├─ verify-now path ─┐   │
   │                   │   │
   ├─ verify-later ────┤   │
   │                   │   │
   ▼                   ▼   ▼
[Limited app] OR [Verification gate]
   │                   │
   ▼                   ▼
[Verification email sent] ◄── (resend N times)
   │
   ▼
[Click link in email]
   │
   ▼
[Email verified, full access]
```

### Key decision points

1. **Verify-now vs verify-later.** Verify-now blocks app entry until verification; verify-later allows partial use with a banner. Best practice: verify-later for content-creation tools (reduces TTV), verify-now for transactional / financial.
2. **Magic link vs password.** Magic link removes password from sign-up (paste the email, no password creation). Often higher conversion for B2C; less appropriate for B2B (no shared login).
3. **Social SSO availability.** Google + Apple are table stakes for consumer; GitHub for developer tools; SSO/SAML for enterprise.
4. **Resend cadence.** Resend allowed after 30s; after 3 failed verifications, surface a "having trouble?" link to support.

### Screens (minimum)

- Sign-up form (1 screen): email + password OR social buttons. NO name/company/role here — defer.
- Account-created confirmation OR limited app shell (with a verify banner)
- "Verification email sent" screen: tells the user where to look, offers Resend (after 30s), shows the email used (so they can fix typos)
- Verification success screen (or auto-redirect to app)
- Failure paths: email-already-exists, weak-password (show inline before submit), social-login-failed

### Failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Hard gate too early | User can't see the product until email is verified | Allow limited use; gate only on high-value actions |
| No resend | User who didn't receive email is stuck | Show resend button + cadence (30s wait) |
| Typo in email, no recovery | User typed wrong email; verification will never arrive | Show the email on the sent-screen so the user can edit |
| Stale links | Verification link expires before user clicks | 24-hour minimum link expiry; show "resend" if expired |
| 8 required fields | High abandonment at sign-up form | Reduce to 2 fields (email + password) or magic link |

## Pattern 3 — Checkout funnel

E-commerce / SaaS purchase. The single highest-leverage flow in any commercial product. Drop-off at any step is revenue loss.

### State diagram

```
[Product / pricing page]
   │
   ▼
[Cart / plan selection]
   │
   ▼
[Sign-in OR guest checkout]
   │
   ├─ existing user ─────┐
   ▼                     │
[New account creation]   │
   │                     │
   ▼                     ▼
[Shipping / billing address]
   │
   ▼
[Payment method]
   │
   ▼
[Order review]
   │
   ▼
[Place order]
   │
   ├─ payment failed ─→ [Retry payment]
   │
   ▼
[Order confirmation]
   │
   ▼
[Post-purchase: receipt email + tracking]
```

### Key decision points

1. **Guest checkout vs forced account creation.** Forced account creation reduces conversion by 20–40% on first-time buyers. Always offer guest checkout for one-off purchases; offer account creation post-purchase ("save your details for next time").
2. **Step count.** Best is 1-step (all on one screen, validate inline) for simple purchases; 3-step max for complex (shipping → payment → review). Beyond 3 steps, drop-off is severe.
3. **Address autocomplete vs free-form.** Autocomplete reduces typos and errors but requires geocoding service. Free-form is fallback.
4. **Payment method choice.** Cards always; Apple Pay / Google Pay for mobile (single-tap = +30% mobile conversion); buy-now-pay-later (Klarna, Affirm) for high AOV.
5. **Pricing transparency.** Total (incl. tax, shipping) MUST appear before payment-method step. Hidden fees revealed at the last step is the #1 abandonment cause.

### Screens (minimum)

- Cart / order summary (with edit-quantity affordance)
- Identity step (sign-in OR guest, with email + password OR just email)
- Address + shipping (single screen if possible)
- Payment method (card form OR Apple/Google Pay)
- Review + place order (read-only summary with edit links per section)
- Confirmation (order number, ETA, receipt email confirmation)

### Failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Hidden fees at last step | High abandonment between Review and Place Order | Show full total (incl. tax + shipping) from cart onwards |
| Forced account creation | Drop-off at identity step | Offer guest checkout; offer account post-purchase |
| Card form rejected with vague error | User retries 3× and abandons | Inline field-level errors; specific messages ("CVV must be 3 digits") |
| No payment retry | One payment failure ends the session | Allow retry with different method; keep cart for 24h |
| Mobile experience is desktop-shrunk | Mobile drop-off > 2× desktop | Single-column, large tap targets, Apple/Google Pay first |
| Slow page-to-page transitions | User leaves between steps | Aim for < 1s; optimistic UI on Place Order |

## Pattern 4 — Password reset

Reactive flow — user has forgotten their password. Critical to get right because every failure means a lost session.

### State diagram

```
[Sign-in page: "Forgot password?"]
   │
   ▼
[Enter email]
   │
   ▼
[Reset email sent] (always — never confirm email exists, for security)
   │
   ▼
[User clicks link in email]
   │
   ▼
[Link valid?]
   │
   ├─ expired / used ─→ [Request new link]
   │
   ▼
[Enter new password] (+ confirm field, + strength meter)
   │
   ▼
[Password updated]
   │
   ▼
[Sign in with new password] OR auto-sign-in
```

### Key decision points

1. **"Email exists" disclosure.** Never confirm or deny that the email is in the system on the request screen — security risk. Show the same "Reset email sent" page regardless.
2. **Link expiry.** 1 hour is the standard. Too short causes frustration; too long is a security risk.
3. **Auto-sign-in after reset.** Modern best practice — the user already proved access to the email. Saves an extra step.
4. **Force sign-out of other sessions.** Optional but recommended after reset — protects against the scenario where the password was forgotten because of a hijack.
5. **Password strength feedback.** Inline as the user types, not after submit. Show strength meter; explain why a password is weak.

### Screens (minimum)

- Forgot-password form (1 field: email)
- "Reset email sent" confirmation
- New password form (new + confirm, strength meter, requirements visible)
- Success → auto-sign-in OR redirect to sign-in

### Failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Email-exists disclosure | "We don't have an account with that email" reveals user enumeration | Always show "If an account exists, an email has been sent" |
| Link too short | Users complain link expired before they could check email | 1-hour minimum; explain expiry in the email |
| No resend | User who didn't get email is stuck | Resend after 60s |
| Weak password accepted | User picks "password123" again | Enforce minimum 8 chars + 1 number/symbol; show strength meter |
| Force-sign-out missing | Compromised account stays compromised after reset | Invalidate all sessions on password change |

## Pattern 5 — Error recovery

The flow that runs when something goes wrong: payment failure, network drop, validation error, server error. Often neglected; often the difference between a recovered session and a lost user.

### State diagram

```
[User submits action]
   │
   ▼
[Validation client-side]
   │
   ├─ fail ─→ [Inline error, stay on form]
   │
   ▼
[Submit to server]
   │
   ▼
[Server response]
   │
   ├─ 4xx (validation) ─→ [Inline field error]
   ├─ 401 (auth) ────────→ [Re-auth prompt]
   ├─ 403 (forbidden) ──→ [Explanation + contact]
   ├─ 404 (not found) ──→ [Resource gone screen + suggested actions]
   ├─ 5xx (server) ─────→ [Generic error + retry button]
   ├─ network drop ─────→ [Offline indicator, queue for retry]
   │
   ▼ (success)
[Success state]
```

### Key decision points

1. **Inline vs page-level error.** Field-specific errors are inline at the field. System-wide errors get a banner at the top of the page or a toast. Never use a modal for non-blocking errors.
2. **Recover vs restart.** Whenever possible, preserve the user's input. A network-failed form submission should NOT discard the form. Save to local storage; restore on next session.
3. **Retry strategy.** Idempotent operations (GET, PUT, DELETE) auto-retry with backoff. Non-idempotent (POST) require user-initiated retry to avoid double-submit.
4. **Specificity.** Vague errors ("Something went wrong") are useless. Be specific: "Your card was declined — try another card or contact your bank." Never expose stack traces.
5. **Escalation path.** Every error screen has a "contact support" link, even if just `mailto:`.

### Screens / states (minimum)

- Inline field error (red text under field; field gets `aria-invalid="true"`)
- Banner error (top of page, dismissable, includes Retry if applicable)
- Toast error (corner notification for transient errors; 5–8s auto-dismiss)
- Full-page error (5xx or 404): icon + headline + 1-line cause + 2 actions ("Try again", "Go home") + support link
- Offline indicator (status bar at top: "You're offline. Changes will sync when you're back.")

### Failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Generic error message | User can't tell what went wrong or what to do | Specific message + suggested action |
| Form input lost on error | User retypes 12 fields after a 500 | Persist form state to local storage on submit attempt |
| Auto-retry on POST | Duplicate orders / charges | User-initiated retry only for non-idempotent ops |
| Modal for transient error | User has to dismiss modal before continuing | Use toast or inline; modals only for blocking errors |
| No support escalation | User who can't self-recover has nowhere to go | Every error screen has "Contact support" link |
| Stack trace exposed | Security risk, also looks unprofessional | Log internally, show user a generic-but-specific message |

## Cross-cutting principles

These apply to every flow above:

1. **Single source of truth for state.** Flow state lives in URL or server, not in component state. Refresh-during-flow MUST land the user where they were.
2. **Persistence > re-entry.** Anything the user typed survives a session interruption (storage, draft saves, partial state).
3. **Forward + back + skip.** Every multi-step flow has unambiguous controls for next, back, and (where applicable) skip.
4. **Progress indication.** Show step N of M whenever there are 3+ steps. Show a progress bar for long async work.
5. **Confirmation only for destructive or irreversible actions.** Delete, charge, send — yes. View, save draft — no.
6. **Mobile parity.** Every flow works on a phone. Test before claiming a flow is done.
7. **Accessibility.** Tab order matches visual order. Focus is managed on screen transitions. Errors are announced to screen readers (`aria-live`).

## Cross-references

- `TECH-no-dead-end-screens.md` — every screen has a forward path
- `TECH-mermaid-flowchart-screen-map.md` — diagramming flows as Mermaid screen-maps
- `TECH-split-large-flows-subflow-linking.md` — when a flow is too big for one diagram
- `TECH-wireframe-html-mobile-first.md` — wireframing the screens in each pattern
- `../../amw-design-principles/ai-slop-avoid.md` — V Interaction and motion (form transitions, validation patterns)
- `../../amw-infographics/references/TECH-data-viz-templates.md` — `Template 4` conversion funnel visualizes drop-off in these patterns
