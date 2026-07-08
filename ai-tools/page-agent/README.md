# Page Agent — INSTALLED + VERIFIED WORKING (2026-07-07)
Installed page-agent@1.11.0. Live test: gave it ONE English sentence → it filled 2 form fields + clicked submit, verified via real DOM changes. Works.

## Fastest eval (proven working) — one line, demo LLM (eval only, do NOT ship)
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.11.0/dist/iife/page-agent.demo.js" crossorigin="true"></script>

## PRODUCTION — drop into asf-live / any client site (bring your own model)
NEVER expose an LLM key client-side. Use a proxy route + point Page Agent at it.

### 1. Client component (Next.js / React) — components/Copilot.tsx
```tsx
'use client'
import { useEffect } from 'react'
import { PageAgent } from 'page-agent'
export function Copilot() {
  useEffect(() => {
    const agent = new PageAgent({
      model: 'meta/llama-3.1-70b-instruct', // any OpenAI-compatible model
      baseURL: '/api/agent',                // your proxy (hides key, dodges CORS)
      apiKey: 'proxy',                      // dummy; real key stays server-side
      language: 'en-US',
    })
    return () => agent.dispose()
  }, [])
  return null
}
```
Mount `<Copilot/>` in the dashboard layout → clients talk to their dashboard.

### 2. Proxy route (hides key) — app/api/agent/route.ts  → forwards to NVIDIA NIM (free, OpenAI-compatible)
```ts
export const runtime = 'edge'
export async function POST(req: Request) {
  const body = await req.text()
  const r = await fetch('https://integrate.api.nvidia.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${process.env.NVIDIA_API_KEY}` },
    body,
  })
  return new Response(r.body, { status: r.status, headers: { 'Content-Type': 'application/json' } })
}
```

## Level-ups (in docs)
- Chrome extension → multi-tab tasks (work across the whole browser, not one page)
- MCP server (beta) → JARVIS/Claude control the client's page over MCP

## Where it plugs into the machine
DELIVERY layer. Every ASF dashboard + client site gets a talk-to-it copilot for free.
Proven working. Reference test: Projects/websites/page-agent-test/test.html
