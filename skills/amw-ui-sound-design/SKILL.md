---
name: amw-ui-sound-design
description: Programmatic UI sound design using Web Audio API. Activates on narrow audio-specific triggers — "design UI sound", "click sound", "notification chime", "toggle feedback", "hover sound", "success audio", "error audio", "whoosh effect", "UI sound library", "Web Audio API". Does NOT activate on broad design vocabulary ("design a page", "build a UI") — those route to amw-design-principles. Direct-port from MIT-licensed ui-sound-design-skill (© 2026 Danny Williams).
version: 0.1.0
author: ai-maestro-webdesign (direct-port from dannyjpwilliams/ui-sound-design-skill, MIT)
---

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are sound-specific only — `amw-design-principles` routes here when audio interaction is in scope. Pairs with [amw-motion-designer-agent](../../agents/amw-motion-designer-agent.md) and [amw-sound-designer-agent](../../agents/amw-sound-designer-agent.md) for holistic interaction design.

```
▁▃▅▇█▇▅▃▁  U I   S O U N D   D E S I G N  ▁▃▅▇█▇▅▃▁
```

Describe what your UI should sound like.
Preview it, tweak it, and download it from the browser.

# UI Sound Design

Translate plain-English sound descriptions into working Web Audio API code. No audio engineering background needed — describe what you want to hear, and this skill provides the synthesis knowledge to make it real.

## Workflow

Every sound follows this loop: **Describe → Generate → Listen → Refine** (with optional **Review** for auditing existing code)

### 1. Describe

The user describes the sound in plain language. Ask clarifying questions using this framework:

**Four questions before generating any sound:**

1. **What triggers it?** (click, hover, toggle, notification, transition, success, error)
2. **What's the emotional tone?** (satisfying, subtle, urgent, playful, professional, minimal)
3. **How prominent should it be?** (barely perceptible, noticeable, attention-grabbing)
4. **Any reference points?** (iOS keyboard, Slack notification, macOS trash, game UI, "like a bubble popping")
5. **Have an audio reference file?** If the user has a .wav or .mp3 file they want to match, direct them to run the analyzer:

   ```
   node bin/amw-sound-analyze.mjs path/to/reference.wav
   ```

   Then paste the output back. When a sound profile is provided:
   1. Load [audio-file-references](references/audio-file-references.md) for interpretation guidance
> [audio-file-references.md] What Is a Sound Profile? · How to Use a Sound Profile · Field Reference · Analysis-to-Category Mapping · Brightness Mapping (Spectral Centroid → Vocabulary Bridge) · Envelope → Vocabulary Bridge · Harmonic Content → Synthesis Approach · Limitations
   2. Read the `synthesis_suggestion` block for initial parameters
   3. Match to the closest **sound category** using `recipe_starting_point`
   4. Load that recipe from [sound-recipes](references/sound-recipes.md)
> [sound-recipes.md] Click · Toggle · Hover · Success · Error · Warning · Notification · Whoosh · Pop · Complete Sound Library
   5. Override recipe defaults with the profile's suggested parameters
   6. Apply any vocabulary bridge terms from the profile's `VOCABULARY MATCH` section
   7. Proceed to Generate as normal

If the user gives a vague request like "make a click sound", use sensible defaults from the recipes and generate immediately — don't over-ask.

### 2. Generate

