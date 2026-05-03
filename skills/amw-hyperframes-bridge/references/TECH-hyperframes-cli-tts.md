---
name: TECH-hyperframes-cli-tts
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/tts.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Flags](#flags)
  - [Voice naming scheme](#voice-naming-scheme)
  - [Speed tuning](#speed-tuning)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: `hyperframes tts` — text-to-speech via Kokoro-82M

## What it does

Generates narration audio from text using the local Kokoro-82M TTS model. 12 bundled voices (Kokoro-82M ships 54 total; the CLI exposes 12 via `BUNDLED_VOICES` in `tts/manager.ts`), with tone / gender / language variants. Offline — no API calls. Output is a WAV file suitable for dropping into a hyperframes composition as the narration track.

## When to use

In Step 5 of the capture pipeline, or any time a composition needs narration. Faster than record-and-edit for iterative drafts; voice choice is load-bearing, so audition before committing.

## How it works

```bash
# Basic (af_heart is the default voice — DEFAULT_VOICE in tts/manager.ts)
npx hyperframes tts "Text here" --voice af_heart --output narration.wav

# From file
npx hyperframes tts script.txt --voice bf_emma

# Override phonemizer language (English text, Italian phonemization for accent)
npx hyperframes tts "Ciao a tutti" --voice af_heart --lang it --output accented.wav

# List available voices
npx hyperframes tts --list
```

### Flags

| Flag | Alias | Default | Description |
|---|---|---|---|
| positional | — | — | Text to speak, or path to a `.txt` file |
| `--output` | `-o` | `speech.wav` | Output file path |
| `--voice` | `-v` | `af_heart` | Voice ID (see Voice naming scheme below) |
| `--speed` | `-s` | `1.0` | Speech speed multiplier (0.1–3.0) |
| `--lang` | `-l` | auto-detected from voice prefix | Phonemizer language override. Accepts: `en-us`, `en-gb`, `es`, `fr-fr`, `hi`, `it`, `pt-br`, `ja`, `zh`. Use when you want a specific accent (e.g. English text with French phonemization). Mismatched voice/lang is valid stylization — a note is printed but it is not an error. |
| `--list` | — | false | List available voices and exit |
| `--json` | — | false | Output result as JSON |

### Voice naming scheme

Voices are named `<lang><gender>_<name>` (underscore between gender and name):

- `af_` = American female, `am_` = American male
- `bf_` = British female, `bm_` = British male
- Plus non-English prefixes for Kokoro's other language packs

The voice prefix determines the auto-detected phonemizer language: `a`=`en-us`, `b`=`en-gb`, `e`=`es`, `f`=`fr-fr`, `h`=`hi`, `i`=`it`, `j`=`ja`, `p`=`pt-br`, `z`=`zh`. Use `--lang` to override.

Examples: `af_nova`, `af_bella`, `am_michael`, `bf_emma`, `bf_isabella`, `bm_george`.

### Speed tuning

- Default speech rate is ~160 wpm (typical narration pace)
- Slower / calmer brands can use `--speed 0.9` for ~145 wpm
- Faster / energetic brands can use `--speed 1.1` for ~175 wpm

Over-slowing (<0.85) introduces artifacts. Over-speeding (>1.15) loses clarity.

## Minimal example

```bash
# Draft narration for a launch teaser
cat scripts/narration.txt
# Address verification, in under 120 milliseconds.
# Bad addresses cost logistics teams real money...

npx hyperframes tts scripts/narration.txt \
  --voice af_heart \
  --output narration.wav

# Listen; if the voice feels wrong for the brand, try af_nova (American female, lively):
npx hyperframes tts scripts/narration.txt --voice af_nova --output narration-alt.wav
# Or am_michael (American male, neutral):
npx hyperframes tts scripts/narration.txt --voice am_michael --output narration-alt2.wav
```

*Attributed to the hyperframes-cli skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-cli/SKILL.md`.*

## Gotchas

- Voice auditions matter. Technical brands rarely want enthusiastic-startup voices. Luxury brands rarely want casual voices.
- Kokoro-82M is local; no API cost, but first invocation downloads the model (~200 MB).
- Numbers, acronyms, and brand names sometimes get mispronounced. Use SSML-like hints inline: `'Acme' is spelled A-C-M-E` or `120 ms (pronounced "one-twenty milliseconds")` if the model pronounces wrong.
- TTS output is deterministic for the same voice + text + speed. Re-running is reproducible.

## Cross-references

- [TECH-hyperframes-cli-transcribe](TECH-hyperframes-cli-transcribe.md) — transcribe the TTS output for timing
  > What it does · When to use · How it works · Models · Output schema · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-5-vo](TECH-hyperframes-capture-step-5-vo.md) — full VO + timing step
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
