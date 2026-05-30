---
name: TECH-ux-laws-encyclopedia
category: design-principles-ux-foundations
source: clean-room compilation (T-149 batch9 Wave 2 Round 3); UX laws are general professional knowledge — original author/year cited per law
license: this file = MIT (plugin license); no verbatim copy from copyrighted sources; restatement of well-documented findings in original prose
also-in: see `design-heuristics.md` for shorter Gestalt/Fitts/Hick subset used in atomic audits; `TECH-ux-laws-quick-reference-table.md` for the one-page lookup table
---

# UX laws encyclopedia

A working reference of the laws, principles, and effects that govern human-computer interaction. Each entry follows the same structure:

1. **Source** — original author and approximate year so a reader can trace the literature.
2. **Statement** — the plain-English version of what the law claims.
3. **When it applies** — the interaction types and situations where the law usefully predicts behavior.
4. **When it does NOT apply / common misuse** — limits, edge cases, and the fashionable misreadings to avoid.
5. **Web-design example** — a concrete application in the page, screen, or component the plugin actually produces.
6. **Related references** — cross-links to other TECH-*.md files (when relevant).

The laws are grouped roughly: motor/perceptual laws first (Fitts, Hick), memory/cognition laws next (Miller, Cognitive Load), motivational and emotional laws (Goal-Gradient, Peak-End), Gestalt perception, attention and habituation (Banner Blindness, Serial Position), behavioral models (Fogg, Sigmoid), Norman's foundational vocabulary (Mental Model, Affordance, Signifier, Mapping, Constraints, Feedback), and the meta-laws about software systems themselves (Tesler, Postel, Conway, Hofstadter).

## Table of Contents

