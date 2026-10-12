#!/usr/bin/env python3
"""Generate a CMX3600 EDL from cuts.json — imports into Premiere, Resolve,
Avid, FCP (via converters), and most pro NLEs.

Usage:
    python3 export_edl.py cuts.json /abs/output.edl
"""
import json
import sys


def tc(frames, fps):
    fpsi = round(fps)
    f = int(frames)
    return (f"{f // (3600 * fpsi):02d}:{f % (3600 * fpsi) // (60 * fpsi):02d}:"
            f"{f % (60 * fpsi) // fpsi:02d}:{f % fpsi:02d}")


def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    fps = spec["fps"]
    name = spec.get("sequence_name", "perfect cut")
    src_name = spec["source"].rsplit("/", 1)[-1]

    lines = [f"TITLE: {name}", "FCM: NON-DROP FRAME", ""]
    rec = 0
    for n, c in enumerate(spec["clips"], 1):
        dur = c["out_frame"] - c["in_frame"]
        lines.append(
            f"{n:03d}  AX       AA/V  C        "
            f"{tc(c['in_frame'], fps)} {tc(c['out_frame'], fps)} "
            f"{tc(rec, fps)} {tc(rec + dur, fps)}")
        lines.append(f"* FROM CLIP NAME: {src_name}")
        lines.append("")
        rec += dur
    open(out, "w").write("\n".join(lines) + "\n")
    print(f"{len(spec['clips'])} events -> {out}")


if __name__ == "__main__":
    main()