1. Match the description to a **sound category** (see quick reference below)
2. Load the recipe from [sound-recipes](references/sound-recipes.md)
> [sound-recipes.md] Click · Toggle · Hover · Success · Error · Warning · Notification · Whoosh · Pop · Complete Sound Library
3. Apply the **vocabulary bridge** to translate adjectives into parameter changes
4. For novel sounds not covered by recipes, compose from building blocks in [web-audio-building-blocks](references/web-audio-building-blocks.md)
> [web-audio-building-blocks.md] AudioContext Setup · Oscillator Types · Gain Envelopes (ADSR) · White Noise Generation · Filter Types (BiquadFilterNode) · Frequency Sweeps · Layering Oscillators · FM Synthesis (Bell/Metallic Tones) · Reusable Factory Pattern · Common Mistakes · Per-Sound-Type Parameter Bounds · Validation Checklist · Appendix — Tone.js abstractions: Setup, Synth Types, Recipes, Effects, Volume in Tone.js, Converting Tone.js to Vanilla Web Audio, When to Use Tone.js vs Vanilla
5. Output format: **HTML preview** by default (adapt `assets/sound-preview.html`), or ES module / React hook / class if requested

> NOTE: The HTML preview template is not yet ported. Use the source path `reports_dev/batch9/extracted/ui-sound-design-skill-main/skills/ui-sound-design/assets/sound-preview.html` for now; T-001b will port it under `skills/amw-ui-sound-design/assets/` in a follow-up.

### 3. Listen

Provide the HTML preview file so the user can open it in a browser and hear the sound immediately. Each sound includes a download button that exports a .wav file for use in production code or handoff to developers. Include labeled buttons for each sound variation. The preview must:
- Handle AudioContext suspension (user gesture to start)
- Use the singleton AudioContext pattern
- Include visual feedback on play (the template handles this)

### 4. Refine

When the user gives feedback, translate it using the vocabulary bridge and adjust parameters. Common refinement patterns:
- "I like it but..." → tweak 1-2 parameters
- "Completely wrong" → try a different recipe/approach
- "Too much/little" → scale the relevant parameter up/down
- "More like X" → identify what makes X distinctive and match those characteristics

### 5. Review (optional)

Enter review mode when the user says "review", "audit", or "check my sound code", or pastes existing Web Audio code for evaluation.

**Steps:**
1. Load rules from [web-audio-safety](references/web-audio-safety.md)
> [web-audio-safety.md] Priority Levels · Critical — Context Management · Critical — Envelope Safety · High — Envelope & Scheduling · High — Sound Design · Medium — Parameters · Per-Sound-Type Parameter Bounds · Review Mode — Output Format
2. Scan the code against each rule, starting with Critical priority
3. Report findings using the format in `web-audio-safety.md` — one line per violation with `file:line — [rule-id] description`
4. Provide a summary table (pass/fail counts by priority)
5. Suggest concrete fixes for each failing rule

**When to stay in generate mode:** If the user's request is ambiguous (e.g., "here's my click sound" without asking for review), default to the generative workflow. Only enter review mode when the intent to audit is clear.

## Vocabulary Bridge

This is the core translation layer. When the user uses subjective language, map it to synthesis parameters:

| User Says | Parameter Change | Example |
|-----------|-----------------|---------|
| "Brighter" | Raise frequency or filter cutoff | Filter cutoff 1500 → 3000 Hz |
| "Warmer" | Lower filter cutoff, use sine/triangle wave | Switch sawtooth → sine, cutoff 3000 → 1200 |
| "Darker" | Lower frequency, reduce high harmonics | Add lowpass filter at 800 Hz |
| "Snappier" | Shorter attack and decay | Decay 0.15 → 0.05s |
| "Softer" | Lower volume, longer attack, gentle envelope | Volume 0.3 → 0.15, attack 0 → 0.01s |
| "Louder" / "More prominent" | Raise volume (max 0.8) | Volume 0.2 → 0.4 |
| "Fuller" / "Richer" | Layer oscillators, add detune | Add second osc detuned +7 cents |
| "Thinner" | Remove layers, use sine wave, raise highpass | Single sine, highpass at 500 Hz |
| "More metallic" | FM synthesis, inharmonic ratios | Mod ratio 1.4, increase mod depth |
| "More organic" / "Natural" | Use noise components, subtle randomness | Mix in filtered noise burst |
| "Shorter" / "Crisper" | Reduce total duration | Duration 0.15 → 0.06s |
| "Longer" / "More sustained" | Increase duration and sustain | Duration 0.1 → 0.3s, add sustain phase |
| "More playful" | Higher pitch, bounce/overshoot | Frequency +200 Hz, add pitch overshoot |
| "More professional" | Subtle, clean, minimal | Lower volume, sine wave, short duration |
| "Retro" / "8-bit" | Square wave, quantized pitch | Switch to square, use note frequencies |
| "Bubbly" | Rapid pitch drop, sine wave | startFreq 2000, quick exponential drop |

