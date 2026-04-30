---
name: TECH-uxeval-button-conventions
category: uxeval-dim
source: SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md
also-in:
---

# TECH: Button conventions (position + visual weight + spacing + labels)

## What it does

Component-specific reference for button evaluation. Buttons are the highest-frequency component in the evaluator's scope — they carry the primary action, so position, visual weight, and label precision matter more than on any other element.

## When to use

On every evaluation that includes a button group (CTA stack, form submit, navbar, modal action row, card footer).

## How it works

### Position

- **Primary action** (Sign Up, Submit, Buy, Save) → RIGHT
- **Secondary action** (Cancel, Sign In, Back) → LEFT of primary
- **Utility controls** (theme toggle, settings, language) → FAR RIGHT, after primary group

Industry baseline (observed convention):

| Site | Pattern |
|---|---|
| GitHub | [Sign In] [Sign Up] — secondary left, primary right |
| Stripe | [Sign In] [Start now →] — secondary left, primary right |
| Google | [Sign In] [Create account] — same |
| Notion | [Log in] [Get Notion free] — same |

Verdict: secondary LEFT, primary RIGHT is the standard in western LTR contexts.

### Visual weight

- **Primary** — filled background, brand color, shadow
- **Secondary** — ghost/outline, no fill, subtle border
- **Utility** — icon-only or minimal text, neutral color

Primary and secondary must not share weight. If both have filled backgrounds, the user sees no hierarchy.

### Spacing

- Between button groups: 1.5 rem (24 px) minimum
- Between buttons in the same group: 0.5-0.75 rem (8-12 px)
- Touch targets: 44 × 44 px minimum on mobile (WCAG 2.2)

### Labels

- Conventional labels: "Sign Up" (not "Get Started"), "Sign In" (not "Login")
- Say exactly what happens: "Delete Account" (not "Proceed")
- Verb-first for actions: "Create Project", "Send Message"
- Destructive buttons name the consequence: "Delete 'Q4 Report'" (not "Confirm")

## Minimal example

Modal action row done right:

```html
<div class="modal-actions" style="display:flex; gap:12px; justify-content:flex-end;">
  <button class="btn btn-ghost">Cancel</button>
  <button class="btn btn-primary">Delete Project</button>
</div>
<!-- Secondary (Cancel) left, primary (Delete Project) right -->
<!-- Primary is filled + destructive-color; secondary is ghost -->
<!-- 12 px between; 24 px to any adjacent group -->
<!-- Label names the specific consequence -->
```

*Attributed to the ux-evaluator skill + balsamiq-button-principles — `SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md`.*

## Gotchas

- RTL languages (Arabic, Hebrew) invert the primary-right rule. Evaluate at the layout's logical-direction level, not visual direction.
- Touch targets of 44 px minimum only applies to touch surfaces. Desktop-only components can use smaller hit areas but must still have 24 px+ clickable regions for accessibility.
- Ghost + filled pair is the cleanest visual-weight contrast. Ghost + outline + filled three-way mixes can work but require careful color and spacing tuning.
- "Get Started" is warmer than "Sign Up" but less specific. Both are acceptable for a top-of-funnel CTA; "Sign Up" wins for decision-stage.

## Cross-references

- `TECH-uxeval-3-dimension-framework.md`
- `TECH-uxeval-navigation-conventions.md`, `TECH-uxeval-form-conventions.md`
- `balsamiq-button-principles.md`
- `../SKILL.md`
- `../../amw-ux-designer/references/TECH-ux-rule-interaction.md` — microcopy rule
