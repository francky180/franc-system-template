#!/usr/bin/env python3
"""Build a speech map for a talking-head clip: waveform-accurate speech blocks
with the transcript words that fall inside each block.

Usage:
    python3 speech_map.py <video_path> <whisper_json_path> [--out map.json]

Output JSON:
{
  "source": "/abs/path.mp4", "fps": 30.0, "width": 1920, "height": 1080,
  "duration": 106.93, "samplerate": 48000,
  "blocks": [
    {"i": 0, "start": 16.387, "end": 19.418, "onset": 16.3878,
     "text": "Canada has joined the AI arms race,",
     "gap_after": 1.30},
    ...
  ]
}

start/end come from the sensitive pass (-38dB) — full speech envelope incl. tails.
onset comes from the hard pass (-30dB) — first frame of actual voice, breath-proof.
gap_after is the silence between this block and the next (seconds).
"""
import json
import re
import subprocess
import sys

MIN_SILENCE = "0.25"     # silences shorter than this stay inside a block

# LOCKED defaults — hand-tuned and frame-verified on reference footage
# 2026-06-10. These are absolute and proven; they are ALWAYS tried first.
IN_DB = "-30dB"          # starts: ignores breaths/mouth noise
OUT_DB = "-38dB"         # ends: catches soft word tails

# Rescue calibration (used ONLY when the locked defaults produce a degenerate
# map — see is_degenerate). Thresholds anchor to the speaker's level (p90 of
# windowed RMS). Offsets reproduce -30/-38 on the reference footage.
IN_OFFSET = 14
OUT_OFFSET = 22
FLOOR_GUARD = 10


def flag(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def calibrate(path):
    """Measure windowed RMS (0.1s @ 48k) and derive thresholds from the
    speaker's level. Returns (in_db, out_db) as strings like '-30dB'."""
    import tempfile
    tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False).name
    subprocess.run(
        ["ffmpeg", "-nostdin", "-i", path,
         "-af", f"asetnsamples=n=4800,astats=metadata=1:reset=1,"
                f"ametadata=print:key=lavfi.astats.Overall.RMS_level:file={tmp}",
         "-f", "null", "-"], capture_output=True)
    vals = sorted(float(m) for m in
                  re.findall(r"RMS_level=(-?[\d.]+)", open(tmp).read()))
    if len(vals) < 20:
        return "-30dB", "-38dB"  # too short to calibrate; reference defaults
    speech = vals[int(len(vals) * 0.90)]
    floor = vals[int(len(vals) * 0.10)]
    out_db = max(speech - OUT_OFFSET, floor + FLOOR_GUARD)
    in_db = max(speech - IN_OFFSET, out_db + 6)
    return f"{in_db:.0f}dB", f"{out_db:.0f}dB"


def ffprobe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,r_frame_rate,width,height,sample_rate:format=duration",
         "-of", "json", path],
        capture_output=True, text=True, check=True).stdout
    info = json.loads(out)
    meta = {"duration": float(info["format"]["duration"])}
    for s in info["streams"]:
        if s["codec_type"] == "video":
            num, den = s["r_frame_rate"].split("/")
            meta["fps"] = int(num) / int(den)
            meta["width"], meta["height"] = s["width"], s["height"]
        elif s["codec_type"] == "audio":
            meta["samplerate"] = int(s.get("sample_rate", 48000))
    return meta


def silences(path, noise):
    out = subprocess.run(
        ["ffmpeg", "-nostdin", "-i", path,
         "-af", f"silencedetect=noise={noise}:d={MIN_SILENCE}", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", out)]
    return starts, ends


def is_degenerate(blocks, duration):
    """True when a block map can't be real speech structure: everything is one
    giant block (thresholds below the noise floor) or speech is shredded into
    confetti (thresholds above the speaker's level)."""
    if not blocks:
        return True
    speech = sum(e - s for s, e in blocks)
    if speech > 0.95 * duration:        # silences never detected
        return True
    tiny = sum(1 for s, e in blocks if e - s < 0.4)
    return len(blocks) > 10 and tiny / len(blocks) > 0.7   # fragment confetti


def speech_blocks(sil_starts, sil_ends, duration):
    """Invert the silence list into speech intervals."""
    blocks, cursor = [], 0.0
    events = sorted([(t, "s") for t in sil_starts] + [(t, "e") for t in sil_ends])
    in_silence = False
    for t, kind in events:
        if kind == "s" and not in_silence:
            if t - cursor > 0.05:
                blocks.append([cursor, t])
            in_silence = True
        elif kind == "e":
            cursor = t
            in_silence = False
    if not in_silence and duration - cursor > 0.05:
        blocks.append([cursor, duration])
    return blocks


def main():
    video, whisper_json = sys.argv[1], sys.argv[2]
    out_path = flag("--out", "speech_map.json")
    in_db = flag("--in-db", IN_DB)
    out_db = flag("--out-db", OUT_DB)

    meta = ffprobe(video)
    sens_starts, sens_ends = silences(video, out_db)
    hard_starts, hard_ends = silences(video, in_db)
    blocks = speech_blocks(sens_starts, sens_ends, meta["duration"])

    if is_degenerate(blocks, meta["duration"]) and "--in-db" not in sys.argv:
        in_db, out_db = calibrate(video)
        print(f"locked thresholds produced a degenerate map — "
              f"rescue calibration: in {in_db} / out {out_db}")
        sens_starts, sens_ends = silences(video, out_db)
        hard_starts, hard_ends = silences(video, in_db)
        blocks = speech_blocks(sens_starts, sens_ends, meta["duration"])
    else:
        print(f"thresholds: in {in_db} / out {out_db} (locked defaults)")
    onsets = sorted(hard_ends)  # -30dB silence_end == voice onset

    words = []
    tx = json.load(open(whisper_json))
    for seg in tx.get("segments", []):
        for w in seg.get("words", []):
            if "start" in w:
                words.append((w["start"], w.get("word", "").strip()))

    result = []
    for i, (bs, be) in enumerate(blocks):
        onset = next((o for o in onsets if bs - 0.05 <= o <= be), bs)
        text = " ".join(w for t, w in words if bs - 0.15 <= t < be + 0.05)
        gap = round(blocks[i + 1][0] - be, 3) if i + 1 < len(blocks) else None
        result.append({"i": i, "start": round(bs, 4), "end": round(be, 4),
                       "onset": round(onset, 4), "text": text, "gap_after": gap})

    meta.update({"source": video, "blocks": result})
    json.dump(meta, open(out_path, "w"), indent=1)
    print(f"{len(result)} speech blocks -> {out_path}")
    for b in result:
        print(f"  [{b['i']:2d}] {b['start']:8.2f}-{b['end']:8.2f}  {b['text'][:80]}")


if __name__ == "__main__":
    main()
