# Upscaling video and images (Topaz)

The `upscale` command makes an existing video or image sharper and higher-resolution via Topaz on Fal.

```bash
python3 ~/.claude/skills/media-gen/scripts/generate.py upscale \
  --input "<path to source video or image>" \
  [--target-height 1080] \
  [--factor 2] \
  [--fps 30] \
  [--type video|image] \
  [--model <model-key>]
```

(Windows: `python` + full script path.)

**Requires ffmpeg/ffprobe** for dimension probing and the `--fps` re-encode. Without it, pass `--factor` explicitly.

**How it avoids stretching (important).** The script reads the source dimensions with ffprobe and applies a *single* `upscale_factor` to both axes. It never hard-sets a width and height, so the aspect ratio is always preserved. (Forcing a non-16:9 source into a fixed 1920x1080 is the #1 cause of stretched upscales; this script cannot do that.)

- `--target-height` (default 1080): factor is computed from the source height to hit this.
- `--factor`: explicit multiplier instead; takes precedence over target-height.
- Input type is inferred from the extension; force with `--type` if needed.

## Cost rules — quote video upscales before running

Topaz video bills per second of output:

- up to 720p: ~$0.01/s
- 720p to 1080p: ~$0.02/s
- above 1080p: ~$0.08/s
- **Price DOUBLES if the output is 60fps.**

For a 60fps source going to 1080p, either accept the doubled rate or pass `--fps 30` to re-encode the source to 30fps first (the script does this locally before upload, halving the cost). State the math (`$/s x seconds = $total`) and wait for an explicit yes, same as the video-gen rule. **Image upscales are cheap (per-image, not per-second) and run autonomously.**

## Reality check to set expectations

Upscaling sharpens and cleans; it does not invent detail that was never captured. A very soft or low-bitrate source comes out cleaner but won't become true crisp HD. Best on footage that's already decent but just low-resolution.

Output saves as `upscaled-NN.mp4` / `upscaled-NN.png` in a dated folder, with `prompt.md` recording the source dimensions and factor used.
