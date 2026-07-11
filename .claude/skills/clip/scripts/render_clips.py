#!/usr/bin/env python
"""Render vertical captioned clips from a source video.
Usage: python render_clips.py <source.mp4> <words.json> <segments.json> <outdir>
segments.json = [{"start":sec,"end":sec,"title":"slug","hook":"..."}]
Output: <outdir>/clip_01_slug.mp4 ... (1080x1920, blurred-bg framing, burned reel captions)"""
import os, sys, json, subprocess, re

source, words_path, segs_path, outdir = sys.argv[1:5]
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
    vf = ("[0:v]split=2[bg][fg];"
          "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=22[bgb];"
          "[fg]scale=1080:-2[fgs];"
          "[bgb][fgs]overlay=(W-w)/2:(H-h)/2[v];"
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