- [Fitts's Law](#fittss-law)
- [Hick-Hyman Law](#hick-hyman-law)
- [Miller's Law (7 plus-or-minus 2)](#millers-law-7-plus-or-minus-2)
- [Doherty Threshold](#doherty-threshold)
- [Goal-Gradient Effect](#goal-gradient-effect)
- [Von Restorff Effect (Isolation Effect)](#von-restorff-effect-isolation-effect)
- [Tesler's Law (Conservation of Complexity)](#teslers-law-conservation-of-complexity)
- [Jakob's Law](#jakobs-law)
- [Pareto Principle (80/20)](#pareto-principle-8020)
- [Zeigarnik Effect](#zeigarnik-effect)
- [Peak-End Rule](#peak-end-rule)
- [Aesthetic-Usability Effect](#aesthetic-usability-effect)
- [Cognitive Load Theory](#cognitive-load-theory)
- [Information Foraging Theory](#information-foraging-theory)
- [Gestalt: Proximity](#gestalt-proximity)
- [Gestalt: Similarity](#gestalt-similarity)
- [Gestalt: Closure](#gestalt-closure)
- [Gestalt: Continuity (Good Continuation)](#gestalt-continuity-good-continuation)
- [Gestalt: Common Region](#gestalt-common-region)
- [Gestalt: Common Fate](#gestalt-common-fate)
- [Gestalt: Figure-Ground](#gestalt-figure-ground)
- [Banner Blindness](#banner-blindness)
- [Serial Position Effect](#serial-position-effect)
- [Chunking](#chunking)
- [Fogg Behavior Model (B = MAT)](#fogg-behavior-model-b--mat)
- [Sigmoid Adoption Curve (Diffusion of Innovations)](#sigmoid-adoption-curve-diffusion-of-innovations)
- [Mental Model](#mental-model)
- [Affordance](#affordance)
- [Signifier (Norman)](#signifier-norman)
- [Mapping](#mapping)
- [Constraints](#constraints)
- [Feedback Loop](#feedback-loop)
- [Postel's Law (Robustness Principle)](#postels-law-robustness-principle)
- [Conway's Law](#conways-law)
- [Hofstadter's Law](#hofstadters-law)
- [Cross-references](#cross-references)

---

## Fitts's Law

**Source.** Paul M. Fitts, 1954, "The information capacity of the human motor system in controlling the amplitude of movement," *Journal of Experimental Psychology*.

**Statement.** The time to acquire a target with a pointer is a function of the distance to the target and the size of the target. Formally, `T = a + b * log2(D/W + 1)` where `D` is distance and `W` is target width along the axis of motion. In practice: **closer and bigger targets are faster to hit; far and small targets are slowest.**

**When it applies.**

- Any pointing task: mouse, touch, trackpad, stylus, eye-tracker. Touch hit-targets are the most common modern application.
- Predicting which CTA users will choose when several are visible: the larger, closer one wins disproportionately.
- Justifying minimum hit-target sizes (44x44 px on touch per Apple HIG; 48x48 dp on Android).
- Edges and corners of a screen behave as infinitely large targets along one axis (the cursor cannot overshoot). This is why macOS puts the menu bar at the top and Windows puts the Start button in the corner.

**When it does NOT apply / common misuse.**

- Doesn't apply to keyboard navigation, voice, or gesture-only interfaces.
- "Make every button bigger" is the common misreading. Bigger targets cost layout real estate and reduce information density; the law just says **the buttons that matter most should be big and close**, not all buttons.
- Doesn't help predict whether the user will find the target in the first place — that's a search task, governed by Hick-Hyman and information-foraging.

**Web-design example.**

A pricing page with three plans. The recommended plan's CTA button is 56 px tall and centered in the viewport; the other two are 40 px tall and offset. Per Fitts's Law, the recommended CTA is roughly 1.4x faster to click and the visual placement primes the choice. The page also places the primary CTA near the bottom of the visible hero so it sits close to where the user's mouse already is after scrolling.

**Related references.**

- `design-heuristics.md` §II — atomic-audit version of Fitts's Law.
- `TECH-touch-targets.md` (if present) — exact pixel rules for touch.
- `spacing-rhythm.md` — vertical rhythm interacts with target sizes.

---

## Hick-Hyman Law

**Source.** William Edmund Hick, 1952, and Ray Hyman, 1953, working independently on choice-reaction time. Often called simply "Hick's Law."

**Statement.** The time to make a decision increases logarithmically with the number of equally probable choices. `T = b * log2(n + 1)`. In practice: **more choices = slower decisions, but at a decelerating rate — going from 2 to 4 options costs more than going from 8 to 16.**

**When it applies.**

- Menus, dropdowns, nav bars, plan selectors, filter lists. Any UI where the user picks one from N.
- Justifying short top-nav bars (3–7 items) on landing pages where conversion depends on a fast choice.
- Choosing between progressive disclosure (start with 3 options, expand on click) vs flat lists.
- Multi-step forms vs all-at-once forms.

**When it does NOT apply / common misuse.**

- The law assumes **equally probable, fully understood** choices. If 9 of 10 menu items are obviously irrelevant to the user's goal, those 9 do not cost decision time — the user is effectively choosing from 1.
- Doesn't apply when the user is searching for a specific item they already have in mind (that's a visual scan, not a decision).
- "Fewer choices is always better" is the common misreading. A Netflix front page with 6 movies would be terrible; the law just says the *decision among visible alternatives* gets slower. Categorize and group to keep effective `n` small at each level.
- Heavily-grouped lists effectively reduce `n` per group — a sidebar of 30 items split into 5 sections of 6 is closer to "decide among 5, then among 6" than "decide among 30."

**Web-design example.**

A SaaS pricing page with 3 plans (Hobby, Pro, Enterprise) plus a "Compare all features" link below. The default view shows 3 choices; per Hick-Hyman, this keeps the decision under ~2 seconds. The link expands into a 12-row comparison table on demand — the cost is paid only by users who actually want it. The opposite anti-pattern is the early-2000s e-commerce footer with 80 link items: every visitor pays the search cost regardless of intent.

**Related references.**

- `design-heuristics.md` §III.
- `TECH-landing-anatomy.md` — landing-page section budgets.

---

## Miller's Law (7 plus-or-minus 2)

**Source.** George A. Miller, 1956, "The magical number seven, plus or minus two: Some limits on our capacity for processing information," *Psychological Review*.

**Statement.** The number of objects an average human can hold in working memory is about 7, plus or minus 2. Miller's original paper covered a range of perceptual and memory tasks; the "7+/-2" tagline is a simplification.

**When it applies.**

- Phone-number formatting, OTP codes, license plates — anything the user must read, remember briefly, and re-enter.
- Navigation depth: a deeply nested menu where the user must remember "I went Settings → Account → Privacy → Sharing → Apps" exceeds working memory and the user backs out.
- Step counts in wizards (best 3–7 steps).
- Items on a single screen that the user must compare without scrolling.

**When it does NOT apply / common misuse.**

- Miller never said "show only 7 items in a menu." He said working memory holds about 7 *chunks*. A list of 50 grouped restaurants ("Italian: 12, Japanese: 8, ...") holds only as many chunks as the user needs to compare at once, not 50.
- Modern psychometrics revises working memory closer to 4 chunks (Cowan, 2001). The 7+/-2 number is approximate, not precise.
- "Menu items must be under 7" is the common misreading. The right framing is: **chunk and group so the user never holds more than ~7 items in working memory simultaneously**.

**Web-design example.**

A checkout flow with 5 steps (Cart → Shipping → Payment → Review → Confirmation). Each step shows a step indicator with the current step highlighted; the user does not need to remember which step they're on. Compare to a wizard with 11 unlabeled "Next" steps and no indicator — by step 6 the user has lost track of where they are and how much further to go.

**Related references.**

- `design-heuristics.md` §IV.
- [Chunking](#chunking) — the technique used to *expand* effective working memory.

---

## Doherty Threshold

**Source.** Walter J. Doherty and Ahrvind J. Thadani, IBM, 1982, "The Economic Value of Rapid Response Time."

**Statement.** Productivity soars when a computer and its users interact at a pace (under 400 ms) that ensures neither has to wait on the other. The original IBM study found a sharp productivity inflection at sub-400-ms response times.

**When it applies.**

- Any interactive surface where the user takes an action and waits for a response: typing, clicking, scrolling, searching.
- Setting performance budgets: 100 ms feels instant, 300 ms feels responsive, 1 s feels delayed, 10 s breaks attention entirely.
- Justifying optimistic UI (show success before the server confirms) and skeleton screens (show layout before content loads).
- Designing search-as-you-type, live filters, and inline validation.

**When it does NOT apply / common misuse.**

- Not all operations *can* be under 400 ms (large file uploads, complex queries, third-party API calls). For those, the law shifts to "give feedback every 400 ms about progress" — not "make it finish in 400 ms."
- The 400-ms number is rough. The deeper insight is that human flow state is broken by waits long enough that the user stops anticipating and starts mind-wandering. That threshold varies by task complexity.

**Web-design example.**

A search input that filters a 10,000-row product list. Naive implementation: send a request on every keystroke and wait for the network. Result: 800-ms lag per character, user gives up. Doherty-aware implementation: debounce 150 ms, show a skeleton row immediately, return results from cached client-side index for prefix matches, fall back to server only on miss. Felt latency: under 100 ms for the common case.

**Related references.**

- `TECH-motion-budgets.md` — animation durations sit inside Doherty's budget.
- `runtime-conventions.md` — perceived-performance guidelines.

---

## Goal-Gradient Effect

**Source.** Clark L. Hull, 1932, observed in rats running a maze; reformulated for human consumer behavior by Ran Kivetz, Oleg Urminsky, and Yuhuang Zheng, 2006, "The Goal-Gradient Hypothesis Resurrected" (Journal of Marketing Research).

**Statement.** The tendency to approach a goal increases with proximity to the goal. People accelerate as they near completion.

**When it applies.**

- Progress bars, completion meters, "5 of 7 steps complete" indicators.
- Loyalty programs ("3 more coffees until a free one"). Kivetz et al. showed customers buy coffees faster once they can see the reward approaching.
- Multi-step forms — completion rates climb sharply between step N-1 and step N.
- Onboarding checklists — users who complete 60% of the list finish at much higher rates than those at 30%.

**When it does NOT apply / common misuse.**

- The effect requires the user to *see* the goal approaching. Hidden progress doesn't trigger it.
- Fake progress (starting the bar at 20% to feel "closer") is a common misuse. Users notice and trust collapses on the next interaction.
- Doesn't work for goals the user doesn't actually want. A progress bar on a feature flow the user is forced through doesn't accelerate completion — it just shows them how much pain remains.

**Web-design example.**

A 5-step checkout. Step 1 shows "Step 1 of 5" with a 20%-filled bar. Step 4 shows "Step 4 of 5" with an 80%-filled bar AND a subtle visual nudge ("Almost done! One more step"). Drop-off between steps 4 and 5 is measurably lower than between steps 1 and 2.

**Related references.**

- `TECH-form-multi-step.md` — multi-step form patterns.
- [Zeigarnik Effect](#zeigarnik-effect) — the related "open task" pull.

---

## Von Restorff Effect (Isolation Effect)

**Source.** Hedwig von Restorff, 1933, "Über die Wirkung von Bereichsbildungen im Spurenfeld" (German psychology journal).

**Statement.** When multiple homogeneous stimuli are present, the one that differs from the rest is more likely to be remembered. Differentiation drives recall.

**When it applies.**

- Highlighting the "recommended" plan on a pricing page (different color, larger card, "MOST POPULAR" badge).
- Primary CTA styling — one filled button among ghost buttons gets clicked more often.
- Search results — making the sponsored result *visually distinct enough to be remembered* but *similar enough to be trusted* is a known dark pattern problem.
- Notifications — a red badge among gray icons commands attention because of isolation.

**When it does NOT apply / common misuse.**

- Doesn't apply when "everything is highlighted" — if every card has a "POPULAR" badge, the isolation evaporates and recall returns to baseline. This is the "every-row-bold" anti-pattern.
- The differentiated item is more *memorable*, not necessarily more *correct*. Designers sometimes isolate the wrong item (high-margin plan, not the user-fit plan) — that's a dark-pattern application of the law, not a bug in the law.

**Web-design example.**

Three pricing plans laid out in a row. Plans A and C use a white card with gray border; plan B uses a navy card with white text and a "Most popular" badge. Click-through rate on B is 2-3x A and C. The effect collapses if a second plan is also highlighted ("Best for teams") — the user is then choosing between TWO differentiated items, which by definition cannot both be differentiated.

**Related references.**

- `TECH-brand-voltage.md` — visual-weight rules; isolation is one application.

---

## Tesler's Law (Conservation of Complexity)

**Source.** Larry Tesler, 1984, while at Xerox PARC working on user-friendly software.

**Statement.** For any system, there is a certain amount of complexity that cannot be reduced. The only question is **who bears the burden** — the developer, the system, or the user. Hiding complexity in the UI does not eliminate it; it merely moves it.

**When it applies.**

- Form design: every field a developer omits to "simplify" the form is a piece of information someone (the user, the support team, the data-cleanup script) will pay for later.
- Settings screens: hiding a setting "to reduce clutter" still leaves the underlying choice somewhere — maybe it's now buried three menus deep, maybe it's a hardcoded default that a fraction of users will hate.
- Onboarding: skipping a configuration step on signup means the user faces the same configuration the first time they try to do real work, but now without the supportive context of onboarding.

**When it does NOT apply / common misuse.**

- "Adding complexity is fine because someone will pay for it" is a common misreading. The law says complexity cannot be eliminated — it doesn't say complexity is harmless. Pushing it onto users at the wrong moment (mid-task) causes abandonment.
- Doesn't apply to *artificial* complexity (badly modeled data, unnecessary configuration). Those can be removed entirely. Tesler refers to *essential* complexity.

**Web-design example.**

A photo-upload feature. Naive design: a single "Upload" button. The user uploads a 50-MB file; the server times out; the user retries; same result. Essential complexity (file-size limits, format conversion, progress feedback) was hidden, and the user pays for it in failed uploads. Tesler-aware design: client-side resize/compress for >10 MB, format-conversion hint, chunked upload with progress, "Cancel" button always visible. Complexity is now in the UI where it can be communicated, not in opaque server failures.

**Related references.**

- `TECH-form-async-submit.md` — example of explicitly communicating async complexity.

---

## Jakob's Law

**Source.** Jakob Nielsen, 2000, "End of Web Design." Often referenced in Nielsen Norman Group publications.

**Statement.** Users spend most of their time on other sites. This means users prefer your site to work the same way as all the other sites they already know.

**When it applies.**

- Conventional placements: logo top-left, primary nav top, search top-right, footer at bottom. Deviating from these is expensive without strong justification.
- Form conventions: email first, then password; "Sign in" and "Sign up" as distinct labels; password reset accessible from sign-in.
- E-commerce patterns: cart icon top-right, product image gallery left, price + CTA on the right, reviews below.
- Standard icon meanings: hamburger = nav, magnifying-glass = search, gear = settings, person = account.

**When it does NOT apply / common misuse.**

- "Copy everyone else exactly" is the common misreading. The law says users *prefer familiar patterns*, not that no innovation is allowed. The bar for breaking a pattern is "does the new pattern offer enough benefit to overcome the learning cost?"
- Doesn't apply equally across contexts. A specialized professional tool (Figma, Photoshop) can and must invent patterns its niche audience learns. A mass-market consumer site cannot.
- New patterns *do* become conventions over time. Hamburger menus were unfamiliar in 2008 and ubiquitous by 2014. Jakob's Law says you don't get to skip the unfamiliarity tax during transition.

**Web-design example.**

A SaaS dashboard places the user account menu at the top-left next to the logo (unconventional — usually top-right). Initial user-test sessions show 8 of 10 testers can't find their account settings. The team moves the menu to top-right; recognition rises to 9 of 10 immediately, no training needed. Jakob's Law cost them one week of redesign because they ignored it.

**Related references.**

- `design-heuristics.md` §V.
- `TECH-landing-anatomy.md` — conventional landing-page sections.

---

## Pareto Principle (80/20)

**Source.** Vilfredo Pareto, 1896, observing land ownership in Italy (20% of the population owned 80% of the land); generalized to many domains thereafter.

**Statement.** Roughly 80% of the effects come from 20% of the causes. In UX: most users use a small fraction of features most of the time; most revenue comes from a small fraction of users.

**When it applies.**

- Feature prioritization: identify the 20% of features that drive 80% of usage; invest disproportionately in their polish.
- Information architecture: the top 20% of pages are typically the entry point for 80% of sessions — those pages must have flawless first-impression behavior.
- Customer support tickets: 20% of issue types generate 80% of volume — fix those first to reduce support load.
- Performance budgets: the 20% of bundles loaded on the critical path matter most.

**When it does NOT apply / common misuse.**

- The numbers are not exact. Sometimes it's 90/10, sometimes 70/30. The principle is "expect heavy skew," not "exactly 80/20."
- The remaining 80% of features (used by 20% of users) often *justify the product's existence for those users*. Pruning them aggressively can hurt retention of high-value cohorts.
- Doesn't say "ignore the long tail." Some long-tail features are loved by power users who drive word-of-mouth.

**Web-design example.**

A team analyzes a project-management app's analytics. 80% of user-sessions use 6 features: dashboard, task list, task detail, comments, search, notifications. The team budgets 80% of UI-polish effort on those 6 surfaces — micro-animations, empty-state copy, error recovery, keyboard shortcuts. The remaining 40-some features get adequate, but not premium, treatment. Power-user complaints about the long tail are tracked separately and addressed in a slower cadence.

**Related references.**

- (none specific; informs every prioritization decision)

---

## Zeigarnik Effect

**Source.** Bluma Zeigarnik, 1927, studying waiters in a Berlin cafe (they remembered open orders but forgot completed ones).

**Statement.** People remember uncompleted or interrupted tasks better than completed ones. Open loops occupy mental attention until closed.

**When it applies.**

- Onboarding checklists — the visible "open" items pull the user back to complete them.
- Progress meters with explicit "X of Y done" — the unfinished items are mentally heavier than the finished ones.
- Save indicators — "Unsaved changes" is a Zeigarnik trigger that motivates saving.
- Form drafts auto-saved server-side — the user sees the draft on return and feels the pull to finish.

**When it does NOT apply / common misuse.**

- Doesn't apply if the user has emotionally disengaged from the task. A failed onboarding 6 months ago with a half-complete checklist is forgotten, not haunting.
- Can be weaponized into dark patterns (LinkedIn-style "Your profile is 47% complete" guilt-tripping) — that triggers the effect but corrodes trust.
- Some tasks *should* be allowed to close-without-completion. A form where the user starts and decides not to continue should not pursue them via email reminders — that crosses into harassment.

**Web-design example.**

A SaaS onboarding shows 5 setup steps in a sidebar: 3 are checked, 2 remain open. On the next session, the user lands on the dashboard and the sidebar still shows "2 of 5 setup steps remaining." Open-loop pull drives ~30% higher completion than a hidden checklist would. The key constraint: the open items must be **actually valuable to the user**, not just engagement-bait.

**Related references.**

- [Goal-Gradient Effect](#goal-gradient-effect) — they often co-occur in checklists.

---

## Peak-End Rule

**Source.** Daniel Kahneman, with collaborators, 1993 and later, "Evaluations by Moments: Past and Future" and *Thinking, Fast and Slow* (2011).

**Statement.** People judge an experience largely based on how they felt at its peak (most intense moment) and at its end, rather than on the average or total. The middle is mostly forgotten.

**When it applies.**

- Onboarding finales — the last screen of onboarding sets the user's recall of the whole onboarding.
- Error handling — a frustrating error mid-session is a "peak" that dominates recall even if the rest of the session was smooth.
- Checkout completion — a delightful confirmation screen (animation, friendly copy, clear next step) substantially improves post-purchase sentiment.
- Cancellation flows — make the *cancel* end positive (no guilt-trip, clear data-export, "we'd love feedback") and former users return at a measurably higher rate.

**When it does NOT apply / common misuse.**

- The rule is about *remembered* experience, not *lived* experience. Don't use it to justify a painful middle by promising a great ending — the painful middle still happens.
- Doesn't apply equally across personality types or cultures; some users are more sensitive to total/average than peak/end.

**Web-design example.**

A multi-step form for opening a bank account. The middle steps are necessarily tedious (identity verification, address, employment). The team focuses energy on (a) the *peak* — making the identity-verification scan moment feel quick and trustworthy with clear progress feedback, and (b) the *end* — a celebratory "Welcome to [bank], your account is open. Here's what to do next" screen with an actionable next step. Post-signup NPS rises sharply with no change to the middle.

**Related references.**

- (none specific in plugin; informs onboarding, error handling, completion flows)

---

## Aesthetic-Usability Effect

**Source.** Masaaki Kurosu and Kaori Kashimura, 1995, "Apparent usability vs. inherent usability" (ATM-interface study).

**Statement.** Users perceive aesthetically pleasing designs as more usable than less-pleasing designs, even when the underlying functionality is identical. Beauty creates a halo around perceived ease-of-use.

**When it applies.**

- Visual polish on early product impressions — a beautiful landing page is forgiven minor usability mistakes that an ugly one is not.
- Investor demos, sales presentations — perceived quality drives perceived usability.
- A/B testing — variant A may "test better" purely because it looks better, not because it's more usable.

**When it does NOT apply / common misuse.**

- The halo wears off as users encounter actual usability problems. A beautiful app the user can't accomplish their task with becomes a "pretty but broken" app — and the "broken" judgment sticks.
- Real-world long-term use weighs actual usability heavily. The aesthetic-usability effect is strongest at first impression and weakest after sustained use.
- "Make it pretty and we don't need usability testing" is the dangerous misreading. Aesthetic is *additive*, not substitutive.

**Web-design example.**

Two checkout flows are A/B tested. Variant A uses default browser controls; variant B uses custom-styled controls with subtle micro-animations and a balanced grid. Variant B wins in initial NPS surveys but conversion rates are similar. Six months later, B's conversion drifts down because a confusing field-grouping (a real usability flaw) finally surfaces — the aesthetic halo no longer masked it.

**Related references.**

- [Halo effects of fully developed visual hierarchies](#) — see `design-heuristics.md` §VI for visual hierarchy.

---

## Cognitive Load Theory

**Source.** John Sweller, 1988, "Cognitive Load During Problem Solving: Effects on Learning," *Cognitive Science*.

**Statement.** Working memory has a limited capacity. Three categories of load consume it: **intrinsic** (inherent difficulty of the task), **extraneous** (load imposed by the *way* the task is presented), and **germane** (load that contributes to building durable knowledge). Designers should minimize extraneous load and stay within the user's intrinsic + germane capacity.

**When it applies.**

- Any interface that requires the user to learn, remember, decide, or compute.
- Complex forms, dashboards, settings screens.
- Tutorials, documentation, onboarding flows.
- Comparing options (price tables, feature matrices) — extraneous load from poor layout dominates.

**When it does NOT apply / common misuse.**

- "Reduce cognitive load" is often misused to justify removing necessary information. The goal is to reduce *extraneous* load (poor layout, inconsistent labels, decorative noise), not intrinsic load (the actual choice the user must make).
- Doesn't apply much to passive consumption (video, music). Applies sharply to active interaction.

**Web-design example.**

A SaaS settings page lists 40 toggles in a single flat list with inconsistent labels ("Enable X" vs "X off" vs "Disable Y"). Extraneous load is high — the user must parse each toggle's polarity individually. Refactor: group into 6 sections (Account, Notifications, Privacy, Billing, Integrations, Advanced), use consistent positive labels ("Send weekly digest: on/off"), and add a search field. Intrinsic load (40 settings) is unchanged; extraneous load drops sharply; user satisfaction rises.

**Related references.**

- [Miller's Law](#millers-law-7-plus-or-minus-2) — working memory capacity.
- [Chunking](#chunking) — extending working memory via grouping.

---

## Information Foraging Theory

**Source.** Peter Pirolli and Stuart Card, Xerox PARC, 1995-2007. Inspired by optimal foraging theory in biology.

**Statement.** Users seeking information behave like predators: they follow "information scent" toward expected food (relevant information), abandon trails that smell weak, and pivot when a better patch is visible. The link text, snippet, breadcrumb, or category label is the "scent" — if it doesn't smell like the goal, the user leaves.

**When it applies.**

- Link labels, button labels, navigation, search results.
- Documentation tables of contents (a strong-scent ToC keeps the user reading; a weak-scent ToC sends them to Google).
- Search result snippets (the snippet is the scent; users skip results with weak scent even if highly ranked).
- Faceted filters in e-commerce — a clear filter taxonomy is high-scent, a vague one is low.

**When it does NOT apply / common misuse.**

- Doesn't apply to users who arrive with a specific URL or task in mind (they're not foraging, they're executing).
- "Use clickbait" is a misreading. Strong scent is *accurate predictive labeling*, not over-promise. Click-bait that doesn't deliver causes the next forager to discount future scent from that source.

**Web-design example.**

A documentation portal. Naive navigation: "Getting Started," "Concepts," "Reference," "Advanced." Information scent is weak — what's in each section? Foraging-aware refactor: "Quick start (5 min)," "Build your first integration," "API reference: endpoints A-Z," "Optimization guides for high-volume." Each label predicts what the user will find. Time-to-first-useful-page drops measurably.

**Related references.**

- `TECH-microcopy-patterns.md` — link and button labels.
- `TECH-seo-information-architecture.md` (if present) — same logic for SEO snippets.

---

## Gestalt: Proximity

**Source.** Max Wertheimer, Kurt Koffka, Wolfgang Köhler — Gestalt psychology, ~1910-1930s.

**Statement.** Elements that are close together are perceived as belonging together. Distance signals grouping.

**When it applies.**

- Form-field labeling (label close to its field, not floating ambiguously).
- Section separation (large vertical gaps between sections, small gaps within).
- Card content (title, body, meta tightly grouped inside the card; large gap between cards).
- Toolbars (related actions clustered, unrelated actions separated).

**When it does NOT apply / common misuse.**

- "Equal spacing everywhere" is the common violation. If gaps within and between groups are identical, proximity stops signaling grouping and the eye must search.
- Doesn't apply when other Gestalt cues (color, enclosure, common region) override proximity. A red field-label next to a blue field-label far away can group with the blue field by common similarity even though proximity says otherwise.

**Web-design example.**

A product detail page lists 8 specifications in two columns. Naive layout: rows separated by 12 px, columns separated by 12 px. Eye doesn't know whether to read across rows or down columns. Proximity-aware: rows separated by 12 px, columns separated by 32 px. Eye reads down each column naturally.

**Related references.**

- `design-heuristics.md` §I.1.
- `spacing-rhythm.md` — 8 pt grid that implements proximity.

---

## Gestalt: Similarity

**Source.** Same Gestalt school, ~1910-1930s.

**Statement.** Elements that share visual attributes (color, shape, size, texture) are perceived as related. Visual sameness implies functional sameness.

**When it applies.**

- All clickable items share a consistent treatment (one accent color or one icon convention).
- All "secondary text" shares one muted gray.
- All form-error states share one red treatment + one icon.
- Tag/chip systems where category groups are color-coded.

**When it does NOT apply / common misuse.**

- "Make everything look different to be visually interesting" violates similarity and creates a Where's-Waldo screen.
- Conversely, "make every button look the same so nothing competes" can flatten visual hierarchy. Similarity must be applied per *category*, not globally.

**Web-design example.**

A dashboard has 4 link types: navigation, in-text references, external links, and "buy now" CTAs. Naive design: every link is blue underlined text. Users can't predict which links open new tabs, which scroll the same page, which navigate. Similarity-aware: nav = solid color block, in-text = dark blue with no underline, external = blue with external-link icon, CTA = filled button. Each category is internally similar and externally distinct.

**Related references.**

- `design-heuristics.md` §I.2.

---

## Gestalt: Closure

**Source.** Same Gestalt school, ~1910-1930s.

**Statement.** The brain automatically completes incomplete shapes. A partial outline is perceived as a whole.

**When it applies.**

- Card design — three sides of a rectangle plus consistent padding are enough; full borders are not required.
- Loading skeletons that imply structure without committing to specific content.
- Icon design — incomplete circles, partial brackets, suggestive shapes.
- Visual grouping using subtle background tints instead of hard borders.

**When it does NOT apply / common misuse.**

- "Use closure everywhere to reduce visual noise" can backfire when the shape is too incomplete and users can't reconstruct it.
- High-stakes interactions (delete, irreversible actions) should not rely solely on closure to communicate boundary — make the affordance explicit.

**Web-design example.**

A product card uses no border at all — just a 16 px padding inside, a thin 1 px bottom-line, and a hover state that adds a subtle shadow. The brain reads it as a card; visual noise is much lower than a full-bordered design.

**Related references.**

- `design-heuristics.md` §I.3.

---

## Gestalt: Continuity (Good Continuation)

**Source.** Same Gestalt school, ~1910-1930s.

**Statement.** The eye prefers to follow smooth curves and straight lines rather than abrupt direction changes. Aligned elements feel like one group.

**When it applies.**

- Vertical alignment of form labels and inputs.
- Grid-based layouts where every column edge aligns precisely.
- Reading flow — text aligned along an invisible vertical line keeps the eye on track.
- Connecting nodes in a diagram with curves that don't double-back.

**When it does NOT apply / common misuse.**

- Forced alignment of unrelated content creates false grouping.
- Long lines without visual rest points create monotony.

**Web-design example.**

A 3-column footer with link lists. Naive: each list has a different vertical start due to mismatched header heights. Continuity-aware: all column-header baselines align on the same line; all link-row baselines align too. The footer reads as one band, not three disjointed islands.

**Related references.**

- `design-heuristics.md` §I.4.

---

## Gestalt: Common Region

**Source.** Stephen Palmer, 1992, extending the classical Gestalt set.

**Statement.** Elements enclosed within the same boundary (a border, background tint, panel, or card) are perceived as belonging together — even more strongly than proximity alone would suggest.

**When it applies.**

- Cards, panels, sidebars — anything with a visible region boundary.
- Settings sections with subtle gray backgrounds separating categories.
- Form fieldsets with `<fieldset>` borders or background tints.
- Drag-and-drop zones — the highlighted drop region tells the user "everything inside here is part of one operation."

**When it does NOT apply / common misuse.**

- Heavy borders everywhere produce visual clutter; subtle tints or whitespace often serve common region better.
- A region with mixed content (some related, some not) signals false grouping.

**Web-design example.**

A pricing page groups "What's included" features into a card with a light gray background. Above the card, a section header "Hobby plan includes" sits on the white page background. The card boundary creates common region; the header sits in a different region. Users scan card content as one unit.

**Related references.**

- `design-heuristics.md` §I.5.

---

## Gestalt: Common Fate

**Source.** Same Gestalt school + later research on motion perception.

**Statement.** Elements that move together are perceived as belonging together, even if they are otherwise dissimilar.

**When it applies.**

- Staggered list animations — items sliding in together feel like one group.
- Parallax scrolling — elements moving at the same rate are read as one layer.
- Drag-select in spreadsheets — items moving with the cursor are grouped by selection.
- Page transitions — content sliding in unison from the right reads as "one new screen."

**When it does NOT apply / common misuse.**

- Animations that overload common-fate (everything moves all the time) destroy the signal.
- Doesn't apply to static surfaces.

**Web-design example.**

A "Cookie banner" component slides up from the bottom; the "Accept all" and "Reject all" buttons inside slide up with the banner at the same velocity. Common fate tells the user "these buttons belong to this banner." A buggy version where the buttons fade in 200 ms after the banner is up reads as "two separate things showing up" — slower to parse.

**Related references.**

- `TECH-motion-budgets.md` — animation timings.

---

## Gestalt: Figure-Ground

**Source.** Edgar Rubin, 1915, "Synsoplevede Figurer" (the Rubin vase).

**Statement.** The visual field is divided into figure (the focus of attention) and ground (background). The brain assigns figure-ground status automatically; designers must control which element gets figure status.

**When it applies.**

- Modal dialogs (modal is figure, dimmed page is ground).
- Hero sections (main message is figure, background image is ground).
- Buttons on textured backgrounds (button surface must be figure even if background is busy).
- Text-on-image (the text must be figure — backed by overlay or shadow if needed for contrast).

**When it does NOT apply / common misuse.**

- Insufficient contrast between figure and ground makes the figure ambiguous. Decorative backgrounds that compete with content for figure status reduce readability.
- "Use a faint background pattern to add visual interest" frequently violates figure-ground when the pattern is too strong.

**Web-design example.**

A landing-page hero uses a full-bleed background photo. Naive: white headline text directly on the photo. Some photos have light areas where the headline becomes ground (unreadable). Figure-ground-aware: add a dark gradient overlay over the photo bottom-half so the headline always has contrast; or use a solid color section underneath for the headline. Figure status is now stable across all photo variants.

**Related references.**

- `color-system.md` — contrast ratios that preserve figure-ground.

---

## Banner Blindness

**Source.** Jan Panero Benway and David M. Lane, 1998, "Banner Blindness: Web Searchers Often Miss 'Obvious' Links." Confirmed by Nielsen Norman Group multiple times since.

**Statement.** Web users learn to ignore content that looks like advertising, even when it's not. Anything that resembles a banner ad — bright colors, oversized, top-of-page placement, "OFFER!" copy — gets visually filtered out.

**When it applies.**

- Hero sections that look too "promotional" (bright colors + bold CTA + stock photo) can get scanned past.
- Sidebar promotions, even legitimate ones, are largely ignored.
- Right-rail content in editorial sites is read at much lower rates than left-side content.
- Anything with the visual DNA of an ad-tech ad — randomly-placed, attention-stealing, brand-mismatched — is blind-spotted.

**When it does NOT apply / common misuse.**

- Doesn't apply to logged-in users in a familiar app — they're not in "scanning for ads" mode.
- Doesn't apply to content the user actively searched for.
- "Make CTAs less prominent" is the wrong fix. The right fix is "make CTAs look like content, not like ads" — integrated into the page rhythm, with editorial typography.

**Web-design example.**

A news site adds an in-article newsletter signup. Variant A: a bright-yellow card with "SUBSCRIBE NOW!" — gets ignored. Variant B: a quiet card with the article's same typography, a "If you liked this, get our weekly digest" headline, and a subtle in-flow input. Variant B converts substantially better because it doesn't read as an ad.

**Related references.**

- `TECH-microcopy-patterns.md` — CTA copy tone.

---

## Serial Position Effect

**Source.** Hermann Ebbinghaus, 1885, on memory recall. Combination of **primacy** (first items remembered well) and **recency** (last items remembered well); middle items least remembered.

**Statement.** People are most likely to remember the first and last items in a series. The middle is forgotten.

**When it applies.**

- Navigation order — first and last items in a top nav are most memorable.
- Tab order — first and last tabs draw most attention.
- List-based content — the first 2-3 and last 1-2 items dominate recall.
- Presentations — the first slide and last slide are remembered; the middle blurs.

**When it does NOT apply / common misuse.**

- Doesn't apply to short lists (3 or fewer items — all positions are roughly equal).
- "Always put the most important thing first" is a useful heuristic but ignores recency. The most important thing in a long list could go first OR last; the worst place is the middle.
- Doesn't override Von Restorff — an isolated item in the middle still gets remembered.

**Web-design example.**

A 7-item top nav for a SaaS product. Critical items (Dashboard, Settings) are placed first; the most-used utility (Help) is placed last. The middle items (Reports, Integrations, Team, Billing) are accessed via direct deep-linking from elsewhere, so their middle position is acceptable. User-test recall confirms first/last items dominate.

**Related references.**

- [Chunking](#chunking) — used in conjunction to split long lists into segments where serial position resets.

---

## Chunking

**Source.** George A. Miller, 1956, in the same paper as Miller's Law. Further developed in cognitive psychology.

**Statement.** Working memory holds a small number of *chunks*, not bits. By grouping bits into meaningful chunks, the effective capacity expands dramatically — "1492" is one chunk for someone who knows the year, four chunks for someone who doesn't.

**When it applies.**

- Phone numbers, credit-card numbers, OTP codes — group digits in 3-4 character clusters.
- Long lists — split by section, by date, by category.
- Form layout — group related fields under section headers.
- Reading rhythm — paragraphs > sentences > words.

**When it does NOT apply / common misuse.**

- Bad chunking (groups that don't reflect actual meaning) adds extraneous load instead of reducing it. A phone number chunked as "123-4567-890" instead of "123-456-7890" is *harder* than no chunking.
- Doesn't apply when the user is dealing with already-chunked content (a single ID number, a single price).

**Web-design example.**

A credit-card input. Naive: a single long text field with no formatting. User reads the printed card number ("4929 1234 5678 9010") and types it as one string, often mis-typing. Chunking-aware: auto-insert spaces every 4 digits as the user types ("4929 1234 5678 9010"), match the visual layout of the physical card, reduce typo rate substantially.

**Related references.**

- [Miller's Law](#millers-law-7-plus-or-minus-2).
- [Cognitive Load Theory](#cognitive-load-theory).

---

## Fogg Behavior Model (B = MAT)

**Source.** BJ Fogg, Stanford, 2009, "A Behavior Model for Persuasive Design."

**Statement.** Behavior (B) is a function of Motivation (M), Ability (A), and a Trigger (T) occurring at the same moment: `B = MAT`. If any one of the three is missing or insufficient, the behavior doesn't happen.

**When it applies.**

- Designing for action: get the user to sign up, complete a form, click a CTA, share a link.
- Diagnosing why a behavior isn't happening: is motivation low? Is the action too hard (ability)? Or is there no trigger to prompt it?
- Onboarding sequencing: introduce triggers when motivation is high (right after a win) and ability is high (when the user already has context).

**When it does NOT apply / common misuse.**

- "Just add more triggers (notifications, emails, banners)" without checking motivation and ability backfires. Spammy triggers reduce future motivation.
- Lowering ability requirements (one-click sign-up via OAuth) only helps if motivation is also present.
- High motivation can compensate for low ability (a determined user will tolerate friction); high ability cannot compensate for zero motivation.

**Web-design example.**

A SaaS team wonders why "Invite teammate" usage is low. Diagnosis with Fogg: motivation (users do want their teammates onboard, but it's not urgent), ability (invite flow requires copying emails from another tab — high friction), trigger (no prompt anywhere in the product). Fix: add a one-click "Invite from Google Workspace" (raise ability), trigger the prompt during the moment the user does their first successful action (motivation is high right after a win). Invite rates roughly triple.

**Related references.**

- [Goal-Gradient Effect](#goal-gradient-effect), [Zeigarnik Effect](#zeigarnik-effect) — motivation-related effects.

---

## Sigmoid Adoption Curve (Diffusion of Innovations)

**Source.** Everett Rogers, 1962, *Diffusion of Innovations*. The "innovators-early adopters-early majority-late majority-laggards" S-curve.

**Statement.** New technologies and products are adopted on an S-shaped curve. A small group of innovators tries first; if they validate it, early adopters follow; then the early majority creates the mainstream wave; late majority and laggards trail. Successful adoption requires explicit design for each phase.

**When it applies.**

- Feature rollouts — new features need an innovator/early-adopter on-ramp (opt-in beta, prominent "Try the new ___" entry point) before mass rollout.
- Product positioning — landing pages for early-adopter audiences emphasize novelty and capability; landing pages for early-majority audiences emphasize reliability and social proof.
- Pricing — early adopters tolerate higher friction; late majority needs frictionless onboarding.

**When it does NOT apply / common misuse.**

- Not every product adopts on a clean S-curve. Some die in the chasm between early adopters and early majority (Geoffrey Moore's "Crossing the Chasm" elaboration).
- The numbers in Rogers' original framework (2.5% innovators, 13.5% early adopters, etc.) are illustrative, not predictive for every product.

**Web-design example.**

A SaaS launches a major redesign. Rollout strategy: 5% of users get the new version via a "Try the new dashboard" prompt (innovators, early adopters); their feedback is captured via a sidebar widget; refinements happen for 4 weeks; then a 50% A/B test; finally a full rollout with a "Switch to the previous design" escape hatch (laggard accommodation). User-trust impact is much lower than a flag-day rollout.

**Related references.**

- `TECH-deployment-targets.md` — rollout pacing.

---

## Mental Model

**Source.** Kenneth Craik, 1943, *The Nature of Explanation*. Applied to HCI by Donald Norman, *The Design of Everyday Things* (1988, revised 2013).

**Statement.** Users hold internal mental models of how a system works. These models may be incomplete or inaccurate, but they drive the user's predictions and actions. UI design succeeds when the system's behavior matches the user's mental model.

**When it applies.**

- Onboarding — surface the system's mental model explicitly when it differs from user expectations.
- Iconography — use icons whose meaning matches the user's existing mental model (a floppy disk for "save" still works among users who never used floppies, because the mental model is now "save icon" rather than "literal floppy").
- Error recovery — if the system's actual state diverges from the user's mental model, error messages must bridge the gap, not just report the technical fault.

**When it does NOT apply / common misuse.**

- "Just train the user" rarely works at scale; mental models are sticky and changing them takes years.
- "Show a system diagram" doesn't impart a mental model unless the user has reason to study it.

**Web-design example.**

A cloud-storage app shows a "Folder" hierarchy. Users build a mental model: folders are physical containers, files live inside one folder, moving = relocating. When the team adds tagging (a file can have multiple tags), the introduction screen explicitly bridges: "Tags are like labels. A file can have many tags. Unlike folders, tags don't contain the file — they describe it." Mental model is updated in one screen; without the explicit bridge, users misuse tags as if they were folders.

**Related references.**

- [Jakob's Law](#jakobs-law) — users import mental models from other sites.

---

## Affordance

**Source.** James J. Gibson, 1979, *The Ecological Approach to Visual Perception*. Adapted to HCI by Donald Norman.

**Statement.** An affordance is a property of an object that suggests how it can be used. A handle affords pulling; a button affords pressing. In digital interfaces, affordances are perceived properties: a 3D-shaded button affords clicking; a flat block of text does not.

**When it applies.**

- Button design — visual depth, shadow, hover state communicate "pressable."
- Drag handles — striped or dotted icons afford grabbing.
- Resizable panels — corner triangles afford drag-to-resize.
- Scrollable areas — visible scrollbar (or scroll-cue) affords scrolling.

**When it does NOT apply / common misuse.**

- "Flat design" purposely strips affordances for aesthetic cleanliness. The trade-off: users have to learn that flat shapes are clickable — usability suffers, then recovers as the convention becomes familiar.
- Norman's later refinement: affordance is what an object *enables*; what *communicates* the affordance is a **signifier** (see next entry). The two concepts are often conflated.

**Web-design example.**

A flat-design dashboard uses no shadows or borders on buttons; only color signals "clickable." First-time users hover items to discover which are interactive — costly. Refactor: keep the flat aesthetic but add a subtle hover state (slight darkening or underline) on every clickable surface. The affordance is now perceptible.

**Related references.**

- [Signifier](#signifier-norman) — the visual cue that communicates the affordance.

---

## Signifier (Norman)

**Source.** Donald Norman, 2008, refining his earlier use of "affordance" in *The Design of Everyday Things*.

**Statement.** A signifier is a perceptible cue that tells the user where an affordance is and how to use it. The button's shadow is a signifier of its press-affordance. The cursor changing to a hand on hover is a signifier of clickability.

**When it applies.**

- Visual states (hover, focus, active) — these are signifiers of interactivity.
- Cursor types — `cursor: pointer` for clickable elements is a built-in browser signifier.
- Labels on icons (without a label, the icon's affordance is often invisible).
- Empty-state copy — "Click 'New project' to create your first project" is a verbal signifier.

**When it does NOT apply / common misuse.**

- Removing signifiers in pursuit of "clean design" is the common misuse. Discoverability collapses.
- Over-signifying everything (every element pulses, glows, animates on hover) defeats the purpose — nothing stands out.

**Web-design example.**

A dashboard's "Settings" gear icon has no label and no hover effect. Most new users don't try clicking it. Refactor: add a tooltip label on hover, a subtle scale-up on hover, and a label below the icon for first-week users. Click-through quadruples without changing the icon itself.

**Related references.**

- [Affordance](#affordance) — the property; signifier is the cue.
- `TECH-microcopy-patterns.md` — labels as verbal signifiers.

---

## Mapping

**Source.** Donald Norman, *The Design of Everyday Things*.

**Statement.** Mapping is the relationship between controls and their effects. Good mapping is natural — the up-arrow scrolls up, the volume slider moves right to get louder, the steering wheel turns right to turn the car right. Bad mapping requires the user to remember an arbitrary translation.

**When it applies.**

- Stove burners — the canonical bad-mapping example (four knobs in a row controlling burners in a square layout).
- Volume controls (vertical sliders vs horizontal — but always "more = up or right" in the user's mental model).
- Form fields (labels above inputs map to the input below them; right-aligned labels map ambiguously).
- Buttons in dialogs (primary on the right in macOS, on the left in Windows — system convention drives mapping).

**When it does NOT apply / common misuse.**

- Some mappings are arbitrary by domain (red = stop, green = go is a Western convention that doesn't hold universally).
- Skeuomorphic UIs over-applied mapping in some cases (a digital book that requires literally "turning" pages with a swipe — naturalistic but slower than a tap on a "Next" button).

**Web-design example.**

A volume control on a media player uses a vertical slider; "up" is louder. A second volume control on a separate page uses a horizontal slider where "right" is louder. The mapping is consistent within each control (more = away from origin) but inconsistent across the product. Refactor: pick one convention (say, horizontal sliders where "right is more") and use it everywhere.

**Related references.**

- (none specific in plugin; informs every control design)

---

## Constraints

**Source.** Donald Norman, *The Design of Everyday Things*. Four types: physical, cultural, semantic, logical.

**Statement.** Constraints restrict the actions a user can take and reduce the chance of error. A good design uses constraints to make the right action obvious and the wrong action impossible (or at least requiring confirmation).

**When it applies.**

- Date pickers that disallow past dates for future-only flows (appointment booking).
- Disabling the "Submit" button until all required fields are valid.
- Currency inputs that accept only numbers and one decimal point.
- File-upload restrictions (specific extensions, size limits) communicated before upload.

**When it does NOT apply / common misuse.**

- Over-constraining causes user frustration. "You can only enter your name in capitals" is a constraint that solves the developer's problem at the user's expense.
- Hidden constraints (the form rejects input but doesn't explain why) are worse than no constraint.
- Constraints must be communicated *before* the user attempts the wrong action, not as a punishment after.

**Web-design example.**

A booking form for next-day delivery. Past dates and the current date are visually disabled in the date picker; today's date is grayed-out with an explanation ("Same-day not available — earliest is tomorrow"). The user cannot select an invalid date and the reason is clear. Compare to a form that accepts any date and shows an error after submission — the user must guess what went wrong.

**Related references.**

- `TECH-form-validation-patterns.md` — implementation of constraints in form UX.

---

## Feedback Loop

**Source.** Norbert Wiener, 1948, cybernetics; applied to HCI by Donald Norman.

**Statement.** Every user action must be followed by perceptible system feedback. Without feedback, the user doesn't know whether the action registered, whether it succeeded, or what happened next. The feedback must arrive within the Doherty Threshold.

**When it applies.**

- Button clicks — visual press-state, then state-change confirming the action.
- Form submissions — loading indicator, then success or error message.
- Long-running operations — progress meter that updates regularly.
- Background actions — toast notifications confirming async work completed.

**When it does NOT apply / common misuse.**

- Excessive feedback (every keystroke triggers a popup) is worse than none.
- Late feedback (the success message appears 8 seconds after the action, after the user has moved on) is worse than late-then-instant feedback flow.

**Web-design example.**

A "Save changes" button on a settings page. Click → immediate button-press state → spinner replaces the label → on success, the button shows "Saved" briefly (1.5 s) then returns to "Save changes" with the changes preserved. The user has three feedback signals (press, loading, success) within Doherty budget. Compare to a button that does nothing visible until the page reloads 3 seconds later — uncertainty is high.

**Related references.**

- [Doherty Threshold](#doherty-threshold).
- `TECH-form-async-submit.md`.

---

## Postel's Law (Robustness Principle)

**Source.** Jon Postel, 1980, RFC 760 / RFC 793 (TCP specification). Sometimes phrased as "Be conservative in what you send, be liberal in what you accept."

**Statement.** Be conservative in what you do; be liberal in what you accept from others. Originally for network protocols, widely applied to UX: accept user input flexibly (whitespace, capitalization, accidental punctuation) even though you internally use a strict format.

**When it applies.**

- Email input — accept trailing whitespace, normalize case (`USER@EXAMPLE.COM` and `user@example.com` are the same address).
- Phone-number input — accept any combination of spaces, hyphens, parens, country-code prefixes; normalize to E.164 on save.
- Search — accept misspellings via fuzzy match.
- URL input — accept `http://`, `https://`, no protocol, trailing slashes; normalize on save.

**When it does NOT apply / common misuse.**

- Security-sensitive contexts (passwords, signatures) cannot be liberal — exact match is required.
- "Be liberal" can shade into "accept ambiguous input and silently guess." That breaks trust when the guess is wrong. Always show the user the normalized form so they can correct it.
- The original networking-Postel-Law has critics (Eric Allman, 2011, and IETF discussions): being too liberal can encode bad practice into the ecosystem. UX-Postel is mostly safe because the system controls the canonicalization.

**Web-design example.**

A subscription form accepts `Jane.Doe+newsletter@gmail.com` and stores it as `jane.doe@gmail.com` (Gmail dot-and-plus normalization). The user sees the normalized form on the next screen ("We'll send confirmations to jane.doe@gmail.com") so they're not surprised later. Liberal acceptance + transparent normalization.

**Related references.**

- `TECH-form-validation-patterns.md`.

---

## Conway's Law

**Source.** Melvin E. Conway, 1968, "How Do Committees Invent?"

**Statement.** Organizations design systems that mirror their own communication structures. The seams of the software match the seams of the org chart.

**When it applies.**

- UI inconsistency across product areas often reflects different teams owning different surfaces (and not talking to each other).
- Microservice boundaries map to team boundaries.
- Documentation organization usually mirrors the writing team's structure, not the reader's needs.
- When refactoring a product to feel like one cohesive whole, the underlying team structure may need to change first (or the cross-team coordination overhead may dominate).

**When it does NOT apply / common misuse.**

- Conway didn't claim every misalignment is inevitable. He observed the strong tendency; deliberate design (shared design systems, cross-team review, unified IA) can counteract it.
- "Just reorg the team" can fix Conway-shaped problems but creates its own disruption.

**Web-design example.**

A company's marketing site, app dashboard, and help center each look different — different fonts, different navigation patterns, different button styles. The marketing team owns marketing.com, the product team owns app.com, the support team owns help.com. Users perceive three different companies. Conway-aware fix: create a shared design-system team (or shared design system) that all three consume; the org-chart unification flows into the design unification.

**Related references.**

- (none specific in plugin; informs design-system strategy)

---

## Hofstadter's Law

**Source.** Douglas Hofstadter, 1979, *Gödel, Escher, Bach*.

**Statement.** It always takes longer than you expect, even when you take into account Hofstadter's Law. The law is self-referential: factoring in expected overruns doesn't fully compensate for the next layer of overrun.

**When it applies.**

- Estimating design or development work — multiply your best estimate by 1.5-3x for first-of-its-kind work.
- Product roadmaps — features always slip; communicate ranges, not dates.
- A/B test durations — recruiting enough traffic for significance always takes longer than the back-of-envelope math suggests.
- User-testing schedules — getting the right number of participants, the right tasks, the right room takes longer than booking N hours of recruiter time.

**When it does NOT apply / common misuse.**

- Routine, well-understood work (the team's 50th login form) is not subject to large overruns.
- "Just pad the estimate" is a partial fix. Hofstadter's Law applies to the *new and uncertain* parts; the well-understood parts estimate accurately.

**Web-design example.**

A design team estimates 2 weeks to redesign the settings page. Hofstadter-aware: they communicate a 2-4 week range internally, prep a "minimum-viable redesign" version that ships at 2 weeks if needed, plan the full version for 4. Stakeholder trust is preserved when reality lands at 3.5 weeks because the range was communicated up front.

**Related references.**

- (none specific in plugin; informs project planning)

---

## Cross-references

- `../design-heuristics.md` — atomic-audit version of Gestalt, Fitts, Hick (subset of this encyclopedia).
- `TECH-ux-laws-quick-reference-table.md` — one-page lookup table for the most-used laws.
- `TECH-microcopy-patterns.md` — application of Information Foraging, Affordance, Signifier in copy.
- `TECH-form-validation-patterns.md` — Constraints, Feedback Loop, Postel's Law in form UX.
- `TECH-form-multi-step.md` — Goal-Gradient, Zeigarnik Effect, Serial Position in wizards.
- `TECH-motion-budgets.md` — Doherty Threshold, Common Fate in animation timing.
- `../spacing-rhythm.md`, `../typography-system.md`, `../color-system.md` — token systems that implement Gestalt and figure-ground.
- `../ai-slop-avoid.md` — many AI-slop patterns are violations of these laws (Banner Blindness, Von Restorff dilution, weak information scent).

**End of encyclopedia.** Cross-link from any TECH-*.md or SKILL.md when a UX decision requires citing the underlying law.
