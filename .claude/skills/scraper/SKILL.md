---
name: scraper
description: Plain-English web scraping with ScrapeGraphAI — pull leads, emails, listings, jobs, directories or any repeating list off a page by describing it in words instead of writing selectors. Use when asked to scrape, extract, or "pull every X from this page/site".
---

# scraper — plain-English extraction (ScrapeGraphAI + OmniRoute)

An LLM reads the rendered page and returns structured rows, so it keeps working when
the site changes its markup. Runs on **OmniRoute** (`localhost:20128`), so scrapes
cost **$0** — no OpenAI key, no per-row billing.

## Terrain (Windows — this is not the blog's Mac setup)

| | |
|---|---|
| venv | `~/ai-tools/scraper-env` (create: `python -m venv ~/ai-tools/scraper-env`) |
| python | `~/ai-tools/scraper-env/Scripts/python.exe` — **`Scripts/`, not `bin/`** |
| runner | `~/ai-tools/scrape.py` (copy from this repo's `ai-tools/scrape.py`) |
| output | CSV → `~/Downloads/` |

## Run it

```bash
PY="$HOME/ai-tools/scraper-env/Scripts/python.exe"
$PY $HOME/ai-tools/scrape.py "<plain-English ask>" "<url>" [out-name]
```

Example:
```bash
$PY $HOME/ai-tools/scrape.py \
  "every business name, phone number and rating" \
  "https://example.com/results" orlando-roofers
```

Prints a markdown table. Writes `Downloads/<out-name>.csv` automatically when rows > 10.

## Rules

- **Always show the table in chat.** The CSV is the artifact, the table is the answer.
- **Verify before reporting.** Print the row count and eyeball a couple of rows — an
  empty or hallucinated result must never be reported as a successful scrape.
- **OmniRoute must be running.** Check with `curl -s -m 5 localhost:20128/v1/models`.
  If it's down, say so — do not silently fall back to a paid OpenAI key.
- **Heavy pages on an 8GB box:** Playwright Chromium plus a 1M-context model is real
  memory. One scrape at a time; close other Chrome windows for big jobs.
- **Leads land in a real system**, not just a spreadsheet — mirror them into the
  asf-business `contacts` table with `consent='cold'` so they can never be mistaken
  for opt-ins and mailed by accident.

## What it does NOT solve

Most people already have more scrapers and contact lists than they can use. If you hold
**contacts you cannot safely mail**, more rows is rarely the bottleneck — if a
request smells like "collect more names", ask what happens to them after.
