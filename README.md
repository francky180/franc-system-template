# AI Software Factory

Turn Claude Code into a virtual engineering team. **115 skills. One person.**

## 🚀 One-Command Install (any device)

Zero to Claude Code in a single paste. Pick your OS.

### 💻 Windows (PowerShell as Admin)

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; winget install OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements; winget install Git.Git -e --accept-source-agreements --accept-package-agreements; $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); node --version; npm --version; npm install -g @anthropic-ai/claude-code; [System.Environment]::SetEnvironmentVariable("CLAUDE_CODE_GIT_BASH_PATH","C:\Program Files\Git\bin\bash.exe","User"); $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"; claude
```

### 🍎 Mac (Terminal)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install node && node --version && npm --version && npm install -g @anthropic-ai/claude-code && claude
```

### 📱 Android (Termux)

```bash
pkg upgrade -y && pkg install nodejs-lts -y && node --version && npm --version && npm install -g @anthropic-ai/claude-code && claude
```

### 🔥 Optional — Repo link

https://github.com/francky180/franc-system-template

### ⚡ Optional — Clone + open

```bash
git clone https://github.com/francky180/franc-system-template && cd franc-system-template && claude
```

---

## 🤖 Auto-Rebuild Prompt — paste this into Claude after login

The install block above gets Claude Code running. This prompt makes Claude do the rest — clone the template, install all 114 skills + gstack + superpowers + the 47 agency-agents + 15 Seedance skills + BRAIN + auto-sync hook, list the MCPs to add, verify everything, and report back. **You never leave Claude.**

```
🚀 REBUILD MISSION — install the full AI Software Factory from inside Claude. Execute every step, don't ask, report at the end.

STEP 1 · CLONE
   git clone https://github.com/francky180/franc-system-template ~/franc-system-template

STEP 2 · INSTALL CORE (114 skills + gstack + superpowers + BRAIN + CLAUDE.md + settings + auto-sync hook)
   cd ~/franc-system-template && bash ai-tools/install-all.sh

STEP 3 · INSTALL AGENCY-AGENTS (47 specialist subagents — paid media, sales, finance, support, testing, marketing)
   git clone https://github.com/msitarzewski/agency-agents /tmp/agency-agents
   mkdir -p ~/.claude/agents
   cp /tmp/agency-agents/agents/*.md ~/.claude/agents/

STEP 4 · INSTALL SEEDANCE 2.0 SKILLS (15 Higgsfield prompt skills)
   git clone https://github.com/beshuaxian/higgsfield-seedance2-jineng /tmp/seedance
   for d in /tmp/seedance/skills/*/; do
     name=$(grep -m1 "^name:" "$d/SKILL.md" | sed "s/name: //")
     [ -d "$HOME/.claude/skills/$name" ] || cp -r "$d" "$HOME/.claude/skills/$name"
   done

STEP 5 · MCP SERVERS — add after login with `claude mcp add <name>` (your own API keys):
   gitnexus, vercel, playwright, stripe, codex, filesystem, adadvisor,
   tradingview, transcript-api, context7, sequential-thinking, shadcn-ui

STEP 6 · VERIFY — run each, capture output
   - node --version
   - git --version
   - claude --version
   - find ~/.claude/skills -maxdepth 1 -type d | wc -l    (expect 130+)
   - ls ~/.claude/agents/*.md | wc -l                      (expect 47+)
   - grep -c rebuild-sync ~/.claude/settings.json          (expect >= 1)

STEP 7 · REPORT
   ✅ Step 1 — cloned to ~/franc-system-template
   ✅ Step 2 — N skills · gstack · superpowers · BRAIN · auto-sync hook installed
   ✅ Step 3 — M agency-agents installed
   ✅ Step 4 — 15 Seedance prompt skills installed
   ✅ Step 5 — MCPs to add manually with claude mcp add
   ✅ Verify — Node vXX · Git X.X · Claude X.X · NNN skills · MM agents · hook present

   End with: "Rebuild complete. Type /help to see all skills, then /office-hours to start your first build."

RULES
• Execute, don't ask. No "can I?" — just do it.
• install-all.sh and the copies are additive (no-clobber) — they never delete your existing skills.
• If a step fails, don't halt. Complete the rest, then show the one-line fix for the failure.
• Tone: short, confident, no apologies, no filler.
```

