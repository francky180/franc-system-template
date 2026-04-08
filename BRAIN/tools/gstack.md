# gstack

## Role
Virtual engineering team for Claude Code. 23+ specialist roles, real browser, design tools, security auditing, and complete sprint workflow. Turns one developer into a full team.

## Layer
Tools — Execution layer (pairs with [[tools/Superpowers]])

## Source
- **Author**: Garry Tan (Y Combinator CEO)
- **Repo**: https://github.com/garrytan/gstack
- **License**: MIT
- **Requires**: Bun v1.0+, Node.js (Windows)

## Install

In Claude Code, paste:

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup
```

Then add gstack section to project CLAUDE.md.

**Windows note**: Node.js required alongside Bun (Bun has a Playwright pipe bug on Windows).

## The Sprint

**Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect**

Each skill feeds into the next. Nothing falls through the cracks.

## Specialist Roles (23+)

### Phase: THINK
| Skill | Specialist | What They Do |
|-------|-----------|--------------|
| `/office-hours` | YC Office Hours | 6 forcing questions that reframe product before code |
| `/plan-ceo-review` | CEO / Founder | Find the 10-star product. 4 modes: Expansion, Selective, Hold, Reduction |
| `/plan-eng-review` | Eng Manager | Lock architecture, data flow, edge cases, test matrix |
| `/plan-design-review` | Senior Designer | Rate each dimension 0-10, explain what 10 looks like |
| `/plan-devex-review` | DX Lead | Benchmark against competitors, trace friction, 20-45 questions |
| `/autoplan` | Review Pipeline | One command: CEO + design + eng review automatically |

### Phase: BUILD
| Skill | Specialist | What They Do |
|-------|-----------|--------------|
| `/design-consultation` | Design Partner | Build complete design system from scratch |
| `/design-shotgun` | Design Explorer | Generate 4-6 AI mockup variants, comparison board, taste memory |
| `/design-html` | Design Engineer | Mockup to production HTML. 30KB, zero deps. Detects React/Svelte/Vue |

### Phase: REVIEW
| Skill | Specialist | What They Do |
|-------|-----------|--------------|
| `/review` | Staff Engineer | Finds bugs that pass CI but break prod. Auto-fixes obvious ones |
| `/codex` | Second Opinion | Independent review from OpenAI Codex CLI. Cross-model analysis |
| `/cso` | Chief Security Officer | OWASP Top 10 + STRIDE threat model. Zero false positives |
| `/design-review` | Designer Who Codes | Design audit + atomic fix commits |
| `/devex-review` | DX Tester | Live developer experience audit |

### Phase: TEST
| Skill | Specialist | What They Do |
|-------|-----------|--------------|
| `/qa` | QA Lead | Real browser, find bugs, fix with atomic commits, regression tests |
| `/qa-only` | QA Reporter | Same methodology, report only, no code changes |
| `/benchmark` | Performance Engineer | Core Web Vitals, page load, before/after per PR |
| `/browse` | QA Engineer | Real Chromium, ~100ms/command, persistent sessions |

### Phase: SHIP
| Skill | Specialist | What They Do |
|-------|-----------|--------------|
| `/ship` | Release Engineer | Tests, VERSION bump, CHANGELOG, push, PR. One command |
| `/land-and-deploy` | Release Engineer | Merge PR, wait CI, verify production health |
| `/canary` | SRE | Post-deploy monitoring: console errors, perf, page failures |
| `/document-release` | Technical Writer | Updates ALL project docs to match what shipped |

### Phase: REFLECT
| Skill | Specialist | What They Do |
|-------|-----------|--------------|
| `/retro` | Eng Manager | Weekly retro, per-person breakdowns, shipping streaks |
| `/learn` | Memory | Manages learnings across sessions. Knowledge compounds |

### Safety & Utility
| Skill | What It Does |
|-------|-------------|
| `/careful` | Warns before destructive commands |
| `/freeze` | Lock edits to one directory |
| `/guard` | Both careful + freeze |
| `/unfreeze` | Remove edit lock |
| `/investigate` | Root-cause debugging, auto-freezes to module |
| `/pair-agent` | Multi-agent browser sharing with security isolation |
| `/setup-browser-cookies` | Import cookies from Chrome/Arc/Brave/Edge |
| `/gstack-upgrade` | Self-updater |

## Browser Architecture

- Persistent Chromium daemon (sub-second commands ~100ms after first call)
- Ref system (`@e1`, `@e2`) for element interaction without CSS selectors
- Cookie import from real browsers
- Anti-bot stealth via `/open-gstack-browser`
- Sidebar agent for natural language browser control
- Browser handoff for CAPTCHAs/MFA

## Integration

- **Pairs with**: [[tools/Superpowers]] (process discipline)
- **Used by**: [[tools/Claude_Code]] (primary environment)
- **Works with**: Conductor (10-15 parallel sprints), OpenClaw, Codex, Cursor, and 8+ AI agents

## Connected

- [[tools/Claude_Code]]
- [[tools/Superpowers]]
- [[systems/AI_SOFTWARE_FACTORY]]
- [[core/SPRINT_WORKFLOW]]
