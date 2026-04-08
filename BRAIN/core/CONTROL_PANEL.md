# CONTROL PANEL

Full operating manual for the BRAIN system.

**Connected**: [[navigation/index]]

---

## What This System Is

BRAIN is your local AI operating system — a single folder that holds all intelligence, prompts, automation blueprints, and architecture docs. It works with:

- **Claude Code** — paste `core/MASTER_PROMPT.md` as system instruction
- **Claude Desktop** — use as project instructions in any Claude project
- **ManyChat** — follow `automations/manychat-flow.md` to build DM flows
- **Vercel** — follow `automations/vercel-api-plan.md` to scaffold API routes
- **Obsidian** — open `C:\Users\franc\BRAIN` as a vault for linked navigation
- **VS Code** — open as workspace for editing and development

---

## How To Use Each File

### `core/MASTER_MEMORY.md`
**When**: Starting a new Claude conversation, onboarding a new AI tool, or refreshing context.
**How**: Copy relevant sections into your system prompt or project instructions.

### `core/MASTER_PROMPT.md`
**When**: Setting up Claude Code, Claude Desktop, or any AI assistant.
**How**: Paste the entire file as your system instruction.

### `automations/manychat-flow.md`
**When**: Building or modifying Instagram DM automation.
**How**: Follow the flow architecture diagram. Each vertical has its own trigger keywords and routes.

### `automations/vercel-api-plan.md`
**When**: Scaffolding backend API routes in any project.
**How**: Use the shared API pattern as your template.

### `automations/webhook-map.md`
**When**: Wiring services together or debugging data flow.
**How**: Follow the connection diagram top-to-bottom.

### `systems/architecture.md`
**When**: Understanding how the full system fits together.
**How**: Read the layered architecture diagram.

### `systems/FULL_SYSTEM.md`
**When**: Seeing every node in the entire operating system.
**How**: Navigate the system map or view in Obsidian graph.

### `systems/FULL_BUSINESS_FLOW.md`
**When**: Understanding the revenue pipeline end-to-end.
**How**: Follow the 8-stage linear flow: TRAFFIC → STRIPE → LOOP.

### `tools/` folder
**When**: Understanding what each tool does and how they chain.
**How**: Start at Claude_Code and follow the toolchain.

### `projects/` folder
**When**: Checking status or finding a project's connections.
**How**: Each project node lists its tools and deployment status.

---

## Maintenance Rules

1. **Update `navigation/dashboard.md`** when project status changes
2. **Update `core/MASTER_MEMORY.md`** when business context changes
3. **Update `automations/webhook-map.md`** when adding a new service connection
4. **Update system nodes in `systems/live/`** when integrations change
5. **Never edit `claude-export/`** — those are raw backups, read-only
6. **Keep files linked** — new files should link to their direct parent or neighbor only (not to FULL_SYSTEM)

---

## Adding New Files

1. Create the file in the appropriate folder
2. Add a link to it from `navigation/index.md`
3. Add a row to `navigation/dashboard.md`
4. Link to the most relevant parent note (not FULL_SYSTEM directly)

---

## Opening In Each Tool

| Tool | How to Open |
|------|------------|
| **Obsidian** | Open Vault → select `C:\Users\franc\BRAIN` |
| **VS Code** | File → Open Folder → `C:\Users\franc\BRAIN` |
| **Claude Code** | `cd C:\Users\franc\BRAIN` then work normally |
| **File Explorer** | Navigate to `C:\Users\franc\BRAIN` |
