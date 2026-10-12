#!/usr/bin/env python
"""Pick viral clip moments from transcript.txt using a free NVIDIA NIM model.
Replaces the manual Claude moment-picking step — $0 per call.

Usage: python pick_moments.py <transcript.txt> <outdir> [n_clips]
Writes <outdir>/segments.json  ->  [{"start":44.9,"end":79.0,"title":"slug","hook":"..."}]

TWO THINGS THIS FIXES (2026-09-14)
----------------------------------
1. MODEL EOL. minimax-m2.7 died 2026-07-27, minimax-m3 died 2026-09-09, and
   there is now no minimax on NIM at all. Hardcoding one model guarantees this
   breaks again, so the model is RESOLVED AT RUNTIME from a preference list.
   ⚠️ A model can be listed by /v1/models and still 404 on invoke (both
   nemotron entries did on 2026-09-14) — so candidates are PROBED with a real
   call, never trusted from the listing.

2. SILENT TRUNCATION. The old version cut the transcript at 48,000 chars and
   picked every clip from the opening stretch — on a 92-minute podcast that was
   the first ~31%, and the back hour was never seen. Now the transcript is split
   into WINDOWS, each window is asked for its own best moments, and the results
   are merged and ranked. Coverage is the whole video.

Key: NVIDIA_API_KEY env. Override the model with NVIDIA_CLIP_MODEL if you want.
"""
import os, sys, json, re, math, urllib.request, urllib.error

# Hooks routinely contain emoji, and Windows stdout defaults to cp1252 — printing
# one raised UnicodeEncodeError AFTER segments.json was already written, which made
# a successful run look like a crash. Force UTF-8 on stdout instead.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

transcript_path = sys.argv[1]
outdir = sys.argv[2]
n_clips = int(sys.argv[3]) if len(sys.argv) > 3 else 4

KEY = os.environ.get("NVIDIA_API_KEY")
assert KEY, 'no NVIDIA_API_KEY in environment (run: setx NVIDIA_API_KEY "nvapi-...")'

API = "https://integrate.api.nvidia.com/v1"
WINDOW = 40000          # chars per window — well inside context, leaves room for the reply
# Order is MEASURED, not guessed (2026-09-14, 19k-char prompt, max_tokens=2000):
#   openai/gpt-oss-20b            17s   <- 4.6x faster, so it leads
#   deepseek-v4-flash-0731        79s
# 2026-10-10: deepseek-v4-flash-0731, gpt-oss-120b, qwen3-next, llama-4-maverick all return 410 Gone.
# Live that night: gpt-oss-20b (10s WITH reasoning_effort=low), deepseek-v4.1-flash, glm-5.3-flash, kimi-k2.6.
CANDIDATES = [
    "openai/gpt-oss-20b",
    "deepseek-ai/deepseek-v4.1-flash",
    "z-ai/glm-5.3-flash",
    "moonshotai/kimi-k2.6",
    "mistralai/mistral-large-2-instruct",
]


def call(model, prompt, max_tokens=2500, timeout=300):
    # 🚨 max_tokens is a TIME budget here, not just a size cap. These are reasoning
    # models and they spend the whole allowance thinking: at 16000 deepseek ran
    # past 300s and timed out on every window, which is why the first run of this
    # rewrite returned 2 clips instead of 4. We need a ~300-char JSON array, so
    # 2500 is generous. Do not raise it.
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.3, "top_p": 0.95, "max_tokens": max_tokens, "stream": False}
    # 🚨 2026-10-10: without this, gpt-oss-20b spent all 2500 (and 6000) tokens reasoning,
    # finish=length, content '' -> "0 candidates" on EVERY window. With it: 10s, valid JSON.
    if model.startswith("openai/gpt-oss"):
        payload["reasoning_effort"] = "low"
    req = urllib.request.Request(
        API + "/chat/completions", data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
                 "Accept": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    msg = resp["choices"][0]["message"]
    # Reasoning models put the answer in `content`; if that is empty or truncated
    # the JSON may still be sitting in `reasoning_content`. Try both.
    return (msg.get("content") or "") + "\n" + (msg.get("reasoning_content") or "")


def resolve_model():
    """Pick the first candidate that ACTUALLY ANSWERS. Listing is not enough."""
    forced = os.environ.get("NVIDIA_CLIP_MODEL")
    order = ([forced] if forced else []) + CANDIDATES
    live = set()
    try:
        req = urllib.request.Request(API + "/models", headers={"Authorization": f"Bearer {KEY}"})
        live = {m["id"] for m in json.loads(urllib.request.urlopen(req, timeout=60).read()).get("data", [])}
    except Exception:
        pass                                   # listing is a hint, not a gate
    for m in order:
        if live and m not in live and m != forced:
            continue
        try:
            out = call(m, 'Reply with ONLY this JSON array and nothing else: [{"ok":1}]',
                       max_tokens=60, timeout=60)
            if "{" in out:
                return m
        except Exception:
            continue
    sys.exit("No working NIM model. List them with:\n"
             f'  curl -s {API}/models -H "Authorization: Bearer $NVIDIA_API_KEY"\n'
             "then set NVIDIA_CLIP_MODEL to one that answers.")


def parse_segments(text):
    """Grab the LAST JSON array in the reply (the answer, not an echoed example)."""
    for m in reversed(re.findall(r"\[\s*\{.*?\}\s*\]", text, re.DOTALL)):
        try:
            return json.loads(m)
        except json.JSONDecodeError:
            continue
    return []


def windows(text, size):
    """Split on line boundaries so a window never starts mid-timestamp."""
    lines, out, cur, n = text.splitlines(True), [], [], 0
    for ln in lines:
        cur.append(ln); n += len(ln)
        if n >= size:
            out.append("".join(cur)); cur, n = [], 0
    if cur:
        if out and n < size * 0.35:            # fold a runt tail into the previous window
            out[-1] += "".join(cur)
        else:
            out.append("".join(cur))
    return out or [text]


# 🚨 KEEP THIS PROMPT SHORT. Measured 2026-09-14 on a 40k-char window:
#   terse prompt (below)          13s, finish=stop, valid JSON
#   verbose prompt w/ rules list  TIMED OUT past 300s
# These are reasoning models — every extra instruction is another thing they
# deliberate about, and the deliberation is charged against max_tokens, so a
# "more thorough" prompt produces LESS output, not more. Do not pad it.
PROMPT = """Pick the {k} BEST standalone 15-60 second clips IN THIS SECTION.
Each must start at a clean sentence boundary and contain a hook plus a complete payoff.
Favour bold claims, surprising numbers, funny beats, strong emotion.
{brain}
Answer immediately. Do not deliberate. Return ONLY a JSON array, no prose:
[{{"start":<seconds>,"end":<seconds>,"title":"kebab-slug","hook":"caption","score":<1-10>}}]
The (start_seconds-end_seconds) numbers on each line are absolute seconds into the
full video - copy them exactly.

TRANSCRIPT SECTION:
{chunk}
"""

# CLIP BRAIN (optional): one short line of what actually got views on your accounts,
# read from ../brain/rules.txt if you keep one. Kept to one line on purpose: a longer
# prompt makes these reasoning models time out (see the note above). CLIP_BRAIN=0 turns it off.
_bp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "brain", "rules.txt")
BRAIN_LINE = ""
if os.environ.get("CLIP_BRAIN", "1") != "0" and os.path.exists(_bp):
    BRAIN_LINE = open(_bp, encoding="utf-8").read().strip()[:380] + "\n"
    print("clip brain: " + BRAIN_LINE.strip(), flush=True)
