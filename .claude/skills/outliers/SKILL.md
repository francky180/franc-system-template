---
name: outliers
description: "Find what's ALREADY going viral on a topic before making a video (outlier research playbook). Use for /outliers, 'what's working on X', 'find viral videos about', 'research before I film', 'title ideas', or before writing any faceless / clip / content script. Free: yt-dlp, no API."
---

# /outliers — research what works, THEN make it

*The biggest predictor a video does well is that other people are already making viral videos
about this topic. Don't have AI invent ideas from nothing — research what's working and why,
then make your own.*

Requires: Python 3.10+, `pip install yt-dlp`, and the `/yt` skill (its `scripts/yt_grab.py` pulls hooks).

## Step 0 — read what already works for the user
If the user has their own performance notes (best hooks, top posts), read them first. Their proven
rules beat anything scraped. Carry them into Step 4.

## Step 1 — parallel niches (5)
From the idea, list 5 neighbouring topics the same audience also watches.
Example "credit repair" → collections pay-for-delete, 700 score fast, business credit, secured cards.

## Step 2 — run the finder on the idea + each niche
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/outliers/scripts/outliers.py "<topic>" --n 40 --top 10 --hooks 5 --out o_<slug>.json
#   --shorts   keep <=3 min videos only and compare vs the channel's Shorts tab
```
~1 min per topic. Run topics in parallel (background) when doing 5+.
**Score = views ÷ that channel's median of its last 15 uploads.** 10x on a small channel = the
TOPIC/HOOK did the work (copyable). A 1M video on a 5M channel is just a big channel (not copyable).
Ignore rows with `?` score (channel had <3 uploads).

## Step 3 — why each top outlier won
For the top 5-8: title formula, the promise, the first spoken line (`HOOK:`), the format (talking
head / screen record / faceless B-roll / list). Name the pattern: number, contrarian ("STOP
paying collections"), secret/leak, year-stamp ("in 2026"), "you vs them", speed ("in DAYS").

## Step 4 — rewrite for the user
For each winner: 1 title + 1 spoken hook (first 2 seconds) in the user's voice and niche, keeping
the pattern, never copying words. No income claims, no guarantees, label AI content, add
"#ad / Affiliate link" where it applies.

## Output
```
TOPIC — top outliers
1. 149x  3.1k views (channel norm 21)  "Easiest Way To Start A Credit Repair Business in 2026"
   WHY: year-stamp + "easiest" + business-opportunity promise
   YOURS: "<your title in the same pattern>" · hook: "<first 2 seconds>"
```

## Limits (say them, don't hide them)
- YouTube only (search is free + unblocked). Instagram/TikTok search needs a login.
- `--hooks` needs captions; many Shorts have none → hook blank, read the title instead.
- Keep yt-dlp updated (`python -m pip install -U yt-dlp`) before calling anything "broken".
- Feeds `/faceless` (Step 1 of that pipeline) and `/clip` title picks.
