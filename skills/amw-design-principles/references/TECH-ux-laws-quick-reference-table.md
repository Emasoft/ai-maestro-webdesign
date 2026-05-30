---
name: TECH-ux-laws-quick-reference-table
category: design-principles-ux-foundations
source: clean-room compilation (T-149 batch9 Wave 2 Round 3); one-page summary derived from `TECH-ux-laws-encyclopedia.md`
license: this file = MIT (plugin license)
also-in: see `TECH-ux-laws-encyclopedia.md` for the full entries with sources and edge cases
---

# UX laws quick-reference table

One-page lookup. For each law: a short application area, and a concrete web-design example. For deeper coverage (source, when it does NOT apply, common misuse), see `TECH-ux-laws-encyclopedia.md`.

The tables below split the 31 laws into 5 thematic groups so each table is narrow enough to read on a terminal or PR diff. The columns are: **Law** (short name), **Application** (one-line: when to apply it), **Example** (one-line: concrete web-design instance).

## Motor and perceptual laws

```
+----------------------+-------------------------------+----------------------------------+
| Law                  | Application                   | Example                          |
+----------------------+-------------------------------+----------------------------------+
| Fitts's Law          | Target size + distance        | 56px primary CTA, 40px secondary |
| Hick-Hyman Law       | Choice menu length            | 3 pricing plans, not 12          |
| Doherty Threshold    | Sub-400ms response budgets    | Skeleton screens; optimistic UI  |
+----------------------+-------------------------------+----------------------------------+
```

## Memory and cognition laws

```
+----------------------+-------------------------------+----------------------------------+
| Law                  | Application                   | Example                          |
+----------------------+-------------------------------+----------------------------------+
| Miller's Law 7+-2    | Working memory capacity       | 5-step wizard with step indicator|
| Cognitive Load       | Minimize extraneous load      | Group 40 settings into 6 sections|
| Information Foraging | Information scent in labels   | "API reference: A-Z" not "Refs"  |
| Chunking             | Group bits into meaning       | "4929 1234 5678 9010" credit card|
| Serial Position      | First and last items recalled | Most-used nav items at edges     |
+----------------------+-------------------------------+----------------------------------+
```

## Motivation and emotion laws

```
+----------------------+-------------------------------+----------------------------------+
| Law                  | Application                   | Example                          |
+----------------------+-------------------------------+----------------------------------+
| Goal-Gradient        | Visible progress accelerates  | "Step 4 of 5" + 80% progress bar |
| Von Restorff         | Differentiated item recalled  | One filled CTA among ghost btns  |
| Zeigarnik Effect     | Open loops pull attention     | Onboarding checklist on sidebar  |
| Peak-End Rule        | Peak moment + ending dominate | Celebratory completion screen    |
| Aesthetic-Usability  | Beauty halos perceived ease   | Polished CSS + micro-animations  |
| Fogg Behavior B=MAT  | Motivation, Ability, Trigger  | Invite prompt after first win    |
+----------------------+-------------------------------+----------------------------------+
```

## Gestalt grouping principles

```
+----------------------+-------------------------------+----------------------------------+
| Law                  | Application                   | Example                          |
+----------------------+-------------------------------+----------------------------------+
| Proximity            | Close elements group          | Tight gaps in card, wide between |
| Similarity           | Like-styled elements relate   | All CTAs same color, weight, size|
| Closure              | Brain completes shapes        | 3-side card, padding, bottom-line|
| Continuity           | Eye follows smooth lines      | Footer column headers all align  |
| Common Region        | Shared boundary groups        | Settings sections on tinted bg   |
| Common Fate          | Moving-together items group   | Cookie banner btns slide as one  |
| Figure-Ground        | Focus vs background           | Dark overlay on hero photo text  |
+----------------------+-------------------------------+----------------------------------+
```

## Attention, behavior, and system laws

```
+----------------------+-------------------------------+----------------------------------+
| Law                  | Application                   | Example                          |
+----------------------+-------------------------------+----------------------------------+
| Banner Blindness     | Avoid ad-DNA on real content  | Editorial-tone newsletter card   |
| Jakob's Law          | Match other-site conventions  | Logo top-left, account top-right |
| Pareto 80/20         | 20% of features = 80% use     | Polish dashboard + tasks first   |
| Tesler's Law         | Complexity moves, not removes | Explicit upload progress + retry |
| Sigmoid Adoption     | Stage rollouts by user cohort | 5% beta, then 50%, then 100%     |
| Mental Model         | Match user expectations       | "Tags vs folders" intro screen   |
| Affordance           | Object property suggests use  | Subtle shadow on clickable cards |
| Signifier            | Cue that reveals affordance   | Hover state + cursor pointer     |
| Mapping              | Control-to-effect correspond  | Right-slider = louder volume     |
| Constraints          | Restrict invalid actions      | Past dates disabled in picker    |
| Feedback Loop        | Action gets system response   | Spinner then "Saved" toast       |
| Postel's Law         | Liberal in, conservative out  | Accept any phone format, E.164   |
| Conway's Law         | UI seams = org seams          | Shared design-system team        |
| Hofstadter's Law     | Takes longer than expected    | Communicate 2-4 week range       |
+----------------------+-------------------------------+----------------------------------+
```

## How to use this table

1. **Diagnosing a UX problem.** Scan the Application column for the closest match to the symptom (e.g. "users can't find the CTA" → check Fitts's Law, Banner Blindness, Signifier).
2. **Justifying a design choice.** Cite the law in code review or design review. Example: "Per Fitts's Law and Von Restorff, the recommended plan card is 56px tall and uses a distinct navy fill."
3. **Auditing a finished design.** Walk the table top-to-bottom and ask "Is my design consistent with this law? If not, can I explain why the exception is worth it?"
4. **Going deeper.** Each law has a full entry in `TECH-ux-laws-encyclopedia.md` with source, when-NOT-to-apply, and common misuse — read that before citing the law in a contentious decision.

## Cross-references

- `TECH-ux-laws-encyclopedia.md` — full encyclopedia with source citations and edge cases.
- `../design-heuristics.md` — atomic-audit subset (Gestalt, Fitts, Hick) used in detailed visual reviews.
- `../ai-slop-avoid.md` — many AI-slop patterns are violations of these laws.
