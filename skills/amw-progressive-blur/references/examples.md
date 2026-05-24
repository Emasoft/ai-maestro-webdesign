## Table of Contents

- [LinearBlur — sticky top fade](#linearblur--sticky-top-fade)
- [RadialBlur — center-clear spotlight](#radialblur--center-clear-spotlight)
- [Error handling](#error-handling)

# progressive-blur — worked examples and error handling

Copy-paste JSX for both components, plus the symptom → cause → fix table. See `references/api.md` for the prop reference and `references/chrome-gotcha.md` for the Chrome ancestor limitation.

## LinearBlur — sticky top fade

A sticky scroll container whose top edge progressively blurs the content scrolling under a title bar:

```jsx
import { LinearBlur } from "progressive-blur";

export function FadeTopOverlay({ children }) {
  return (
    // The blur overlay must NOT share an ancestor that has BOTH
    // overflow:hidden AND border-radius (Chromium #40778541).
    <div style={{ position: "relative", height: 360 }}>
      <div style={{ overflowY: "auto", height: "100%" }}>{children}</div>

      <LinearBlur
        side="top"                 // blur strongest at the top edge, clears downward
        strength={64}              // 64px peak blur
        steps={8}                  // 8 stacked layers — smooth ramp
        falloffPercentage={95}     // almost the whole band is gradient
        tint="rgba(0,0,0,0.08)"    // faint dark wash for legibility
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 96,              // the band height to blur
          // pointer-events:none is already set by the component — clicks pass through
        }}
        aria-hidden                // decorative overlay
      />
    </div>
  );
}
```

## RadialBlur — center-clear spotlight

For a center-clear radial spotlight blur (e.g. a hover effect over an image), swap to `RadialBlur`, drop `side`, size the overlay to cover the area, and animate its `transform: scale(...)`:

```jsx
import { RadialBlur } from "progressive-blur";

<RadialBlur
  strength={32}
  steps={8}
  falloffPercentage={85}     // solid-blur core is the inner 15% of the radius
  tint="transparent"
  style={{ position: "absolute", inset: 0, zIndex: -1 }}
/>
```

## Error handling

- **No blur appears:** the overlay has no size, is behind the content (`z-index`), or sits over a transparent area — `backdrop-filter` blurs what is **behind** the element, so there must be content beneath it. Give the overlay explicit dimensions and ensure it stacks above the blurred content.
- **Edge looks banded/stepped instead of smooth:** `steps` is too low for the band size — raise `steps` (resolution) until the banding disappears; expect higher GPU cost.
- **Whole band is blurred with no clear region (or vice-versa):** adjust `falloffPercentage`. `0` = hard/uniform blur (no gradient); `100` = the entire band is gradient. The solid-blur region is `100 - falloffPercentage`% of the band.
- **Blur fades from the wrong edge (`LinearBlur`):** set `side` to the edge where the blur should be **strongest**; the gradient always fades toward the opposite edge.
- **Rendering breaks / artifacts in Chrome around rounded containers:** an ancestor has both `overflow: hidden` and `border-radius` (Chromium #40778541) — separate those properties onto different elements or skip the rounding in Chrome. See `references/chrome-gotcha.md`.
- **Clicks/scroll don't reach content under the overlay:** something re-enabled `pointer-events` on the overlay root. Leave it at the component's default (`none`).
- **No blur on an older/unsupported browser:** `backdrop-filter` is unavailable — the effect degrades to no blur. This is expected graceful degradation, not a bug.
- **User actually wants a uniform blur, not a gradient:** stop and hand back to the orchestrator — a one-line CSS `filter: blur()` is the right tool, not this component.
