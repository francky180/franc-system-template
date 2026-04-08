# AI Software Factory

Complete unified system combining [[tools/Superpowers]] (process discipline) and [[tools/gstack]] (specialist execution) into a full virtual engineering organization.

**Connected**: [[systems/FULL_SYSTEM]] | [[systems/architecture]]

---

## How They Fit Together

```
SUPERPOWERS (Process)              GSTACK (Execution + Tooling)
========================           ==============================
Brainstorming ──────────────────>  /office-hours (deeper, product-focused)
Writing Plans ──────────────────>  /plan-ceo-review -> /plan-eng-review -> /autoplan
Subagent-Driven Dev ────────────>  Implementation with /review gates
Test-Driven Development ────────>  /qa (browser-based verification)
Requesting Code Review ─────────>  /review + /codex (multi-model)
Finishing Branch ───────────────>  /ship + /land-and-deploy + /canary
Systematic Debugging ───────────>  /investigate + /browse
Verification ───────────────────>  /qa + /benchmark
```

**Superpowers** = the **discipline** (TDD, spec-first, plan-first, quality gates)
**gstack** = the **team** (23 specialists, browser, design tools, security, deploy pipeline)

---

## The Full Sprint Lifecycle

```
╔══════════════════════════════════════════════════════════════════╗
║  PHASE 1: THINK                                                  ║
║                                                                  ║
║  User has an idea                                                ║
║       │                                                          ║
║       ├── /office-hours (gstack) ── 6 forcing questions          ║
║       ├── brainstorming (superpowers) ── Socratic design Q&A     ║
║       └── Write spec doc ── User approves                        ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  PHASE 2: PLAN                                                   ║
║                                                                  ║
║  Design approved                                                 ║
║       │                                                          ║
║       ├── /plan-ceo-review (gstack) ── Scope challenge           ║
║       ├── /plan-eng-review (gstack) ── Architecture lock         ║
║       ├── /plan-design-review (gstack) ── Design quality         ║
║       └── writing-plans (superpowers) ── Bite-sized tasks        ║
║           OR /autoplan (gstack) ── All reviews in one command    ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  PHASE 3: BUILD                                                  ║
║                                                                  ║
║  Plan approved                                                   ║
║       │                                                          ║
║       ├── subagent-driven-dev (superpowers)                      ║
║       │     ├── Fresh agent per task                             ║
║       │     ├── TDD enforced (test-driven-development)           ║
║       │     ├── Spec compliance review ── must pass              ║
║       │     └── Code quality review ── must pass                 ║
║       │                                                          ║
║       └── /design-shotgun + /design-html (gstack) for UI work   ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  PHASE 4: REVIEW                                                 ║
║                                                                  ║
║  All tasks complete                                              ║
║       │                                                          ║
║       ├── /review (gstack) ── Staff engineer review              ║
║       ├── /codex (gstack) ── Multi-model second opinion          ║
║       ├── /cso (gstack) ── Security audit (OWASP + STRIDE)      ║
║       └── Final code reviewer subagent (superpowers)             ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  PHASE 5: TEST                                                   ║
║                                                                  ║
║  Reviews pass                                                    ║
║       │                                                          ║
║       ├── Run full test suite                                    ║
║       ├── /qa (gstack) ── Real browser, find + fix bugs          ║
║       └── /benchmark (gstack) ── Core Web Vitals, perf           ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  PHASE 6: SHIP                                                   ║
║                                                                  ║
║  QA passes                                                       ║
║       │                                                          ║
║       ├── /ship (gstack) ── Tests, VERSION, CHANGELOG, PR       ║
║       ├── /land-and-deploy (gstack) ── Merge, CI, verify prod   ║
║       └── /canary (gstack) ── Post-deploy monitoring             ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  PHASE 7: REFLECT                                                ║
║                                                                  ║
║  Shipped                                                         ║
║       │                                                          ║
║       ├── /retro (gstack) ── Weekly retro, shipping streaks      ║
║       └── /learn (gstack) ── Log learnings for future sessions   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Quick Reference: Which Skill When?

| When You Need... | Invoke | System |
|---|---|---|
| Product thinking before code | `/office-hours` | gstack |
| Socratic design refinement | `brainstorming` | Superpowers |
| Challenge scope and vision | `/plan-ceo-review` | gstack |
| Lock architecture | `/plan-eng-review` | gstack |
| Design quality audit | `/plan-design-review` | gstack |
| DX quality audit | `/plan-devex-review` | gstack |
| Write implementation plan | `writing-plans` | Superpowers |
| Full auto-review pipeline | `/autoplan` | gstack |
| Execute plan with subagents | `subagent-driven-development` | Superpowers |
| Build a design system | `/design-consultation` | gstack |
| Explore visual designs | `/design-shotgun` | gstack |
| Turn mockup to production HTML | `/design-html` | gstack |
| Code review | `/review` | gstack |
| Second AI opinion | `/codex` | gstack |
| Security audit | `/cso` | gstack |
| Root-cause debugging | `/investigate` | gstack |
| Browser-based QA | `/qa` or `/qa-only` | gstack |
| Performance benchmarks | `/benchmark` | gstack |
| Ship code | `/ship` | gstack |
| Deploy + verify | `/land-and-deploy` | gstack |
| Post-deploy monitoring | `/canary` | gstack |
| Update all docs | `/document-release` | gstack |
| Weekly retro | `/retro` | gstack |
| Browse the web | `/browse` | gstack |
| Safety guardrails | `/careful`, `/freeze`, `/guard` | gstack |
| Session learnings | `/learn` | gstack |
| TDD enforcement | `test-driven-development` | Superpowers |
| Systematic debugging | `systematic-debugging` | Superpowers |
| Git worktree isolation | `using-git-worktrees` | Superpowers |
| Finish development branch | `finishing-a-development-branch` | Superpowers |

---

## Parallel Sprints

With Conductor or multiple Claude Code sessions, run 10-15 sprints simultaneously:
- Each sprint follows the full lifecycle independently
- Git worktrees provide isolation per branch
- Smart review routing (CEO doesn't review infra, design review skips backend)
- `/retro global` aggregates across all projects

---

## Connected

- [[tools/Superpowers]] — Process discipline
- [[tools/gstack]] — Specialist execution
- [[tools/Claude_Code]] — Primary environment
- [[core/SPRINT_WORKFLOW]] — The master prompt
- [[systems/architecture]] — Full system architecture
