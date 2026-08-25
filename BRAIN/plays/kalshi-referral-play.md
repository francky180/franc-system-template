# Play: Kalshi Referral — "Trade the Outcome"

**Asset:** `https://kalshi.com/sign-up/?referral=f7ea1241-d50f-4229-81c2-985744e7f091&utm_source=perps_web_int`
**Type:** Personal referral / affiliate-style acquisition play
**Status:** Draft — confirm payout terms before spending time or money

---

## 1. What the link actually is

| Part | Value | Meaning |
|------|-------|---------|
| Destination | `kalshi.com/sign-up` | Account creation page (not a market page — cold landing) |
| `referral` | `f7ea1241-…7091` | Your referral ID. This is what gets you credited. |
| `utm_source` | `perps_web_int` | Kalshi's own internal tag: perpetuals surface, web, internal. It is **their** source tag, not yours — it tells you nothing about where *your* traffic came from. |

**Immediate implication:** the URL as-is gives you zero channel attribution. If you push this to more than one place, you cannot tell what worked. Fix that before you post anything (see §6).

Kalshi is a CFTC-regulated US event-contract exchange — users buy/sell yes/no contracts on real-world outcomes (elections, econ prints, sports, weather, crypto levels). The `perps` tag points at their perpetual-style products, which are the higher-frequency, trader-facing surface.

---

## 2. The economics (fill this in before you run it)

Referral programs of this type pay on a **funded + traded** trigger, not on sign-up. Do not assume a flat bounty per click.

Confirm these four numbers from Kalshi's current referral terms:

1. **Trigger** — sign-up? first deposit? first N contracts traded? deposit minimum?
2. **Payout** — flat bounty, revenue share on fees, or both? Cap per referrer?
3. **Window** — how long after click does the attribution cookie live?
4. **Eligibility** — states excluded, KYC requirements, self-referral rules, whether paid ads / incentivized traffic are allowed.

Then compute your break-even:

```
Effective CPA = (spend + hours × your rate) / funded referrals
Play is live only if:  payout per funded referral  >  Effective CPA
```

Rough funnel decay to plan against (assume until you have real data):
`100 clicks → ~15–25 sign-ups → ~5–10 funded → ~4–8 payout-qualified`

That means **a payout event costs you roughly 15–25 clicks**. Price your effort accordingly.

---

## 3. Who this converts

Converts:
- Sports bettors who already have DK/FD accounts and are hunting better pricing
- Crypto and perps traders (the `perps_web_int` surface is built for them)
- Election / macro / news-cycle obsessives — the "I called that" crowd
- FinTwit, econ-print watchers (CPI, NFP, Fed days)

Does not convert:
- General audiences. "Sign up for a trading app" is not a hook.
- Anyone outside the US or in an excluded state — wasted click.
- Under-18. Do not target them, ever.

---

## 4. The core creative insight

**Nobody signs up for a link. They sign up for a market.**

The unit of content that works is a *specific live market with a live price*, plus a reason the price is interesting. The link is the last line, not the point.

| ❌ Dead | ✅ Works |
|---------|---------|
| "Sign up for Kalshi, best prediction market" | "Market has Fed cutting at 71¢. Every economist I read says that's high. Here's why I'm on the other side." |
| "Use my link for a bonus" | "This is what a 4% CPI print pays out. I took the position this morning at 34¢." |
| Screenshot of the app | Screenshot of *your position*, with the P&L visible |

Post the market. Explain the read. Drop the link underneath with disclosure.

---

## 5. Channel plan

| Channel | Fit | Notes |
|---------|-----|-------|
| **X / Twitter** | ★★★★★ | Best fit. Thread on a live market, then reply-under-breaking-news. Highest velocity on Fed days, CPI, election nights, big games. |
| **Group chats / Discord** | ★★★★★ | Highest conversion rate, lowest volume. Warm traffic converts 5–10×. Only in servers where it's allowed. |
| **YouTube Shorts / TikTok** | ★★★☆☆ | Reach is there, but financial-promo policy is strict and enforcement is inconsistent. Disclose in-video **and** in caption. Expect some takedowns. |
| **Reddit** | ★★☆☆☆ | Most relevant subs ban referral links outright. Read every sidebar. Getting banned from r/sportsbook costs more than one payout is worth. |
| **Newsletter / blog** | ★★★★☆ | Slow, but compounding and fully compliant. A single evergreen "how event contracts work" post keeps earning. |
| **Paid ads** | ☆☆☆☆☆ | Do not, unless Kalshi's terms explicitly permit it. Fastest way to get your referral ID killed. |

---

## 6. Fix the tracking before you post

Add your own source parameter so you can tell channels apart. Keep `referral` exactly as-is — that is what pays you.

```
X thread     …&utm_medium=x_thread
Discord      …&utm_medium=discord_warm
Shorts       …&utm_medium=yt_shorts
Newsletter   …&utm_medium=newsletter
```

Then wrap each variant in a short link you control (Bitly, Dub, your own domain) so you get click counts Kalshi's dashboard won't give you.

