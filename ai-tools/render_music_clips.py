"""Vertical music clips — 9:16 blurred-bg reframe, NO burned captions.

    python render_music_clips.py <source.mp4> <segments.json> <outdir> <prefix>

Captions are deliberately omitted. Auto-transcription of Haitian Creole (and most
low-resource languages) comes back as garbled French, and wrong lyrics burned over
an artist's own record is worse than no lyrics at all. Add captions only from
lyrics supplied by the artist.
"""
import json
import os
import re
import subprocess
import sys

source, segs_path, outdir, prefix = sys.argv[1:5]
style = sys.argv[5] if len(sys.argv) > 5 else "blur"
segs = json.load(open(segs_path, encoding="utf-8"))
os.makedirs(outdir, exist_ok=True)

STYLES = {
    # whole frame kept, blurred fill above/below — nothing is ever cropped out
    "blur": ("[0:v]split=2[bg][fg];"
             "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=22[bgb];"
             "[fg]scale=1080:-2[fgs];"
             "[bgb][fgs]overlay=(W-w)/2:(H-h)/2[outv]"),
    # full-bleed punch-in — fills the phone, but cuts the left/right of the frame
    "punch": ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
              "crop=1080:1920[outv]"),
    # compromise: bigger foreground (78% width) over the blurred bed
    "hybrid": ("[0:v]split=2[bg][fg];"
               "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=26[bgb];"
               "[fg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1400:788,scale=1080:-2[fgs];"
               "[bgb][fgs]overlay=(W-w)/2:(H-h)/2[outv]"),
}
VF = STYLES[style]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:30]


made = []
for i, seg in enumerate(segs, 1):
    a, b = float(seg["start"]), float(seg["end"])
    tag = "" if style == "blur" else f"_{style}"
    out = f"{prefix}_{i:02d}_{slug(seg.get('title', f'clip{i}'))}{tag}.mp4"
    cmd = ["ffmpeg", "-hide_banner", "-y", "-ss", str(a), "-to", str(b),
           "-i", os.path.abspath(source),
           "-filter_complex", VF, "-map", "[outv]", "-map", "0:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", out]
    r = subprocess.run(cmd, cwd=outdir, capture_output=True, text=True)
    if r.returncode == 0:
        made.append(out)
        print(f"OK {out}  ({b - a:.0f}s)")
    else:
        tail = r.stderr.strip().splitlines()[-1] if r.stderr else "?"
        print(f"FAIL {out}: {tail}")

print(f"\n{len(made)}/{len(segs)} clips -> {outdir}")
