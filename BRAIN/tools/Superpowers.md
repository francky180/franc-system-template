# Superpowers

## Role
Process discipline engine for AI coding agents. Enforces design-first, test-first, review-always methodology. 14 composable skills that transform Claude Code into a disciplined engineering team.

## Layer
Tools — Process layer (feeds into [[tools/gstack]])

## Source
- **Author**: Jesse Vincent (obra)
- **Repo**: https://github.com/obra/superpowers
- **License**: MIT
- **Version**: 5.0.7

## Install

```bash
/plugin install superpowers@claude-plugins-official
```

Or via marketplace:

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

## Skills (14)

| Skill | Trigger | What It Does |
|-------|---------|--------------|
| **brainstorming** | Before ANY creative work | HARD-GATES code. Socratic Q&A, one question at a time, produces spec before code |
| **writing-plans** | After design approval | Breaks specs into 2-5 min tasks with exact paths, full code, zero placeholders |
| **subagent-driven-development** | Plan approved | Fresh subagent per task + two-stage review (spec compliance then code quality) |
| **executing-plans** | Plan approved (alternative) | Batch execution with human checkpoints |
| **test-driven-development** | During ALL implementation | RED-GREEN-REFACTOR. Code before test = DELETE IT |
| **systematic-debugging** | Bug investigation | 4-phase root cause. Evidence over guessing |
| **dispatching-parallel-agents** | Independent tasks | Concurrent subagent workflows |
| **requesting-code-review** | Between tasks | Reviews against plan, severity-based blocking |
| **receiving-code-review** | After review feedback | Responding to review comments |
| **using-git-worktrees** | Before implementation | Isolated workspace per feature branch |
| **finishing-a-development-branch** | All tasks complete | Merge/PR decision, worktree cleanup |
| **verification-before-completion** | Before declaring done | Ensures it actually works, not "looks fixed" |
| **writing-skills** | Creating new skills | Meta-skill for skill authoring |
| **using-superpowers** | Orientation | Introduction to the skills system |

## Hard Rules

1. **NEVER write code without a design** — Every project goes through brainstorming first, no matter how simple
2. **NEVER write production code without a failing test** — RED-GREEN-REFACTOR is mandatory
3. **NEVER skip reviews** — Spec compliance first, then code quality. Both must pass
4. **NEVER declare done without verification** — Run tests, prove it works
5. **YAGNI ruthlessly** — Don't add beyond what was asked

## Workflow

```
Brainstorming → Writing Plans → Subagent-Driven Dev → Code Review → Finish Branch
     │                │                  │                  │              │
  Spec doc      Plan with tasks    Fresh agent/task    Two-stage       Merge/PR
  approved       2-5 min each      TDD enforced       review gates    cleanup
```

## Integration

- **Feeds into**: [[tools/gstack]] (execution layer)
- **Used by**: [[tools/Claude_Code]] (primary environment)
- **Philosophy**: Design before code, test before implement, verify before ship

## Connected

- [[tools/Claude_Code]]
- [[tools/gstack]]
- [[systems/AI_SOFTWARE_FACTORY]]
- [[core/SPRINT_WORKFLOW]]
