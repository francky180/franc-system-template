#!/usr/bin/env python
"""Transcribe a long audio file with Groq Whisper by splitting it first.

The stock transcribe.py posts the whole file, which 413s past Groq's upload cap —
a 110-minute podcast is ~52MB. This splits into fixed-length chunks, transcribes
each, and shifts every timestamp back into whole-file time so words.json and
transcript.txt are byte-compatible with what render_clips.py expects.

Usage: python transcribe_chunked.py <audio.mp3> <outdir> [chunk_seconds]
"""
import os, sys, json, subprocess, urllib.request, urllib.error, glob, time

audio_path, outdir = sys.argv[1], sys.argv[2]
CHUNK = int(sys.argv[3]) if len(sys.argv) > 3 else 720  # 12 min

key = None
envpath = os.path.expanduser("~/.config/watch/.env")
if os.path.exists(envpath):
    for line in open(envpath):
        if line.strip().startswith("GROQ_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"').strip()
key = key or os.environ.get("GROQ_API_KEY")
assert key, "no GROQ_API_KEY found"

chunkdir = os.path.join(outdir, "_chunks")
os.makedirs(chunkdir, exist_ok=True)
for old in glob.glob(os.path.join(chunkdir, "*.mp3")):
    os.remove(old)

# 48kbps mono is ample for speech recognition and keeps every chunk far under the cap.
print(f"splitting into {CHUNK}s chunks...", flush=True)
subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", audio_path,
    "-f", "segment", "-segment_time", str(CHUNK), "-ac", "1", "-ar", "16000",
    "-b:a", "48k", os.path.join(chunkdir, "part_%03d.mp3"),
], check=True)

parts = sorted(glob.glob(os.path.join(chunkdir, "part_*.mp3")))
print(f"{len(parts)} chunks", flush=True)

def transcribe(path):
    boundary = "----clipboundary"
    def field(name, value):
        return (f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n').encode()
    body = field("model", "whisper-large-v3")
    body += field("response_format", "verbose_json")
    body += field("timestamp_granularities[]", "word")
    body += field("timestamp_granularities[]", "segment")
    body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\n'
             f'Content-Type: audio/mpeg\r\n\r\n').encode() + open(path, "rb").read() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/audio/transcriptions", data=body,
        headers={"Authorization": f"Bearer {key}", "User-Agent": "Mozilla/5.0 clip-skill",
                 "Accept": "application/json",
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    return json.loads(urllib.request.urlopen(req, timeout=600).read())

all_words, all_segs = [], []
for i, p in enumerate(parts):
    offset = i * CHUNK
    for attempt in range(3):
        try:
            r = transcribe(p)
            break
        except urllib.error.HTTPError as e:
            # 429 = rate limited; back off rather than dropping a chunk, because a
            # missing chunk would silently shift nothing but lose that whole window.
            if e.code in (429, 503) and attempt < 2:
                wait = 20 * (attempt + 1)
                print(f"  chunk {i}: HTTP {e.code}, retrying in {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise
    for w in (r.get("words") or []):
        all_words.append({"word": w["word"], "start": w["start"] + offset, "end": w["end"] + offset})
    for s in (r.get("segments") or []):
        all_segs.append({"start": s["start"] + offset, "end": s["end"] + offset, "text": s["text"]})
    print(f"  chunk {i+1}/{len(parts)} ok  (+{offset}s)  words={len(r.get('words') or [])}", flush=True)

json.dump(all_words, open(os.path.join(outdir, "words.json"), "w"))

def mmss(t):
    return f"{int(t//60):02d}:{int(t%60):02d}"

with open(os.path.join(outdir, "transcript.txt"), "w", encoding="utf-8") as f:
    for s in all_segs:
        f.write(f"[{mmss(s['start'])}-{mmss(s['end'])}] ({s['start']:.1f}-{s['end']:.1f}) {s['text'].strip()}\n")

print(f"words={len(all_words)} segments={len(all_segs)} -> {outdir}/words.json + transcript.txt")
