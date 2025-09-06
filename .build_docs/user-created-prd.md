# VibeLayerAI —  (PRD) v2.1 (Mobile Parity, Build‑Ready)

**Status:** Final — Build‑Ready
**Owner:** Product (Omar)
**Scope:** Conversation‑aware visual effects for **public livestreams** (TikTok Live, Twitch, YouTube).
**Stack (locked):** Control Panel — **Next.js 15 + React + TypeScript + shadcn/ui (PWA)**. Web Overlay — **Headless TypeScript + WebGL (Pixi/regl) + Lottie**. Mobile — **iOS (Swift/Metal) + Android (Kotlin/OpenGL ES/Vulkan) with Lottie**. Agents — **LangGraph + PydanticAI**. AI — **Google‑only** (Speech‑to‑Text v2; **Gemini 2.5 Flash** for intent; **Gemini 2.5 Flash Image** for Phase‑2 sprites, off‑path). Data/API — **Convex**. Auth — **BetterAuth** or **NextAuth** (adapter). Secrets — **Doppler**. Monorepo — **pnpm** workspaces.

---

## 1. Executive Summary

**Live Effects AI** is a web‑ and mobile‑first, privacy‑aware, real‑time effects system for livestream creators. It listens (with consent), interprets conversation intent (multi‑speaker aware, music‑robust), and surfaces **ranked, one‑tap effects** rendered as a transparent overlay (web) or native overlay (mobile) while the creator streams. A **Brand Kit** ensures consistent aesthetic. A prominent **Panic** control guarantees safety. ROI analytics correlate effects to tips/donations.

**Primary JTBD:** “Turn live moments into reactive visuals without breaking the creator’s flow — on **mobile or desktop**.”
**Key differentiators:** p95 ≤ 500 ms suggestions; **mobile feature parity** with native overlay+encode; Google‑only AI for speed/cost; **agentic orchestration**; deterministic effect packs; enterprise‑grade security/cost guardrails.

---

## 2. Goals & SLOs (Non‑Negotiable)

**Technical (Marcus priority):**

* **Suggestion latency** (partial transcript → top‑3 UI): **p50 ≤ 300 ms**, **p95 ≤ 500 ms** (web & mobile).
* **Activation → first frame:** **≤ 100 ms** (web overlay), **≤ 120 ms** (mobile).
* **Runtime:** **60 fps target / 30 fps floor**; **dropped frames ≤ 1% p95**.
* **Overlay ready (URL → ready):** **≤ 500 ms**.
* **Reliability uptime:** **> 99.5%** (overlay + WS hub + companion aggregate).

**Business (Sarah priority):**

* **Activation D0 ≥ 60%** (enable listening + ≥1 trigger).
* **Income lift tracking enabled:** report **Δ tips/donations per hour** and **Δ conversion rate** vs. baseline.

**UX (Jamie priority):**

* **Zero‑config success rate:** ≥ **70%** creators trigger an effect with **no settings changed** on first **mobile** session.
* **Suggestion CTR ≥ 35%** (median stream).

---

## 3. Non‑Goals (MVP)

* Public template marketplace.
* Third‑party social feed.
* On‑path T2I; Phase‑2 only, **async/off‑path**.

---

## 4. Personas & Use Cases

* **TikTok Mobile Creator (primary):** Streams from phone; needs one‑hand UI, brand consistency, and instant Panic.
* **Streamer (Twitch/YouTube):** Desktop studio; wants auto fireworks on wins.
* **Podcaster (Live):** Needs tasteful lower‑thirds, low CPU, and brand control.

**JTBD:** Stay in flow; impress audience; predictable performance; mobile parity.

---

## 5. Product Scope

### 5.1 Must‑Have (GA — Web + Mobile Parity)

