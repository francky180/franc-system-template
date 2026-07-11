#!/usr/bin/env python
"""Transcribe an audio file with Groq Whisper (word-level timestamps).
Usage: python transcribe.py <audio.mp3> <outdir>
Writes <outdir>/words.json (list of {word,start,end}) and <outdir>/transcript.txt (timestamped, readable)."""
import os, sys, json, urllib.request, urllib.error

audio_path, outdir = sys.argv[1], sys.argv[2]

key = None
for envpath in (os.path.expanduser("~/.config/watch/.env"),):
    if os.path.exists(envpath):
        for line in open(envpath):
            if line.strip().startswith("GROQ_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip()
key = key or os.environ.get("GROQ_API_KEY")
assert key, "no GROQ_API_KEY found (~/.config/watch/.env or env)"

boundary = "----phimindflowclip"
def field(name, value):
    return (f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n').encode()
body = field("model", "whisper-large-v3")
body += field("response_format", "verbose_json")
body += field("timestamp_granularities[]", "word")
body += field("timestamp_granularities[]", "segment")
body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\n'
         f'Content-Type: audio/mpeg\r\n\r\n').encode() + open(audio_path, "rb").read() + b"\r\n"
body += f"--{boundary}--\r\n".encode()

req = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", data=body,
    headers={"Authorization": f"Bearer {key}", "User-Agent": "Mozilla/5.0 phimindflow-clip",
             "Accept": "application/json", "Content-Type": f"multipart/form-data; boundary={boundary}"})
resp = json.loads(urllib.request.urlopen(req, timeout=300).read())

words = resp.get("words") or []
segs = resp.get("segments") or []
json.dump(words, open(os.path.join(outdir, "words.json"), "w"))

# readable timestamped transcript (segment-level) for Claude to pick moments
def mmss(t):
    return f"{int(t//60):02d}:{int(t%60):02d}"
with open(os.path.join(outdir, "transcript.txt"), "w", encoding="utf-8") as f:
    for s in segs:
        f.write(f"[{mmss(s['start'])}-{mmss(s['end'])}] ({s['start']:.1f}-{s['end']:.1f}) {s['text'].strip()}\n")
print(f"words={len(words)} segments={len(segs)} -> {outdir}/words.json + transcript.txt")
