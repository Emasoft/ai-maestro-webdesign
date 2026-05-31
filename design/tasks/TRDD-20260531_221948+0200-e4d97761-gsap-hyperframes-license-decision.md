---
trdd-id: e4d97761-ecfc-4619-bcc3-7054ce9ab76e
title: GSAP-via-hyperframes licensing decision — accept, video-path-only
status: completed
created: 2026-05-31T22:19:48+0200
updated: 2026-05-31T22:19:48+0200
---

# TRDD-e4d97761 — GSAP-via-hyperframes licensing decision (accept, video-path-only)

**Filename:** `design/tasks/TRDD-20260531_221948+0200-e4d97761-gsap-hyperframes-license-decision.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## ⏵ STATE — READ THIS FIRST (authoritative; the decision is settled) — 2026-05-31

**Decision (settled by the owner):** KEEP `external/hyperframes/` as a plugin
backend. The GSAP transitive dependency it carries is acceptable because GSAP
imposes **no licensing fee** for our use. The plugin's **no-GSAP-in-website-code**
rule remains in full force, unchanged.

Do NOT re-investigate or re-litigate this in a future session. The facts below
were verified from primary sources; the decision is final.

## What was verified

1. **hyperframes uses GSAP.** `@hyperframes/player` declares `gsap` (`^3.12.5`,
   resolved to `gsap@3.15.0` in `external/hyperframes/bun.lock`). A hyperframes
   composition *is* a paused GSAP timeline; it ships a GSAP authoring skill.
   **No paid `@gsap/*` club plugins** are referenced (only free core gsap). GSAP
   is not vendored on disk (installed at render time).
2. **GSAP 3.15.0 license** (from `greensock/GSAP@3.15.0` `package.json`):
   `Standard 'no charge' license: https://gsap.com/standard-license`. No separate
   LICENSE file is bundled.
3. **Commercial use is free, no fee triggers** (verified from
   <https://gsap.com/standard-license>): *"Can I really use GSAP in commercial
   projects without paying anything? Yes, really! Commercial usage is covered
   under the standard license."* Use is granted *"on any website, web
   application, or digital interface by any person or entity."* Even the
   formerly members-only plugins (SplitText, MorphSVG) are now free for
   commercial use. There are no mandatory-payment scenarios. → **A commercial
   advert/video produced via hyperframes owes GSAP nothing.**
4. **The rendered MP4 contains no GSAP.** GSAP runs at render time inside the
   headless browser to animate DOM frames; ffmpeg encodes the resulting pixels.
   The delivered `.mp4` neither embeds nor redistributes GSAP code — so the
   output is not even a GSAP "distribution."
5. **Residual caveat (philosophical only):** GSAP's license, though free for all
   use, is GreenSock/Webflow's own license, **not** an OSI-approved open-source
   license (not MIT/Apache).

## The decision + the policy

- **Keep hyperframes** (and its GSAP-based video-render path).
- **No-GSAP-in-website-code rule REMAINS** (CLAUDE.md "Animation stack order";
  `skills/amw-hyperframes-bridge/SKILL.md`; `agents/amw-video-producer-agent.md`;
  `skills/amw-design-principles/references/TECH-pattern-vocabulary.md` animation-
  stack override). Webpage output uses the native / `animations.html` /
  Popmotion stack — never GSAP.
- **GSAP is permitted ONLY inside hyperframes video compositions** (output =
  pixels, no redistribution). This scoping already existed in the codebase and
  is correct; this TRDD records *why* it is acceptable.
- **Acknowledgment:** `README.md` discloses the GSAP transitive dependency, the
  free-commercial-use fact, and the video-path-only scoping.

## Durable artifacts to read before acting

- `README.md` → Acknowledgments section (the user-facing disclosure).
- <https://gsap.com/standard-license> (primary license source).
- Commits: `e6035b2` (disclose GSAP dep), `55222b0` (cite confirmed license),
  plus the README finalize commit that accompanies this TRDD.

## Why this exists

The owner's hard rule is "no proprietary or commercial things in the plugin
(except Anthropic)." GSAP triggered that concern. The investigation established
GSAP is free for all commercial use (no fees, ever, including ads) and is
confined to the video path with zero redistribution — so it does not bind any
downstream web/video developer. The only residual is that GSAP's license is not
OSI-open, which the owner accepted given (a) no fee, (b) video-path isolation,
(c) the no-GSAP-in-website-code rule staying in force. Recorded so the question
is never re-opened from scratch.
