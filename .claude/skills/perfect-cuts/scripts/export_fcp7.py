#!/usr/bin/env python3
"""Generate a gapless FCP7 XML (xmeml v5) timeline from a cut list.
Imports into Premiere Pro (File > Import), DaVinci Resolve (File > Import Timeline),
and FCP via conversion.

Usage:
    python3 export_fcp7.py cuts.json

cuts.json:
{
  "source": "/abs/path/clip.mp4",
  "fps": 30.0, "width": 1920, "height": 1080, "samplerate": 48000,
  "sequence_name": "clip perfect cut",
  "output": "/abs/out.xml",
  "clips": [{"in_frame": 491, "out_frame": 584}, ...]   // source frames
}

Clips are laid back-to-back from frame 0 — zero gap space by construction.
"""
import json
import math
import sys
import urllib.parse
import uuid

# NTSC rates map to their integer timebase with ntsc=TRUE
NTSC = {23.976: 24, 29.97: 30, 59.94: 60}


def rate_info(fps):
    for ntsc_fps, tb in NTSC.items():
        if abs(fps - ntsc_fps) < 0.01:
            return tb, "TRUE"
    return round(fps), "FALSE"


def file_block(src_name, pathurl, tb, ntsc, src_frames, w, h, sr, indent, video=True):
    pad = " " * indent
    video_chars = f"""{pad}    <video>
{pad}      <samplecharacteristics>
{pad}        <rate><timebase>{tb}</timebase><ntsc>{ntsc}</ntsc></rate>
{pad}        <width>{w}</width>
{pad}        <height>{h}</height>
{pad}        <anamorphic>FALSE</anamorphic>
{pad}        <pixelaspectratio>square</pixelaspectratio>
{pad}        <fielddominance>none</fielddominance>
{pad}      </samplecharacteristics>
{pad}    </video>
""" if video else ""
    return f"""{pad}<file id="file-1">
{pad}  <name>{src_name}</name>
{pad}  <pathurl>{pathurl}</pathurl>
{pad}  <rate><timebase>{tb}</timebase><ntsc>{ntsc}</ntsc></rate>
{pad}  <duration>{src_frames}</duration>
{pad}  <media>
{video_chars}{pad}    <audio>
{pad}      <samplecharacteristics>
{pad}        <samplerate>{sr}</samplerate>
{pad}        <sampledepth>16</sampledepth>
{pad}      </samplecharacteristics>
{pad}    </audio>
{pad}  </media>
{pad}</file>"""


def links(n):
    return f"""            <link>
              <linkclipref>clipitem-video-{n}</linkclipref>
              <mediatype>video</mediatype>
              <trackindex>1</trackindex>
              <clipindex>{n}</clipindex>
            </link>
            <link>
              <linkclipref>clipitem-audio-{n}</linkclipref>
              <mediatype>audio</mediatype>
              <trackindex>1</trackindex>
              <clipindex>{n}</clipindex>
              <groupindex>1</groupindex>
            </link>"""


def main():
    spec = json.load(open(sys.argv[1]))
    src = spec["source"]
    fps = spec["fps"]
    tb, ntsc = rate_info(fps)
    w, h, sr = spec["width"], spec["height"], spec.get("samplerate", 48000)
    src_name = src.rsplit("/", 1)[-1]
    stem = src_name.rsplit(".", 1)[0]
    seq_name = spec.get("sequence_name", f"{stem} perfect cut")
    pathurl = "file://" + urllib.parse.quote(src)
    src_frames = spec.get("source_frames", 0) or int(math.ceil(spec.get("source_duration", 0) * fps))

    vitems, aitems, timeline = [], [], 0
    for n, c in enumerate(spec["clips"], 1):
        dur = c["out_frame"] - c["in_frame"]
        start, end = timeline, timeline + dur
        timeline = end
        common = f"""            <name>{stem}</name>
            <enabled>TRUE</enabled>
            <duration>{dur}</duration>
            <start>{start}</start>
            <end>{end}</end>
            <in>{c["in_frame"]}</in>
            <out>{c["out_frame"]}</out>"""
        vitems.append(f"""          <clipitem id="clipitem-video-{n}">
{common}
{file_block(src_name, pathurl, tb, ntsc, src_frames, w, h, sr, 12)}
            <sourcetrack>
              <mediatype>video</mediatype>
              <trackindex>1</trackindex>
            </sourcetrack>
{links(n)}
          </clipitem>""")
        aitems.append(f"""          <clipitem id="clipitem-audio-{n}">
{common}
{file_block(src_name, pathurl, tb, ntsc, src_frames, w, h, sr, 12, video=False)}
            <sourcetrack>
              <mediatype>audio</mediatype>
              <trackindex>1</trackindex>
            </sourcetrack>
            <channelcount>2</channelcount>
{links(n)}
          </clipitem>""")

    uid = str(uuid.uuid4())
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="5">
  <sequence id="sequence-{uid}">
    <uuid>{uid}</uuid>
    <name>{seq_name}</name>
    <duration>{timeline}</duration>
    <rate><timebase>{tb}</timebase><ntsc>{ntsc}</ntsc></rate>
    <in>0</in>
    <out>{timeline}</out>
    <timecode>
      <rate><timebase>{tb}</timebase><ntsc>{ntsc}</ntsc></rate>
      <frame>0</frame>
      <displayformat>NDF</displayformat>
    </timecode>
    <media>
      <video>
        <format>
          <samplecharacteristics>
            <rate><timebase>{tb}</timebase><ntsc>{ntsc}</ntsc></rate>
            <width>{w}</width>
            <height>{h}</height>
            <anamorphic>FALSE</anamorphic>
            <pixelaspectratio>square</pixelaspectratio>
            <fielddominance>none</fielddominance>
          </samplecharacteristics>
        </format>
        <track>
{chr(10).join(vitems)}
        </track>
      </video>
      <audio>
        <numOutputChannels>2</numOutputChannels>
        <format>
          <samplecharacteristics>
            <samplerate>{sr}</samplerate>
            <sampledepth>16</sampledepth>
          </samplecharacteristics>
        </format>
        <track>
{chr(10).join(aitems)}
        </track>
      </audio>
    </media>
  </sequence>
</xmeml>
"""
    out = spec["output"]
    open(out, "w").write(xml)
    secs = timeline / fps
    print(f"{len(spec['clips'])} clips, {secs:.2f}s -> {out}")


if __name__ == "__main__":
    main()
