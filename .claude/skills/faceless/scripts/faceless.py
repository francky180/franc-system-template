"""Faceless short builder: plan.json -> voice -> AI B-roll (fal) -> captioned 9:16 mp4.

  python faceless.py voice    plan.json            # edge_tts voice + word timings (free)
  python faceless.py shots    plan.json [--dry]    # fal text-to-video per shot; --dry = cost only, $0
  python faceless.py assemble plan.json            # ffmpeg: cut shots to the voice, burn captions
  python faceless.py all      plan.json            # voice + shots + assemble

plan.json = {"slug","title","caption","voice"?,"model"?,"lines":[{"say":"...","shot":"prompt","file"?:"local.mp4"}]}
One line = one sentence of voiceover = one shot. A line with "file" uses that clip instead of generating.
"""
import asyncio, json, math, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

VOICE = "en-US-AndrewMultilingualNeural"
DEFAULT_MODEL = "bytedance/seedance-2.0/mini/text-to-video"   # ~$0.07/s; Veo/Kling for hero shots
W, H = 1080, 1920
GOLD = "&H004EA8C9"   # ASS is BGR: #C9A84E


def env(name, *files):
    if os.environ.get(name):
        return os.environ[name]
    for f in files:
        p = Path(f).expanduser()
        if p.exists():
            for ln in p.read_text(encoding="utf-8").splitlines():
                if ln.strip().startswith(name + "="):
                    return ln.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def http(method, url, headers=None, body=None, raw=None, timeout=120):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    h = {"Content-Type": "application/json", "User-Agent": "faceless/1"} | (headers or {})
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        txt = r.read()
    try:
        return json.loads(txt)
    except Exception:
        return txt


def load(plan_path):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    work = Path(plan_path).parent / plan.get("slug", "short")
    work.mkdir(parents=True, exist_ok=True)
    return plan, work


# ---------- 1. voice ----------
async def _tts(text, voice, out):
    import edge_tts
    words = []
    c = edge_tts.Communicate(text, voice, boundary="WordBoundary", rate="+6%")
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"w": ch["text"], "t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
    return words


def voice(plan, work):
    text = " ".join(l["say"].strip() for l in plan["lines"])
    words = asyncio.run(_tts(text, plan.get("voice", VOICE), work / "voice.mp3"))
    # map each line to its time span using the running word count
    i, spans = 0, []
    for l in plan["lines"]:
        n = len(re.findall(r"[\w'$%.,-]+", l["say"])) or 1
        seg = words[i:i + n] or words[-1:]
        spans.append([seg[0]["t"], seg[-1]["t"] + seg[-1]["d"]])
        i += n
    for k in range(len(spans) - 1):
        spans[k][1] = spans[k + 1][0]           # each shot runs until the next line starts
    spans[-1][1] += 0.6
    json.dump({"words": words, "spans": spans}, open(work / "timing.json", "w"), indent=1)
    print(f"voice: {len(words)} words, {spans[-1][1]:.1f}s -> {work / 'voice.mp3'}")


# ---------- 2. shots (fal) ----------
def price_per_sec(model):
    try:
        j = http("GET", f"https://fal.ai/api/models?keywords={model.split('/')[1]}")
        for m in j.get("items", []):
            if m.get("id") == model:
                t = m.get("pricingInfoOverride") or ""
                x = re.search(r"\$([0-9.]+)\**\s*(?:per|/)\s*second", t)
                return float(x.group(1)) if x else None
    except Exception:
        return None


