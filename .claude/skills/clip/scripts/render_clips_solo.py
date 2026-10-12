#!/usr/bin/env python
"""Render vertical captioned clips from a source video.
Usage: python render_clips.py <source.mp4> <words.json> <segments.json> <outdir>
segments.json = [{"start":sec,"end":sec,"title":"slug","hook":"..."}]
Output: <outdir>/clip_01_slug.mp4 ... (1080x1920, SOLO-SUBJECT centre crop, burned reel captions)

Use this instead of render_clips.py when only ONE person is on camera. The
blurred-background version letterboxes a 16:9 frame into 9:16, which leaves the
speaker occupying only the middle third of a phone screen. This crops to 9:16
and fills the frame, so the subject is roughly 3x larger.

Optional 5th arg: horizontal crop centre as a 0-1 fraction (default 0.5).
Use it when the speaker is not dead centre, e.g. 0.42 nudges the crop left."""
import os, sys, json, subprocess, re

source, words_path, segs_path, outdir = sys.argv[1:5]
CX = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5   # crop centre, 0-1
words = json.load(open(words_path))
segs = json.load(open(segs_path))

def ts(t):
    h=int(t//3600); m=int((t%3600)//60); s=t%60
    return f"{h:01d}:{m:02d}:{s:05.2f}"

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Reel, Arial Black, 76, &H00FFFFFF, &H000014FF, &H00000000, &H64000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 7, 4, 2, 70, 70, 540, 1

[Events]
Format: Layer, Start, End, Style, MarginL, MarginR, MarginV, Effect, Text
"""

def slug(s):
    return re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')[:30]

made=[]
for i, seg in enumerate(segs, 1):
    a, b = float(seg["start"]), float(seg["end"])
    sg = slug(seg.get("title", f"clip{i}"))
    ass_path = os.path.join(outdir, f"_clip_{i}.ass")
    # words in range, grouped 3 per caption, offset to clip start
    inr = [w for w in words if w.get("start") is not None and w["end"] > a and w["start"] < b]
    chunks, cur = [], []
    for w in inr:
        cur.append(w)
        if len(cur) >= 3:
            chunks.append(cur); cur=[]
    if cur: chunks.append(cur)
    lines=[]
    for ch in chunks:
        st=max(0, ch[0]["start"]-a); en=max(st+0.3, ch[-1]["end"]-a)
        txt=" ".join(w["word"].strip().upper() for w in ch).replace("\n"," ")
        eff="{\\fad(50,30)\\t(0,110,\\fscx114\\fscy114)\\t(110,190,\\fscx100\\fscy100)}"
        lines.append(f"Dialogue: 0,{ts(st)},{ts(en)},Reel,70,70,540,,{eff}{txt}")
    open(ass_path,"w",encoding="utf-8").write(ASS_HEAD+"\n".join(lines)+"\n")

    out = os.path.join(outdir, f"clip_{i:02d}_{sg}.mp4")
    ass_rel = os.path.basename(ass_path)
    # Crop a 9:16 window out of the 16:9 source and fill the frame with it.
    # cw = ih*9/16; x is clamped so the window can never run off the edge.
    vf = (f"[0:v]crop=ih*9/16:ih:'clip((iw-ih*9/16)*{CX},0,iw-ih*9/16)':0,"
          f"scale=1080:1920,setsar=1[v];"
          f"[v]subtitles={ass_rel}[outv]")
    cmd=["ffmpeg","-hide_banner","-y","-ss",str(a),"-to",str(b),"-i",os.path.abspath(source),
         "-filter_complex",vf,"-map","[outv]","-map","0:a",
         "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
         "-c:a","aac","-b:a","160k",os.path.basename(out)]
    r=subprocess.run(cmd, cwd=outdir, capture_output=True, text=True)
    if r.returncode==0:
        made.append(out); print(f"OK clip {i}: {os.path.basename(out)}  ({b-a:.0f}s)")
    else:
        print(f"FAIL clip {i}: {r.stderr.strip().splitlines()[-1] if r.stderr else '?'}")
print(f"\n{len(made)}/{len(segs)} clips rendered to {outdir}")