1. **Listening & Intent:** STT v2 streaming + VAD, **speaker diarization**, **music/speech gate**.
2. **Suggestions & Ranker:** Gemini 2.5 Flash labels; deterministic ranker with **brandScore**, speaker routing (Host‑only), cooldowns.
3. **Brand Consistency:** **Brand Kit** (palette, fonts, allowed categories, motion intensity) applied everywhere.
4. **Emergency Controls:** **Panic** (UI, hotkey, optional voice).
5. **Rendering:**

   * **Web Overlay:** Headless TS + WebGL/Lottie; premultiplied‑alpha; WS client.
   * **Mobile Overlay:** iOS (Metal + Lottie) / Android (GL/Vulkan + Lottie), deterministic seeds, thermal governor.
6. **Streaming:**

   * **Web:** Overlay URL for OBS/TikTok Live Studio (first‑class integration & guide).
   * **Mobile:** In‑app **RTMP** out where stream key/ingest is permitted; otherwise full AI features without video injection.
7. **Control Panel (PWA) & Mobile UI:** Live queue, manual library, brand kit, thresholds, speaker routing, Panic.
8. **ROI Analytics:** Effect→income correlation; dashboard (earnings per hour, per effect, lift vs. baseline).
9. **Security/Privacy/Observability:** Tokens, CSP/SRI/Trusted Types, Doppler, SLO dashboards, runbooks.

### 5.2 Phase‑2 (off‑path T2I & advanced encode)

* **Gemini 2.5 Flash Image** sprites (SynthID), cached; voice commands.
* Encoder enhancements: 60 fps profile; HEVC/AV1 where supported.

---

## 6. Architecture Overview

* **apps/control-panel** — Next.js 15 + React + shadcn/ui; **mobile‑first PWA**; TanStack Query + Zustand; **BetterAuth/NextAuth**; Stripe.
* **apps/overlay** — Static bundle (CDN). Headless TS + WebGL/Lottie; premultiplied‑alpha; WS client; zero React in render loop.
* **apps/mobile‑ios** — Swift/Metal + AVFoundation + Lottie; native RTMP encoder.
* **apps/mobile‑android** — Kotlin/OpenGL ES/Vulkan + CameraX + Lottie; native RTMP encoder.
* **services/ws‑hub** — Node/Fastify WS, JWT, rooms, autoscale; region‑aligned with Convex.
* **services/agents** — **LangGraph + PydanticAI** orchestrating STT ↔ Gemini Flash ↔ ranker ↔ safety ↔ governor ↔ renderer; Observer for SLO/ROI.
* **data/api** — **Convex** (rooms, suggestions, activations, quotas, telemetry, ROI; live queries).
* **AI** — Google Cloud **STT v2** (streaming, diarization), **Gemini 2.5 Flash** (text), **Gemini 2.5 Flash Image** (Phase‑2, async).

**Data flow:** Mic → AEC/VAD → **Music gate** → STT (+diarization) → Intent → Rank (brand/speaker) → Safety/Quota → `{effect.activate}` → Overlay render → **RTMP out (mobile)** / Studio compose (web) → Telemetry/ROI → Convex.

---

## 7. Agentic Architecture (LangGraph + PydanticAI, Google‑Only)

**Agents:**

* **ListenerAgent** (GCP STT v2 + diarization + music classifier) → emits `speech.partial|final {speakerId, musicProb}`.
* **IntentAgent** (Gemini 2.5 Flash) → `intent.detected {label, confidence, speakerId}`.
* **SuggestionAgent** (deterministic ranker) → obeys **Brand Kit** + **speaker routing** (Host‑only) → `suggest.emit` (top‑N, TTL).
* **SafetyAgent** (policy/blocklists) → gates sensitive intents.
* **GovernorAgent** (quotas/tier/cooldowns).
* **RendererAgent** (WS/mobile commands; first‑frame SLO).
* **T2IAgent** (Phase‑2; async sprites; cache).
* **ObserverAgent** (SLO + ROI correlation + alerts).

