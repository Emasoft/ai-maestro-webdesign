# TECH-shader-types — deeper notes on each of the 11 background types

## Table of Contents

- [1. `mesh-gradient`](#1-mesh-gradient)
- [2. `voronoi`](#2-voronoi)
- [3. `liquid-metal`](#3-liquid-metal)
- [4. `chrome`](#4-chrome)
- [5. `pulsar`](#5-pulsar)
- [6. `black-hole`](#6-black-hole)
- [7. `glass`](#7-glass)
- [8. `spiral`](#8-spiral)
- [9. `particles`](#9-particles)
- [10. `fireworks`](#10-fireworks)
- [11. `plasma`](#11-plasma)
- [Library / runtime choice](#library-runtime-choice)
- [Accessibility checklist](#accessibility-checklist)

For each of the 11 types catalogued in `SKILL.md`, this reference adds:

- The mathematical / geometric primitive that drives the look.
- The default-tasteful parameter range (what to suggest as a starting point).
- The dial that, when overdriven, ruins the effect.
- Library-agnostic implementation hints.

## 1. `mesh-gradient`

- **Primitive:** N Gaussian blobs interpolated in colour space, then composited. The base layer is a multi-stop linear or radial gradient; blobs animate in worldspace.
- **Tasteful range:** 3..5 colour stops, 2..4 blobs, drift speed 0.05..0.2 cycles/sec.
- **What ruins it:** more than 6 blobs → muddled "neon puddle." Drift speed >0.5 → reads as nausea-inducing.
- **Implementation hints:** WebGL fragment shader is the cleanest. A Canvas2D version exists (gradient-radial composite operations) but loses smoothness on high-DPI. Three.js `ShaderMaterial` on a fullscreen plane is the standard recipe.

## 2. `voronoi`

- **Primitive:** F1 / F2 distance to N seed points; render the field as cells with edges where F2 − F1 is small.
- **Tasteful range:** 30..120 cells per 1920px, edge thickness 1..2px, drift speed 0.02..0.1.
- **What ruins it:** > 300 cells → mush; edges thicker than 3px → reads as cracks.
- **Implementation hints:** GPU implementation has O(N) cost per pixel, so density caps before perf collapses. CPU-side Lloyd relaxation gives prettier results but precomputes static layouts.

## 3. `liquid-metal`

- **Primitive:** Reflective normal map driven by a flowing noise field; lit by a moving directional light.
- **Tasteful range:** ripple frequency 0.5..2 Hz, polish 0.6..0.9, light angle 30..60° from horizontal.
- **What ruins it:** polish > 0.95 → mirror with no surface detail; ripple > 4 Hz → reads as static noise.
- **Implementation hints:** A normal-map texture animated by perlin / simplex noise + a Fresnel-weighted reflection of an HDR or static-gradient environment map. WebGL standard.

## 4. `chrome`

- **Primitive:** Flat reflective plane with a moving environment map; highlight bands are bright stripes in the envmap.
- **Tasteful range:** 2..4 highlight bands, light angle 20..40°, polish 0.85..0.95.
- **What ruins it:** > 5 bands → distracting; rotation animation faster than 0.5 cycles/sec → optical-illusion strobe risk.
- **Implementation hints:** Cheap. A `radial-gradient` + `linear-gradient` composite in CSS gets 80% of the way; WebGL adds the moving highlights.

## 5. `pulsar`

- **Primitive:** Distance from centre × `sin(distance × frequency − time × speed)` → ring intensity.
- **Tasteful range:** pulse rate 0.5..1.5 Hz, decay distance 200..600px, 1..2 colour stops.
- **What ruins it:** > 3 Hz → strobe / accessibility hazard; multiple centres → competing rings.
- **Implementation hints:** Trivially cheap fragment shader. Also doable in Canvas2D with `radialGradient` redrawn each frame.

## 6. `black-hole`

- **Primitive:** Polar warp around centre + disk-band colour function. Lensing is a uv-displace proportional to `1/r²`.
- **Tasteful range:** disk thickness 60..120px, lens strength 0.6..0.8, rotation 0.05..0.15 cycles/sec.
- **What ruins it:** lens strength > 0.9 → singularity artefacts; rotation > 0.3 → motion sickness.
- **Implementation hints:** Fragment shader. Heavy. Consider rendering at half-resolution and upscaling for mobile.

## 7. `glass`

- **Primitive:** Voronoi tessellation as facet boundaries + per-facet refraction sampling of a backdrop.
- **Tasteful range:** facet count 8..24, refraction strength 0.02..0.08.
- **What ruins it:** > 40 facets → looks like cracked windshield. Refraction > 0.15 → unreadable backdrop.
- **Implementation hints:** Closest cousin of `amw-liquid-glass`'s real-time WebGL refraction. Use the same library if you also need component-level glass; this catalog covers ONLY the fullscreen-background usage.

## 8. `spiral`

- **Primitive:** `θ` and `r` in polar coordinates → spiral function (logarithmic / Archimedean) → band intensity from `sin(spiral × frequency)`.
- **Tasteful range:** tightness 0.05..0.2 turns/radius, band thickness 4..8px.
- **What ruins it:** tightness > 0.5 → hypnotic / strobe; thickness > 12px → reads as graphic-design clip-art.
- **Implementation hints:** Trivially cheap fragment shader.

## 9. `particles`

- **Primitive:** N point sprites with positions / velocities updated each frame; rendered with additive blending.
- **Tasteful range:** 500..1500 particles, drift 20..60px/sec, size 1..3px.
- **What ruins it:** > 3000 particles on mobile → frame drops. Drift > 100px/sec → reads as snow not stars.
- **Implementation hints:** WebGL `gl.POINTS` with a CPU-side update loop is standard. PixiJS provides a good high-level wrapper.

## 10. `fireworks`

- **Primitive:** Time-discrete bursts spawning short-lived particle clouds with gravity + air drag.
- **Tasteful range:** 1 burst every 2..4 sec, 60..120 particles per burst, lifetime 1..2 sec.
- **What ruins it:** continuous overlapping bursts → fatigue; bursts > 200 particles → fps drops.
- **Implementation hints:** Event-driven. Pause when tab is hidden. Often paired with audio cues — be considerate of users on muted devices.

## 11. `plasma`

- **Primitive:** Sum of N sine waves of (x, y, time) mapped to colour via a palette LUT. Classic demo-scene effect.
- **Tasteful range:** 3..5 waves, frequency 0.005..0.02 cycles/px, speed 0.5..1.5 cycles/sec.
- **What ruins it:** > 8 waves → noise; speed > 3 → seizure risk.
- **Implementation hints:** Trivially cheap fragment shader. Also a fantastic Canvas2D demo for old hardware.

## Library / runtime choice

- **Three.js** — full 3D library; overkill for a background, but if the project already uses Three.js, reuse it.
- **PixiJS** — 2D-first WebGL, simpler API than Three for fullscreen shader planes.
- **Custom GLSL fragment shader on a `<canvas>` element** — smallest footprint; recommended when only one background type is needed.
- **`amw-hypercomp/SKILL.md`** — already shipped in this plugin; compiles TS image-processing pipelines to SVG filters. Perfect for the 17 image-overlay effects; less suited to the 11 generative-background types.

## Accessibility checklist

Before any shader background ships:

- `prefers-reduced-motion: reduce` → freeze animation on the first frame.
- `document.visibilityState !== 'visible'` → pause the render loop.
- `prefers-color-scheme` → adjust palette for the active scheme.
- Any text on top has either a solid card backdrop (90% opaque min) or a `text-shadow` that produces AA contrast at all animation frames.
- A static fallback poster image is set as `background-image` on the host element so users without WebGL still see SOMETHING coherent.
