# Non-negotiable rules

## Table of Contents

- [Rules 1–7](#rules)
- [Cross-references](#cross-references)

## Rules

These rules are enforced before delivery. Any FAIL triggers a remediation loop.

1. **Never fabricate data.** Every stat, figure, or fact must come from the user input. No plausible-sounding invented numbers.

2. **No generic display fonts.** Inter, Roboto, Arial, Helvetica, Plus Jakarta Sans, Syne, Outfit, Space Grotesk, and Rajdhani are banned as the display/heading font (Rajdhani is a rounded-geometric grotesk that reads as exactly the SaaS-display font the banned list filters out). Use Bebas Neue, Teko, Orbitron, Bungee, or Press Start 2P.

3. **No emojis as icons.** Phosphor Icons only: `<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>`.

4. **Brand color first.** If the user supplies a hex or logo, derive the palette from it — do not default to generic tech blue/purple.

5. **Dark mode is the default.** Near-black `#060606`–`#090909`. Words like "whitepaper", "report", or "institutional" do NOT override dark mode.

6. **User-supplied real assets only.** No AI-generated images, no invented testimonials, no stock placeholders. If the user references a game / NFT project, expect to incorporate their imagery.

7. **Footer by default.** 60% of real pieces have a small attribution/logo strip at the bottom. Omit only when the user explicitly says no footer.

## Cross-references

- [SKILL](../SKILL.md) — parent skill (amw-infographics)
- [_design-dna](_design-dna.md) — full design DNA
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — orchestrator's broader anti-slop checklist
