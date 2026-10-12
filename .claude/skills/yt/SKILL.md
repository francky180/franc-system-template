---
name: yt
description: Give it any video link and get the metadata + a clean timestamped transcript with NO API and no credits, then study/summarise it or hand it to /clip. Use when the user drops a YouTube link, says "watch this", "transcribe this", "what does this video say", "study this video", "summarise this talk", or pastes a video URL with no other instruction.
---

# /yt — link in, transcript out, no API

Scrapes the caption track the platform already publishes. **No API key, no credits, nothing billed.**

The tool: `~/.claude/skills/yt/scripts/yt_grab.py` (needs Python 3.10+ and `pip install yt-dlp`)

```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/yt/scripts/yt_grab.py "<url>" --chunk 90 --out study.txt
```

Then **read `study.txt` and answer the user's actual question.** Do not dump the raw
transcript into chat — they asked about the video, not for a wall of text.

## Flags

| flag | what it does |
|---|---|
| `--chunk 90` | group into 90-second timestamped blocks — **the default choice**, keeps timestamps usable for clipping |
| `--plain` | one flowing paragraph, no timestamps — for pure summarising |
| `--out FILE` | write to a file instead of stdout (**use this**; long videos are big) |
| `--info-only` | metadata + available caption languages, no transcript |
| `--lang es` | prefer a language (default `en`) |
| `--json` | metadata as JSON |

## 🚨 What actually works — verified 2026-09-13 by running it, not assumed

| | result |
|---|---|
| **YouTube** | ✅ **full** — metadata + manual & auto captions, every URL form (`youtu.be/…`, `?v=…&t=120s`, bare 11-char ID) |
| **TikTok** | ✅ metadata + video. **No caption tracks published** → use the Whisper fallback below |
| **Vimeo** | ⚠️ needs a logged-in session (`--cookies-from-browser chrome`), and that fails while Chrome is open — the cookie DB is locked (yt-dlp issue #7271) |
| Others | 1,747 extractors listed. The big platforms fight scrapers, so **try it and see** |

🔑 **So it is NOT "any link" — say so plainly rather than promising and failing.**
It is excellent on YouTube, good on TikTok, and per-platform elsewhere.

🚨 **KEEP yt-dlp UPDATED — this is the single highest-value gotcha.**
On 2026-09-13 TikTok returned *"Unexpected response from webpage request"* on
**2026.06.09** and worked perfectly on **2026.08.19**. Vimeo's cryptic
`401 Unauthorized` became an honest "you need to log in". A three-month-old
yt-dlp silently loses platforms.

```bash
python -m pip install -U yt-dlp
```
**Any new "Unexpected response" / auth error: update FIRST, before concluding a
platform is unsupported.**

⚠️ **Manual captions beat auto.** The script prefers human-written subtitles and
falls back to auto-generated. The gap is large — manual gives real punctuation
and `(Laughter)` / `(Applause)`; auto gives a run-on with ASR errors ("never
gonna let you down" came back as "I'm going to let you down"). **When quoting
the video, say which kind you got** — the header line reports it.

## No captions at all?

The script exits **2** and prints the fallback. That path costs nothing either
(Groq free tier: `GROQ_API_KEY` env or `~/.config/watch/.env`; needs the `/clip` skill):

```bash
python -m yt_dlp -f "ba[ext=m4a]/ba" -o audio.%(ext)s "<url>"
python ~/.claude/skills/clip/scripts/transcribe.py audio.m4a .
```

## Then what — pick the job the user actually asked for

- **"what does it say" / "summarise"** → read the file, answer in chat. Lead with
  the single most useful thing, not a chronological retelling.
- **"study this"** → pull the claims, the numbers, and anything that contradicts
  what the user already believes. Cite timestamps so they can jump to them.
- **"clip it" / "make shorts"** → this skill gets the transcript; **`/clip` does
  the cutting.** Do not rebuild it — `/clip` already does yt-dlp → Whisper →
  AI moment-picking → 9:16 burned captions, free.
- **A claims-heavy video** (money, health, trading) → verify the numbers before
  repeating any of them. A confident YouTuber is not evidence.

## Token economics — why the cleaner exists

YouTube auto-captions are built for a rolling on-screen display: every cue
repeats the previous line plus a few words, and every word carries an inline
timing tag. Raw, it is mostly duplication.

```
Rick Astley 3:33    14,807 -> 1,446 chars   10.2x smaller
TED talk    14:04  113,187 -> 11,974 chars   9.5x smaller
```

`scripts/vtt_clean.py` strips the tags and the rolling repeat. **Never paste a raw
`.vtt` into context** — it is ~10x the tokens for the same words.

## Gotchas

- ⚠️ `--print` and `--write-auto-sub` in the same yt-dlp call **silently skip the
  subtitle write**. Fetch metadata and captions in separate calls (the script
  already does).
- ⚠️ Run with `PYTHONIOENCODING=utf-8`. The Windows console is cp1252 and any
  non-ASCII in a title will raise `UnicodeEncodeError` on print — the file write
  is fine, so it looks like a failure when it is not.
- ⚠️ Use a Python that has yt-dlp installed (`python -m yt_dlp --version` to check).
- ⚠️ yt-dlp ages fast against platform changes. A new "Unexpected response"
  error usually means it needs updating: `python -m pip install -U yt-dlp`.
