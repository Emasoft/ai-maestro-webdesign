## Table of Contents

- [The bug](#the-bug)
- [Mitigations](#mitigations)
- [Why this is not a config error](#why-this-is-not-a-config-error)

# progressive-blur — Chrome overflow + border-radius gotcha

## The bug

Setting **both** `overflow: hidden` **and** `border-radius` on an ancestor of a masked `backdrop-filter` breaks rendering in Chrome (Chromium issue [40778541](https://issues.chromium.org/issues/40778541)). The upstream demo works around it by only applying the ancestor's `border-radius` when **not** in Chrome.

## Mitigations

In order of preference:

1. Don't combine `overflow: hidden` + `border-radius` on a shared ancestor of the blur overlay.
2. Move the `border-radius` (or the clipping) to a different element than the one with `overflow: hidden`.
3. Apply rounding conditionally (skip it in Chrome) if the rounded clip is essential.

## Why this is not a config error

This is an upstream/browser limitation, not a config error — document it for the user; do not try to "fix" it inside the component. Surface it; do not patch the component.
