---
version: alpha
name: Aurora Spa Brand
description: A clean Variant 1 DESIGN.md fixture that should validate as PASS.

colors:
  primary: "#1A2A2E"
  on-primary: "#F5F2EC"
  secondary: "#8EA9B0"
  surface: "#FFFFFF"
  ink: "#1A1C1E"
  hairline: "#E5E7EB"
  success: "#1F7A3A"
  warning: "#B46E08"
  error: "#A02323"

typography:
  display:
    fontFamily: Cormorant Garamond
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.1
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55

rounded:
  none: 0px
  sm: 4px
  md: 8px

spacing:
  base: 16px
  sm: 8px
  md: 16px
  lg: 32px

elevation:
  none: "none"
  sm: "0 1px 2px rgba(0,0,0,0.08)"

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
---

# Aurora Spa Brand Design System

> A minimal clean fixture: every required block is present, references resolve,
> sections are in canonical order, and the `name` field is set.

## Overview

Aurora Spa is a hospitality brand fixture used to exercise the V1 validator.

## Colors

- **Primary (`#1A2A2E`):** Brand voltage for primary actions.
- **Secondary (`#8EA9B0`):** Subtle supporting accent.

## Typography

- **Display:** Cormorant Garamond 700 at 56px.
- **Body:** Inter 400 at 16px.

## Layout

- **Base unit:** 16px
- **Spacing scale:** 8, 16, 32 px.

## Elevation & Depth

Two tiers: flat and lightly elevated.

## Shapes

Soft 8px radii on most surfaces.

## Components

- **Button (primary):** Solid primary background, light ink on top.
- **Card:** Surface background with primary text.

## Do's and Don'ts

**Do:**
- Do keep contrast above WCAG-AA on every text/background pair.

**Don't:**
- Don't introduce colors outside this palette.
