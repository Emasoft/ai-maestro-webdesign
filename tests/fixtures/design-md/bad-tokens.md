---
name: Dangling Token References
description: Components and colors reference primitives that do not exist.

colors:
  primary: "#0F4C81"
  surface: "#FFFFFF"

rounded:
  md: 8px

components:
  button-primary:
    backgroundColor: "{colors.missing-primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.xxl}"
  card:
    borderColor: "{colors.nonexistent-hairline}"
---

# Dangling Token References

> Every `{...}` reference here points to a name that does NOT exist in the
> frontmatter. The validator must emit `[P0/R1] Unresolved reference` findings
> for each one and FAIL the file.

## Overview

placeholder

## Colors

placeholder

## Typography

placeholder

## Layout

placeholder

## Elevation & Depth

placeholder

## Shapes

placeholder

## Components

placeholder

## Do's and Don'ts

placeholder
