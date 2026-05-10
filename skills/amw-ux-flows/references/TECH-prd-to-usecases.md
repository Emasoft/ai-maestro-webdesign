---
name: TECH-prd-to-usecases
category: ux-flow-prd
source: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-prd-to-usecases

## What it does

Extracts a structured **use-case list** from a Product Requirements
Document (PRD) or a user-supplied feature list. Each use case gets a
canonical 7-field shape: ID, Name, Actors, Preconditions, Main Flow,
Alternative Flows, Postconditions. The list becomes the input to every
downstream phase (diagrams, wireframes, handoff).

## When to use

- **Phase 1 of the `ux-flows` skill** — every invocation starts here.
- **Whenever a PRD exists** at `docs/product/prd.md`, read it first.
- **When no PRD exists**, ask the user for a feature list. Do NOT
  invent use cases from thin air — that produces false requirements
  downstream.

Do not proceed to Phase 2 (Mermaid diagrams) without user approval of
the use-case list. Approval is mandatory.

## How it works

For each use case, document:

| Field | Description |
|---|---|
| `ID` | `UC-001`, `UC-002`, ... — padded to 3 digits for sorting |
| `Name` | Short descriptive name (3–6 words) |
| `Actors` | Who participates — User, System, Admin, Third-Party API, etc. |
| `Preconditions` | What must be true before the flow starts |
| `Main Flow` | Numbered step-by-step sequence (5–12 steps) |
| `Alternative Flows` | Branches, error paths, edge cases |
| `Postconditions` | What is true after the flow completes |

Save the list to `docs/ux-flows/use-cases.md`.

Present the list to the user for approval:

```
I've extracted 5 use cases from the PRD:
1. UC-001: User Registration
2. UC-002: User Login
3. UC-003: Password Reset
4. UC-004: Profile Edit
5. UC-005: Account Deletion

Approve this list or ask me to adjust (merge, split, add, remove).
```

Do not advance until the user explicitly confirms.

## Minimal example

Registration use case:

```markdown
### UC-001: User Registration

**Actors:** Prospective User, Email Service, Database

**Preconditions:**
- User is not logged in
- Email address is not already registered

**Main Flow:**
1. User navigates to /register
2. User enters email, password, and accepts terms
3. System validates email format and password strength
4. System hashes password with bcrypt
5. System creates user row in database with `email_verified=false`
6. System sends verification email via Email Service
7. User receives email with verification link
8. User clicks link → System marks `email_verified=true`
9. System redirects user to login page

**Alternative Flows:**
- 3a. Email format invalid → show inline error, stay on form
- 3b. Password too weak → show strength meter feedback
- 5a. Email already registered → show "account exists, sign in?" prompt
- 7a. Email not received → "resend verification" button after 60s

**Postconditions:**
- User row exists in `users` table
- `email_verified=true`
- User can log in
```

## Gotchas

- **IDs must be unique and stable.** Once the user approves UC-001, it
  stays UC-001 forever — even if use cases are added later. Never
  renumber after approval; it invalidates all downstream references in
  diagrams and wireframes.
- **Alternative flows include EVERY error path the user might hit.**
  Skipping error flows produces wireframes without error states, which
  ship incomplete UX.
- **Postconditions are assertable.** "User is happy" is not a
  postcondition. "User row exists with `email_verified=true`" is.
- **Main flow uses imperative present tense.** "User navigates",
  "System validates" — not "User navigated" or "User will navigate".
- **Group tightly-coupled flows as alternative flows, not separate use
  cases.** Password reset-via-email is an alternative of login, not a
  standalone UC — unless the product has two independent flows for it.
- **Stop at 10–15 use cases per feature set.** Beyond that, the PRD is
  too broad; ask the user to split into modules and process one at a
  time.

## Cross-references

- [SKILL](../SKILL.md) — Phase 1 of the workflow
- [TECH-4-phase-mandatory-workflow](TECH-4-phase-mandatory-workflow.md) — the overall pipeline
  > What it does · When to use · How it works · Phase 1 — Use case extraction (Phase-1 gate) · Phase 2 — Mermaid diagrams · Phase 3 — HTML wireframes (MANDATORY) · Phase 4 — Consolidation handoff · Minimal example · Gotchas · Cross-references
- [TECH-use-case-document-schema](TECH-use-case-document-schema.md) — the file shape written to disk
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-mermaid-flowchart-screen-map](TECH-mermaid-flowchart-screen-map.md) — Phase 2 consumes these use
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  cases
