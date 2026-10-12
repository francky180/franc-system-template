#!/usr/bin/env python3
"""Generate an SRT caption file aligned to the EDITED timeline from cuts.json.
Each kept clip becomes one subtitle spanning its place on the new timeline.
Useful for CapCut imports and as a sanity-read of the final cut.

Requires each clip in cuts.json to carry a "text" field.

Usage:
    python3 export_srt.py cuts.json /abs/output.srt
"""
import json
import sys


def ts(seconds):
    ms = int(round(seconds * 1000))
    return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    fps = spec["fps"]
    blocks, t = [], 0.0
    for n, c in enumerate(spec["clips"], 1):
        dur = (c["out_frame"] - c["in_frame"]) / fps
        text = c.get("text", "").strip()
        if text:
            blocks.append(f"{n}\n{ts(t)} --> {ts(t + dur)}\n{text}\n")
        t += dur
    open(out, "w").write("\n".join(blocks))
    print(f"{len(blocks)} captions -> {out}")


if __name__ == "__main__":
    main()
