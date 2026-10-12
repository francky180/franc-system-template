#!/usr/bin/env python3
"""Render a cuts.json to a single MP4 — frame-accurate, gapless.

Uses one ffmpeg filter_complex (trim + concat, full re-encode). Never use
stream-copy concat of separately encoded segments: timestamps glitch and
players show frozen frames (learned 2026-06-10).

Usage:
    python3 render_mp4.py cuts.json /abs/output.mp4
"""
import json
import subprocess
import sys


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    fps = spec["fps"]
    clips = spec["clips"]

    parts, vlabels, alabels = [], [], []
    for n, c in enumerate(clips):
        s, e = c["in_frame"] / fps, c["out_frame"] / fps
        parts.append(
            f"[0:v]trim=start={s:.4f}:end={e:.4f},setpts=PTS-STARTPTS[v{n}];"
            f"[0:a]atrim=start={s:.4f}:end={e:.4f},asetpts=PTS-STARTPTS[a{n}];")
        vlabels.append(f"[v{n}]")
        alabels.append(f"[a{n}]")
    fc = "".join(parts) + "".join(
        f"{v}{a}" for v, a in zip(vlabels, alabels)
    ) + f"concat=n={len(clips)}:v=1:a=1[outv][outa]"

    cmd = ["ffmpeg", "-nostdin", "-i", spec["source"],
           "-filter_complex", fc, "-map", "[outv]", "-map", "[outa]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
           "-y", out]
    subprocess.run(cmd, check=True, capture_output=True)
    total = sum(c["out_frame"] - c["in_frame"] for c in clips) / fps
    print(f"{len(clips)} clips, {total:.2f}s -> {out}")


if __name__ == "__main__":
    main()
