## Table of Contents

- [Section 10 — Naming Convention (Page > Section > Block > Element)](#section-10-naming-convention-page-section-block-element)
- [Section 11 — Page Specifications](#section-11-page-specifications)
- [Section 12 — Composite Components](#section-12-composite-components)
- [Section 13 — Token Mapping](#section-13-token-mapping)
- [Section 14 — i18n References](#section-14-i18n-references)
- [When to use these extensions](#when-to-use-these-extensions)
- [Cross-references](#cross-references)


# Extension sections 10-14 — optional Variant 2 enhancements

**Source:** `docs_dev/extracted/google-labs/gen-design-spec-1-001-design-md-schema/`. Original docs are Korean-only; this file synthesizes the structural intent in English. The plugin treats these as **optional** extensions to Variant 2 (community 9-section) format. They are NOT part of Variant 1 (canonical Google `@google/design.md`); when converting to Variant 1 they are dropped or moved to prose.

These extensions exist because the 9 base sections of Variant 2 cover only visual rules (look-and-feel). They lack:
- "What to build" (page-level specs, requirements)
- Component composition (LoginPage as a unit, not just Button + Input)
- Token-to-Tailwind / token-to-CSS-var mapping table
- i18n string-resource mapping

Extensions 10-14 fill those gaps. Use them only when the user explicitly asks for page-level specs, composite component definitions, multi-CSS-framework token mapping, or i18n integration.

---

## Section 10 — Naming Convention (Page > Section > Block > Element)

**Purpose:** Provide a tool-neutral hierarchical naming for everything in the design. The same name is used in Figma layers, in React components, and in requirements docs.

**Pattern:**
```
Page > Section > Block > Element

LoginPage > HeroSection > CredentialBlock > EmailInput
DashboardPage > StatsSection > MetricCardBlock > NumberDisplayElement
```

**Author rules:**
- All four levels are mandatory for any UI element referenced from requirements.
- Names are PascalCase across all levels.
- A "Page" is a top-level route. A "Section" is a major content region. A "Block" is a reusable composite (Card, Form). An "Element" is a leaf primitive (Input, Button, Label).

**Section template:**
```markdown
## 10. Naming Convention

All UI elements follow `Page > Section > Block > Element` four-level naming.

### Pages
| Page name | Route | Purpose |
|---|---|---|
| LoginPage | /login | User authentication |
| DashboardPage | / | Authenticated home |
| ProfilePage | /profile | User settings |

### Sections (per Page)
| Page | Section | Purpose |
|---|---|---|
| LoginPage | HeroSection | Brand mark + headline |
| LoginPage | CredentialSection | Email + password form |
| DashboardPage | StatsSection | Top-line KPIs |

### Blocks (composite components)
| Block | Used in | Composes |
|---|---|---|
| CredentialBlock | LoginPage > CredentialSection | EmailInput + PasswordInput + RememberCheckbox |
| StatCardBlock | DashboardPage > StatsSection | NumberDisplay + Label + TrendArrow |

### Elements (primitives)
| Element | Type | Component |
|---|---|---|
| EmailInput | input[type=email] | Input.tsx |
| PasswordInput | input[type=password] | Input.tsx |
| RememberCheckbox | input[type=checkbox] | Checkbox.tsx |
```

---

## Section 11 — Page Specifications

**Purpose:** For each Page named in Section 10, declare its layout variant, requirements, and supported state set.

**Section template:**
```markdown
## 11. Page Specifications

### LoginPage

- **Route:** `/login`
- **Variants:** `page` (default), `modal` (used in onboarding overlay), `bottom-sheet` (mobile)
- **Layout:** centered single-column, max-width 480px, vertical rhythm 8px multiples
- **Required sections (in order):** HeroSection, CredentialSection, SocialAuthSection (optional), FooterLinks
- **States:** idle, loading (during auth), error (auth failed), success (redirect)
- **Token slots:**
  - `BrandHeader.logo` — replaceable per project
  - `SocialAuthSection.providers` — list slot (empty = section hidden)
- **i18n keys:**
  - `login.title` — "Sign in"
  - `login.email-label` — "Email address"
  - `login.password-label` — "Password"
  - `login.submit` — "Sign in"
  - `login.forgot` — "Forgot password?"
  - `login.signup-prompt` — "Don't have an account?"

### DashboardPage
…
```

**Variants** (page / modal / bottom-sheet) are how the same Page Template is reused across project contexts. The plugin's Variant 1 spec has no equivalent — page-level reuse is outside its scope.

---

## Section 12 — Composite Components

**Purpose:** Declare composite components that are reusable units larger than primitives but smaller than full Pages. These are the "Block" level from Section 10.

**Section template:**
```markdown
## 12. Composite Components

### LoginForm

Composes: `EmailInput + PasswordInput + RememberCheckbox + SubmitButton`.

**Props:**
- `onSubmit(credentials)` — required
- `error: string | null` — banner message
- `loading: boolean` — disables submit, shows spinner
- `rememberDefault: boolean` — initial value for remember checkbox

**Layout:**
- Stacked vertical, 16px gap between fields
- Submit button full-width, primary variant
- Error banner above submit, danger variant

**ARIA:**
- `<form aria-labelledby="login-title">`
- Error: `role="alert" aria-live="assertive"`

### SignupForm
…

### StatCard
…
```

This section gives the AI agent enough to render the composite without re-deriving structure from primitives every time.

---

## Section 13 — Token Mapping

**Purpose:** Single table mapping each design token across the four namespaces it appears in: descriptive name, hex/value, CSS custom property, Tailwind class.

**Section template:**
```markdown
## 13. Token Mapping

### Colors

| Design name | Hex | CSS variable | Tailwind class |
|---|---|---|---|
| Primary | #1A1C1E | --primary | bg-primary, text-primary |
| Secondary | #6C7278 | --secondary | bg-secondary, text-secondary |
| Tertiary | #B8422E | --tertiary | bg-tertiary, text-tertiary |
| Surface | #F7F5F2 | --surface | bg-surface |
| Text Primary | #1A1C1E | --text-primary | text-text-primary |
| Border Subtle | #E5E2DD | --border-subtle | border-border-subtle |

### Typography

| Design name | Family | Size | Weight | Line height | CSS class | Tailwind |
|---|---|---|---|---|---|---|
| h1 | Public Sans | 48px | 600 | 1.1 | .text-h1 | text-5xl font-semibold leading-tight |
| body-md | Public Sans | 16px | 400 | 1.6 | .text-body | text-base font-normal leading-relaxed |

### Spacing

| Design name | px | rem | CSS variable | Tailwind |
|---|---|---|---|---|
| xs | 4px | 0.25rem | --space-xs | p-1, m-1 |
| sm | 8px | 0.5rem | --space-sm | p-2, m-2 |
| md | 16px | 1rem | --space-md | p-4, m-4 |
| lg | 32px | 2rem | --space-lg | p-8, m-8 |
| xl | 64px | 4rem | --space-xl | p-16, m-16 |

### Rounded

| Design name | px | CSS variable | Tailwind |
|---|---|---|---|
| sm | 4px | --rounded-sm | rounded-sm |
| md | 8px | --rounded-md | rounded-md |
| lg | 12px | --rounded-lg | rounded-lg |
| full | 9999px | --rounded-full | rounded-full |
```

This section is hugely valuable for AI agents that need to translate between three or four token namespaces. Without it, agents reverse-engineer the mapping every time, often inconsistently.

---

## Section 14 — i18n References

**Purpose:** Declare every user-facing string in the design with stable i18n keys, so locale-specific copy can be dropped in without touching the design system.

**Section template:**
```markdown
## 14. i18n References

### String resource format

All user-facing strings live in `i18n/<locale>.json`. Keys use dotted scope: `<page>.<element>` or `<page>.<element>.<state>`.

### Locale-neutral key list

| Key | English (default) | Notes |
|---|---|---|
| `login.title` | Sign in | Hero headline |
| `login.email-label` | Email address | Field label |
| `login.email-placeholder` | name@example.com | Field placeholder |
| `login.password-label` | Password | Field label |
| `login.submit` | Sign in | Primary CTA |
| `login.error.invalid-credentials` | The email or password is incorrect. | Error banner copy |
| `login.error.network` | Could not reach the server. Try again. | Network failure |
| `dashboard.welcome` | Welcome back, {{name}} | Interpolated |
| `dashboard.empty-state.title` | Nothing here yet | Empty state |
| `dashboard.empty-state.cta` | Create your first item | Empty state CTA |

### Pluralization

For locales requiring plural rules (Russian, Arabic, Polish), use ICU MessageFormat:

```
"item.count": "{count, plural, =0 {No items} one {# item} other {# items}}"
```

### RTL flip

Locales `ar`, `he`, `fa`, `ur`: design respects bidi via CSS logical properties (`margin-inline-start`, `text-align: start`). No string-level RTL marker needed.

### Locale list (project-specific)

- `en` — default (this file)
- `fr` — French (Canadian + European share keys)
- `ja` — Japanese (CJK rules per `TECH-cjk-localization.md`)
- `ko` — Korean
- `zh-CN` — Simplified Chinese
- `zh-TW` — Traditional Chinese
- `ar` — Arabic (RTL)
```

---

## When to use these extensions

The plugin emits Sections 10-14 only on explicit request:

| User intent | Extensions |
|---|---|
| "Just give me a DESIGN.md" | 1-9 only |
| "I need page-level specs too" | + 10, 11 |
| "I want LoginPage as a reusable component" | + 10, 11, 12 |
| "I need to map tokens to Tailwind classes" | + 13 |
| "Add i18n key support" | + 14 |
| "Full extended format" | 1-14 |

Default behavior: 1-9 only (Variant 2 base) or Variant 1 (8 sections + frontmatter). The agent does NOT proactively offer 10-14 unless triggered.

---

## Cross-references

- [canonical-spec-google-alpha](./canonical-spec-google-alpha.md) — Variant 1 (no extension support)
  > File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Top-level fields · Type definitions · Component property tokens (spec.md L312-L319) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Section content guidance · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
- [community-9-section-spec](./community-9-section-spec.md) — Variant 2 base
  > Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
- [community-9-section-template](./community-9-section-template.md) — Variant 2 skeleton with optional 10-14 placeholders
  > Optional extension sections · Validation · Cross-references
- [TECH-13-converting-variant2-to-1](./TECH-13-converting-variant2-to-1.md) — what gets dropped when extensions are present and we convert to V1
  > What it does · When to use · When NOT to use · Conversion overview · Token extraction from V2 prose · Colors · Typography · Spacing · Rounded · Components · Mermaid state diagram · Sections 8-9 merging · Information that may be lost · Inputs · Validation after conversion · Round-trip notes · Cross-references
