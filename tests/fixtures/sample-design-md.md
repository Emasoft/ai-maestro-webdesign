---
version: alpha
name: Sample Showcase Brand
description: A minimal Variant 1 DESIGN.md fixture for showcase generator tests.

colors:
  primary: "#0F4C81"
  on-primary: "#FFFFFF"
  secondary: "#FFD23F"
  on-secondary: "#1A1C1E"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  on-surface: "#1A1C1E"
  canvas: "#FAFAFA"
  ink: "#1A1C1E"
  ink-muted: "#6C7278"
  hairline: "#E5E7EB"
  success: "#1F7A3A"
  warning: "#B46E08"
  error: "#A02323"

typography:
  headline-display:
    fontFamily: Manrope
    fontSize: 56
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 36
    fontWeight: 700
    lineHeight: 1.15
  body-md:
    fontFamily: Inter
    fontSize: 16
    fontWeight: 400
    lineHeight: 1.55
  label-md:
    fontFamily: Inter
    fontSize: 13
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.04em

rounded:
  none: 0
  sm: 4
  md: 8
  lg: 12
  full: 9999

spacing:
  base: 16
  xs: 4
  sm: 8
  md: 16
  lg: 32
  xl: 64

elevation:
  none: "none"
  sm: "0 1px 2px rgba(0,0,0,0.08)"
  md: "0 4px 12px rgba(0,0,0,0.10)"
  lg: "0 12px 32px rgba(0,0,0,0.15)"

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 12
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    borderColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 12
  input-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    rounded: "{rounded.sm}"
    padding: 10
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: 20
---

# Sample Showcase Brand Design System

> Minimal fixture used to drive `tests/test_amw_design_md_showcase.py`.

## Overview

This is a fixture DESIGN.md. Tokens are real and renderable but the brand is fictional.

## Colors

- **Primary (`#0F4C81`):** Brand voltage; used for primary actions and headlines.
- **Secondary (`#FFD23F`):** Supporting accent; used sparingly for highlights.
- **Tertiary (`#B8422E`):** Limited-use destructive accent.

## Typography

- **Display & headlines:** Manrope 800/700.
- **Body:** Inter 400 at 16px.
- **Labels:** Inter 600 with letter-spacing.

## Layout

- **Base unit:** 16px
- **Spacing scale (px):** 4, 8, 16, 32, 64

## Elevation & Depth

Four tiers from flat to elevated.

## Shapes

Friendly soft radii on the 4px grid.

## Components

- **Button (primary):** Used for the single most important action per screen.
- **Card:** Internal padding follows spacing.lg.

## Do's and Don'ts

**Do:**
- Do use the primary color sparingly.
- Do maintain WCAG AA contrast.

**Don't:**
- Don't introduce colors outside this palette.
- Don't mix radius scales on a single screen.