**Topics:** `speech.partial`, `speech.final`, `intent.detected`, `suggest.emit`, `auto.trigger`, `effect.activate`, `effect.done`, `rate.limit.hit`, `overlay.ready`, `overlay.health`, `roi.event`.
**Contracts (PydanticAI):** `Transcript{speakerId, musicProb}`, `Intent{speakerId}`, `Suggestion{brandScore}`, `ActivateCmd{deadlineMs}`.
**Guardrails:** per‑node SLO checks; **Kill Switches** per agent node and effect pack; checkpoints; retries with back‑pressure.

---

## 8. Privacy, Safety & Compliance (Public Livestream Mode)

* **Context:** Public broadcast; still minimize processing.
* **Default:** **Transcripts‑only**, ephemeral windows; **no audio upload** by default; big **Listening** indicator; pause hotkey.
* **Sensitive intents (no auto‑trigger):** self‑harm, hate, NSFW, politics, trademark/brands.
* **Retention:** Telemetry 24h (crash repro) → anonymized aggregates.
* **Platform filters:** TikTok/Twitch/YouTube “no‑go” effect lists configured.

---

## 9. Security & Token Hardening

**Overlay/mobile token (JWT/EdDSA):** `iss`, `aud`, `sub=sessionId`, `iat`, `nbf`, `exp ≤ 180s`, `jti` (nonce).
**Replay prevention:** store `jti` in TTL store (≤5 min); reject reuse.
**Signed URL (web):** `/overlay?token=<JWT>` (only).
**Headers (panel):** CSP (no `unsafe-inline`), **SRI** for all static, **Trusted Types**, **HSTS** 6 months, **COOP/COEP**, **X‑Frame‑Options**\*\*:DENY\*\*.
**Build gates:** SCA clean; secret scan clean; bundle budgets (§12) enforced.

---

## 10. Environment & Secrets (Doppler)

* Doppler project `live-effects-ai`, configs: `local`, `dev`, `staging`, `prod`, `preview`.
* Injection: `doppler run -c <env> -- …` across panel, ws‑hub, agents; **no secrets** in overlay/mobile bundles.
* **Public keys** must start `NEXT_PUBLIC_` (panel only).
* Keys: Google creds (prefer Workload Identity in cloud), Gemini, Convex, Stripe, WS signing, Auth provider.
* **Rotation:** 90 days; audit enabled.

---

## 11. Capacity & Load Model

**Targets (per region):** 500 concurrent overlays; **1,000 concurrent mobile listeners**; **2,000 WS connections** total; **150 suggestions/sec** burst (50/sec sustained).
**Mobile session budgets:** 1 WS + 1 STT stream; **uplink ≤ 100 kbit/s** for STT; **RTMP ≤ 3 Mbps** at 1080p\@30.
**Convex:** ≤ 2 live queries/session; telemetry sample 20% sessions.
**Scale triggers:** CPU > 60% (3 min) **OR** WS send p95 > 150 ms **OR** send queue > 100.
**Soak:** 2 hours @ 50% target; WS drop ≤ 0.1%; send p95 ≤ 150 ms.
**Chaos:** kill 1 WS pod → reconnect ≤ 3 s; no duplicate triggers.

---

## 12. Device/Browser/GPU Matrix & Budgets

**Web Matrix:** Win11 Chrome (Intel Iris Xe), macOS 14 Safari 17+ (Apple M1/M2), Win11 Chrome (NVIDIA GTX 1650).
**Mobile Matrix:** iOS **A15+** (iPhone 13+), Android **Snapdragon 8 Gen1+** / recent Mali/Adreno equivalents.
**Budgets:** Web overlay JS ≤ **1.5 MB gz**; textures ≤ **8 MB**; heap ≤ **100 MB**; VRAM soft cap ≤ **256 MB**.
**Fallback ladder:** particles 2000→1200→700 → blur off → **Lottie‑only** → pause activations.
**Triggers:** RAF long‑task ratio > 10% over 30 s **or** CPU > 45% for 15 s.

---

## 13. Feature Requirements & Acceptance Criteria (GA)

### 13.1 Intelligent Suggestions

