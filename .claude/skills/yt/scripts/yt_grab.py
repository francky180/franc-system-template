"""
yt_grab.py — hand it any video link, get back metadata + a clean transcript.

NO API KEY. NO CREDITS. Nothing is billed.
yt-dlp reads the page the way a browser does and pulls the caption track the
platform already publishes. That is the same "scrape it, don't call an API"
approach used for the ForexFactory calendar.

Works on 1,747 sites (YouTube, TikTok, Vimeo, X/Twitter, Instagram, Reddit,
Rumble, SoundCloud, Twitch, …) plus a `generic` extractor that finds video on
ordinary web pages. URL form does not matter: full link, youtu.be short link,
?t=120s, or a bare 11-character YouTube ID all resolve.

USAGE
    python yt_grab.py "<url>"                      # metadata + clean transcript
    python yt_grab.py "<url>" --chunk 60           # 60-second timestamped blocks
    python yt_grab.py "<url>" --plain              # one flowing paragraph
    python yt_grab.py "<url>" --lang es            # prefer a language
    python yt_grab.py "<url>" --out study.txt      # write to a file
    python yt_grab.py "<url>" --info-only          # metadata only, no transcript

EXIT CODES
    0 ok · 2 no captions published (use --whisper-hint for the fallback) · 1 error
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vtt_clean import parse as vtt_parse, _hhmm  # noqa: E402

PY = sys.executable


def run(args, timeout=300):
    return subprocess.run([PY, "-m", "yt_dlp", "--no-warnings"] + args,
                          capture_output=True, text=True, timeout=timeout,
                          encoding="utf-8", errors="replace")


def get_info(url):
    r = run(["--skip-download", "--dump-single-json", url])
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "yt-dlp failed").strip()[:400])
    d = json.loads(r.stdout)
    return {
        "title": d.get("title"),
        "channel": d.get("channel") or d.get("uploader"),
        "duration": d.get("duration"),
        "upload_date": d.get("upload_date"),
        "views": d.get("view_count"),
        "likes": d.get("like_count"),
        "url": d.get("webpage_url") or url,
        "id": d.get("id"),
        "extractor": d.get("extractor_key"),
        "description": (d.get("description") or "")[:2000],
        "subs": sorted((d.get("subtitles") or {}).keys()),
        "auto": sorted((d.get("automatic_captions") or {}).keys()),
    }


def fetch_vtt(url, lang, workdir):
    """Prefer human-written subtitles; fall back to auto-generated."""
    for flag, kind in (("--write-sub", "manual"), ("--write-auto-sub", "auto")):
        r = run(["--skip-download", flag, "--sub-lang", lang, "--sub-format", "vtt",
                 "-o", os.path.join(workdir, "c.%(ext)s"), url])
        hits = glob.glob(os.path.join(workdir, "c*.vtt"))
        if hits:
            return hits[0], kind
        del r
    return None, None


def main():
    ap = argparse.ArgumentParser(description="Any video link -> metadata + clean transcript, no API")
    ap.add_argument("url")
    ap.add_argument("--lang", default="en", help="preferred caption language (default en)")
    ap.add_argument("--chunk", type=int, default=0, help="group transcript into N-second blocks")
    ap.add_argument("--plain", action="store_true", help="no timestamps, one paragraph")
    ap.add_argument("--out", help="write the transcript here")
    ap.add_argument("--info-only", action="store_true")
    ap.add_argument("--json", action="store_true", help="emit metadata as JSON")
    a = ap.parse_args()

    try:
        info = get_info(a.url)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    dur = info["duration"]
    dur_s = _hhmm(dur) if dur else "?"
    if a.json:
        print(json.dumps(info, indent=1, ensure_ascii=False))
    else:
        print(f"TITLE    : {info['title']}")
        print(f"CHANNEL  : {info['channel']}")
        print(f"DURATION : {dur_s}   ({dur} sec)")
        print(f"UPLOADED : {info['upload_date']}   VIEWS: {info['views']:,}" if info["views"]
              else f"UPLOADED : {info['upload_date']}")
        print(f"SOURCE   : {info['extractor']}   {info['url']}")
        print(f"CAPTIONS : manual={info['subs'][:6] or 'none'}  auto={info['auto'][:4] or 'none'}"
              + (f" (+{len(info['auto'])-4} more)" if len(info["auto"]) > 4 else ""))

    if a.info_only:
        return

    if not info["subs"] and not info["auto"]:
        print("\nNO CAPTIONS PUBLISHED for this video.", file=sys.stderr)
        print("Fallback: download the audio and transcribe locally —", file=sys.stderr)
        print('  python -m yt_dlp -f "ba[ext=m4a]/ba" -o audio.%(ext)s "<url>"', file=sys.stderr)
        print('  python ~/.claude/skills/clip/scripts/transcribe.py audio.m4a .', file=sys.stderr)
        sys.exit(2)

    with tempfile.TemporaryDirectory() as wd:
        path, kind = fetch_vtt(a.url, a.lang, wd)
        if not path:
            print(f"\nNo '{a.lang}' caption track. Available: "
                  f"manual={info['subs'][:8]} auto={info['auto'][:8]}", file=sys.stderr)
            sys.exit(2)
        cues = vtt_parse(path)
        raw_bytes = os.path.getsize(path)

    if a.plain:
        body = " ".join(t for _, t in cues)
    elif a.chunk:
        lines, bucket, edge = [], [], cues[0][0]
        for t, text in cues:
            if t >= edge + a.chunk and bucket:
                lines.append(f"[{_hhmm(edge)}] " + " ".join(bucket))
                bucket, edge = [], t
            bucket.append(text)
        if bucket:
            lines.append(f"[{_hhmm(edge)}] " + " ".join(bucket))
        body = "\n\n".join(lines)
    else:
        body = "\n".join(f"[{_hhmm(t)}] {text}" for t, text in cues)

    words = len(body.split())
    hdr = (f"\nTRANSCRIPT ({kind} captions, {a.lang}): {len(cues)} cues -> "
           f"{words} words, {len(body):,} chars  (raw vtt was {raw_bytes:,} — "
           f"{raw_bytes/max(len(body),1):.1f}x smaller)")
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(f"{info['title']}\n{info['channel']} | {dur_s} | {info['url']}\n\n{body}\n")
        print(hdr)
        print(f"wrote {a.out}")
    else:
        print(hdr + "\n")
        print(body)


if __name__ == "__main__":
    main()
