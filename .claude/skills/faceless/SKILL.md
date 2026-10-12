---
name: faceless
description: "Faceless short-video pipeline: topic -> /outliers research -> script -> free AI voice (edge-tts) -> fal AI B-roll shots -> captioned 9:16 mp4 ready to post. Use for /faceless, 'make a faceless video', 'faceless channel', 'make a short about X'."
---

# /faceless — one topic in, one finished Short out

`/outliers` (ideas) → Claude (script + shot list) → edge-tts (voice, free) → fal (B-roll) →
ffmpeg (cut to the voice + burned captions) → a finished 1080x1920 mp4 for review.

## Prerequisites (one-time)
- Python 3.10+, ffmpeg on PATH, `pip install edge-tts yt-dlp`
- `FAL_KEY` env var, or `FAL_KEY=...` in `~/.config/fal/.env` (fal.ai → API keys). Only needed for generated shots.

## Rules first
- **Show the fal cost before spending** (`shots --dry`) and get the user's OK. Report the balance after.
- **No income claims, no guarantees.** Label AI content: the video carries an "AI visuals" corner tag;
  also tick the platform's altered/synthetic-content disclosure when it applies.
- **Avoid "mass-produced / repetitive" demonetization:** a real angle, varied visuals, no template spam,
  never the same script twice. Read `references/director_kit.md` §anti-demonetization.
- The user reviews the finished mp4 before anything is posted. This skill never posts.

## Step 1 — idea (never from nothing)
Run `/outliers "<topic>"` (and its 5 niches). Pick the top outlier PATTERN.

## Step 2 — script + shots (Claude as director)
Read `references/director_kit.md` (distilled from the 15 seedance-* skills + photoreal prompting):
2-second hook formula, 45s beat table, shot template. Promise in line one, one clear shape
(3 steps / 2 mistakes / 1 rule), 100-120 words per 45s. Write `plan.json`:
```json
{"slug":"stop-paying-collections","title":"Stop Paying Collections (Do This First)",
 "caption":"... #shorts",
 "model":"bytedance/seedance-2.0/mini/text-to-video",
 "lines":[{"say":"Paying your collections will not fix your credit.","shot":"<director shot prompt>"}]}
```
- 5-8 lines, 30-45s total; one sentence = one shot. Hook line = a number, a contradiction, or a stake.
- Each `shot` = the kit template: size+subject+action, every object named, camera move, lens, light,
  grade, realism line. One locked look for the whole video. Vary shot size/move every line.
- `"file": "path.mp4"` on a line reuses a real clip instead of generating.
- Models: seedance-2.0 mini t2v (~$0.07/s, default drafts) · `fal-ai/veo3.1/lite` / Kling 3 for hero shots.

## Step 3 — build
```bash
S=~/faceless-work ; mkdir -p $S ; cd $S
PYTHONIOENCODING=utf-8 python ~/.claude/skills/faceless/scripts/faceless.py voice    plan.json
PYTHONIOENCODING=utf-8 python ~/.claude/skills/faceless/scripts/faceless.py shots    plan.json --dry   # cost, $0
PYTHONIOENCODING=utf-8 python ~/.claude/skills/faceless/scripts/faceless.py shots    plan.json         # spends fal
PYTHONIOENCODING=utf-8 python ~/.claude/skills/faceless/scripts/faceless.py assemble plan.json
```
Shots are generated at the length of their voice line (4-15s), submitted in parallel, then
stretched ≤1.35x / last-frame-held to fit. Re-running skips shots already on disk — redo one shot
by deleting its `shot_NN.mp4`. Default voice: `en-US-AndrewMultilingualNeural` (set `"voice"` in plan.json to change).

## Step 4 — LOOK before delivering
Pull 3 frames (`ffmpeg -ss T -i final.mp4 -frames:v 1 f.jpg`) and Read them: captions readable, no
text-in-video artefacts, shots match the line. Then hand the user the mp4 path with the title + caption.
Posting is the user's call, through whatever scheduler they use.