## Sound Categories — Quick Reference

| Category | Duration | Recipe | Trigger | Key Character |
|----------|----------|--------|---------|---------------|
| Click | 10–80ms | `references/sound-recipes.md#click` | Button press, tap | Noise burst, bandpass filtered |
| Toggle | 80–200ms | `references/sound-recipes.md#toggle` | Switch on/off | Rising/falling pitch sweep |
| Hover | 30–80ms | `references/sound-recipes.md#hover` | Mouse enter | Gentle, nearly subliminal |
| Success | 200–500ms | `references/sound-recipes.md#success` | Task complete, save | Ascending major third |
| Error | 150–400ms | `references/sound-recipes.md#error` | Validation fail, rejected | Descending, buzzy |
| Warning | 150–350ms | `references/sound-recipes.md#warning` | Caution state | Double pulse, mid-range |
| Notification | 200–800ms | `references/sound-recipes.md#notification` | New message, alert | Bell-like FM synthesis |
| Whoosh | 100–400ms | `references/sound-recipes.md#whoosh` | Page transition, slide | Filtered noise sweep |
| Pop | 30–80ms | `references/sound-recipes.md#pop` | Add item, bubble, appear | Sine with pitch drop |
| Custom | varies | [web-audio-building-blocks](references/web-audio-building-blocks.md) | Anything else | Compose from building blocks |
> [web-audio-building-blocks.md] AudioContext Setup · Oscillator Types · Gain Envelopes (ADSR) · White Noise Generation · Filter Types (BiquadFilterNode) · Frequency Sweeps · Layering Oscillators · FM Synthesis (Bell/Metallic Tones) · Reusable Factory Pattern · Common Mistakes · Per-Sound-Type Parameter Bounds · Validation Checklist · Appendix — Tone.js abstractions: Setup, Synth Types, Recipes, Effects, Volume in Tone.js, Converting Tone.js to Vanilla Web Audio, When to Use Tone.js vs Vanilla

## Critical Implementation Rules

### AudioContext user-gesture requirement
Browsers block audio until a user interaction (click, tap, keydown). Always initialize or resume the AudioContext inside an event handler. The singleton pattern in [web-audio-building-blocks](references/web-audio-building-blocks.md) handles this.
> [web-audio-building-blocks.md] AudioContext Setup · Oscillator Types · Gain Envelopes (ADSR) · White Noise Generation · Filter Types (BiquadFilterNode) · Frequency Sweeps · Layering Oscillators · FM Synthesis (Bell/Metallic Tones) · Reusable Factory Pattern · Common Mistakes · Per-Sound-Type Parameter Bounds · Validation Checklist · Appendix — Tone.js abstractions: Setup, Synth Types, Recipes, Effects, Volume in Tone.js, Converting Tone.js to Vanilla Web Audio, When to Use Tone.js vs Vanilla

### Never ramp gain to zero
`exponentialRampToValueAtTime(0, ...)` throws an error. Always ramp to `0.001` — it's inaudible but mathematically valid. This applies to every sound. No exceptions.

### Node cleanup
- OscillatorNodes auto-disconnect after `stop()` — no manual cleanup needed
- BufferSourceNodes are one-shot — create a new one each play
- For long-lived filter/gain nodes, call `disconnect()` when done
- Never create a new AudioContext per sound — use the singleton

