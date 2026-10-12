---
name: media-gen
description: Generate and upscale AI images and videos via Fal.ai using a curated registry of best-in-class models. Use whenever the user asks to create, generate, make, render, or produce a photo, image, picture, or video. Phrases like "make me an image of...", "generate a video of...", "create a photo where...", "I want a picture of...", "turn this into a video". Also use to upscale or enhance an existing video or image to HD ("upscale this", "make this HD", "sharpen this clip").
---

# Media Gen Skill

Local image and image-to-video pipeline that hits Fal.ai. Models are swappable via `models.json`.

> **Cross-platform note:** Examples use `python3` and the Mac/Linux script path `~/.claude/skills/media-gen/scripts/generate.py`. On Windows, use `python` and the full path, e.g. `C:\Users\<you>\.claude\skills\media-gen\scripts\generate.py`. The script self-installs the `fal-client` SDK on first run.

## Operating principles

1. **Refine the prompt before sending it.** The user's casual description is the brief, not the prompt. Expand it into a strong prompt matched to the chosen model's style.
2. **Use the registry defaults** unless the user names a model: image = `nano-banana-pro`, image with references = `nano-banana-pro-edit`, video = `seedance-2-pro`, upscale = Topaz. Read `models.json` only when the user names a different model, you need video pricing, or you're updating the registry. The script prints the registry's age on every run — if it's over 30 days old, offer a refresh once, then drop it.
3. **Be conversational, not form-driven.** One question at a time, accept defaults.
4. **Don't auto-animate.** After an image, ask "want to turn this into a video?" — never assume.
5. **Quote video cost before running.** Fal bills video by the second. Read `unit_price_per_second_usd` (and `pricing_note` — some models price by resolution tier) from `models.json`, state `price x duration x N videos`, and wait for an explicit yes. If the price field is missing, WebFetch `https://fal.ai/models/{fal_id}` — don't guess. Default duration is **5s**, never 10s first. Image gen is cheap (~$0.04/image) and runs autonomously.
6. **On script error, relay the stderr message** — it contains the exact fix (key setup, install command, 404 remediation).

## Workflow

### Step 1: Read intent

Extract subject + action, implicit style cues (photo, illustration, cinematic), and derive a 3-5 word kebab-case **working title** (`dog-swimming-tennis-ball`). Don't ask for the title; only confirm if genuinely ambiguous.

### Step 2: Refine the prompt

Expand into 2-4 sentences: lighting, composition, lens/camera language, environment, mood. Nano Banana Pro wants natural-language descriptive prompts, NOT weighted token syntax (`(masterpiece:1.4)` etc).

Show the refined prompt. Ask: **"Run this, or want to adjust?"** Their edits are the source of truth.

### Step 3: Generate the image

```bash
python3 ~/.claude/skills/media-gen/scripts/generate.py image \
  --prompt "<refined prompt>" \
  --title "<working-title>" \
  [--model <model-key>] \
  [--aspect-ratio "16:9"] \
  [--resolution "2K"] \
  [--input-image "<ref-path>" ...]
```

The script prints a JSON line with `image_path` and `folder`. Display the local path.

To lock a character/style to earlier outputs, pass them via repeatable `--input-image` AND switch to `--model nano-banana-pro-edit` (the default model silently ignores references) — full workflow in `references/character-consistency.md`; read it whenever the user wants the same character/face/style across generations.

### Step 4: Offer animation

Ask: **"Want to turn this into a video?"** If yes, collect conversationally (one question at a time):

- **Motion prompt** — what *happens* (different from the image prompt): "The dog paddles forward, water splashing, slight camera dolly in."
- **Duration** — default **5s**. Only escalate to 10s if the user asks after seeing a 5s draft.

Quote the cost per principle 5 and wait for a yes. Then:

```bash
python3 ~/.claude/skills/media-gen/scripts/generate.py video \
  --image "<image_path>" \
  --prompt "<motion prompt>" \
  --title "<working-title>" \
  --folder "<folder from step 3>" \
  --duration 5 \
  [--model <model-key>] \
  [--resolution "1080p"]
```

## Upscaling (Topaz)

When the user wants to upscale/enhance/sharpen an existing video or image, read `references/upscale.md` first — it has the command, the aspect-ratio guarantee, and the cost-tier rules (video upscales must be cost-quoted; 60fps doubles the price).

## Output structure

One dated folder per generation under the `config.json` output root (default `~/Documents/Media Gen/`):

```
2026-04-28-dog-swimming-tennis-ball/
├── prompt.md      # full metadata: prompts, models, params
├── image-01.png   # increments: image-02.png, ...
└── video-01.mp4   # only if the video step ran
```

## Registry updates

If the user asks to refresh `models.json`: WebSearch/WebFetch fal.ai/models for image + video modalities, propose new top-tier entries (`fal_id`, `best_for`, pricing) and default bumps as a diff, get approval before writing, set `last_updated` to today.

## Rules of thumb

- **Don't drift from the user's intent.** Refining is not rewriting the vision. If they say "a dog," don't decide it's a golden retriever.
- **One generation per request.** No preemptive variants.