* **User Story:** As a creator, I want relevant effects suggested in real time so I can trigger them without thinking.
* **Functional:** STT v2 streaming; Gemini 2.5 Flash labels: `birthday, win, loss, magic, gratitude, hype, romance`; ranker = intent×confidence×recency×diversity×**brandScore**; emit top‑3 (TTL=5s).
* **AC (G/W/T):** Given listening ON and phrase “happy birthday,” When confidence ≥ 0.85, Then ≥ 3 suggestions appear **≤ 500 ms p95**, tagged `celebration.birthday`, no duplicates; cooldown **8 s** for auto‑trigger.

### 13.2 Auto‑Trigger

* **Functional:** Threshold slider (0.5–0.95); debounce 8 s.
* **AC:** When threshold met, exactly **one** effect plays with `source=auto`; Undo available **5 s**.

### 13.3 Manual Library & Search

* **Functional:** Filter by tags/FPS cost; instant search; thumbnails.
* **AC:** Search ≤ **150 ms**; activation ≤ **100 ms**.

### 13.4 Effect Activation & Runtime

* **AC:** First frame ≤ **100 ms** (web) / **120 ms** (mobile); 60 fps target / 30 floor; dropped frames ≤ **1% p95**; alpha preserved in recordings.

### 13.5 Web Overlay & Studio Integration

* **AC:** Overlay URL ready ≤ **500 ms**; reconnect ≤ **3 s**; up to 3 overlays per scene with z‑order control; TikTok Live Studio presets verified.

### 13.6 Safety & Governor

* **AC:** Sensitive intents never auto‑trigger; manual override shows warning; quotas enforced and `rate.limit.hit` logged.

### 13.7 Multi‑Speaker Handling (Collabs)

* **Functional:** Diarization `speakerId`; per‑speaker thresholds; **Host‑only** toggle; speaker badges in queue.
* **AC:** With Host‑only ON, guest phrases never auto‑trigger; badges visible for all suggestions.

### 13.8 Background Music Filtering

* **Functional:** Music/speech classifier; gate when `musicProb > 0.7`; spectral subtraction; speech energy threshold.
* **AC:** With trending sound at −5 dB vs speech, WER degradation ≤ **+5%**; lyric false triggers reduced ≥ **80%** vs naive.

### 13.9 Brand Consistency Controls

* **Functional:** **Brand Kit** (colors, fonts, allowed categories, motion intensity); ranker **brandScore**; linting.
* **AC:** Disallowed categories never suggested; applied colors respect palette within ΔE ≤ **3**.

### 13.10 Emergency Controls (Panic)

* **Functional:** Big **Panic** (UI, hotkey, optional voice).
* **AC:** Panic stops active effect in **≤ 200 ms**, prevents new activations for **10 s**, and shows **Undo** within **5 s**.

### 13.11 Mobile Render & Streaming

* **Functional:** Native overlay (Metal/GL) composited on camera; **RTMP** out where ingest allowed.
* **AC:** 1080p\@30 floor on A15+/SD8G1+ with dropped frames ≤ **1% p95**; reconnect ≤ **3 s**.

### 13.12 ROI Dashboard

* **Functional:** Effect activations + donation/tip events (connectors/manual/CSV); **60 s post‑effect** + **±30 s** model; confidence scoring.
* **AC:** Dashboard renders per‑effect lift; R² ≥ **0.6** on synthetic dataset; flags low‑confidence sessions.

---

## 14. Effect Pack Spec (Determinism) & Certification

**Preset JSON (required):** `id`, `engine('webgl'|'lottie'|'metal'|'gl')`, `params{}`, `seed`, `timebase('frames'|'ms')`, `gpuCost(1..5)`, `seizureRisk(boolean)`.
**Certification checklist:** deterministic seed; fps profile on target matrices; seizure‑risk test; SynthID on AI sprites; JSON schema validation in CI.
**AC:** Same seed+params render bit‑identical for 30 s on same device.

---

## 15. Cost & Quota Guardrails

