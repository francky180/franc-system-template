#!/usr/bin/env python
"""Pick viral clip moments from transcript.txt using MiniMax (free NVIDIA NIM).
Replaces the manual Claude moment-picking step — $0 per call.

Usage: python pick_moments.py <transcript.txt> <outdir> [n_clips]
Writes <outdir>/segments.json  ->  [{"start":44.9,"end":79.0,"title":"slug","hook":"..."}]

Key: NVIDIA_API_KEY env (persisted). Model: NVIDIA_MINIMAX_MODEL or minimaxai/minimax-m2.7.
"""
import os, sys, json, re, urllib.request, urllib.error

transcript_path = sys.argv[1]
outdir = sys.argv[2]
n_clips = int(sys.argv[3]) if len(sys.argv) > 3 else 4

key = os.environ.get("NVIDIA_API_KEY")
assert key, "no NVIDIA_API_KEY in environment (run: setx NVIDIA_API_KEY \"nvapi-...\")"
model = os.environ.get("NVIDIA_MINIMAX_MODEL", "minimaxai/minimax-m2.7")

transcript = open(transcript_path, encoding="utf-8").read()
# Guard the prompt size — keep it well under context for long videos.
if len(transcript) > 48000:
    transcript = transcript[:48000]

prompt = f"""You are the viral-clip editor of OpusClip. Below is a timestamped transcript
(each line: [MM:SS-MM:SS] (start_seconds-end_seconds) text).

Pick the {n_clips} BEST standalone short-form clips. Each clip MUST:
- be 15-60 seconds long
- start at a clean sentence boundary (never mid-sentence)
- contain a hook + a complete thought/payoff (self-contained, makes sense alone)
- favor: bold claims, surprising facts, funny beats, clean question->answer, strong emotion

Return ONLY a JSON array, no prose, no markdown fences. Each item:
{{"start": <seconds float>, "end": <seconds float>, "title": "<kebab-case-slug>", "hook": "<scroll-stopping caption to post with the clip>"}}
Use the (start_seconds-end_seconds) numbers from the lines for start/end.

TRANSCRIPT:
{transcript}
"""

payload = {
    "model": model,
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3,
    "top_p": 0.95,
    "max_tokens": 16000,
    "stream": False,
}
req = urllib.request.Request(
    "https://integrate.api.nvidia.com/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "application/json"},
)
try:
    resp = json.loads(urllib.request.urlopen(req, timeout=240).read())  # M2.7 reasoning ~60-120s
except urllib.error.HTTPError as e:
    sys.exit(f"MiniMax HTTP {e.code}: {e.read().decode()[:400]}")

msg = resp["choices"][0]["message"]
# M2.7 is a reasoning model: answer is in `content`; if that's empty/truncated,
# the JSON may still be in `reasoning_content`. Try both.
content = (msg.get("content") or "") + "\n" + (msg.get("reasoning_content") or "")
# Strip any markdown fences; grab the LAST JSON array (the final answer, not an example).
matches = re.findall(r"\[\s*\{.*?\}\s*\]", content, re.DOTALL)
if not matches:
    sys.exit(f"No JSON array in model output (finish={resp['choices'][0].get('finish_reason')}):\n{content[:600]}")
segments = json.loads(matches[-1])

# Validate + clamp.
clean = []
for s in segments:
    try:
        st, en = float(s["start"]), float(s["end"])
    except (KeyError, TypeError, ValueError):
        continue
    if en <= st:
        continue
    if en - st > 75:           # hard cap so a clip never runs long
        en = st + 60
    title = re.sub(r"[^a-z0-9]+", "-", str(s.get("title", "clip")).lower()).strip("-")[:32] or "clip"
    clean.append({"start": round(st, 1), "end": round(en, 1), "title": title, "hook": str(s.get("hook", "")).strip()})

assert clean, "model returned no usable segments"
json.dump(clean, open(os.path.join(outdir, "segments.json"), "w", encoding="utf-8"), indent=2)
print(f"picked {len(clean)} moments via {model} -> {outdir}/segments.json")
for c in clean:
    print(f"  [{c['start']:.1f}-{c['end']:.1f}] {c['title']}  — {c['hook'][:60]}")
