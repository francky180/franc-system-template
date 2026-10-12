"""
Turn a YouTube auto-caption .vtt into clean, readable, timestamped text.

WHY THIS EXISTS
---------------
YouTube's auto-captions are built for a rolling on-screen display, not for
reading. Every cue repeats the tail of the previous cue and adds a few words,
and each word carries its own inline timing tag:

    00:00:21.800 --> 00:00:25.950
    We're no strangers to
    love.<00:00:22.800><c> You</c><00:00:23.039><c> know</c><00:00:23.279><c> the</c>

Fed to a model raw, that triples the token count and reads like a stutter.
This strips the tags and the rolling repeats, leaving one clean line of new
speech per timestamp.

USAGE
    python vtt_clean.py cap.en.vtt                 -> timestamped text to stdout
    python vtt_clean.py cap.en.vtt --plain         -> no timestamps, one paragraph
    python vtt_clean.py cap.en.vtt --chunk 60      -> group into 60-second blocks
    python vtt_clean.py cap.en.vtt --out clean.txt
"""
import argparse
import re
import sys

TAG = re.compile(r"<[^>]*>")                     # <00:00:19.039> and <c>…</c>
CUE = re.compile(r"(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})")


def _secs(ts):
    h, m, rest = ts.split(":")
    s, ms = re.split(r"[.,]", rest)
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def _hhmm(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


def parse(path):
    """Return [(start_seconds, text)] with tags stripped and rolling repeats removed."""
    raw = open(path, encoding="utf-8", errors="replace").read().splitlines()
    cues, start, buf = [], None, []

    def flush():
        if start is None:
            return
        text = " ".join(buf).strip()
        text = TAG.sub("", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            cues.append((start, text))

    for line in raw:
        m = CUE.search(line)
        if m:
            flush()
            start, buf = _secs(m.group(1)), []
        elif start is not None and line.strip() and not line.startswith(("WEBVTT", "Kind:", "Language:")):
            buf.append(line)
    flush()

    # Drop the rolling repeat. Each cue tends to restate the previous line and
    # append new words, so keep only the part that is genuinely new.
    out, prev = [], ""
    for t, text in cues:
        if text == prev:
            continue
        new = text
        if prev:
            # If this cue starts with the whole previous line, keep the remainder.
            if text.startswith(prev):
                new = text[len(prev):].strip()
            else:
                # Otherwise find the longest suffix of prev that opens this cue.
                words = prev.split()
                for i in range(len(words)):
                    tail = " ".join(words[i:])
                    if tail and text.startswith(tail):
                        new = text[len(tail):].strip()
                        break
        if new:
            out.append((t, new))
            prev = text
        else:
            prev = text
    return out


def main():
    ap = argparse.ArgumentParser(description="Clean a YouTube .vtt into readable text")
    ap.add_argument("vtt")
    ap.add_argument("--plain", action="store_true", help="no timestamps, one flowing paragraph")
    ap.add_argument("--chunk", type=int, default=0, help="group into N-second blocks")
    ap.add_argument("--out", help="write here instead of stdout")
    a = ap.parse_args()

    cues = parse(a.vtt)
    if not cues:
        print("NO CUES PARSED - is this a valid .vtt?", file=sys.stderr)
        sys.exit(1)

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

    if a.out:
        open(a.out, "w", encoding="utf-8").write(body)
        words = len(body.split())
        print(f"wrote {a.out}  ({len(cues)} cues -> {words} words, {len(body)} chars)")
    else:
        print(body)


if __name__ == "__main__":
    main()
