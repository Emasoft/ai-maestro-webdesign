---
name: TECH-wireframe-html-mobile-first
category: ux-flow-wireframe
source: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/assets/wireframe-template.html
---

# TECH-wireframe-html-mobile-first

## What it does

Produces **self-contained mobile-first HTML wireframes** — one `.html`
file per unique screen, 375px viewport, inline CSS only, grayscale
aesthetic with dashed borders. Every wireframe is clickable (via
`<a href>` navigation) and works in any browser with zero
dependencies.

## When to use

- **Phase 3 of the `ux-flows` workflow** — mandatory for every
  invocation.
- **Whenever a user needs a clickable prototype** to validate navigation
  flow before committing to visual design.
- **Never replace with a real UI mockup** at this stage — the
  deliberately unfinished wireframe aesthetic is the point; it keeps
  stakeholders focused on flow, not colours.

## How it works

### Scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SCREEN_NAME — Wireframe</title>
  <style>
    /* see the template.html shipped with this skill */
  </style>
</head>
<body>
  <div class="wf-screen">
    <!-- header / nav / content / tab-bar / footer -->
  </div>
</body>
</html>
```

### Aesthetic tokens

| Property | Value | Purpose |
|---|---|---|
| Screen width | `375px` | Mobile-first |
| Background | `#f5f5f5` | Neutral gray |
| Container background | `#e0e0e0` | Slightly darker |
| Borders | `1-2px dashed #ccc` | Wireframe-y, unfinished |
| Text | `#444` primary, `#666` secondary, `#888` placeholder | Grayscale |
| Buttons (filled) | `#ccc` background, dashed `#999` border | "This is a button" |
| Buttons (outline) | transparent, dashed `#999` border | Secondary action |
| Cards | `#fff` background, dashed `#ccc` border | Content container |

### Utility classes

| Class | Use |
|---|---|
| `.wf-screen` | Top-level screen container |
| `.wf-header` | Top header bar with title |
| `.wf-nav` | Navigation bar (often with back button) |
| `.wf-content` | Main content area |
| `.wf-input` | Text input field |
| `.wf-button` | Primary filled button |
| `.wf-button-secondary` | Outline button |
| `.wf-card` | Content card |
| `.wf-list-item` | List row |
| `.wf-tab-bar` | Bottom tab bar |
| `.wf-tab-item` | Individual tab |
| `.wf-icon-placeholder` | Square icon placeholder (24×24 or 48×48) |
| `.wf-text-placeholder` | Gray text block (`.short`, `.medium`, `.full` widths) |
| `.wf-divider` | Dashed horizontal separator |
| `.wf-spacer` | 16px vertical spacing |
| `.wf-label` / `.wf-title` / `.wf-subtitle` | Typography |
| `.wf-link` | Navigation wrapper (see
  [TECH-clickable-prototype-navigation](TECH-clickable-prototype-navigation.md)) |
| `.wf-back` | Back button text style |
| `.wf-footer` | Bottom meta footer (screen name + use-case ID) |

## Minimal example

Login screen wireframe:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login — Wireframe</title>
  <style> /* wf-* classes from the template */ </style>
</head>
<body>
  <div class="wf-screen">
    <div class="wf-header">Login</div>

    <div class="wf-content">
      <div class="wf-title">Welcome back</div>
      <div class="wf-subtitle">Sign in to continue</div>
      <div class="wf-spacer"></div>

      <input class="wf-input" placeholder="Email"/>
      <input class="wf-input" type="password" placeholder="Password"/>

      <a href="home.html" class="wf-link">
        <div class="wf-button">Sign In</div>
      </a>

      <a href="forgot.html" class="wf-link">
        <div class="wf-button-secondary">Forgot password?</div>
      </a>

      <div class="wf-divider"></div>

      <a href="register.html" class="wf-link">
        <div class="wf-button-secondary">Create account</div>
      </a>
    </div>

    <div class="wf-footer">
      login.html — UC-002
    </div>
  </div>
</body>
</html>
```

## Gotchas

- **Self-contained means inline CSS.** No external stylesheet, no
  Google Fonts, no CDN. The file must render exactly the same when
  emailed as an attachment.
- **No JavaScript.** Navigation is pure HTML `<a href>`. No onclick, no
  form submits, no JS state. See
  [TECH-clickable-prototype-navigation](TECH-clickable-prototype-navigation.md).
- **Mobile-first, not desktop.** 375px is the target; if the user asks
  for desktop, that is a signal to escalate to `ui-ux-pro-max` or
  `diagram-editorial` for a real layout.
- **Grayscale only.** No brand colours, no accent hues. The wireframe
  must look like a wireframe; it's the visual permission for
  stakeholders to say "the flow is wrong" without getting distracted
  by "the blue is wrong".
- **Footer carries the screen name + UC-ID.** When a stakeholder opens
  `login.html` in isolation, they need to know which use case it
  belongs to. `login.html — UC-002` in the footer is the convention.

## Cross-references

- `../SKILL.md` — Phase 3 of the workflow
- `../assets/wireframe-template.html` — the shipped template
- [TECH-clickable-prototype-navigation](TECH-clickable-prototype-navigation.md) — inter-screen linking rules
- [TECH-no-dead-end-screens](TECH-no-dead-end-screens.md) — the "every screen has an outgoing
  link" rule
- [TECH-wireframe-index-inventory](TECH-wireframe-index-inventory.md) — the `INDEX.md` inventory shape