**Track weekly:**
`clicks → sign-ups → funded → qualified payouts → $ per hour spent`

Kill any channel that hasn't produced a funded referral after 100 clicks.

---

## 7. Compliance guardrails — non-negotiable

- **Disclose every time.** "#ad" alone is weak here. Use plain language: *"I get paid if you sign up and trade through this link."* FTC endorsement rules apply to referral links, not just brand deals.
- **No guaranteed-return language.** Never "risk-free," "free money," "guaranteed," "can't lose," "easy profit." These are the phrases that draw regulator attention and platform bans.
- **State that people can lose money.** Because they can.
- **18+ / eligible states only.** Never target or tag minors. Never post into a teen-audience context.
- **Respect the room.** If a sub, server, or platform bans referral links, that is the rule — a ban costs more than the bounty.
- **Never buy sign-ups, never self-refer, never use alt accounts.** That is fraud against the program and gets the ID clawed back.
- **Don't give financial advice.** Share your own position and reasoning. Do not tell people what to do with their money.

---

## 8. Kill criteria

Stop the play if any of these are true:
- 200 clicks, zero funded referrals
- Payout terms turn out to be revenue-share-only with a long window (you'll wait months for cents)
- Effective CPA exceeds payout after two weeks of real data
- You get one platform strike — the account is worth more than the program

---

## 9. The prompt

Paste this into Claude Code (or any agent) to generate the full campaign. Replace the bracketed fields first.

```
You are running a referral acquisition play for a US prediction-market exchange.

REFERRAL LINK (use verbatim, never alter the `referral` param):
https://kalshi.com/sign-up/?referral=f7ea1241-d50f-4229-81c2-985744e7f091&utm_source=perps_web_int

CONTEXT
- Product: Kalshi — CFTC-regulated US event-contract exchange. Users trade yes/no
  contracts on real outcomes: elections, Fed decisions, CPI prints, sports, weather,
  crypto price levels. The link points at the perps/high-frequency trader surface.
- My audience: [WHERE YOU POST + WHO FOLLOWS YOU + rough follower count]
- My angle/credibility: [e.g. "I post macro takes" / "I'm a sports bettor" / "crypto trader"]
- Channels I'll actually use: [X / Discord / Shorts / newsletter — pick max 2 to start]
- Payout terms I've confirmed: [trigger, amount, window — or write "unknown, assume
  funded+traded trigger"]
- Time I can spend weekly: [hours]

WHAT I NEED

1. THREE CONTENT ANGLES, each built on a specific, currently-plausible market —
   not generic app praise. For each: the market, the price level, the contrarian or
   non-obvious read, and why my audience specifically cares.

2. FOR EACH ANGLE, WRITE THE ACTUAL POSTS:
   - X: a 5-7 post thread, hook post standalone-strong, link in the final post
   - X: 3 short standalone posts usable as replies under breaking news
   - Discord/group-chat: one message that reads like a person, not a promo
   - Short-form video: a 30-second script with on-screen text cues and a spoken
     disclosure line
   Match my voice from the angle/credibility above. No hype vocabulary.

3. A POSTING CALENDAR keyed to real catalysts — Fed meetings, CPI/NFP release days,
   major sporting events, election dates. Volume follows news; so should I.

4. TRACKING SETUP: a distinct tagged URL per channel (preserve the `referral` param
   exactly, add utm_medium), plus the weekly metrics table I should fill in:
   clicks → sign-ups → funded → qualified payouts → $/hour.

5. COMPLIANCE PASS on everything you wrote:
   - Explicit paid-referral disclosure in every single post, in plain English
   - Zero guaranteed-return, "risk-free", or "free money" language
   - Loss disclosure present where required
   - 18+ / eligible-states framing
   - Flag anything likely to trip platform financial-promo policy

CONSTRAINTS
- Never write a post that is just the bare link. Every post leads with a market.
- Never claim or imply guaranteed profit.
- Never recommend a position as advice — frame as my own position and reasoning.
- If you don't know a current market price, mark it [VERIFY PRICE] rather than
  inventing a number.

OUTPUT: markdown, copy-paste ready, organized by channel.
```

### Short version (one-shot)

```
Write me 5 X posts and 2 Discord messages promoting my Kalshi referral link
(https://kalshi.com/sign-up/?referral=f7ea1241-d50f-4229-81c2-985744e7f091&utm_source=perps_web_int)
to an audience of [WHO]. Every post must lead with a specific tradeable market and a
real reason it's interesting — never with the link. Include an explicit "I get paid if
you sign up through this" disclosure in each. No guaranteed-return language. Mark any
price you can't verify as [VERIFY PRICE].
```

---

## 10. Related skills in this repo

| Task | Skill |
|------|-------|
| Set brand voice before generating copy | `brand-context` |
| Build the tagged tracking URLs | `utm-parameter-builder` |
| Check the disclosure language | `ftc-disclosure-spot-checker` |
| Adapt one angle across platforms | `multi-platform-format-adapter` |
| Write the organic captions | `organic-repost-caption-writer` |
| Report on results | `campaign-roi-calculator` |