> **What you end up with:** 114 bundled skills + gstack (~35) + superpowers (~14) + 15 Seedance = **~178 skills**, **47 agency-agents**, the BRAIN vault, and the auto-sync hook. See [Quick Start (5 minutes)](#quick-start-5-minutes) below.

## What You Get When You Clone This Repo

**Bundled in this repo (114 skills — copied to `~/.claude/skills/` on install):**

| Category | Count | Examples |
|---|---|---|
| **Build · Deploy · Ops** | 41 | `/ship` `/land-and-deploy` `/canary` `/investigate` `/qa` `/review` `/retro` `/health` `/cso` `/autoplan` `/plan-ceo-review` `/plan-eng-review` |
| **Creator Marketing** | 31 | `/creator-outreach-sequence-generator` `/campaign-roi-calculator` `/niche-fit-scorer` `/creator-rate-estimator` `/brand-safety-screen` |
| **Marketing Suite** | 15 | `/market-ads` `/market-funnel` `/market-launch` `/market-seo` `/market-social` `/market-copy` `/market-landing` |
| **Design System** | 15 | `/design-consultation` `/design-shotgun` `/banner-design` `/frontend-design` `/ui-styling` `/ui-ux-pro-max` `/slides` |
| **GitNexus (code graph)** | 8 | `/gitnexus-impact-analysis` `/gitnexus-debugging` `/gitnexus-refactoring` `/gitnexus-pr-review` |
| **Best Practices** | 4 | `/next-best-practices` `/vercel-react-best-practices` `/remotion-best-practices` `/playwright-best-practices` |

**Plus installed automatically by `install-all.sh`:**

- **gstack** (~35+ specialist skills) — virtual team clone: CEO mode, eng manager, design lead, release engineer
- **Superpowers** (~14 process skills) — Obra's process toolkit for disciplined AI workflows
- **BRAIN vault** at `~/BRAIN` — Obsidian-navigable knowledge graph with the 100-book principle library
- **CLAUDE.md** global identity file with the 15 Always-On Principles + routing rules
- **settings.json** with the `rebuild-sync` PostToolUse hook (auto-snapshots every edit to a mirror repo)
- **Claude Code CLI** (if not already installed)
- **Bun runtime** (if not already installed)

**Plus added by the Auto-Rebuild Prompt (Steps 3–4):**

- **47 agency-agents** — specialist subagents for paid media, sales, finance, support, testing, marketing (→ `~/.claude/agents/`)
- **15 Seedance 2.0 skills** — Higgsfield cinematic video prompt library

**Post-install totals:** **~178 skill folders** in `~/.claude/skills/` (114 bundled + ~35 gstack + ~14 superpowers + 15 Seedance) and **47 agents** in `~/.claude/agents/`, plus the BRAIN vault and the auto-sync hook. Add the 12 MCPs with `claude mcp add` to complete the stack.

Run `/help` inside Claude Code to list every installed skill.

## The Sprint Lifecycle

Every task follows: **Think > Plan > Build > Review > Test > Ship > Reflect**

| Phase | What Happens |
|-------|-------------|
| Think | `/office-hours` asks 6 forcing questions before code |
| Plan | `/autoplan` runs CEO + design + eng review automatically |
| Build | Subagent-driven development with TDD enforced |
| Review | `/review` + `/cso` for code review + security audit |
| Test | `/qa` opens a real browser and tests your app |
| Ship | `/ship` runs tests, creates PR in one command |
| Reflect | `/retro` weekly retrospective, `/learn` compounds knowledge |

## Quick Start (5 minutes)

**Zero to Claude Code in one command.** Pick your OS and paste the block into your terminal — it installs Node.js, Claude Code, logs you in, and runs the install script.

All you need afterwards is a **Claude Max** subscription.

### 🪟 Windows (PowerShell — run as Administrator)

```powershell
winget install OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements; `
winget install Git.Git -e --accept-source-agreements --accept-package-agreements; `
refreshenv; `
npm install -g @anthropic-ai/claude-code; `
git clone https://github.com/francky180/franc-system-template.git "$HOME\ai-software-factory"; `
cd "$HOME\ai-software-factory"; `
bash ai-tools/install-all.sh; `
claude
```

### 🍎 Mac (Terminal)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
brew install node git && \
npm install -g @anthropic-ai/claude-code && \
git clone https://github.com/francky180/franc-system-template.git ~/ai-software-factory && \
cd ~/ai-software-factory && \
bash ai-tools/install-all.sh && \
claude
```

### 🐧 Linux (Debian / Ubuntu)

```bash
sudo apt update && sudo apt install -y curl git && \
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && \
sudo apt install -y nodejs && \
sudo npm install -g @anthropic-ai/claude-code && \
git clone https://github.com/francky180/franc-system-template.git ~/ai-software-factory && \
cd ~/ai-software-factory && \
bash ai-tools/install-all.sh && \
claude
```

### 📱 Termux (Android)

```bash
pkg upgrade -y && pkg install nodejs-lts git -y && \
npm install -g @anthropic-ai/claude-code && \
git clone https://github.com/francky180/franc-system-template.git ~/ai-software-factory && \
cd ~/ai-software-factory && \
bash ai-tools/install-all.sh && \
claude
```

### What happens

1. Installs Node.js LTS + Git (if missing)
2. Installs Claude Code globally via npm
3. Clones this template to `~/ai-software-factory`
4. Runs `install-all.sh` — copies all 115 skills into `~/.claude/skills/`
5. Launches `claude` — opens browser for Claude Max login (first-time only)

### Verify

Once Claude Code is running, type:

```
/help
```

You should see all 115 skills listed. If `/office-hours`, `/ship`, or `/autoplan` show up, you're done.

### Prerequisites (what the scripts install for you)

- **Git** — installed automatically
- **Node.js 18+** — installed automatically
- **Claude Code** — installed automatically
- **Claude Max subscription** — you need this separately ([claude.ai/pricing](https://claude.ai/pricing))

## All 115 Skills

### gstack — Virtual Engineering Team (40+)

| Command | Specialist | What They Do |
|---------|-----------|--------------|
| `/office-hours` | YC Office Hours | 6 forcing questions before code |
| `/plan-ceo-review` | CEO | Find the 10-star product |
| `/plan-eng-review` | Eng Manager | Lock architecture + test matrix |
| `/plan-design-review` | Designer | Rate design dimensions 0-10 |
| `/plan-devex-review` | DX Lead | Developer experience audit |
| `/autoplan` | Pipeline | All reviews in one command |
| `/review` | Staff Engineer | Finds bugs CI misses |
| `/cso` | Security Officer | OWASP + STRIDE + secrets audit |
| `/qa` | QA Lead | Real browser testing + bug fixes |
| `/qa-only` | QA Reporter | Test and report, no fixes |
| `/ship` | Release Engineer | Tests + PR in one command |
| `/land-and-deploy` | Release Engineer | Merge + verify production |
| `/deploy-to-vercel` | Deploy | Push to Vercel |
| `/canary` | SRE | Post-deploy monitoring |
| `/benchmark` | Perf Engineer | Core Web Vitals regression detection |
| `/investigate` | Debugger | Root-cause debugging |
| `/browse` | QA Engineer | Headless Chromium browser |
| `/open-gstack-browser` | Browser | Visible AI-controlled Chrome |
| `/connect-chrome` | Browser | GStack Browser with sidebar |
| `/webapp-testing` | Tester | Playwright-based web app testing |
| `/design-consultation` | Design Lead | Design system + aesthetic planning |
| `/design-shotgun` | Design Explorer | AI mockup variants + comparison |
| `/design-html` | Design Engineer | Mockup to production HTML |
| `/design-review` | Visual QA | Find and fix visual issues |
| `/retro` | Eng Manager | Weekly retrospective with trends |
| `/learn` | Memory | Cross-session learnings |
| `/health` | Dashboard | Code quality 0-10 score |
| `/codex` | Second Opinion | Independent code review via Codex |
| `/checkpoint` | State | Save + resume working state |
| `/document-release` | Docs | Post-ship documentation update |
| `/setup-deploy` | Config | Configure deploy platform |
| `/setup-browser-cookies` | Auth | Import cookies for testing |
| `/careful` | Safety | Warns before destructive commands |
| `/freeze` | Safety | Lock edits to one directory |
| `/unfreeze` | Safety | Remove directory lock |
| `/guard` | Safety | Full safety mode (careful + freeze) |
| `/pair-agent` | Collab | Pair a remote AI with your browser |
| `/skill-creator` | Meta | Create and test new skills |
| `/gstack-upgrade` | Maintenance | Upgrade gstack to latest |
| `/devex-review` | DX Audit | Live developer experience testing |

### Creator Marketing (31)

| Command | What It Does |
|---------|-------------|
| `/audience-demographic-analyzer` | Analyze influencer audience fit |
| `/brand-safety-screen` | Flag controversial creator content |
| `/campaign-brief-generator` | Generate ready-to-send campaign briefs |
| `/campaign-goal-to-kpi-framework-builder` | Map objectives to KPIs |
| `/campaign-roi-calculator` | Calculate ROI with leadership narrative |
| `/campaign-status-dashboard-digest` | Weekly status for Slack/email |
| `/content-approval-feedback-formatter` | Turn internal notes into creator feedback |
| `/content-capture-checklist-builder` | Monitoring checklist per platform |
| `/content-to-brief-compliance-checker` | Pass/fail against brief requirements |
| `/creator-briefing-faq-generator` | Anticipate creator questions |
| `/creator-content-concept-generator` | 5-10 native content ideas |
| `/creator-negotiation-assistant` | Rate negotiation with trade-off analysis |
| `/creator-outreach-sequence-generator` | Multi-touch outreach across platforms |
| `/creator-posting-compliance-tracker` | Track required vs actual posts |
| `/creator-rate-estimator` | Fair market rate estimation |
| `/engagement-rate-calculator-benchmarker` | Benchmark against platform averages |
| `/ftc-disclosure-spot-checker` | FTC compliance review |
| `/metrics-normalization-formatter` | Clean messy metrics into one table |
| `/multi-platform-format-adapter` | Adapt briefs for TikTok/IG/YT Shorts |
| `/niche-fit-scorer` | Score creator-brand alignment 1-10 |
| `/organic-repost-caption-writer` | Repost captions with proper credit |
| `/paid-ad-copy-adapter` | Turn organic content into ad copy |
| `/paid-social-creative-brief` | Paid social brief from creator posts |
| `/performance-benchmark-setter` | Pre-launch KPI benchmarks |
| `/post-campaign-creator-scorecard` | Score creators after campaign |
| `/quarterly-creator-program-review` | QBR with wins, misses, pivots |
| `/reply-triage-classifier` | Classify influencer replies into actions |
| `/story-metrics-screenshot-parser` | Parse Story insights screenshots |
| `/universal-creator-follow-up-chaser` | Follow-up sequences for any scenario |
| `/utm-parameter-builder` | Generate UTM tracking URLs |
| `/verbal-agreement-summarizer` | Summarize DM/email deal terms |

### Marketing Suite (15)

| Command | What It Does |
|---------|-------------|
| `/market` | Main orchestrator — launches all skills |
| `/market-ads` | Ad creative and copy generation |
| `/market-audit` | Full marketing audit (5 parallel agents) |
| `/market-brand` | Brand voice analysis and guidelines |
| `/market-competitors` | Competitive intelligence analysis |
| `/market-copy` | Copywriting analysis and generation |
| `/market-emails` | Email sequence generation |
| `/market-funnel` | Sales funnel analysis and optimization |
| `/market-landing` | Landing page CRO analysis |
| `/market-launch` | Product launch playbook |
| `/market-proposal` | Client proposal generator |
| `/market-report` | Marketing report (Markdown) |
| `/market-report-pdf` | Marketing report (PDF) |
| `/market-seo` | SEO content audit |
| `/market-social` | Social media calendar and content |

### Design System (12)

| Command | What It Does |
|---------|-------------|
| `/design` | Comprehensive design skill (brand, tokens, logos, banners, slides) |
| `/design-system` | Token architecture + component specs |
| `/frontend-design` | Production-grade UI with high design quality |
| `/canvas-design` | Visual art in PNG/PDF |
| `/banner-design` | Social media, ads, web, print banners |
| `/slides` | Strategic HTML presentations with Chart.js |
| `/ui-styling` | shadcn/ui + Tailwind styling |
| `/ui-ux-pro-max` | 50+ styles, 161 palettes, 57 font pairings |
| `/web-design-guidelines` | Web Interface Guidelines compliance |
| `/brand` | Brand voice and visual identity |
| `/brand-context` | Build brand context for all skills |
| `/brand-guidelines` | Apply brand colors and typography |

### GitNexus — Code Intelligence (7)

| Command | What It Does |
|---------|-------------|
| `/gitnexus-cli` | Index repos, check status, generate wiki |
| `/gitnexus-exploring` | Understand architecture and trace flows |
| `/gitnexus-debugging` | Trace bugs through the knowledge graph |
| `/gitnexus-impact-analysis` | Blast radius before editing code |
| `/gitnexus-refactoring` | Safe rename, extract, split, move |
| `/gitnexus-pr-review` | Review PRs with graph-aware context |
| `/gitnexus-guide` | Tools reference and schema docs |

### Best Practices (4)

| Command | What It Does |
|---------|-------------|
| `/next-best-practices` | Next.js file conventions, RSC, data patterns |
| `/vercel-react-best-practices` | React/Next.js performance from Vercel Engineering |
| `/playwright-best-practices` | Test writing, POM, CI/CD, flaky test fixes |
| `/remotion-best-practices` | Video creation in React |

### Utilities (6)

| Command | What It Does |
|---------|-------------|
| `/pdf` | Read, merge, split, watermark, create PDFs |
| `/mcp-builder` | Build MCP servers for external APIs |
| `/doc-coauthoring` | Structured doc/spec co-authoring workflow |
| `/agent-reach` | 17 platforms via CLI, MCP, curl, Python |
| `/superpowers` | Process discipline (design-first, TDD, review) |
| `/deploy-to-vercel` | Deploy apps to Vercel |

### Speed Comparison

| Task | Human Team | You + This System |
|------|-----------|-------------------|
| Scaffold a feature | 2 days | 15 min |
| Write tests | 1 day | 15 min |
| Build end-to-end | 1 week | 30 min |
| Bug fix + regression test | 4 hours | 15 min |
| Full marketing audit | 2 weeks | 20 min |
| Creator campaign brief | 3 hours | 5 min |

## BRAIN Obsidian Vault

The `BRAIN/` folder is an Obsidian vault with linked navigation:

```
BRAIN/
├── core/           — Master prompt, sprint workflow, control panel
├── navigation/     — Index, dashboard
├── systems/        — Architecture, AI Software Factory reference
├── tools/          — Tool nodes (gstack, marketing, etc.)
├── projects/       — Project template nodes
└── automations/    — Webhook maps, API plans
```

Open it in Obsidian: File > Open Vault > select the `BRAIN` folder.

## Customization

After install, personalize your system:

1. Edit `BRAIN/core/MASTER_PROMPT.md` with your business context
2. Edit `BRAIN/core/MASTER_MEMORY.md` with your stack and preferences
3. Edit `~/CLAUDE.md` with your project-specific routing rules
4. Add your projects to `BRAIN/navigation/dashboard.md`

## Hard Rules (Built Into The System)

1. No code without a design. Ever.
2. No production code without a failing test.
3. No merge without review. Both stages.
4. No "done" without verification.
5. No fixing without investigation first.

## License

Free to use. The underlying tools are MIT licensed:
- gstack: https://github.com/garrytan/gstack
- Superpowers: https://github.com/nicholasgriffintn/superpowers
