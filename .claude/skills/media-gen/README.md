# media-gen

Local image and image-to-video pipeline using Fal.ai. A lightweight, no-subscription alternative to hosted gen UIs: you bring your own Fal key and pay per generation.

## What it does

You describe media casually ("a photo of a dog swimming with a tennis ball"). Claude refines the prompt, picks the current best model from `models.json`, generates the image via Fal.ai, saves it to a dated local folder, and asks if you want to animate it. It can also upscale existing videos/images to HD via Topaz.

All artifacts (`prompt.md`, `image-NN.png`, `video-NN.mp4`) live in one folder per generation.

## Install

This skill is a Claude Code [agent skill](https://docs.claude.com/en/docs/claude-code/skills). Drop the `media-gen` folder into your skills directory and Claude picks it up automatically.

1. **Place the folder:**
   - Mac/Linux: `~/.claude/skills/media-gen/`
   - Windows: `C:\Users\<you>\.claude\skills\media-gen\`

2. **Get a Fal key.** Sign up at https://fal.ai and copy your API key from the dashboard.

3. **Give the skill your key** — either way works, on both OSes:
   - **Easiest:** create a file named `.fal_key` in your home folder (Mac: `~/.fal_key`, Windows: `C:\Users\<you>\.fal_key`) containing just your key on one line.
   - **Or the env var:**
     - Windows: `setx FAL_KEY "your-key-here"`, then **close and reopen your terminal** (`setx` doesn't apply to the current session).
     - Mac/Linux: add `export FAL_KEY="your-key-here"` to `~/.zshrc` (or `~/.bashrc`), then `source ~/.zshrc`.

   The key is read at runtime and never stored in any file inside this folder.

4. **That's it — no manual SDK install.** The script installs the `fal-client` SDK itself on first run (handles Mac's "externally-managed-environment" pip restriction automatically). If you prefer to preinstall: `python3 -m pip install fal-client` (Mac/Linux) or `python -m pip install fal-client` (Windows).

   *Optional:* the `upscale` command works best with **ffmpeg** installed (`brew install ffmpeg` on Mac, `winget install ffmpeg` on Windows). Image and video generation don't need it.

5. **Test it.** In any Claude Code session, say:
   > generate a photo of a single red apple on a white background

   Claude should invoke this skill and run end-to-end.

**Note on Python:** the skill needs Python 3.9+. On Mac/Linux the command is `python3`; on Windows it's `python`. Claude handles this automatically when running the skill.

## How to use it

Just talk to Claude in any session. Triggers:
- *"generate a photo of ..."*
- *"make me an image where ..."*
- *"create a video of ..."*
- *"turn this image into a video"*
- *"upscale this clip / make this HD"*

Claude reads `SKILL.md`, refines the prompt, picks the model, runs `scripts/generate.py`, and saves to `~/Documents/Media Gen/<date>-<slug>/`.

## Updating the model registry

`models.json` is the source of truth for "current best." Two ways to update:

**Manual:** Edit the file. Bump `default` to the new winner. Update `last_updated`.

**Assisted:** In any Claude session, say *"check fal.ai for new image and video models and update the media-gen registry."* Claude will WebFetch fal.ai/models, compare, propose a diff, and write the update on your approval.

## Configuration

Edit `config.json` to change the output root directory. Default is `~/Documents/Media Gen`. Tilde and env vars expand.

## File structure

```
media-gen/
├── SKILL.md            # Workflow instructions Claude reads
├── README.md           # This file
├── config.json         # Output dir
├── models.json         # Curated registry of "current best" Fal models
├── references/
│   ├── upscale.md              # Topaz upscale workflow + cost tiers
│   └── character-consistency.md # Same-character-across-shots workflow
└── scripts/
    └── generate.py     # CLI: image | video | upscale
```

## Troubleshooting

| Error | Fix |
|---|---|
| `FAL_KEY not set` | Create `~/.fal_key` (Mac) / `C:\Users\<you>\.fal_key` (Windows) containing your key, or set the env var per Install step 3 |
| `couldn't install fal-client automatically` | Install manually: `python3 -m pip install --user --break-system-packages fal-client` (Mac) or `python -m pip install fal-client` (Windows) |
| `404` on a `fal_id` | Model slug drifted on Fal. Open https://fal.ai/models, find the new slug, update `models.json` |
| `couldn't resolve output_path` | Fal changed the response schema for that model. Check the raw result in stderr, update `output_path` in `models.json` (e.g. `images[0].url` vs `video.url`) |
| Generation just hangs | Fal queue can be slow. Images usually under 30s, videos 1-3 min. Downloads time out and retry automatically |

## Cost reality (verified July 2026)

- Nano Banana Pro: ~$0.04 per image
- Seedance 2.0 Pro 5s: ~$1.51 at 720p, ~$3.40 at 1080p
- Seedance 2.0 Fast 5s: ~$1.21 (720p max)
- Kling v3 Pro 5s: ~$0.84 (~$0.56 with audio off)

Images are near-free; video is where the money goes — which is why Claude always quotes the exact cost and waits for your yes before any video run. Verify current pricing at fal.ai/pricing.
