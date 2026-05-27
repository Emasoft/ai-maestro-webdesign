---
name: TECH-microcopy-patterns
category: design-principles-copywriting
source: clean-room reimplementation (T-135 batch9; underlying technique drawn from common-knowledge microcopy patterns documented in many sources)
license: this file = MIT (plugin license); NO verbatim copy from any GPL-2.0 source — derived from documented behavior and standard UX-writing conventions only
also-in: globalCC skill `technical-writing` for long-form prose; `accessibility-a11y` for screen-reader copy
---

# Microcopy patterns

## Table of Contents

- [What it does](#what-it-does)
- [When to apply](#when-to-apply)
- [Button labels — verb + object](#button-labels--verb--object)
- [Empty-state copy — action-oriented](#empty-state-copy--action-oriented)
- [Error messages — specific and recoverable](#error-messages--specific-and-recoverable)
- [Confirmation modals — destructive vs neutral](#confirmation-modals--destructive-vs-neutral)
- [Loading and progress messages — truthful estimates](#loading-and-progress-messages--truthful-estimates)
- [Success messages — brief celebration + next action](#success-messages--brief-celebration--next-action)
- [Cross-references](#cross-references)

## What it does

Defines the patterns the multilingual-copywriter agent and the wireframe-builder agent apply when authoring or auditing the small surfaces of a UI — buttons, empty states, errors, confirmations, loading indicators, success toasts. These are the surfaces where bad copy converts a clear interaction into a confused one.

The rules below are **format and behavior** rules, not verbatim copy templates. Each rule describes what the resulting text must do; the writer composes the actual sentence per locale, brand voice, and context. A button labeled "OK" in a destructive-confirmation modal violates the **verb + object** rule and the **destructive-distinct** rule simultaneously; the fix is "Delete project" (or its locale equivalent), not a fresh OK with a red background.

## When to apply

- Any time a sub-agent produces a string that will sit on a button, an empty-state placeholder, an error toast, a confirmation dialog, a loading indicator, or a success message.
- Any time the multilingual-copywriter agent classifies a row in its output as **microcopy** (per §9 of its skill-decision matrix).
- Any time the wireframe-builder agent is filling slot copy for the same surfaces and the brief did not provide finished text.

## Button labels — verb + object

Every primary button label states the **action the user is taking on the page** as a verb followed by a noun object. The user reads the label and predicts what will happen on click.

| Anti-pattern | Why it fails | Verb + object replacement |
|---|---|---|
| "OK" | The user has to remember what dialog they opened. | "Save changes" / "Delete project" / "Send invite" — whatever the dialog was about. |
| "Submit" | The user has to remember which form. Also reads as bureaucratic. | "Create account" / "Place order" / "Send message". |
| "Yes" / "No" on a destructive prompt | The user must remember the question. Verb + object makes the action self-describing. | "Delete account" / "Keep account" — both state the outcome explicitly. |
| "Continue" without context | Continue to what? | "Continue to payment" / "Continue to step 3 of 4". |
| "Get started" used as the only label on a primary CTA above the fold | Sounds promising but conveys no information about what gets started. | "Create your first project" / "Start the 14-day trial" — name the outcome. |

**Length rule:** primary-action labels target ≤ 3 words in English; the multilingual-copywriter agent uses morphological-equivalent length in the target locale. Secondary labels (text links) can be longer when they need a phrase ("Skip and continue without signing up").

**Imperative mood**, not gerund. "Save changes", not "Saving changes" (which describes a state, not an action — gerund forms belong on loading indicators, not buttons). The exception is dialog cancel buttons, which use the user's existing-state verb ("Keep changes", "Stay signed in").

## Empty-state copy — action-oriented

An empty state has three jobs in order:
1. Confirm to the user that the list is intentionally empty, not loading or broken.
2. Briefly explain what the user would normally see here.
3. Offer the next concrete action (with a button or link).

The empty-state copy is **not** a marketing surface; it is a navigation surface. Avoid "Nothing here yet — but you're going to love it when there is!" because it confirms emptiness without offering a path forward.

| Anti-pattern | Verb-driven replacement |
|---|---|
| "No items found." | "You haven't created any projects yet. **Create your first project** to start tracking." |
| "Sorry, nothing to show!" | "No invoices match your filters. **Clear filters** to see all invoices." |
| "Whoops, looks like you're new here." | "Your team has no shared boards yet. **Create a board** and your teammates will see it here." |

**Pattern: confirm + explain + offer.** Each empty state contains those three beats. If the user cannot take a next action (e.g., the empty state is a read-only consumer view), confirm + explain still apply; the offer becomes a link to documentation or a "Check back later" reassurance.

## Error messages — specific and recoverable

A good error message tells the user (a) what failed, (b) why, (c) what they can do to fix it. A bad error message tells them only (a) and stops.

| Anti-pattern | What's wrong | Specific + recoverable replacement |
|---|---|---|
| "An error occurred." | No information about which error or how to recover. | "We couldn't save your changes because your session expired. **Sign in again** to continue." |
| "Invalid input." | The user does not know which field, which constraint, or how to fix it. | "Phone number must include the country code (e.g., +1 555 0100)." |
| "Server error." (on a public-facing form) | Tells the user the server failed but offers no recourse. | "Something went wrong on our end. **Retry** in a moment, or **contact support** if it keeps happening." |
| "404 — Page not found." | Tells the user the URL is wrong but does not help them get back. | "We can't find that page. It may have moved. **Go to the home page** or **search the site**." |

**Three banned phrases in error messages:**
- "Oops!" — minimizes a real failure and sets a casual tone in a moment that may be high-stakes.
- "Please try again." (with no diagnosis) — implies the user did something wrong without saying what.
- "Sorry for the inconvenience." (alone) — apology without recourse is filler.

**Voice for errors:** matter-of-fact, not chirpy. The user is already mildly stressed; perky tone reads as tone-deaf. Calm, specific, recoverable.

## Confirmation modals — destructive vs neutral

Destructive actions (delete, cancel a subscription, leave a team, revoke access) carry irreversible consequences. Their confirmation modals are visually and verbally distinct from neutral confirmations (save, send, submit).

**Destructive confirmation pattern:**
- Title states the action and the object: "Delete project?", not "Are you sure?".
- Body names the consequence in concrete terms ("All 47 files and their version history will be permanently deleted").
- Primary button repeats the destructive verb ("Delete project"), styled in the destructive color (red in most palettes).
- Secondary button states the preserve-intent verb ("Keep project"), styled neutral.
- Optional friction: typed confirmation ("Type the project name to confirm") for high-stakes deletions.

**Neutral confirmation pattern:**
- Title states the positive outcome: "Save changes?".
- Body summarizes what will change.
- Primary button repeats the action verb ("Save changes").
- Secondary button reverses ("Discard"). Avoid "Cancel" when the modal is itself canceling something — overloaded "cancel" is confusing ("Cancel subscription" with a "Cancel" button: cancel what?).

**Pattern rule:** the two buttons in a confirmation modal must name **opposite outcomes**, not abstract OK/Cancel. The user reads the two button labels and knows which is destructive and which preserves their current state.

## Loading and progress messages — truthful estimates

Loading indicators that lie ("This will only take a moment...") for 30 seconds erode trust. Honest progress copy maintains trust and lowers abandonment.

| Anti-pattern | Truthful replacement |
|---|---|
| "Just a moment..." (for any operation) | "Generating your report — usually takes 10-20 seconds." (when actual P50 is ~15 seconds) |
| "Loading..." for an upload | "Uploading photo (2.4 MB)... 38% complete." |
| Infinite spinner with no text | Spinner + "Connecting to your account..." then update as state progresses. |
| "Almost done!" repeated for minutes | Stage-named progress: "Step 2 of 4: Optimizing images" then "Step 3 of 4: Uploading to server". |

**Length-of-operation rule:**
- < 1 second: no indicator needed; the operation feels instant.
- 1-3 seconds: simple spinner with a verb label ("Saving...").
- 3-10 seconds: spinner + estimate ("Compiling — about 5 seconds.").
- > 10 seconds: progress bar with percentage or stage names; offer a cancel button.
- > 60 seconds: surface a "We'll email you when it's done" option; long-running ops should not require the user to wait at the screen.

**Truthful does not mean exact.** "About 10 seconds" is honest; "exactly 10.0 seconds" is fake. Estimate from P50 latency; if P95 is double P50, say "usually 10 seconds, sometimes longer" rather than promise the P50.

## Success messages — brief celebration + next action

Success messages confirm the action completed AND nudge the user to their next step. They do not over-celebrate ("Amazing! Incredible! You did it!"); they confirm and redirect.

| Anti-pattern | Brief + next-action replacement |
|---|---|
| "Done!" | "Saved. **View your changes** or keep editing." |
| "Success!" | "Invoice sent to alex@example.com. **Send another** or **view in dashboard**." |
| "Great job! You're amazing!" (after a routine form submit) | "Profile updated. **View your profile**." |
| Toast that disappears in 2 seconds with no next-action link | Toast with action link: "Invite sent to alex@example.com. **Undo**." (undo within 5-10 seconds) |

**Pattern: confirmation verb + object (past tense or stative) + next-action link.** "Saved." alone is fine in low-stakes contexts. "Saved your changes. View dashboard." adds the next-action affordance.

**Toast duration:** success toasts auto-dismiss in 5-7 seconds; error toasts persist until user-dismissed (do not auto-dismiss an error the user has not seen).

**Undo is a feature, not a courtesy.** When the success message confirms a destructive-ish action (archived, deleted, sent), include an undo affordance with a real time window. "Email sent — Undo (5s)" is more trustworthy than "Email sent forever, no take-backs."

## Cross-references

- [TECH-voice-tone-archetypes.md](./TECH-voice-tone-archetypes.md) — the 7 voice/tone archetypes that color how these patterns are voiced
- [agents/amw-multilanguage-copywriter-agent.md](../../../agents/amw-multilanguage-copywriter-agent.md) §9 row "Microcopy per UI context" — agent uses this file
- [skills/amw-design-principles/ai-slop-avoid.md](../ai-slop-avoid.md) — banned slop phrases ("amazing!", "incredible!", "Oops!") this file builds on
- [skills/amw-design-principles/SKILL.md](../SKILL.md) — orchestrator that routes microcopy authoring through the copywriter agent
- [skills/amw-pretext/SKILL.md](../../amw-pretext/SKILL.md) — per-script typography concerns when microcopy is translated to CJK / RTL locales
