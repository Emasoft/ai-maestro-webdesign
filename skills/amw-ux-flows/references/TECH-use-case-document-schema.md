---
name: TECH-use-case-document-schema
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


# TECH-use-case-document-schema

## What it does

Defines the canonical Markdown shape of `docs/ux-flows/use-cases.md` —
the use-case list file that Phase 1 writes and every downstream phase
reads. The file is a sequence of per-UC sections, each with the same
7-field structure, so Phase 2 and Phase 3 can parse it reliably.

## When to use

- **End of Phase 1** — write this file before asking for user approval.
- **Phase 2 entry point** — read this file to produce the per-UC
  diagrams.
- **Phase 3 entry point** — read this file to identify unique screens.

## How it works

File layout:

```markdown
# Use Cases — [App Name]

> Approved on YYYY-MM-DD by <user>
> Source: docs/product/prd.md (or "user-supplied feature list")

## UC-001: [Short Name]

**Actors:** <comma-separated>

**Preconditions:**
- <assertion>
- <assertion>

**Main Flow:**
1. <step>
2. <step>
3. <step>

**Alternative Flows:**
- 3a. <branch>
- 5a. <error>

**Postconditions:**
- <assertion>
- <assertion>

---

## UC-002: [Next Short Name]
...
```

## Minimal example

Two-UC file for a simple auth flow:

```markdown
# Use Cases — My SaaS App

> Approved on 2026-04-22 by emanuele
> Source: docs/product/prd.md

## UC-001: User Registration

**Actors:** Prospective User, Email Service, Database

**Preconditions:**
- User is not logged in
- Email is not already registered

**Main Flow:**
1. User navigates to /register
2. User enters email + password + accepts terms
3. System validates format and password strength
4. System creates user row with email_verified=false
5. System sends verification email
6. User clicks verification link → email_verified=true
7. System redirects to login

**Alternative Flows:**
- 3a. Invalid email format → inline error
- 3b. Weak password → strength meter feedback
- 5a. Email already registered → "account exists, sign in?"

**Postconditions:**
- User row exists with email_verified=true
- User can log in

---

## UC-002: User Login

**Actors:** Registered User, Auth Service, Database

**Preconditions:**
- User row exists with email_verified=true

**Main Flow:**
1. User navigates to /login
2. User enters email + password
3. Auth service verifies password hash
4. Auth service issues accessToken + refreshToken
5. Frontend stores tokens
6. User redirected to /home

**Alternative Flows:**
- 3a. Wrong password → "invalid credentials" error
- 3b. Unverified email → "verify email first" prompt

**Postconditions:**
- User has valid session tokens
- User can access authenticated endpoints
```

## Gotchas

- **The `---` separator between UCs is required.** Phase 2 parser uses
  it to chunk the file. Missing separators cause the parser to merge
  adjacent UCs into a single blob.
- **IDs use exactly three-digit padding** (`UC-001`, not `UC-1`).
  Lexicographic sorting keeps them in numeric order without numeric
  parsing.
- **Numbered lists in Main Flow, bulleted lists in Preconditions /
  Postconditions.** Phase 2 parser treats numbered lists as ordered
  sequences (fed into the flowchart) and bullets as unordered
  assertions (fed into the state diagram).
- **Alternative flow numbering follows main-flow step numbers.**
  `3a. Invalid email` = alternative branching from step 3. Using
  decimal numbering (`3.1`, `3.2`) is ambiguous — the `3a`, `3b`
  convention is standard.
- **Header order matters** for the parser: Actors → Preconditions →
  Main Flow → Alternative Flows → Postconditions. Don't reorder.
- **One UC = one user goal**, not one feature. "Registration" is a
  goal; "email verification" is a sub-flow of that goal, documented as
  steps 5-6 or as an alternative flow.

## Cross-references

- [SKILL](../SKILL.md) — Phase 1 of the workflow
- [TECH-prd-to-usecases](TECH-prd-to-usecases.md) — how each UC section is filled in
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-4-phase-mandatory-workflow](TECH-4-phase-mandatory-workflow.md) — pipeline that consumes this file
  > What it does · When to use · How it works · Phase 1 — Use case extraction (Phase-1 gate) · Phase 2 — Mermaid diagrams · Phase 3 — HTML wireframes (MANDATORY) · Phase 4 — Consolidation handoff · Minimal example · Gotchas · Cross-references
- [TECH-mermaid-flowchart-screen-map](TECH-mermaid-flowchart-screen-map.md) — Phase 2 parser reads this
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
