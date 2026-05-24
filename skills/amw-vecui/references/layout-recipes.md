# vecui — Layout recipes

> The canonical "center, align-to-side, expand-on-hover, look-at-cursor" patterns, verbatim in shape from the upstream demo (`src/App.tsx`).

## Table of Contents

- [Layout recipe](#layout-recipe)
- [Worked example](#worked-example)
- [Rotation and coordinate system](#rotation-and-coordinate-system)

## Layout recipe

The vecui mental model for "position element B relative to element A", expressed as vector arithmetic:

1. **Build the anchor rect.** `const anchor = rect(dim.div(-2), dim)` centers a box of dimension `dim` on the origin (offset origin by minus half the dimension).
2. **Walk to the target slot.** Start from `anchor.o`, then chain offsets: `.add(anchor.d.x, 0)` moves right by the anchor's width, `.add(padding, 0)` adds a gap.
3. **Center on the cross axis.** `anchor.d.sub(box.d).div(2).y` is the vertical offset that centers `box` against `anchor`; add it (use `.y` to take only the vertical component).
4. **Apply.** Spread `placed.as.styleObject()` onto the element.

Keep computed paddings/gaps on the 8pt grid (see spacing-rhythm) and feed those values into the vector offsets (`.add(padding, 0)`).

## Worked example

A centered "anchor" box with a second box aligned to its right edge, kept vertically centered, expandable on hover:

```typescript
import { vec, rect } from "vecui";

const padding = 16;

// Anchor (yellow): centered on the origin.
const anchorDim = vec({ x: 200, y: 200 });
const anchorRect = rect(anchorDim.div(-2), anchorDim);

// Aligned (pink): right of the anchor, vertically centered.
const otherRect = rect(vec(0), vec(150, 150));
const alignedRect = otherRect.setO(
  anchorRect.o
    .add(anchorRect.d.x, 0)               // move to the anchor's right edge
    .add(
      padding,                            // horizontal gap
      anchorRect.d.sub(otherRect.d).div(2).y  // vertical centering offset
    )
);

// Expand-on-hover by a fixed pixel amount, regardless of size:
const hoverExpand = vec(8, 8);
const hoveredRect = rect(
  alignedRect.o.sub(hoverExpand),         // grow toward top-left
  alignedRect.d.add(hoverExpand.mul(2))   // ...and add to both sides
);

// "Look at the cursor" rotation for a centered element:
const angleRad = vec(window.innerWidth / 2, window.innerHeight / 2)
  .lookAt(vec(mouseX, mouseY));
```

## Rotation and coordinate system

`rotRad`/`rotDeg` rotate counterclockwise in standard math orientation; `lookAt` assumes a left-handed system and offsets by `front` (`"x" | "y" | "-x" | "-y"`, default `"x"`). If a rotation looks mirrored, check the y-axis direction (screen y grows downward) and the `front` argument before assuming a bug.

vecui is math only — it has no animation loop, no `requestAnimationFrame`, no time concept. Drive its values from the plugin animations starter or the host framework's value layer.
