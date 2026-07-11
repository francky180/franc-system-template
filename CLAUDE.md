# 🚀 START HERE — Client Setup Rules

Paste your OS command below into a terminal. It installs everything in one go.

## Rule 1 — Install Claude Code + this system (one command, any device)

### 🪟 Windows (PowerShell — run as Administrator)
```powershell
winget install OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements; winget install Git.Git -e --accept-source-agreements --accept-package-agreements; npm install -g @anthropic-ai/claude-code; git clone https://github.com/francky180/franc-system-template.git "$HOME\ai-software-factory"; cd "$HOME\ai-software-factory"; bash ai-tools/install-all.sh; claude
```

### 🍎 Mac (Terminal)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install node git && npm install -g @anthropic-ai/claude-code && git clone https://github.com/francky180/franc-system-template.git ~/ai-software-factory && cd ~/ai-software-factory && bash ai-tools/install-all.sh && claude
```

### 🐧 Linux (Debian / Ubuntu)
```bash
sudo apt update && sudo apt install -y curl git && curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt install -y nodejs && sudo npm install -g @anthropic-ai/claude-code && git clone https://github.com/francky180/franc-system-template.git ~/ai-software-factory && cd ~/ai-software-factory && bash ai-tools/install-all.sh && claude
```

### 📱 Termux (Android)
```bash
pkg upgrade -y && pkg install nodejs-lts git -y && npm install -g @anthropic-ai/claude-code && git clone https://github.com/francky180/franc-system-template.git ~/ai-software-factory && cd ~/ai-software-factory && bash ai-tools/install-all.sh && claude
```

## Rule 2 — Log in to Claude Max
When `claude` launches, it opens your browser. Log in with your **Claude Max** account ([claude.ai/pricing](https://claude.ai/pricing)). First-time only.

## Rule 3 — Verify 115 skills loaded
In Claude Code, type:
```
/help
```
You should see `/office-hours`, `/ship`, `/autoplan`, and 112 more. If yes — you're ready.

## Rule 4 — Start every task with `/office-hours`
Before building anything, run `/office-hours`. Six forcing questions that save weeks of wrong direction.

## Rule 5 — Ship with `/ship`
Tests + PR + deploy in one command. Don't push manually.

## Rule 6 — Deep Readiness Pass (the Architect Bootstrap)

After the initial rebuild finishes, paste this **second prompt** into Claude. It audits the cloned repo, installs any missing dependencies, detects the framework, and starts the project — all without leaving Claude.

```
Act as a senior AI systems architect, senior full-stack engineer, senior repo setup operator, and careful QA/deployment assistant.

MISSION:
Perform a full automatic bootstrap and readiness pass for the public repo only inside the CURRENT Claude Code session, without making me leave Claude.

IMPORTANT CONTEXT:
- I am already inside Claude Code
- Do NOT tell me to go back to PowerShell, Terminal, or Command Prompt unless absolutely necessary
- Do NOT reinstall global tools that are already installed
- Do NOT break any working setup
- Be non-destructive, organized, and precise
- If something already exists, verify it instead of recreating it

PUBLIC REPO ONLY:
https://github.com/francky180/franc-system-template

CORE GOAL:
Automatically prepare the environment so the repo is cloned if needed, opened, inspected, dependencies installed if needed, and ready to run from inside this Claude session.

EXECUTION RULES:
- Do not ask unnecessary questions
- Do not create duplicate folders
- Do not overwrite working files unless required
- Prefer checking first, then acting
- If a step cannot be completed automatically, explain exactly what blocked it and give the single next command needed
- Show progress clearly by phase
- Keep all actions safe and reversible

PHASE 1 — ENVIRONMENT CHECK
1. Identify the current working directory
2. Confirm basic tools available in this environment:
   - git
   - node
   - npm
3. Report versions if available
4. Do NOT reinstall them if already present

PHASE 2 — REPO ACQUISITION
1. Check whether folder "franc-system-template" already exists in the current workspace
2. If missing, clone:
   git clone https://github.com/francky180/franc-system-template
3. If it already exists, do not duplicate it
4. Report the final folder path

PHASE 3 — PROJECT ENTRY
1. Change into:
   franc-system-template
2. Confirm the active working directory
3. Briefly inspect the repo structure and report key files/folders found

PHASE 4 — SAFE PROJECT AUDIT
Inside the repo:
1. Check for important project files such as:
   - package.json
   - package-lock.json
   - pnpm-lock.yaml
   - yarn.lock
   - README
   - .env.example
   - next.config.*
   - tsconfig.json
   - vercel.json
2. Detect the likely stack/framework
3. Summarize what kind of project it is
4. Do not invent files that are not there