def shots(plan, work, dry=False):
    tm = json.load(open(work / "timing.json"))
    model = plan.get("model", DEFAULT_MODEL)
    todo = []
    for k, l in enumerate(plan["lines"]):
        out = work / f"shot_{k:02d}.mp4"
        if l.get("file") or out.exists():
            continue
        need = tm["spans"][k][1] - tm["spans"][k][0]
        todo.append((k, l, max(4, min(15, math.ceil(need))), out))
    pps = price_per_sec(model)
    est = sum(s for _, _, s, _ in todo) * (pps or 0)
    print(f"shots: {len(todo)} to generate with {model} · {sum(s for _, _, s, _ in todo)}s · "
          f"{'~$%.2f' % est if pps else 'price unknown'}")
    if dry or not todo:
        return
    key = env("FAL_KEY", "~/.config/fal/.env")
    if not key:
        sys.exit("FAL_KEY missing: set the FAL_KEY env var or save FAL_KEY=... in ~/.config/fal/.env")
    hdr = {"Authorization": f"Key {key}"}
    jobs = []
    for k, l, secs, out in todo:   # submit all, then poll: fal runs them in parallel
        body = {"prompt": l["shot"], "aspect_ratio": "9:16", "duration": str(secs)}
        r = http("POST", f"https://queue.fal.run/{model}", hdr, body)
        jobs.append((k, out, r["status_url"], r["response_url"]))
        print(f"  shot {k}: submitted ({secs}s)")
    while jobs:
        time.sleep(6)
        for job in list(jobs):
            k, out, s_url, r_url = job
            st = http("GET", s_url, hdr).get("status")
            if st == "COMPLETED":
                res = http("GET", r_url, hdr)
                v = (res.get("video") or {}).get("url") or (res.get("videos") or [{}])[0].get("url")
                if v:
                    urllib.request.urlretrieve(v, out)
                    print(f"  shot {k}: done")
                else:
                    print(f"  shot {k}: FAILED {str(res)[:200]}")
                jobs.remove(job)
            elif st not in ("IN_QUEUE", "IN_PROGRESS"):
                print(f"  shot {k}: {st}")
                jobs.remove(job)


# ---------- 3. assemble ----------
def ass_time(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def captions(words, path, label):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial Black,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,7,3,2,60,60,560,1
Style: Tag,Arial,30,&H99FFFFFF,&H99FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,9,40,40,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for i in range(0, len(words), 3):           # 3 words on screen, the spoken one in gold
        grp = words[i:i + 3]
        for j, w in enumerate(grp):
            s = w["t"]
            nxt = words[i + j + 1]["t"] if i + j + 1 < len(words) else None
            e = nxt if nxt is not None and nxt - (w["t"] + w["d"]) < 0.8 else w["t"] + w["d"] + 0.15   # no flicker in short pauses
            txt = " ".join((f"{{\\c{GOLD}}}{x['w'].upper()}{{\\c&H00FFFFFF}}" if x is w else x["w"].upper()) for x in grp)
            ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Cap,,0,0,0,,{txt}")
    end = words[-1]["t"] + words[-1]["d"] + 1
    ev.append(f"Dialogue: 0,{ass_time(0)},{ass_time(end)},Tag,,0,0,0,,{label}")
    Path(path).write_text(head + "\n".join(ev) + "\n", encoding="utf-8")


def ff(*args):
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg: " + r.stderr[-800:])


def probe_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def assemble(plan, work):
    tm = json.load(open(work / "timing.json"))
    parts = []
    for k, l in enumerate(plan["lines"]):
        src = Path(l["file"]) if l.get("file") else work / f"shot_{k:02d}.mp4"
        if not src.exists():
            sys.exit(f"missing {src} (run: shots)")
        need = tm["spans"][k][1] - (0 if k == 0 else tm["spans"][k][0])
        have = probe_dur(src) or need
        slow = min(1.35, max(1.0, need / have))      # stretch a little, then hold the last frame
        out = work / f"part_{k:02d}.mp4"
        ff("-i", str(src), "-t", f"{need:.3f}", "-an", "-vf",
           f"setpts={slow:.3f}*PTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,"
           f"tpad=stop_mode=clone:stop_duration={need:.2f},format=yuv420p",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(out))
        parts.append(out.name)
    (work / "parts.txt").write_text("".join(f"file '{p}'\n" for p in parts))
    captions(tm["words"], work / "caps.ass", plan.get("label", "AI visuals"))
    final = work / f"{plan.get('slug', 'short')}.mp4"
    cwd = os.getcwd()
    os.chdir(work)                                    # relative paths dodge Windows filter escaping
    try:
        ff("-f", "concat", "-safe", "0", "-i", "parts.txt", "-i", "voice.mp3",
           "-vf", "subtitles=caps.ass", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
           "-crf", "19", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-shortest", final.name)
    finally:
        os.chdir(cwd)
    print(f"final: {final}  ({probe_dur(final):.1f}s)")


if __name__ == "__main__":
    step, plan_path = sys.argv[1], sys.argv[2]
    plan, work = load(plan_path)
    if step in ("voice", "all"):
        voice(plan, work)
    if step in ("shots", "all"):
        shots(plan, work, dry="--dry" in sys.argv)
    if step in ("assemble", "all"):
        assemble(plan, work)
