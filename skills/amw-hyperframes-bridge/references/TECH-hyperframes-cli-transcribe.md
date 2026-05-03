---
name: TECH-hyperframes-cli-transcribe
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/transcribe.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Models](#models)
  - [Output schema](#output-schema)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: `hyperframes transcribe` — audio → word-level timestamps

## What it does

Transcribes an audio or video file into word-level timestamps using Whisper. Also imports existing `.srt` / `.vtt` subtitles or OpenAI-format JSON. The output is `transcript.json` with per-word `start` / `end` in seconds — consumed by the capture pipeline's Step 5 to map narration to STORYBOARD beats.

## When to use

Immediately after `hyperframes tts` produces narration audio, or whenever you have pre-recorded narration / subtitles you want to sync visual elements to.

## How it works

```bash
# Audio file
npx hyperframes transcribe audio.mp3

# Video file (extracts audio first)
npx hyperframes transcribe video.mp4 --model medium.en --language en

# Import existing subtitles
npx hyperframes transcribe subtitles.srt
npx hyperframes transcribe subtitles.vtt

# Import OpenAI whisper JSON
npx hyperframes transcribe openai-response.json
```

### Models

Whisper model tiers, accuracy vs speed:

| Model | Accuracy | Speed | Size |
|---|---|---|---|
| `tiny.en` | Low | Very fast | ~75 MB |
| `base.en` | Medium | Fast | ~140 MB |
| `small.en` | Good | Medium | ~460 MB |
| `medium.en` | Very good | Slow | ~1.5 GB |
| `large-v3` | Best | Very slow | ~3 GB |

Default model is `small.en` (per `whisper/manager.ts` `DEFAULT_MODEL = 'small.en'`). `medium.en` is the next tier up — use it when accuracy on brand names, acronyms, or accented speech is unsatisfactory. `large-v3` is worth using for heavy accents, mixed languages, or critical deliverables.

### Output schema

```json
{
  "segments": [
    {
      "id": 0,
      "start": 0.30,
      "end": 2.47,
      "text": "Address verification, in under 120 milliseconds.",
      "words": [
        { "word": "Address",       "start": 0.30, "end": 0.74 },
        { "word": "verification",  "start": 0.74, "end": 1.41 },
        { "word": ",",             "start": 1.41, "end": 1.42 },
        { "word": "in",            "start": 1.42, "end": 1.55 },
        { "word": "under",         "start": 1.55, "end": 1.82 },
        { "word": "120",           "start": 1.82, "end": 2.10 },
        { "word": "milliseconds.", "start": 2.10, "end": 2.47 }
      ]
    }
  ]
}
```

## Minimal example

```bash
# Transcribe the TTS output
npx hyperframes transcribe narration.wav --model medium.en --language en

# transcript.json is written alongside narration.wav
# Map to beats in STORYBOARD.md:
#   Beat 1 = segments[0]  → 0.30-2.47s
#   Beat 2 = segments[1]  → 2.47-7.12s
#   ...
```

*Attributed to the hyperframes-cli skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-cli/SKILL.md`.*

## Gotchas

- Word boundaries from Whisper are accurate to ~80 ms. Don't snap visual elements to exact word starts — a small lead-in (50-150 ms before the word) usually looks better.
- `--language en` is faster than auto-detect. Specify when you know the language.
- `tiny.en` miss-transcribes numbers and proper nouns often. For any composition where exact word-timing matters, use at least `small.en`.
- SRT / VTT imports use their declared timestamps, which may not match the audio file's actual timing — verify by scrubbing in `preview`.

## Cross-references

- [TECH-hyperframes-cli-tts](TECH-hyperframes-cli-tts.md), [TECH-hyperframes-capture-step-5-vo](TECH-hyperframes-capture-step-5-vo.md)
  > What it does · When to use · How it works · Flags · Voice naming scheme · Speed tuning · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
