# Question Templates for Design Tasks

## Table of Contents

- [Universal must-ask (every design task)](#universal-must-ask-every-design-task)
- [Task-specific additions](#task-specific-additions)
- [Questions NOT to ask](#questions-not-to-ask)
- [Suggested format](#suggested-format)
- [Tip](#tip)

> **Rule**: before kicking off any design task, ask at least 10 questions. Be greedy, don't be shy.
> One focused round of questions beats three rounds of rework.

---

## Universal must-ask (every design task)

### 1. Context & starting point
- Is there an existing design system / UI kit / brand book? Send it over.
- Any reference sites / product screenshots / style examples you like? Send them.
- Is there an existing codebase to reference (colors, fonts, spacing tokens)?
- Three brand keywords (e.g. "restrained, craft, cold" — not "modern, elegant").

### 2. Task & goal
- What core job does this design need to do? (sell / tell / teach / recruit / retain / …)
- What's the success metric? (CTR / completion rate / share rate / user feedback)
- Who is the audience? What device do they view it on?
- What's the context of use? (phone quick-scroll / desktop reading / meeting projection / printed collateral)

### 3. Variant dimensions
- How many variants do you need? (minimum 3)
- Which dimension should the variants focus on? **Visual / layout / interaction / copy / animation** (can pick more than one).
- Any interest in a "novel, anti-formula" option? Or keep everything conservative?

### 4. Tweaks
- Which parameters would you like to be adjustable? (primary color / font size / corner radius / light-dark mode / layout density)
- Do you want a Tweaks control panel?

### 5. Hard constraints
- Size / ratio / length limits.
- Words / colors / elements that must not appear.
- Elements / information / logos that must be included.
- Delivery format (HTML / PPT / image / PDF / code).

---

## Task-specific additions

### Landing page / Website

- Do we need mobile adaptation, or desktop-only?
- Any backend / interaction needed, or pure presentation?
- Do we want a hero section above the fold, or jump straight into the core message?
- Any SEO / performance constraints?

### Slides / Deck

- Who's presenting? Live or remote?
- How long does each slide stay on screen? (drives font size and density)
- Do you need speaker notes?
- Print requirement? (PDF / editable PPTX / projection-only)
- Any past deck templates to reference?

### App / Prototype

- Platform: iOS / Android / web / desktop.
- Hi-fi (real UI) or lo-fi (wireframe)?
- Real interactions, or is click-through navigation enough?
- Do you need mock data? Real data is even better.
- Device frame needed? (iPhone shell / browser chrome)

### Poster / Single image

- Size / use case / distribution platform.
- Do we need to reserve space for copy / logo?
- Purely visual, or heavy with text?
- Any image elements that must be included?

### Infographic / Data viz

- Send the data source.
- What is the **one** conclusion the piece has to deliver? (one chart, one point — don't try to say three things)
- Do I pick the chart type, or have you already decided?
- Black-and-white print friendly, or color-first?

### Brand collateral (business cards / invitations / emblems)

- Existing brand guidelines / vector logo files.
- Print or digital? Print → CMYK / bleed / size.
- Under what circumstances will the user see it?
- Any "tone samples" (e.g. "like Aesop")?

---

## Questions NOT to ask

- "What style do you want?" — too vague, the user can't answer, forces them to think twice.
- "Modern minimalist or retro?" — a false either/or, manufacturing a choice that doesn't exist.
- "Should we add animation?" — better to ask "which moments need to draw attention?"
- "What font should we use?" — that's a professional call. You decide; recommend with a reason.
- "What do you think about the color?" — you're the designer. Show a proposal first, then collect feedback.

---

## Suggested format

When asking in a batch, use a **questions_v2-style** structured list:

```markdown
## Quick questions before we start

**On context**
1. Any existing design system? If yes, send it.
2. Reference examples you like? Links or screenshots.

**On goal**
3. What's the core job of this page?
4. Audience and device?

**On variants**
5. How many options do you want?
6. Should the variants focus on visual or interaction?

**On Tweaks**
7. Which parameters should stay adjustable later?

**On constraints**
8. What must be included?
9. What absolutely must not appear?
10. Delivery format?
```

---

## Tip

> If the user genuinely can't answer some of the questions right now, fill in with **"my default"**:
> "If you don't have a specific preference, I'll default to X — tell me if you want it changed."
> That preserves your judgment without blocking the workflow.
