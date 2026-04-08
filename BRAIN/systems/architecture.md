# System Architecture

Full connected architecture of Franc's AI business ecosystem.

**Connected**: [[systems/FULL_SYSTEM]]

---

## Layered Architecture

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
║              │  MANYCHAT   │  DM qualifier + router            ║
║              └──────┬──────┘                                  ║
║                     │  webhook POST                           ║
║              ┌──────▼──────┐                                  ║
║              │   VERCEL    │  API routes per project           ║
║              └──────┬──────┘                                  ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 3 — MONETIZATION                                       ║
║                                                               ║
║    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ║
║    │   FREE      │  │   $250      │  │   $1,500    │         ║
║    │  Broker /   │  │  Course /   │  │ Management/ │         ║
║    │  Affiliate  │  │  Core pkg   │  │  DFY pkg    │         ║
║    └─────────────┘  └─────────────┘  └─────────────┘         ║
║                            │                                  ║
║                     ┌──────▼──────┐                           ║
║                     │   STRIPE    │  Checkout + webhooks       ║
║                     └─────────────┘                           ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 4 — INTELLIGENCE                                       ║
║                                                               ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     ║
║  │ CLAUDE   │  │   GHL    │  │   N8N    │  │ REMOTION │     ║
║  │Code/Desk │  │  (CRM)   │  │ (future) │  │ (video)  │     ║
║  └──────────┘  └──────────┘  └──────────┘  └──────────┘     ║
╠═══════════════════════════════════════════════════════════════╣
║  LAYER 5 — BRAIN (THIS SYSTEM)                                ║
║                                                               ║
║  C:\Users\franc\BRAIN\                                        ║
║  ├── core/           Intelligence & prompts                   ║
║  ├── navigation/     Entry points & status                    ║
║  ├── systems/live/   Business flow nodes                      ║
║  ├── tools/          Tool chain nodes                         ║
║  ├── projects/       Project nodes                            ║
║  ├── automations/    Execution specs                          ║
║  └── claude-export/  Raw source data                          ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Per-Project Architecture

### phimindflow-site (Forex)

```
Instagram → ManyChat DM → Vercel API (:3001) → Stripe / Genesis FX
```

**Theme**: dark + gold | **Status**: LIVE on Vercel

### ai-agency-system (ClientFlow)

```
Instagram → ManyChat DM → Vercel API (:3003) → Stripe checkout
```

**Theme**: dark + gold | **Status**: Active on GitHub

### credit-system (CreditPath)

```
Instagram → ManyChat DM → Vercel API (:3002) → Affiliate links
```

**Theme**: light + blue | **Status**: In progress (0 commits)

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
| DM Auto | ManyChat | Webhook integration |
| CRM | GHL | Stub only |
| Orchestration | N8N | Planned |
