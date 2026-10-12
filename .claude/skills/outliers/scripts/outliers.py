"""Outlier finder: which videos on a topic beat their OWN channel's normal by the most.

Free (yt-dlp scrapes YouTube search, no API key). Usage:
  python outliers.py "credit repair" --shorts --n 40 --top 15 --hooks 5 --out out.json
Score = video views / median views of that channel's last 15 uploads (same format).
A 10x outlier on a 2k-view channel beats a 1M-view video on a 5M-view channel: the TOPIC did the work.
"""
import argparse, json, statistics, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

PY = sys.executable
import os
YT_GRAB = os.path.join(os.path.expanduser("~"), ".claude", "skills", "yt", "scripts", "yt_grab.py")


def ytjson(target, limit):
    r = subprocess.run([PY, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", str(limit), target],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    try:
        return json.loads(r.stdout).get("entries") or []
    except Exception:
        return []


def channel_median(url, shorts):
    tab = "/shorts" if shorts else "/videos"
    views = [e.get("view_count") for e in ytjson(url.rstrip("/") + tab, 15) if e.get("view_count")]
    return statistics.median(views) if len(views) >= 3 else None


def hook(url):
    # first ~2 lines of what is SAID = the spoken hook (captions only; Shorts often have none)
    r = subprocess.run([PY, YT_GRAB, url, "--plain"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
    body = r.stdout.split("TRANSCRIPT", 1)
    words = body[1].split("\n", 1)[-1].split() if len(body) == 2 else []
    return " ".join(words[:40]) if r.returncode == 0 and words else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--shorts", action="store_true", help="Shorts only (<=3 min) and compare vs the channel's Shorts tab")
    ap.add_argument("--n", type=int, default=40, help="search results to pull")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--min-views", type=int, default=1000)
    ap.add_argument("--hooks", type=int, default=0, help="pull the spoken hook for the top N")
    ap.add_argument("--out")
    a = ap.parse_args()

    # YouTube search ignores "#shorts"; pull a wider net and keep the short ones instead
    n = a.n * 3 if a.shorts else a.n
    vids = [e for e in ytjson(f"ytsearch{n}:{a.topic}", n) if (e.get("view_count") or 0) >= a.min_views and e.get("channel_url")]
    if a.shorts:
        vids = [e for e in vids if (e.get("duration") or 0) <= 180]
    chans = sorted({e["channel_url"] for e in vids})
    with ThreadPoolExecutor(10) as ex:
        med = dict(zip(chans, ex.map(lambda c: channel_median(c, a.shorts), chans)))

    rows = []
    for e in vids:
        m = med.get(e["channel_url"])
        rows.append({"score": round(e["view_count"] / m, 1) if m else None, "views": e["view_count"], "channel_median": m,
                     "channel": e.get("channel"), "title": e.get("title"), "duration": e.get("duration"),
                     "url": e.get("url") or f"https://www.youtube.com/watch?v={e['id']}"})
    rows.sort(key=lambda r: (r["score"] or 0), reverse=True)
    rows = rows[:a.top]
    if a.hooks:
        with ThreadPoolExecutor(5) as ex:
            for r, h in zip(rows[:a.hooks], ex.map(lambda r: hook(r["url"]), rows[:a.hooks])):
                r["hook"] = h

    print(f"OUTLIERS: {a.topic!r} {'(Shorts)' if a.shorts else ''}  searched {len(vids)} videos, {len(chans)} channels\n")
    for i, r in enumerate(rows, 1):
        sc = f"{r['score']}x" if r["score"] else "  ?"
        print(f"{i:>2}. {sc:>7}  {r['views']:>10,} views (channel norm {int(r['channel_median'] or 0):,})  {r['title']}")
        print(f"            {r['channel']} · {r['duration']}s · {r['url']}")
        if r.get("hook"):
            print(f"            HOOK: {r['hook']}")
    if a.out:
        json.dump({"topic": a.topic, "shorts": a.shorts, "rows": rows}, open(a.out, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