transcript = open(transcript_path, encoding="utf-8").read()
model = resolve_model()
chunks = windows(transcript, WINDOW)
per = max(2, math.ceil(n_clips * 2 / len(chunks)))
print(f"model: {model}   transcript: {len(transcript):,} chars in {len(chunks)} window(s), "
      f"asking {per} per window (full coverage, no truncation)", flush=True)

raw = []
for i, ch in enumerate(chunks, 1):
    try:
        # A dense window can burn its whole budget on reasoning and emit no JSON —
        # that shows up as a clean "0 candidates", not an error, which is exactly
        # how the first two windows of a 92-min podcast went missing. Retry once
        # with a bigger allowance; only the windows that actually need it pay for it.
        got = []
        for mt in (2500, 6000):
            got = parse_segments(call(model, PROMPT.format(k=per, chunk=ch, brain=BRAIN_LINE), max_tokens=mt))
            if got:
                break
        # 2026-10-10: gpt-oss-20b is nondeterministic, the same window gave 0 then 6 on back-to-back runs.
        # If the main model still came back empty, give each other live model one try.
        if not got:
            for alt in [c for c in CANDIDATES if c != model]:
                try:
                    got = parse_segments(call(alt, PROMPT.format(k=per, chunk=ch, brain=BRAIN_LINE), max_tokens=4000, timeout=200))
                except Exception:
                    got = []
                if got:
                    print(f"  window {i}: rescued by {alt}", flush=True)
                    break
        print(f"  window {i}/{len(chunks)}: {len(got)} candidates"
              + ("" if got else "  (empty after retry)"), flush=True)
        raw += got
    except urllib.error.HTTPError as e:
        print(f"  window {i}/{len(chunks)}: HTTP {e.code} {e.read().decode()[:120]}", file=sys.stderr)
    except Exception as e:
        print(f"  window {i}/{len(chunks)}: {str(e)[:120]}", file=sys.stderr)

# ---- validate, clamp, de-overlap, rank -------------------------------------
clean = []
for s in raw:
    try:
        st, en = float(s["start"]), float(s["end"])
    except (KeyError, TypeError, ValueError):
        continue
    if en <= st:
        continue
    if en - st > 75:                            # hard cap so a clip never runs long
        en = st + 60
    if en - st < 10:                            # too short to be a clip
        continue
    title = re.sub(r"[^a-z0-9]+", "-", str(s.get("title", "clip")).lower()).strip("-")[:32] or "clip"
    try:
        score = float(s.get("score", 5))
    except (TypeError, ValueError):
        score = 5.0
    clean.append({"start": round(st, 1), "end": round(en, 1), "title": title,
                  "hook": str(s.get("hook", "")).strip(), "score": score})

clean.sort(key=lambda c: -c["score"])
picked = []
for c in clean:
    if any(c["start"] < p["end"] and p["start"] < c["end"] for p in picked):
        continue                                # drop anything overlapping a better pick
    picked.append(c)
    if len(picked) == n_clips:
        break

assert picked, "model returned no usable segments"
picked.sort(key=lambda c: c["start"])           # chronological on disk
for c in picked:
    c.pop("score", None)
json.dump(picked, open(os.path.join(outdir, "segments.json"), "w", encoding="utf-8"), indent=2)

print(f"\npicked {len(picked)} of {len(clean)} candidates -> {outdir}/segments.json")
span = max(c["end"] for c in picked) - min(c["start"] for c in picked)
print(f"coverage: picks span {span/60:.0f} min of the video")
for c in picked:
    print(f"  [{c['start']:.1f}-{c['end']:.1f}] {c['title']}  — {c['hook'][:60]}")
