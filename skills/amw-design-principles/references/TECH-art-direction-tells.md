---
name: TECH-art-direction-tells
category: design-principles-reference
source: consolidated diagnostic QA-pass adapted from anydesign's "Art Direction Patterns" framework (uxKero/anydesign, MIT) — reimplemented our way; most tells cross-link our existing refs, two (pill-scale coexistence, alpha-overlay scale) are newly added because we lacked them
license: this file = MIT (plugin license)
also-in: "amw-design-md-extractor-agent (runs this as a QA pass after extraction); amw-ux-evaluator (diagnostic lens for design review); amw-design-md-auditor-agent (consistency/drift passes reference these tells)"
---

# ART-DIRECTION TELLS — the QA pass that separates "lists what I see" from "diagnoses how it works"

## Table of Contents

- [What this is](#what-this-is)
- [How to run the pass](#how-to-run-the-pass)
- [Surface-rhythm tells](#surface-rhythm-tells)
- [Token-coexistence tells](#token-coexistence-tells)
- [Color-discipline tells](#color-discipline-tells)
- [Elevation-discipline tells](#elevation-discipline-tells)
- [Composition-discipline tells](#composition-discipline-tells)
- [Cross-references](#cross-references)

## What this is

A consolidated diagnostic checklist of ~16 subtle art-direction patterns that *shallow* analysis routinely misses. Run it as a QA pass **after** extracting/analysing an existing design (or before declaring a new design's intent locked). Each tell prompts the same question: *"Did I notice this? If yes, did I record it in the right place? If no — am I sure it's absent, or did I just not look?"*

Most of these patterns already live, scattered, across the plugin's references (this file cross-links them so they can be run as ONE pass); two were genuinely missing and are defined in full here (marked **NEW**). The point of the pass is the consolidation: a single sweep that catches the diagnostic patterns no single technique file surfaces on its own.

## How to run the pass

For each tell: **present** → ensure it's documented in the right place AND consider whether it should become an explicit brand rule (a Do/Don't). **Absent** → only call it out when the absence is itself diagnostic ("no shadows — flat by design"; "no chromatic accent — the mood is carried by type + surface alone"). **Ambiguous** → log it as an Open Question, do not guess. **Do not pad** by listing every tell that isn't there.

## Surface-rhythm tells

- **Polarity-flipped section bands** — does the page alternate light ↔ dark surfaces as you scroll, with content inverting onto each polarity (depth-by-surface-inversion)? If yes, it's a deliberate rhythm, not noise. → record in the elevation/decoration notes + composition notes; relates to [TECH-token-system-elevation-and-radius](TECH-token-system-elevation-and-radius.md).
- **Atmospheric-gradient scoping** — is a gradient / mesh / wash confined to ONE zone (usually the hero) and forbidden everywhere else? The *scoping discipline* is the signal. → note the discipline; a page-wide generic gradient is the AI-slop failure mode ([ai-slop-avoid](../ai-slop-avoid.md) § VI).
- **Density alternation** — does the page swing between airy zones (heroes, intros) and dense zones (footer link matrices, pricing/comparison tables)? Document the rhythm; it's governed by `DATA_DENSITY` per [TECH-dial-configuration](TECH-dial-configuration.md) and the section-discipline rules in [TECH-layout-discipline](TECH-layout-discipline.md).

## Token-coexistence tells

- **Pill-scale coexistence — NEW.** Does the system run **two distinct corner radii deliberately** — e.g. a small functional radius for nav-scale controls (≈6px inputs/menus) AND a full pill (≈100px / 9999px) for marketing CTAs and tags — and keep them in **separate contexts** (never mixed on the same surface)? This is a mature-system signal, not inconsistency. Record both radii as named tokens AND capture the separation **as a rule** ("pills for marketing CTAs only; functional controls stay at the 6px scale"). The failure mode is mixing both radii in one component cluster, which reads as indecision. (Pairs with the radius scale in [TECH-token-system-elevation-and-radius](TECH-token-system-elevation-and-radius.md).)
- **Mono-usage scope** — is the monospaced face reserved for code only, or also used for captions / eyebrows / status labels / metadata? "Brand uses mono for status indicators" is a real brand decision → record it. (See typography roles in [typography-system](../typography-system.md).)
- **Weight ceiling** — does display type cap at a specific weight (often 600/Semibold) while heavier weights exist in the family but go *unused*? That restraint is deliberate brand discipline, not an omission → record as a Don't. (See [typography-system](../typography-system.md).)
- **Tracking discipline** — is there a clear convention (negative tracking on display, neutral on body, positive on small-caps labels)? Record it in the type notes and reinforce as a rule. (See [typography-system](../typography-system.md).)

## Color-discipline tells

- **Color "voltage"** — is there exactly ONE chromatic moment in an otherwise neutral palette? Where does it appear, and where is it *deliberately withheld*? This is frequently THE brand's signature element. → [TECH-brand-voltage](TECH-brand-voltage.md) + [TECH-signature-move](TECH-signature-move.md).
- **Alpha-overlay scale — NEW.** Alongside the solid color scale, is there a **parallel alpha-only scale** (e.g. `--overlay-04`, `--overlay-08`, `--overlay-12` … or `rgb(0 0 0 / 4%…64%)` steps) used for scrims, hover veils, and legibility washes over photography / gradients? A dedicated alpha ramp — rather than ad-hoc one-off `rgba()` values — is a mature-system signal. Record it as its own token group (distinct from the solid palette), and note what it's scoped to (overlays on imagery, not decorative fills). Its **absence** on an image-heavy design is itself diagnostic (text-on-photo contrast is probably being handled ad-hoc). (Pairs with color roles in [TECH-token-system-color-roles](TECH-token-system-color-roles.md).)
- **Feedback-color restraint** — are success / warning / error colors used ONLY in feedback contexts, or do they leak into decorative use? Restraint = signal of a disciplined system. → [TECH-token-system-color-roles](TECH-token-system-color-roles.md).

## Elevation-discipline tells

- **Stacked vs single-drop shadows** — does the system layer multiple small drops (Geist-style, soft realism) or use one heavier drop (Material-style)? Record which, as a Do. → [TECH-named-color-shadow-techniques](TECH-named-color-shadow-techniques.md).
- **Inset-shadow-as-border** — does the system use an inset 1px shadow in place of a real CSS border for sub-pixel crispness on Retina? Subtle but a real implementation tell. → [TECH-named-color-shadow-techniques](TECH-named-color-shadow-techniques.md).
- **Surface-tone vs shadow for elevation** — is depth established by *surface-color change* (a lighter card on a darker background, common in dark themes) rather than by shadows at all? If so, say it explicitly. → [TECH-token-system-elevation-and-radius](TECH-token-system-elevation-and-radius.md).

## Composition-discipline tells

- **Split-hero vs centered-hero canonicity** — which is canonical for this brand? Mixing both on the same surface is usually a smell. → hero rules in [TECH-layout-discipline](TECH-layout-discipline.md); the brand-defining choice may be the [signature move](TECH-signature-move.md).
- **Asymmetric whitespace** — does the layout use deliberate asymmetric whitespace, or is it symmetric / centered throughout? A strong stylistic marker either way — record which.
- **Image-treatment consistency** — do all images share treatment rules (grayscale→color on hover, fixed aspect ratio, consistent placeholder/loading treatment)? Inconsistency is either legacy debt or deliberate variety — decide which and record it. → image rules in [TECH-layout-discipline](TECH-layout-discipline.md).

## Cross-references

- [TECH-signature-move](TECH-signature-move.md) — the "ONE brand thing"; color-voltage is frequently it.
- [TECH-brand-voltage](TECH-brand-voltage.md) — the single-chromatic-moment discipline.
- [typography-system](../typography-system.md) — weight ceiling, tracking, mono-scope homes.
- [TECH-token-system-elevation-and-radius](TECH-token-system-elevation-and-radius.md) / [TECH-named-color-shadow-techniques](TECH-named-color-shadow-techniques.md) — elevation tells.
- [TECH-token-system-color-roles](TECH-token-system-color-roles.md) — alpha-overlay scale + feedback restraint homes.
- [TECH-layout-discipline](TECH-layout-discipline.md) — hero / whitespace / image-treatment composition tells.
- [ai-slop-avoid](../ai-slop-avoid.md) — the failure modes (page-wide generic gradient, etc.) these disciplines avoid.
