"""Plain-English scraping via ScrapeGraphAI, routed through OmniRoute so it costs $0.

    python scrape.py "<plain-English ask>" "<url>" [out-name]

Prints a markdown table; writes Downloads/<out-name>.csv when rows > 10.
"""
import csv
import json
import os
import re
import sys
import urllib.request

# Windows consoles default to cp1252 and mangle accented text (Siksè -> Siks?).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OMNI_BASE = os.environ.get("OPENAI_BASE_URL", "http://localhost:20128/v1")
OMNI_KEY = os.environ.get("OPENAI_API_KEY", "omniroute")
MODEL = os.environ.get("SCRAPER_MODEL", "auto/best-coding")
DOWNLOADS = r"C:\Users\franc\Downloads"

# Without this the model happily answers in prose and you get one useless row.
SHAPE = (" Return ONLY a JSON array of objects — one object per item, consistent "
         "snake_case keys across every object, no commentary, no markdown fence. "
         "Use null for a field you cannot find. Do not summarise; list every item.")


def gateway_up() -> bool:
    try:
        urllib.request.urlopen(OMNI_BASE.rstrip("/") + "/models", timeout=6).read()
        return True
    except Exception:
        return False


def _json_in(text):
    """Pull a JSON array out of a prose answer, when the model ignored the shape."""
    m = re.search(r"\[\s*\{.*\}\s*\]", text, re.S)
    if not m:
        return None
    try:
        v = json.loads(m.group(0))
        return v if isinstance(v, list) and v and isinstance(v[0], dict) else None
    except Exception:
        return None


def rows_from(result):
    """SmartScraperGraph returns dict / list / {content: ...} depending on the ask."""
    if isinstance(result, str):
        return _json_in(result) or []
    if isinstance(result, list):
        return [r for r in result if isinstance(r, dict)]
    if isinstance(result, dict):
        for v in result.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v
        # single {"content": "...prose..."} — salvage embedded JSON if it's there
        for v in result.values():
            if isinstance(v, str):
                got = _json_in(v)
                if got:
                    return got
        return [result]
    return []


def as_table(rows) -> str:
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    if not cols:
        return "(no columns)"
    out = ["| " + " | ".join(cols) + " |",
           "|" + "|".join(["---"] * len(cols)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "") or "").replace("\n", " ").replace("|", "/")
                                     for c in cols) + " |")
    return "\n".join(out)


def main():
    if len(sys.argv) < 3:
        sys.exit('usage: scrape.py "<ask>" "<url>" [out-name]')
    prompt, url = sys.argv[1], sys.argv[2]
    out_name = sys.argv[3] if len(sys.argv) > 3 else "scrape"

    if not gateway_up():
        sys.exit(f"OmniRoute is not answering at {OMNI_BASE}. "
                 "Start it before scraping — refusing to fall back to a paid key.")

    from scrapegraphai.graphs import SmartScraperGraph

    graph = SmartScraperGraph(
        prompt=prompt + SHAPE,
        source=url,
        config={
            "llm": {
                "api_key": OMNI_KEY,
                "model": f"openai/{MODEL}",
                "base_url": OMNI_BASE,
                "model_tokens": 128000,
            },
            "verbose": False,
            "headless": True,
        },
    )

    try:
        result = graph.run()
    except Exception as e:
        msg = str(e)
        if "combo retry" in msg or "503" in msg or "service_unavailable" in msg:
            sys.exit(
                "OmniRoute exhausted every free provider on this page.\n"
                "That means the page was too large for the free tier, not that scraping failed.\n"
                "Try: a deeper//smaller URL (a category or results page, not a homepage), "
                "SCRAPER_MODEL=auto/best-fast, or re-run in a few minutes."
            )
        sys.exit(f"Scrape failed: {type(e).__name__}: {msg[:400]}")

    rows = rows_from(result)

    if not rows:
        print("NO ROWS. Raw result below — the page may be JS-gated or the ask too vague.")
        print(json.dumps(result, indent=2)[:1500])
        return

    print(as_table(rows))
    print(f"\nROWS: {len(rows)}")

    if len(rows) > 10:
        cols = []
        for r in rows:
            for k in r:
                if k not in cols:
                    cols.append(k)
        path = os.path.join(DOWNLOADS, f"{out_name}.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print(f"CSV: {path}")


if __name__ == "__main__":
    main()
