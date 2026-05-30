# TECH — Email Design Patterns

Email is not a webpage. The rendering surface is 30+ inconsistent clients (Gmail web, Gmail iOS, Outlook 2007–2021, Apple Mail, Yahoo, Spark, Superhuman, Outlook web), most of which strip `<style>` tags, ignore flexbox, drop external CSS, and refuse modern selectors. This file documents the patterns `amw-email-designer-agent` applies before emitting MJML or hand-rolled email HTML.

Mapping note: T-111..T-130 are primarily web-design entries. The email-specific items that touch this catalog are (a) the token / contrast doctrine (which applies because email also has dark mode), (b) the layout-diversity rule (T-124) inverted for email (email rejects layout diversity — every section should look structurally similar so clients render consistently), and (c) the announce-plan-before-coding cue (T-119) which the email-designer applies before writing MJML. The rest of the email content here is clean-room writeup of public email-client behavior; no GPL or unknown-license source.

Provenance: clean-room; based on publicly documented email-client quirks (Litmus, EmailOnAcid, MJML docs, Apple Mail release notes).

---

## Tokens

Email has its own token block — distinct from the web token block because the constraint set differs.

```html
<!-- Email tokens live inside a <style> block in the <head> AND get inlined into every element that uses them.
     Clients that strip <style> still render correctly because the inline style takes over. -->
<style>
  :root {
    --email-bg: #ffffff;
    --email-bg-dark: #1a1a1a;          /* dark-mode body bg */
    --email-text: #1f1f1f;
    --email-text-dark: #e8e8e8;
    --email-muted: #5f5f5f;
    --email-muted-dark: #a8a8a8;
    --email-link: #0066cc;             /* must give ≥ 4.5:1 on both bg variants */
    --email-link-dark: #6cb6ff;
    --email-border: #e0e0e0;
    --email-border-dark: #3a3a3a;
    --email-button-bg: #0066cc;
    --email-button-text: #ffffff;
    --email-max-width: 600px;          /* mobile-safe max; never exceed */
    --email-gutter: 24px;              /* outer table padding */
    --email-section-gap: 32px;
  }
</style>
```

**Hard invariants:**
1. Container max-width 600 px. Wider tables clip on small mobile clients (Apple Mail on iPhone SE, Outlook Web in a side pane).
2. Every visual style is inlined onto its element. `<style>` blocks are reference-only, for clients that DO support them (Apple Mail, Gmail web). Clients that strip `<style>` (Outlook 2007–2021) still render because the inline style is present.
3. No external CSS files. No `<link>` tags. No web fonts loaded via `@import`.
4. Web fonts via `<link>` in the head are a soft hint — assume they never load. The fallback stack must be readable.
5. No JavaScript. Every interactive client strips `<script>`.
6. No flexbox, no grid, no `position`. Layout is `<table>` + `align` + `valign` + `width`.

---

## Pattern 1 — Table layout, single-column responsive

The canonical email skeleton is nested tables with `role="presentation"` to keep AT from reading them as data tables.

```html
<!-- Outer table — sets body background -->
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f4f4f4;">
  <tr>
    <td align="center" valign="top" style="padding:24px 0;">
      <!-- Inner table — sets content max-width -->
      <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="max-width:600px; width:100%; background:#ffffff;">
        <tr>
          <td style="padding:32px 24px;">
            <!-- Content blocks here, each its own nested table for spacing -->
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

Why `width="600"` AND `style="max-width:600px; width:100%"`: Outlook reads the HTML attribute; modern clients read the CSS. On mobile, the percentage-width override lets the inner table shrink to the viewport.

Multi-column layouts (e.g., a 2-up product row) use `<table>` with two `<td>` cells, AND a `<!--[if mso]>` Outlook-conditional that forces single column on Outlook (which renders multi-column tables inconsistently when the parent table is set to `width:100%`).

```html
<!--[if mso]>
<table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0"><tr><td>
<![endif]-->
<!--[if !mso]><!-->
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"><tr>
  <td width="50%" valign="top">column 1</td>
  <td width="50%" valign="top">column 2</td>