### Volume safety
- Default volume: `0.3` (gain value)
- Maximum volume: `0.8` — never exceed this
- Hover sounds: `0.03–0.08` (barely perceptible)
- UI sounds should complement, not dominate — err on the side of quiet

### Scheduling precision
Capture `const now = ctx.currentTime` once at the start of each sound function. Derive all scheduling times from `now`. Never read `currentTime` multiple times.

### Use exponential ramps by default
`exponentialRampToValueAtTime` sounds natural for both volume and frequency. `linearRampToValueAtTime` sounds mechanical. Only use linear for sub-50ms transitions.

## Output Formats

### HTML Preview (default)
Adapt `assets/sound-preview.html`. Self-contained, no dependencies, opens in any browser. Best for the iterative listen-refine loop. Includes WAV download — click the download button on any sound to get a .wav file. Sound functions must use `(ctx, dest)` parameters with fallback defaults for download support, and each sound needs a matching entry in the `durations` map.

### ES Module
```javascript
// ui-sounds.js
export function playClick(options) { /* ... */ }
export function playSuccess(options) { /* ... */ }
```

### React Hook
```javascript
// useUISound.js
export function useUISound() {
  const ctxRef = useRef(null);
  const getCtx = useCallback(() => { /* singleton */ }, []);
  return { playClick, playSuccess, /* ... */ };
}
```

### Sound Library Class
Use the `UISoundLibrary` class from [sound-recipes](references/sound-recipes.md). Bundles all sounds with enable/disable and master volume control.
> [sound-recipes.md] Click · Toggle · Hover · Success · Error · Warning · Notification · Whoosh · Pop · Complete Sound Library

### Tone.js abstractions
For faster prototyping, Tone.js wraps the Web Audio API with higher-level synth types (`Tone.Synth`, `Tone.MetalSynth`, `Tone.NoiseSynth`, `Tone.MembraneSynth`). See the Tone.js appendix in [web-audio-building-blocks](references/web-audio-building-blocks.md) for recipe equivalents and a conversion guide back to vanilla Web Audio.
> [web-audio-building-blocks.md] AudioContext Setup · Oscillator Types · Gain Envelopes (ADSR) · White Noise Generation · Filter Types (BiquadFilterNode) · Frequency Sweeps · Layering Oscillators · FM Synthesis (Bell/Metallic Tones) · Reusable Factory Pattern · Common Mistakes · Per-Sound-Type Parameter Bounds · Validation Checklist · Appendix — Tone.js abstractions: Setup, Synth Types, Recipes, Effects, Volume in Tone.js, Converting Tone.js to Vanilla Web Audio, When to Use Tone.js vs Vanilla

## Resources

### references/
- `sound-recipes.md` — 9 sound categories with parameters, code, tuning guides, variations + `UISoundLibrary` class
- `web-audio-safety.md` — formal validation rules with IDs, priorities, pass/fail examples (review mode)
- `web-audio-building-blocks.md` — oscillators, envelopes, filters, noise, FM synthesis, factory patterns + Tone.js conversion appendix
- `audio-file-references.md` — interpret sound profiles from `bin/amw-sound-analyze.mjs`

### bin/
- `../bin/amw-sound-analyze.mjs` — CLI audio analyzer (`node bin/amw-sound-analyze.mjs <file.wav>`)

### Companion agent
- [amw-sound-designer-agent](../../agents/amw-sound-designer-agent.md) (Tier-4) — spawned by `ai-maestro-webdesign-main-agent` for sound-design jobs

## Attribution

This skill is a direct port of the MIT-licensed `ui-sound-design-skill` (© 2026 Danny Williams). Original source: dannyjpwilliams/ui-sound-design-skill. All synthesis recipes, the vocabulary bridge, and the safety rules are verbatim or near-verbatim with path adjustments for plugin integration. Modifications: orchestrator header, frontmatter adapted for plugin trigger discipline, paths rewritten to bin/ and adjacent skills.