PHASE 5 — DEPENDENCY SETUP
1. If package.json exists, inspect scripts
2. Install dependencies using the appropriate package manager
3. If install fails, diagnose clearly and propose the safest fix
4. Do not run unnecessary installs outside this repo

PHASE 6 — RUN READINESS
1. Determine the correct local start command from the package scripts
2. Determine whether the project should use:
   - npm run dev
   - npm start
   - another documented script
3. If safe and appropriate, start the project
4. If starting automatically is not appropriate, report the exact next command
5. If environment variables are required, identify that clearly without fabricating values

PHASE 7 — FINAL DELIVERY
Provide a clean final report with these sections:

1. CURRENT STATUS
- current working directory
- whether franc-system-template is present
- whether it is the active repo

2. WHAT WAS DONE
- cloned repo or verified existing repo
- dependency installs performed
- detected framework/stack
- whether the project was started successfully

3. WHAT IS READY
- what can be worked on immediately
- what command is next if anything still needs to be run

4. BLOCKERS
- anything that prevented completion
- exact reason
- exact next command only if necessary

5. RECOMMENDED NEXT ACTION
- the single best next step inside this Claude session

SPECIAL INSTRUCTIONS:
- Be proactive
- Execute commands when appropriate instead of only describing them
- Stay inside Claude workflow
- Minimize user effort
- Do not output vague advice
- Do not restart from scratch
- Do not touch unrelated folders
- Do not make assumptions beyond what you can verify
```

**When to run this:** Any time after the initial rebuild. It's idempotent — safe to re-run. Use it whenever you move the repo to a new machine, suspect something's out of sync, or want a readiness audit before starting work.

---

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **franc-system-template** (243 symbols, 233 relationships, 0 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## When Debugging

1. `gitnexus_query({query: "<error or symptom>"})` — find execution flows related to the issue
2. `gitnexus_context({name: "<suspect function>"})` — see all callers, callees, and process participation
3. `READ gitnexus://repo/franc-system-template/process/{processName}` — trace the full execution flow step by step
4. For regressions: `gitnexus_detect_changes({scope: "compare", base_ref: "main"})` — see what your branch changed

## When Refactoring

- **Renaming**: MUST use `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` first. Review the preview — graph edits are safe, text_search edits need manual review. Then run with `dry_run: false`.
- **Extracting/Splitting**: MUST run `gitnexus_context({name: "target"})` to see all incoming/outgoing refs, then `gitnexus_impact({target: "target", direction: "upstream"})` to find all external callers before moving code.
- After any refactor: run `gitnexus_detect_changes({scope: "all"})` to verify only expected files changed.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Tools Quick Reference

| Tool | When to use | Command |
|------|-------------|---------|
| `query` | Find code by concept | `gitnexus_query({query: "auth validation"})` |
| `context` | 360-degree view of one symbol | `gitnexus_context({name: "validateUser"})` |
| `impact` | Blast radius before editing | `gitnexus_impact({target: "X", direction: "upstream"})` |
| `detect_changes` | Pre-commit scope check | `gitnexus_detect_changes({scope: "staged"})` |
| `rename` | Safe multi-file rename | `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` |
| `cypher` | Custom graph queries | `gitnexus_cypher({query: "MATCH ..."})` |

## Impact Risk Levels

| Depth | Meaning | Action |
|-------|---------|--------|
| d=1 | WILL BREAK — direct callers/importers | MUST update these |
| d=2 | LIKELY AFFECTED — indirect deps | Should test |
| d=3 | MAY NEED TESTING — transitive | Test if critical path |

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/franc-system-template/context` | Codebase overview, check index freshness |
| `gitnexus://repo/franc-system-template/clusters` | All functional areas |
| `gitnexus://repo/franc-system-template/processes` | All execution flows |
| `gitnexus://repo/franc-system-template/process/{name}` | Step-by-step execution trace |

## Self-Check Before Finishing

Before completing any code modification task, verify:
1. `gitnexus_impact` was run for all modified symbols
2. No HIGH/CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 (WILL BREAK) dependents were updated

## Keeping the Index Fresh

After committing code changes, the GitNexus index becomes stale. Re-run analyze to update it:

```bash
npx gitnexus analyze
```

If the index previously included embeddings, preserve them by adding `--embeddings`:

```bash
npx gitnexus analyze --embeddings
```

To check whether embeddings exist, inspect `.gitnexus/meta.json` — the `stats.embeddings` field shows the count (0 means no embeddings). **Running analyze without `--embeddings` will delete any previously generated embeddings.**

> Claude Code users: A PostToolUse hook handles this automatically after `git commit` and `git merge`.

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
