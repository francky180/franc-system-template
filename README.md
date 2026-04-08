# AI Software Factory

Turn Claude Code into a virtual engineering team. 102+ skills. One person.

## What This Is

A complete AI-powered software development system that gives you:

- **Superpowers** (14 skills) — Process discipline: design-first, TDD, two-stage code review, subagent-driven development
- **gstack** (35+ skills) — Virtual team: CEO, eng manager, designer, QA lead, security officer, release engineer, and 17 more specialists as slash commands
- **Marketing Suite** (49 skills) — Campaigns, content, outreach, ROI, compliance, creator marketing
- **BRAIN** — Obsidian vault that documents the entire system with linked navigation
- **One-click rebuild** — Script that installs everything on a fresh computer in 5 minutes

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

### Prerequisites

- Git — https://git-scm.com/
- Node.js 18+ — https://nodejs.org/
- Claude Code with Claude Max subscription

### Install

```bash
cd ~
git clone https://github.com/francky180/franc-system-template.git ai-software-factory
cd ai-software-factory
bash ai-tools/install-all.sh
```

### Verify

```bash
ls ~/.claude/skills/
```

You should see `gstack/`, `superpowers/`, and all skill directories.

## What You Get

### gstack Specialists (35+)

| Command | Specialist | What They Do |
|---------|-----------|--------------|
| `/office-hours` | YC Office Hours | 6 forcing questions before code |
| `/plan-ceo-review` | CEO | Find the 10-star product |
| `/plan-eng-review` | Eng Manager | Lock architecture + test matrix |
| `/plan-design-review` | Designer | Rate design dimensions 0-10 |
| `/autoplan` | Pipeline | All reviews in one command |
| `/review` | Staff Engineer | Finds bugs CI misses |
| `/cso` | Security Officer | OWASP + STRIDE audit |
| `/qa` | QA Lead | Real browser testing |
| `/ship` | Release Engineer | Tests + PR in one command |
| `/land-and-deploy` | Release Engineer | Merge + verify production |
| `/canary` | SRE | Post-deploy monitoring |
| `/investigate` | Debugger | Root-cause debugging |
| `/benchmark` | Perf Engineer | Core Web Vitals |
| `/design-shotgun` | Design Explorer | AI mockup variants |
| `/design-html` | Design Engineer | Mockup to production HTML |
| `/browse` | QA Engineer | Real Chromium browser |
| `/retro` | Eng Manager | Weekly retrospective |
| `/learn` | Memory | Cross-session learnings |
| `/careful` | Safety | Warns before destructive commands |
| `/freeze` | Safety | Lock edits to one directory |

### Superpowers Process Skills (14)

| Skill | What It Does |
|-------|-------------|
| brainstorming | Design-first. No code without approval. |
| writing-plans | Bite-sized tasks with complete code |
| subagent-driven-development | Fresh agent per task + two-stage review |
| test-driven-development | RED-GREEN-REFACTOR mandatory |
| systematic-debugging | 4-phase root cause process |
| requesting-code-review | Severity-based review gates |
| using-git-worktrees | Isolated workspace per branch |
| finishing-a-development-branch | Merge/PR decision workflow |

### Speed Comparison

| Task | Human Team | You + This System |
|------|-----------|-------------------|
| Scaffold a feature | 2 days | 15 min |
| Write tests | 1 day | 15 min |
| Build end-to-end | 1 week | 30 min |
| Bug fix + regression test | 4 hours | 15 min |

## BRAIN Obsidian Vault

The `BRAIN/` folder is an Obsidian vault with linked navigation:

```
BRAIN/
├── core/           — Master prompt, sprint workflow, control panel
├── navigation/     — Index, dashboard
├── systems/        — Architecture, AI Software Factory reference
├── tools/          — Tool nodes (Superpowers, gstack, etc.)
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
- Superpowers: https://github.com/obra/superpowers
