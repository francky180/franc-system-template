---
name: render-check
description: >
  Renders a shipped artifact and LOOKS at it before calling the work done. Screenshots a
  deployed page (or compiles a PDF), reads the result back with the Read tool, judges it
  against a checklist, fixes what is broken, and re-renders until clean. Use after any
  deploy, build, or document generation. Triggers on: render check, verify the deploy,
  did it actually render, check the live page, look at it, /render-check.
  ALWAYS run this before reporting a deploy or a generated document as done.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, WebFetch, AskUserQuestion
---

# /render-check — Compile, Look, Iterate

Ported from `/apply` Step 5 in `MadsLorentzen/ai-job-search`
(`.claude/commands/apply.md`), which enforces a rule
worth generalising far past CVs:

> **"Looks fine in the source" is not acceptable.** Page-break and layout decisions are
> unpredictable. Compile the artifact, read the rendered output, and iterate until it passes.

This is **Rule 5 (Verify it yourself)** made mechanical. A green build proves the code
compiled. It does not prove anything rendered. Those are different claims, and only one of
them is what the user actually cares about.

## The Iron Law

**A render is not verified until an image or a PDF has come back through the Read tool.**

Not a 200 status code. Not "the build passed". Not "the HTML contains the string". Those are
proxies, and every one of them has passed while the page was blank.

---

## Step 0: Identify the Artifact

| Artifact | Render command |
|---|---|
| Deployed page | `/web` — navigate, screenshot. **Never `mcp__claude-in-chrome__*`** (workspace policy). |
| Local dev page | start the dev server, then `/web` against `localhost` |
| PDF from HTML | `node tools/html2pdf.mjs <file>.html --pages N` |
| PDF from LaTeX | the template's declared compile command |
| Generated image/video | Read the file directly |

If the artifact is a deploy, get the **real** URL — the production alias, not the raw
deployment URL (raw Vercel URLs 302 to SSO and screenshot as a login page, which reads as a
broken site when it is not).

---

## Step 1: Render

Render at the viewports that matter. For a page that is one deliverable:

- **Desktop** 1440×900
- **Mobile** 390×844 — most of his traffic is Instagram-referred, so this one is not optional

**ISR staleness trap.** A Next.js page with ISR serves the *previous* build once after a
deploy. The first screenshot after shipping can legitimately show old content. Hit the URL
once to warm it, then screenshot. Do not "fix" a bug that was just a stale first response.

---

## Step 2: LOOK

Read the screenshot or PDF back. Actually look at it. Then judge against this checklist —
report it as pass/fail, never as prose.

### Every artifact
- [ ] It rendered at all — not blank, not a spinner frozen mid-load, not an error page
- [ ] No placeholder text survived (`[YOUR_NAME]`, `Lorem ipsum`, `TODO`, `undefined`, `NaN`, `null`)
- [ ] No overlapping or clipped text
- [ ] Images loaded — no broken-image icons, no empty boxes where art belongs

### Web pages
- [ ] Above the fold says what the page is, without scrolling
- [ ] Mobile: nothing overflows horizontally, tap targets are not stacked on top of each other
- [ ] Fonts loaded — no flash-of-fallback frozen into the screenshot
- [ ] Console clean: no uncaught errors, no failed network requests (check both)
- [ ] Any dynamic data actually populated — a chart with no series and a ticker with no prices
      both render "successfully"
- [ ] Interactive elements are present where the design says they are

### PDFs
- [ ] Exactly the declared page count — not one over, not one under
- [ ] Nothing orphaned: a heading must never be the last thing on a page
- [ ] Text layer extracts cleanly: `pdftotext -layout -enc UTF-8 <file> out.txt`
      — no `(cid:*)` markers, no genuine `�`, reading order matches visual order
- [ ] A `�` seen in a Git Bash terminal is usually console rendering, not a real defect —
      confirm by writing to a file and checking bytes before treating it as a finding

---

## Step 3: Fix and Re-render

For each failure: fix the source, re-render, re-read. **Every iteration must end in a fresh
render.** A fix that was not re-rendered is a hypothesis, not a fix.

Cap at **4 iterations**. If it is still failing on the fifth, stop and report honestly:
what is broken, what was tried, what you believe the cause is. A loop that keeps going is
worse than an honest stop — the user can unblock in thirty seconds what an agent will burn
an hour on.

**Page-budget dial**, when a PDF is one page over or under — apply in this order, never jump
straight to cutting content:
1. page margins
2. body font size
3. line height
4. only then cut, lowest-value line first

---

## Step 4: Report

```
RENDER CHECK — <artifact>

Rendered:  <viewports / page count>
Iterations: <n>

[PASS] rendered, no placeholders
[PASS] mobile 390px, no horizontal overflow
[FAIL] console: 1 uncaught TypeError in analytics.js — FIXED, re-rendered, clean
[PASS] dynamic data populated (6 series)

Verdict: SHIP / DO NOT SHIP — <one line>
```

Attach or name the screenshot paths. If anything is still failing, the verdict is
**DO NOT SHIP** — say so plainly rather than softening it. Reporting a broken artifact as
done is the single failure mode this skill exists to prevent.

---

## When NOT to run this

- Pure refactors with no user-visible surface
- Backend-only changes with no page and no document
- Work the user explicitly said not to verify

Everything else that produces something a human will look at: run it.