**AI cost target:** ≤ **\$0.06 / active hour** (Pro).
**Quotas:** suggestions ≤ **250/hr** per stream; Phase‑2 T2I: Free ≤ **20/day**, Pro ≤ **500/mo**.
**Alerts:** 80/90/100% monthly budget; per‑user minute‑rate anomaly.
**Calculator:** `cost = (WPM * minutes * suggestRate * cost_suggest) + (T2I * cost_image)`.

---

## 16. Observability & Runbooks

**Metrics:** suggestion latency/activation latency/fps/cpu‑gpu/reconnects/WER/cost per hour; mobile thermal throttling events.
**Dashboards:** real‑time SLO + weekly cohorts.
**Correlation IDs:** propagate `cid` panel → agents → overlay/mobile.
**Runbooks:**

* **Suggest p95 > 500 ms:** pause IntentAgent enrichment; serve cached bundles; page on‑call.
* **FPS floor breach:** apply degrade ladder; if persists, **Lottie‑only**.
* **WS reconnect storm:** scale hub; throttle telemetry.
  **AC:** Staging drills; recovery < **5 min**; SLOs restored.

### 16.1 ROI & Monetization Analytics

* **Goal:** Attribute **effects → income** with correlation windows.
* **Sources:** Platform connectors, manual logs, CSV.
* **Model:** 60‑second **post‑effect** window + **±30 s** symmetric model; confidence bands.
* **AC:** R² ≥ **0.6** on synthetic tests; low‑confidence flagged.

---

## 17. Localization & Accessibility

**Locales:** EN GA; ES/JA Phase‑2; STT language policy documented.
**Panel/Companion a11y:** keyboard‑only path; large touch targets; ARIA labels; contrast ≥ **4.5:1**.
**AC:** Axe scan passes; mobile can operate one‑handed; keyboard flow on web.

---

## 18. Release Plan

**GA (6 weeks):** Web Overlay + Control Panel (PWA) **and Mobile Apps (iOS + Android)** with full parity (listen/intent/suggest/brand/panic/ROI) and **in‑app RTMP** for accounts with ingest; TikTok Live Studio presets & guide.
**Phase‑2 (10 weeks):** Voice commands; **Gemini Flash Image** sprites (off‑path); encoder 60 fps profile; HEVC/AV1 where supported; expanded locales.
**Stage gates:** p95 ≤ **500 ms**, uptime > **99.5%**, zero‑config ≥ **70%** (mobile), fps ≥ **30 floor** on target devices, crash‑free ≥ **99.7%** overlay sessions.

---

## 19. Risks & Mitigations

* **Platform ingest access:** Some creators lack stream keys. *Mitigation:* Full AI parity regardless; enable live overlay output when eligible; document steps to obtain ingest.
* **Device variance (Android):** Wide GPU/thermal profiles. *Mitigation:* aggressive degradation ladder; Lottie‑only fallback; preflight device profile.
* **Thermals (mobile):** Continuous camera + GPU. *Mitigation:* thermal governor reduces emitters before frame drops; cap resolution/fps under heat.
* **Vendor lock‑in (accepted):** Google‑only AI now; thin internal interface for future portability.
* **Music false triggers:** Classifier + gate + thresholds; test sets per genre.

---

## 20. Data Model (Convex)

**Collections:**
`users { id, email, role, stripeCustomerId }`
`sessions { id, userId, tier, region, deviceType, createdAt }`
`overlays { id, userId, tokenHash, ttl, status }`
`suggestions { id, sessionId, speakerId, intent, confidence, score, brandScore, ttlMs, autoEligible, createdAt }`
`effects { id, kind, engine, params, seed, gpuCost, seizureRisk }`
`activations { id, sessionId, effectId, source, latencyMs, ts }`
`quotas { userId, t2iMonthly, t2iUsed, suggestionsUsed, resetAt }`
`telemetry { sessionId, fps, cpu, gpu, thermal, ts }`
`roi { sessionId, effectId, revenue, eventTs, attributionWindow }`

**Queries/Mutations:** `getOverlayToken()`, `listSuggestions(sessionId)`, `recordActivation()`, `consumeQuota(userId, kind)`, `upsertEffect(effect)`, `recordMonetizationEvent()`.