</tr></table>
<!--<![endif]-->
<!--[if mso]>
</td></tr></table>
<![endif]-->
```

MJML's `<mj-section>` + `<mj-column>` generates this dual-path table soup automatically. Hand-rolling it is error-prone; prefer MJML for any non-trivial layout.

---

## Pattern 2 — Dark mode via media query

Email dark mode has two distinct mechanisms — both required for coverage.

**Mechanism A: `prefers-color-scheme` media query** (Apple Mail, Gmail web, Outlook 365 Mac):

```html
<style>
  @media (prefers-color-scheme: dark) {
    .email-bg          { background-color: #1a1a1a !important; }
    .email-text        { color: #e8e8e8 !important; }
    .email-muted       { color: #a8a8a8 !important; }
    .email-link        { color: #6cb6ff !important; }
    .email-border      { border-color: #3a3a3a !important; }
    .email-img-invert  { filter: invert(1) hue-rotate(180deg); } /* dark-mode logo swap */
  }
</style>
```

Every selector uses `!important` to override the inline styles in dark-mode clients. The classes (`.email-bg`, `.email-text`, etc.) MUST also be attached to the elements alongside the inline style.

**Mechanism B: `[data-ostype="dark"]`** (Outlook iOS/Android dark mode):

Outlook's mobile clients apply their own automatic color inversion regardless of the prefers-color-scheme media query. The mitigation is the `meta` color-scheme tag:

```html
<head>
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
</head>
```

This tells Outlook mobile to respect the embedded dark-mode rules instead of force-inverting.

**Hard rules:**
1. Test contrast in BOTH modes. The same `--email-link` token gives 7.3:1 on `#ffffff` (light) and 5.2:1 on `#1a1a1a` (dark) — both pass; many handpicked colors pass only one.
2. Logos: provide a dark-mode swap. Either via `filter: invert(1) hue-rotate(180deg)` on a single asset (works for monochromatic marks) or via a `.email-logo-light` / `.email-logo-dark` pair with `display: none` toggled by the media query.
3. Buttons keep brand color in both modes — do NOT invert button backgrounds, that makes the CTA recede.

---

## Pattern 3 — Plain-text fallback discipline

Every multipart email has a `text/plain` companion. Spam filters score messages without a plain-text part more aggressively; some users force plain-text rendering for accessibility or speed.

Plain-text generation rules:
1. Mirror the structural order of the HTML (subject → preheader → greeting → primary message → CTA URL exposed as bare text → secondary content → footer).
2. CTA links: emit the full URL on its own line below the link label. `Place your order: https://example.com/order/abc-123` not just `Place your order` (the link target is invisible in plain text).
3. Tracking pixels and image-only content: omit. Plain text has no images.
4. Compliance footer (unsubscribe URL, physical address): emit verbatim. Legal-expert's text is preserved character-for-character.
5. Width target: 72 characters per line for legacy mail-client readability.

Plain-text generation can be delegated (per `amw-email-designer-agent.md` § 10) but the structural mirror requirement is a hard invariant — the Task that produces plain text receives the HTML content map, not freedom to re-order.

---

## Pattern 4 — Transactional vs marketing voice

The two email categories have different rendering, copy, and compliance constraints. Confusing them is the most common email-design mistake.

| Aspect | Transactional | Marketing |
|---|---|---|
| Trigger | User action (purchase, signup, password reset, alert) | Scheduled send to a list |
| Primary purpose | Confirm / inform | Persuade / convert |
| Voice | Direct, factual, brief | Warmer, brand-led, longer |
| Subject line | Specific to the action ("Order #4521 confirmed") | Marketing copy ("New collection just dropped") |
| Layout | Minimal, single dominant content block, often no hero image | Multi-section, hero image, multiple CTAs allowed |
| Unsubscribe link | NOT required (US CAN-SPAM exemption for transactional content), but include preference link | REQUIRED (CAN-SPAM § 5 + CASL § 11) — visible, functioning, one-click |
| Frequency | One per triggering event | Capped by user preferences |
| Personalization | High (order details, name, dynamic data) | Medium (name, segment-based content) |
| Tracking pixels | Discouraged (transactional should be trust-first) | Standard |
| Compliance footer | Sender identity + minimal | Full: sender ID + physical address + unsubscribe + CASL business identification |
| Image weight | Light (no decorative images; one logo) | Heavy (allowed; with `alt` text mandatory) |
| Dark mode | Mandatory | Mandatory |
| Reply-to | Often a real inbox (no-reply only when necessary) | Marketing inbox |

The boundary matters legally: a marketing message wrapped in a transactional template (e.g., a "your order is ready" email that includes a sale banner) loses its CAN-SPAM exemption and becomes subject to the full marketing-compliance set.

---

## Pattern 5 — Compliance footer structural requirements

The footer is the highest-litigation surface in an email. Structural requirements (US):

- Physical postal address of the sender — full street address, not P.O. box only.
- Unsubscribe mechanism — functioning, one-click for marketing emails; honored within 10 business days.
- Sender identity — clear "from" name; no spoofed domains.
- For CASL (Canada): business name + contact info; consent confirmation language.
- For GDPR (EU recipients): no consent-required marketing without proof of opt-in; for transactional, lawful basis statement may be required by some interpretations.

The agent's role is to inject the footer **structurally**. Content comes from legal-expert (T-118-style fork-discipline applies: the agent does not rewrite legal-expert's text).

Per the agent's Conflict Pattern 5: if legal-expert provides the footer as HTML with CSS classes, inline all CSS (class-based styling is stripped by Gmail). Preserve text and link structure exactly. If inlining cannot preserve the visual appearance, escalate.

---

## Pattern 6 — Image and asset handling

- Every `<img>` has `alt` text. Decorative images get `alt=""` (empty, NOT missing). Content images get descriptive alt.
- Images host on a CDN with permanent URLs — never relative paths, never tracking-cookie-protected paths.
- `width` AND `height` attributes are explicit on every image (prevents reflow when images load progressively).
- File format: JPEG for photographs, PNG for logos with transparency, SVG NOT supported (most clients refuse to render inline SVG and many strip linked SVG).
- Image-blocked rendering: every email must remain readable with all images blocked. CTA buttons must be HTML+CSS, not background-image. Section headers must be HTML text, not image-rendered text (Conflict Pattern 4).
- Animated GIF: first frame must communicate the key message. Outlook 2007–2010 shows the first frame only.

---

## Pattern 7 — Preheader (preview text)

The hidden text snippet that appears in the inbox list below the subject line. If absent, clients fill it with the first visible text in the email — often "View in browser" or `[unsubscribe]` if those appear near the top.

```html
<!-- First child of <body>, hidden visually, captured by inbox preview parsers -->
<div style="display:none; overflow:hidden; line-height:1; max-height:0; max-width:0; opacity:0;">
  Your order #4521 has shipped — tracking included.
</div>
<div style="display:none; overflow:hidden; line-height:1; max-height:0; max-width:0; opacity:0;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
```

The second hidden div is "preheader padding" — non-breaking spaces and zero-width non-joiners that push any post-preheader text out of the inbox preview window. Without it, the preview becomes "Your order #4521 has shipped — tracking included. View in browser | Unsubscribe".

Preheader length target: 80–110 characters. Mobile clients show ~30; desktop clients show ~110.

---

## Breaks-if

- Inline styles missing. `<style>`-only rules vanish in Outlook 2007–2021, Yahoo, and many mobile-app clients. The email renders as unstyled HTML.
- Container exceeds 600 px. Mobile clients add horizontal scroll or zoom out, destroying readability.
- Dark-mode rules use class selectors but the classes are not attached to the elements. The dark-mode swap silently fails.
- `<button>` element used for CTA. Many clients render `<button>` inconsistently; use `<a>` with table-cell padding and inline `display: inline-block`.
- Web font is loaded without a fallback stack matching its size. When the web font fails (a common case), the fallback font reflows the layout.
- Compliance footer in `<style>` only. Stripped by Gmail; the email becomes legally non-compliant for that segment of recipients.
- Image with no `alt` attribute. Screen readers announce "image" or skip silently. WCAG 1.1.1 violation; spam filter penalty.
- Plain-text fallback is absent or auto-generated from HTML by the mailer (without structural mirror). Plain-text users see broken content; spam scores rise.
- Logo asset is a single light-mode PNG with no dark-mode swap and no inversion filter. Dark-mode users see a black-on-black mark or an aggressive auto-inverted brand-color shift.
- Marketing email lacks a functioning unsubscribe URL. Per agent's Pattern 2: this is a `blocking_issues` stop — never emit.
- CTA uses a relative URL. Per agent's Pattern 3: also a `blocking_issues` stop.

---

## Component examples

### Example A — Transactional order confirmation skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>Order #4521 confirmed</title>
  <style>
    body { margin: 0; padding: 0; background: #f4f4f4; }
    @media (prefers-color-scheme: dark) {
      .email-bg     { background-color: #1a1a1a !important; }
      .email-card   { background-color: #2a2a2a !important; }
      .email-text   { color: #e8e8e8 !important; }
      .email-muted  { color: #a8a8a8 !important; }
    }
  </style>
</head>
<body>
  <div style="display:none; overflow:hidden; line-height:1; max-height:0; max-width:0; opacity:0;">Order #4521 confirmed — ships Tuesday.</div>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" class="email-bg" style="background:#f4f4f4;">
    <tr><td align="center" style="padding:24px 0;">
      <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" class="email-card" style="max-width:600px; width:100%; background:#ffffff;">
        <tr><td style="padding:32px 24px;">
          <h1 class="email-text" style="margin:0 0 16px; font:600 24px/1.3 -apple-system,BlinkMacSystemFont,sans-serif; color:#1f1f1f;">Order confirmed</h1>
          <p class="email-text" style="margin:0 0 16px; font:400 16px/1.5 -apple-system,sans-serif; color:#1f1f1f;">Thanks, Sam. Your order #4521 ships Tuesday.</p>
          <p class="email-muted" style="margin:0 0 24px; font:400 14px/1.5 -apple-system,sans-serif; color:#5f5f5f;">Tracking: <a href="https://example.com/track/4521" style="color:#0066cc;">https://example.com/track/4521</a></p>
          <table role="presentation" cellspacing="0" cellpadding="0" border="0"><tr><td style="border-radius:6px; background:#0066cc;">
            <a href="https://example.com/order/4521" style="display:inline-block; padding:12px 24px; font:600 16px/1 -apple-system,sans-serif; color:#ffffff; text-decoration:none;">View order details</a>
          </td></tr></table>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
```

Plain-text companion:

```
Order confirmed

Thanks, Sam. Your order #4521 ships Tuesday.

Tracking:
https://example.com/track/4521

View order details:
https://example.com/order/4521

---
Example Co., 123 Main St, San Francisco CA 94102
Manage preferences: https://example.com/email-preferences
```

### Example B — Marketing newsletter with multi-section layout (MJML preferred path)

```xml
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="-apple-system, BlinkMacSystemFont, sans-serif" />
      <mj-text font-size="16px" line-height="1.5" color="#1f1f1f" />
    </mj-attributes>
    <mj-style>
      @media (prefers-color-scheme: dark) {
        .email-bg     { background-color: #1a1a1a !important; }
        .email-card   { background-color: #2a2a2a !important; }
        .email-text   { color: #e8e8e8 !important; }
      }
    </mj-style>
  </mj-head>
  <mj-body width="600px" background-color="#f4f4f4" css-class="email-bg">
    <mj-section background-color="#ffffff" css-class="email-card">
      <mj-column>
        <mj-image src="https://example.com/hero.jpg" alt="Spring collection — three garments on a bench" width="552px" />
        <mj-text css-class="email-text" font-size="28px" font-weight="600">Spring collection just dropped</mj-text>
        <mj-text css-class="email-text">Three new pieces. Crafted for daily wear.</mj-text>
        <mj-button background-color="#0066cc" color="#ffffff" href="https://example.com/spring?utm_source=email&utm_medium=newsletter">Shop the collection</mj-button>
      </mj-column>
    </mj-section>
    <mj-section background-color="#ffffff" css-class="email-card">
      <mj-column width="50%">
        <mj-image src="https://example.com/p1.jpg" alt="Linen shirt" />
        <mj-text css-class="email-text" font-weight="600">Linen shirt</mj-text>
        <mj-text css-class="email-text">$89</mj-text>
      </mj-column>
      <mj-column width="50%">
        <mj-image src="https://example.com/p2.jpg" alt="Canvas tote" />
        <mj-text css-class="email-text" font-weight="600">Canvas tote</mj-text>
        <mj-text css-class="email-text">$45</mj-text>
      </mj-column>
    </mj-section>
    <!-- Compliance footer (text and structure provided verbatim by legal-expert) -->
    <mj-section background-color="#ffffff" css-class="email-card">
      <mj-column>
        <mj-text font-size="12px" color="#5f5f5f">Example Co., 123 Main St, San Francisco CA 94102 · <a href="https://example.com/unsubscribe?u=ABC123" style="color:#5f5f5f;">Unsubscribe</a> · <a href="https://example.com/preferences?u=ABC123" style="color:#5f5f5f;">Manage preferences</a></mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

MJML compiles this to ~400 lines of nested-table HTML with the Outlook conditionals, dark-mode media queries, and inline styles already correctly applied. Use `bin/amw-mjml-render.sh` to compile.

---

## Cross-references

- Color contrast (light + dark): `skills/amw-design-principles/color-system.md` § II — WCAG AA on both background variants.
- Form-error patterns in email contexts (e.g., feedback email with reply CTA): `TECH-form-error-recovery.md` — applies only to the destination web page, not the email itself (email has no JS).
- Microinteractions in email: NONE — email has no JS and animations are unreliable across clients. The `TECH-microinteractions-catalog.md` set is web-only.
- AI-slop email rules: `skills/amw-design-principles/ai-slop-avoid.md` § IV (content and copy) — avoid corporate marketing-speak; § V (interaction and motion) — no animated GIF except where genuinely informative.
- MJML compile path: `bin/amw-mjml-render.sh`.
- The agent's full conflict resolution patterns: `agents/amw-email-designer-agent.md` § 11.
