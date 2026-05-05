# Codex Review - franc-system-template - 2026-04-26

## Summary
Reviewed the clean-mode boot contract against the live workspace root at `C:\Users\franc\Projects`. The public/template repo is not currently a complete source of truth for the four-file contract because `SYSTEM_PROMPT.md` and `CODEX.md` are missing, while root `AGENTS.md` and `CLAUDE.md` contain older template/GitNexus setup material that does not match the live workspace contract.

## Findings (severity-ordered)

### HIGH - Missing clean-mode contract files
**File:** `SYSTEM_PROMPT.md`, `CODEX.md`
**Issue:** The boot prompt expects both files at the template repo root, but neither exists in `franc-system-template` or the freshly cloned `franc-system-template-latest`. This makes Step 0/Step 1 fail for clean installs.
**Suggested fix:** Add root copies of the current live workspace files:
- `C:\Users\franc\Projects\SYSTEM_PROMPT.md`
- `C:\Users\franc\Projects\CODEX.md`

### HIGH - Template AGENTS/CLAUDE drift from live workspace contract
**File:** `AGENTS.md`, `CLAUDE.md`
**Issue:** The template versions contain setup/GitNexus bootstrap content and differ materially from the live clean workspace contract files. A fresh user following the template will not get the same Claude/Codex operating rules as the live workspace.
**Suggested fix:** Merge the clean live contract content from:
- `C:\Users\franc\Projects\AGENTS.md`
- `C:\Users\franc\Projects\CLAUDE.md`

Preserve any template-specific install guidance in `README.md`, `install.ps1`, or dedicated setup docs instead of mixing it into the root operating contract.

### MEDIUM - Boot prompt references template files that the public repo does not publish
**File:** `README.md` or boot prompt source
**Issue:** Clean Mode tells Codex to diff `SYSTEM_PROMPT.md`, `AGENTS.md`, `CLAUDE.md`, and `CODEX.md` at the template root. Two of those paths are missing, so the first boot creates a false failure signal.
**Suggested fix:** Either publish all four files at the template root or update the boot prompt to point at their actual canonical location.

## Test gaps
- No automated check confirms that the template root contains all four required contract files.
- No CI/scripted check compares template contract files against the live workspace contract before publishing.

## Residual risk
After adding the missing files, the template may still contain stale setup instructions in root contract files unless setup content is moved into README/install docs and the four contracts remain policy-only.
