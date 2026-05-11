# System Architecture

Full connected architecture of your AI business ecosystem.

> **Template — customize for your stack.** Replace project rows and tool names with your actual setup.

**Connected**: [[systems/FULL_SYSTEM]]

---

## Layered Architecture (example)

```
╔═══════════════════════════════════════════════════════════════╗
║  LAYER 1 — CONTENT & TRAFFIC                                 ║
║                                                               ║
║  Instagram ──── TikTok ──── YouTube Shorts                    ║
║       │              │              │                          ║
║       └──────────────┴──────────────┘                         ║
║                      │                                        ║
║              Comment / DM / Bio link                          ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 2 — AUTOMATION & CAPTURE                               ║
║                                                               ║
║              ┌─────────────┐                                  ║
║              │ DM_AUTO     │  DM qualifier + router            ║
║              └──────┬──────┘                                  ║
║                     │  webhook POST                           ║
║              ┌──────▼──────┐                                  ║
║              │   WEB API   │  API routes per project           ║
║              └──────┬──────┘                                  ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 3 — MONETIZATION                                       ║
║                                                               ║
║    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ║
║    │   FREE      │  │   $TIER 1   │  │   $TIER 2   │         ║
║    │  Lead /     │  │  Core /     │  │  Premium /  │         ║
║    │  Affiliate  │  │  Standard   │  │  DFY pkg    │         ║
║    └─────────────┘  └─────────────┘  └─────────────┘         ║
║                            │                                  ║
║                     ┌──────▼──────┐                           ║
║                     │  CHECKOUT   │  Stripe / Paddle / etc.    ║
║                     └─────────────┘                           ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 4 — INTELLIGENCE                                       ║
║                                                               ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     ║
║  │ CLAUDE   │  │   CRM    │  │   N8N    │  │ REMOTION │     ║
║  │Code/Desk │  │  (GHL)   │  │ (future) │  │ (video)  │     ║
║  └──────────┘  └──────────┘  └──────────┘  └──────────┘     ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 5 — BRAIN (THIS SYSTEM)                                ║
║                                                               ║
║  ~/BRAIN/                                                     ║
║  ├── core/           Intelligence & prompts                   ║
║  ├── navigation/     Entry points & status                    ║
║  ├── systems/        Architecture documentation               ║
║  ├── tools/          Tool chain nodes                         ║
║  ├── projects/       Project nodes (add your own)             ║
║  ├── automations/    Execution specs                          ║
║  └── claude-export/  Raw source data                          ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Per-Project Architecture (template)

### your-project-1

```
Social → DM Auto → Web API → Checkout / Affiliate
```

**Theme**: your-theme | **Status**: your-status

### your-project-2

```
Social → DM Auto → Web API → Checkout
```

**Theme**: your-theme | **Status**: your-status

### your-project-3

```
Social → DM Auto → Web API → Affiliate links
```

**Theme**: your-theme | **Status**: your-status

> Create one section per project. Use the format above as the starting point.

---

## Tech Stack Reference

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | Next.js | 16.2.1 |
| UI | React | 19 |
| Language | TypeScript | 5 (strict) |
| Styling | Tailwind CSS | 4 (@import) |
| Animation | Motion | 12 |
| Video | Remotion | 4.x |
| Hosting | Vercel | Latest |
| AI (dev) | Claude Code | Opus 4.6 |
| AI (chat) | OpenAI | gpt-4o-mini |
| Payments | Stripe | Checkout + Webhooks |
| DM Auto | ManyChat / Zernio | Webhook integration |
| CRM | GHL | API integration |
| Orchestration | N8N | Planned |
