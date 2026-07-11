---
name: clip
description: Turn a long video (YouTube link or local file) into short vertical captioned clips — OpusClip + Submagic style. Use when the user says "clip this", "make shorts/reels from", "find the best moments", or drops a long video/podcast/interview to repurpose.
---

# /clip — long video → viral vertical clips

Replicates OpusClip (find viral moments + reframe to 9:16) + Submagic (animated burned captions) using ffmpeg + Groq Whisper + AI moment-selection. Free, $0 per clip. Center/blurred-bg framing; true face-tracking needs a GPU box (mediapipe).

## Prerequisites (one-time)
- Python 3.10+, ffmpeg on PATH, `pip install yt-dlp`
- `GROQ_API_KEY` env or in `~/.config/watch/.env` (free key: console.groq.com) — Whisper transcription
- `NVIDIA_API_KEY` env (free key: build.nvidia.com) — MiniMax moment-picking

## Flow

**Step 1 — Prepare (download + transcribe).**
```
WORK=~/Downloads/_clip   # or any temp dir
mkdir -p "$WORK" && cd "$WORK"
# Local file: copy to source.mp4. YouTube/URL:
python -m yt_dlp --no-warnings -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" -o "source.%(ext)s" "<URL>"
ffmpeg -hide_banner -y -i source.mp4 -vn -ac 1 -ar 16000 -b:a 64k audio.mp3
python "<SKILL_DIR>/scripts/transcribe.py" audio.mp3 .
```
(`<SKILL_DIR>` = this skill's folder under your `~/.claude/skills/clip`. If the yt-dlp bin shim is blocked on Windows, `python -m yt_dlp` always works.)

**Step 2 — Pick moments (MiniMax does this — free, the "AI" of OpusClip).**
```
python "<SKILL_DIR>/scripts/pick_moments.py" transcript.txt . 4
```
This calls MiniMax M2.7 (free NVIDIA NIM, `NVIDIA_API_KEY` env) to read `transcript.txt` and write `segments.json` — 3–5 self-contained scroll-stopping segments (hook + payoff, 15–60s, clean sentence starts). $0 per call. Output shape:
```json
[{"start": 44.9, "end": 79.0, "title": "is-time-real", "hook": "Is time permanent?"}]
```
(Last arg = number of clips, default 4. Fallback: if the model is down, Claude can still `Read` transcript.txt and hand-write `segments.json` in the same shape.)

**Step 3 — Render.**
```
python "<SKILL_DIR>/scripts/render_clips.py" source.mp4 words.json segments.json .
```
Outputs `clip_NN_slug.mp4` — 1080x1920, blurred-bg framing (both speakers stay visible), big Arial-Black reel captions with pop-in, synced word-groups.

**Step 4 — Deliver.** Move finished `clip_*.mp4` to `Downloads/`, clean the temp dir, open one for review, and give the user a posting line per clip (the `hook`).

## Notes
- Caption position/size: edit the `Style: Reel` line in `render_clips.py` (Fontsize, MarginV).
- Framing style is blurred-background (best for 2-person talks). For solo/single-subject, a center-crop variant can be swapped into the filtergraph.
- On a GPU box: add mediapipe/opencv for face-tracking reframe; same scripts otherwise.
