---
id: S-032
name: Retro Device
aesthetic_position: developer terminal physical-ui monospace
source_attribution: https://github.com/web-designer-plugin (MIT)
license: MIT
---

# S-032 — Retro Device

## Identity

Retro Device recreates the physical shell of late-1980s to mid-1990s consumer electronics: beige-grey moulded plastic cases, chunky bevelled buttons with tactile press feedback, and LCD-panel green-on-dark display areas. Typography is drawn exclusively from bitmap and monospace faces — VT323 and Press Start 2P — to honour the pixel grid of period hardware. Intended for developer tools, retro games, vintage synthesiser UIs, and nostalgia-first consumer products.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #C0BBAA;
  --color-surface:    #9CB17D;
  --color-text:       #1A2A1A;
  --color-text-muted: #3A4A3A;
  --color-primary:    #2D4A1E;
  --color-accent:     #FF0000;
  --color-border:     #888880;

  /* Typography */
  --font-display: 'Press Start 2P', 'VT323', 'Courier New', monospace;
  --font-body:    'VT323', 'Courier New', 'Courier', monospace;
  --font-mono:    'VT323', 'Courier New', 'Courier', monospace;

  /* Spacing */
  --spacing: 8px;

  /* Shape */
  --radius: 2px;

  /* Shadow — bevelled outset button (classic CSS bevel trick) */
  --shadow:
    inset -1px -1px #ffffff,
    inset  1px  1px #808080,
    inset -2px -2px #dfdfdf,
    inset  2px  2px #404040;

  /* Motion — instant snap, no easing */
  --motion-duration: 50ms;
  --motion-easing:   linear;

  /* Optional — button-press state (translate + inverted shadow) */
  --shadow-pressed:
    inset  1px  1px #ffffff,
    inset -1px -1px #808080,
    inset  2px  2px #dfdfdf,
    inset -2px -2px #404040;

  /* Optional — LCD panel surface */
  --lcd-bg:   #1A2A1A;
  --lcd-text: #9CB17D;
}
```

```ts
// tailwind.config.ts — theme extension
export default {
  theme: {
    extend: {
      colors: {
        bg:      '#C0BBAA',
        surface: '#9CB17D',
        text:    '#1A2A1A',
        muted:   '#3A4A3A',
        primary: '#2D4A1E',
        accent:  '#FF0000',
        border:  '#888880',
        lcd:     { bg: '#1A2A1A', text: '#9CB17D' },
      },
      fontFamily: {
        display: ['"Press Start 2P"', 'VT323', '"Courier New"', 'monospace'],
        body:    ['VT323', '"Courier New"', 'Courier', 'monospace'],
        mono:    ['VT323', '"Courier New"', 'Courier', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '2px',
      },
      boxShadow: {
        bevel: 'inset -1px -1px #fff, inset 1px 1px #808080, inset -2px -2px #dfdfdf, inset 2px 2px #404040',
        pressed: 'inset 1px 1px #fff, inset -1px -1px #808080, inset 2px 2px #dfdfdf, inset -2px -2px #404040',
      },
      transitionDuration: { DEFAULT: '50ms' },
      transitionTimingFunction: { DEFAULT: 'linear' },
    },
  },
}
```

## "Breaks if" invariants

- breaks if a smooth `border-radius` greater than 4px is applied to buttons or panels — period hardware used tight 1-2px moulded corners
- breaks if any non-monospace font is used for body or display copy
- breaks if the bevelled box-shadow is replaced with a soft drop-shadow — outset bevel is the physical identity of the style
- breaks if `--motion-duration` exceeds 100ms — button feedback must feel instantaneous (hardware latency simulation)
- breaks if `--color-bg` moves off the beige-grey plastic range — warm neutral is the chassis colour
- breaks if the LCD surface colour is replaced with white — dark-on-green LCD contrast is structural
- breaks if a gradient is applied to any surface — flat moulded plastic has no gradients

## Canonical render-test pointer

Render-test file: `references/render-tests/S-032-retro-device-test.html` (generated from `references/_test-skeleton.html` + this file's `{{TOKEN}}` block).
Upstream source: web-designer-plugin retro-device demo (MIT).

## Render-test verdict

JOD: pending

## Cross-references

- S-033 Win98 — window-chrome OS metaphor, same era but screen-UI not device-shell
- S-012 Retro Terminal — terminal green-on-black, no physical device metaphor
- S-038 Dark Tech — dark futuristic tech, no retro physicality
- Source: web-designer-plugin (MIT) — https://github.com/web-designer-plugin