---

## 21. API & Event Contracts

**Suggestion**

```json
{
  "id": "sugg_9f2",
  "ts": 1730912345,
  "window": "t-3s..now",
  "speakerId": 1,
  "intent": "celebration.birthday",
  "confidence": 0.91,
  "brandScore": 0.88,
  "candidates": [
    { "effectId": "fireworks_rainbow_v2", "params": {"duration": 2.8} },
    { "effectId": "balloon_float_v1" },
    { "effectId": "confetti_burst_v3" }
  ],
  "autoTriggerEligible": true,
  "ttlMs": 5000
}
```

**Effect Definition**

```json
{
  "id": "sparkles_shower_v3",
  "engine": "webgl",
  "params": {"emitRate": 220, "gravity": 0.25, "lifetime": 1.6, "sprite": "sparkle_04"},
  "seed": 12345,
  "timebase": "frames",
  "gpuCost": 1,
  "seizureRisk": false
}
```

**Activation Event**

```json
{ "event": "effect.activate", "effectId": "sparkles_shower_v3", "source": "auto|manual", "deadlineMs": 100 }
```

**Event Taxonomy (excerpt):** `overlay_ready`, `speech.partial`, `speech.final`, `intent.detected`, `suggest.emit`, `auto.trigger`, `effect.activate`, `effect.done`, `rate.limit.hit`, `fps.sample`, `cpu.gpu.sample`, `thermal.throttle`, `ws.reconnect`, `roi.event`.

---

## 22. Coding, Style & Repo Standards

* **Monorepo:** **pnpm** workspaces; packages: `effects-engine`, `protocol`, `brand-kit`, `config`.
* **UI System:** **shadcn/ui**; consistent tokens; dark mode default.
* **Overlay/Mobile:** deterministic RNG; strict bundle budgets (§12); Metal/GL parity for params & seeds.
* **Type Safety:** strict TS; zod/io‑ts schemas mirrored in Swift/Kotlin models.
* **Testing:** unit (agents, ranker); perf tests (web+mobile overlays); staging drills (runbooks).
* **CI Guards:** lint/typecheck/test; bundle/secret/SCA scans; size budgets.

---

## 23. Acceptance Tests (E2E)

1. **Zero‑config Mobile Start** — Given fresh install, when creator signs in and taps **Listen**, then **≥ 3** suggestions render **≤ 500 ms p95** with no settings changed.
2. **Host‑only on Collab** — With two speakers and Host‑only ON, when guest says “happy birthday,” then **no auto‑trigger**; suggestions show speaker badges.
3. **Music On, Speech Clear** — With trending sound at −5 dB vs speech, when phrase “that’s magical” is said, then **no lyric‑induced triggers**; WER degradation ≤ **+5%**.
4. **Web Overlay Alpha** — When overlay URL added to OBS/TikTok Studio, then ready ≤ **500 ms** and alpha preserved at t=1 s and t=30 s.
5. **Mobile Render + Stream** — With RTMP configured, when effect activates, then first‑frame ≤ **120 ms**, fps ≥ **30 floor**, reconnect ≤ **3 s** on network blip.
6. **Panic Everywhere** — When Panic is triggered, then all effects stop in **≤ 200 ms**, **10 s** lockout applies, **Undo** within **5 s**.

---

## 24. Open Questions

1. TikTok ingest/stream‑key eligibility: rollout assumptions by region.
2. Final pricing tier for Pro; annual discount.
3. Initial locales beyond EN; STT languages roadmap.
4. Minimum Android GPU profiles for marketing guarantees.

---

## 25. Appendices

* **A. Effect JSON Schema** (machine‑readable)
* **B. Sensitive Intent Taxonomy & Blocklists**
* **C. Platform Policy Map (TikTok/Twitch/YouTube)**
* **D. Cost Calculator Inputs** (WPM, suggestRate, T2I usage)
* **E. Runbooks (full)**
* **F. CSP & Security Policy** (final headers)
* **G. Environment & Device Matrix** (full)
