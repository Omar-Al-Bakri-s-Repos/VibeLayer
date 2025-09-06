# Project Brief: VibeLayerAI - Live Effects Platform

**Status:** Build-Ready  
**Created:** 2025-09-06  
**Owner:** Product (Omar)  
**Version:** 1.0  

---

## Executive Summary

**VibeLayerAI** is a mobile-first, real-time visual effects platform that transforms live conversations into reactive overlays for livestream creators. The system listens to speech with consent, interprets conversational intent using AI, and surfaces ranked, one-tap effects that render as transparent overlays on web or native mobile overlays during streaming. 

**Primary Value Proposition:** Turn live moments into reactive visuals without breaking the creator's flow—on mobile or desktop—with sub-500ms suggestion latency and mobile feature parity.

**Target Market:** TikTok Live creators (mobile-first), Twitch streamers (desktop), and live podcasters seeking automated, brand-consistent visual engagement tools.

**Key Differentiator:** Google-only AI stack for speed/cost optimization, agentic orchestration, deterministic effect rendering, and enterprise-grade privacy controls with prominent panic functionality.

---

## Problem Statement

**Current Pain Points:**
- Livestream creators struggle to maintain engagement during dead air or conversational lulls
- Manual effect triggering breaks creator flow and requires constant attention
- Mobile creators have limited access to professional overlay tools compared to desktop streamers
- Existing solutions lack real-time conversation awareness and brand consistency
- Complex technical setup prevents casual creators from accessing professional-quality effects

**Market Impact:**
- 70%+ of live content creation now happens on mobile platforms
- Creators report 15-30% higher tip/donation rates during visually engaging streams
- Current solutions require desktop setups, excluding the fastest-growing mobile creator segment

**Why Now:**
- Real-time AI processing costs have dropped 80% in the past year
- Mobile hardware (A15+/Snapdragon 8 Gen1+) can now handle real-time effects rendering
- Platform APIs increasingly support custom overlays and streaming integrations

---

## Proposed Solution

**Core Concept:**
A conversation-aware AI system that automatically suggests contextually relevant visual effects based on real-time speech analysis, optimized for mobile-first creators with desktop feature parity.

**Solution Architecture:**
- **Listening Layer:** Google Speech-to-Text v2 with speaker diarization and music filtering
- **Intelligence Layer:** Gemini 2.5 Flash for intent classification with agentic orchestration (LangGraph + PydanticAI)
- **Rendering Layer:** WebGL overlays (web) and native Metal/OpenGL overlays (mobile)
- **Control Layer:** PWA-based control panel with mobile-optimized UI

**Key Differentiators:**
- Sub-500ms suggestion latency from speech to UI
- Mobile feature parity with native RTMP streaming integration
- Brand Kit system ensuring visual consistency
- Panic controls for emergency effect stopping
- ROI analytics correlating effects to income generation

---

## Target Users

### Primary User Segment: Mobile TikTok Live Creators
- **Profile:** 16-30 years old, streams from smartphone, 100-50K followers
- **Current Behavior:** Uses basic platform effects, struggles with one-handed operation during streams
- **Pain Points:** Limited effect options, no conversation awareness, difficult multi-tasking
- **Goals:** Increase engagement, maintain brand consistency, operate one-handed while streaming

### Secondary User Segment: Desktop Streamers (Twitch/YouTube)
- **Profile:** 20-35 years old, established streaming setup with OBS/studio software
- **Current Behavior:** Manually triggers effects, uses multiple overlays, focuses on production quality
- **Pain Points:** Reaction time delays, breaking immersion to trigger effects manually
- **Goals:** Automated responses to exciting moments, seamless integration with existing tools

---

## Goals & Success Metrics

### Business Objectives
- **Activation Rate:** ≥60% D0 activation (enable listening + ≥1 effect trigger)
- **Revenue Impact:** Track Δ tips/donations per hour and conversion rate vs baseline
- **Market Penetration:** 10K+ active creators within 6 months of GA launch
- **Platform Coverage:** Support TikTok Live, Twitch, and YouTube Live integrations

### User Success Metrics
- **Zero-Config Success:** ≥70% creators trigger effects with no settings changed (mobile)
- **Suggestion Engagement:** ≥35% median CTR on suggested effects
- **Session Duration:** 20%+ increase in average stream length with effects enabled
- **Creator Retention:** 60%+ monthly active usage after initial activation

### Key Performance Indicators (KPIs)
- **Technical Performance:** p95 suggestion latency ≤500ms, 99.5%+ uptime
- **Rendering Performance:** 60fps target/30fps floor, ≤1% dropped frames p95
- **Mobile Performance:** First frame ≤120ms, thermal throttling events <5% sessions
- **Cost Efficiency:** ≤$0.06 per active hour (AI costs)

---

## MVP Scope

### Core Features (Must Have)
- **Real-Time Speech Processing:** STT v2 streaming with VAD, speaker diarization, music/speech separation
- **AI Intent Classification:** Gemini 2.5 Flash labeling for celebration, wins, losses, gratitude, hype events
- **Smart Suggestion Engine:** Deterministic ranker with brand scoring, speaker routing, cooldowns
- **Brand Consistency System:** Brand Kit controls (palette, fonts, categories, motion intensity)
- **Emergency Controls:** Prominent Panic button (UI, hotkey, optional voice command)
- **Cross-Platform Rendering:** WebGL overlay for web, Metal/OpenGL native overlays for mobile
- **Streaming Integration:** OBS/TikTok Live Studio presets, in-app RTMP for mobile where supported
- **Control Interface:** Mobile-first PWA with live queue, manual library, settings management
- **ROI Analytics:** Effect-to-income correlation tracking with dashboard visualization

### Out of Scope for MVP
- Public template marketplace
- Third-party social media feed integration
- Text-to-image generation (reserved for Phase 2)
- Voice commands (Phase 2 feature)
- Advanced encoder profiles beyond baseline requirements

### MVP Success Criteria
- Zero-configuration success rate ≥70% on mobile
- Technical performance meets all SLO targets (latency, uptime, rendering)
- Successful integration with all three target platforms (TikTok, Twitch, YouTube)
- Demonstrated ROI correlation with R² ≥0.6 on real creator data

---

## Post-MVP Vision

### Phase 2 Features (3-6 months post-MVP)
- **AI-Generated Sprites:** Gemini 2.5 Flash Image for custom effect elements with SynthID
- **Voice Commands:** "Panic," "Fireworks," and custom effect triggers
- **Advanced Encoding:** 60fps profiles, HEVC/AV1 support where platform-supported
- **Enhanced Personalization:** Machine learning for creator-specific effect preferences

### Long-term Vision (1-2 years)
- **Multimodal AI:** Computer vision integration for gesture and facial expression triggers
- **Creator Economy Tools:** Direct monetization features, tip-to-effect automation
- **Platform Expansion:** Instagram Live, Discord Stage, emerging platforms
- **Enterprise Features:** Multi-creator management, advanced analytics, custom branding

### Expansion Opportunities
- **B2B SaaS:** White-label solutions for streaming platforms
- **Education Vertical:** Interactive classroom engagement tools
- **Gaming Integration:** Real-time effect responses to game events
- **Content Creation Tools:** Recording mode for social media content creation

---

## Technical Considerations

### Platform Requirements
- **Target Platforms:** iOS (A15+), Android (Snapdragon 8 Gen1+/equivalent), Web (Chrome/Safari)
- **Browser/OS Support:** Chrome 90+, Safari 17+, Edge 90+; iOS 16+, Android API 31+
- **Performance Requirements:** 60fps target rendering, sub-100ms activation latency, 99.5% uptime

### Technology Preferences
- **Frontend:** Next.js 15 + React + TypeScript + shadcn/ui (PWA architecture)
- **Backend:** Node.js/Fastify WebSocket hub, LangGraph + PydanticAI agents
- **Database:** Convex for real-time data and live queries
- **Infrastructure:** Multi-region deployment with auto-scaling WebSocket connections

### Architecture Considerations
- **Repository Structure:** pnpm monorepo with apps/ and services/ separation
- **Service Architecture:** Microservices with agentic orchestration, event-driven communication
- **Integration Requirements:** Google Cloud STT v2, Gemini API, platform streaming APIs
- **Security/Compliance:** JWT tokens, CSP/SRI headers, Doppler secret management, privacy-first design

---

## Constraints & Assumptions

### Constraints
- **Budget:** Optimize for ≤$0.06 per active creator hour (AI costs)
- **Timeline:** 6 weeks to GA with mobile parity, 10 weeks to Phase 2
- **Resources:** Mobile-first development team, AI/ML integration capabilities required
- **Technical:** Google-only AI stack (vendor lock-in accepted for speed/cost benefits)

### Key Assumptions
- Mobile creators will adopt overlay-based streaming as platforms expand API access
- Real-time AI processing costs continue trending downward
- Target mobile hardware (A15+/SD8G1+) represents sufficient market coverage
- Creators value automated engagement over manual control for routine interactions
- Privacy-conscious design with ephemeral processing will meet creator comfort levels
- Platform streaming APIs remain stable and accessible for overlay integration

---

## Risks & Open Questions

### Key Risks
- **Platform Access Risk:** Limited stream key availability may restrict mobile RTMP functionality
- **Device Performance Risk:** Android fragmentation may impact rendering consistency across devices
- **Thermal Management Risk:** Continuous camera + GPU usage may cause throttling on mobile devices
- **Market Timing Risk:** Competing solutions may emerge with similar AI-driven approaches

### Open Questions
- What percentage of TikTok creators have access to stream keys for custom ingest?
- How will thermal throttling policies vary across Android manufacturers?
- What are the licensing implications for music-filtered speech processing?
- Should we prioritize iOS or Android for initial mobile launch if resource constraints arise?

### Areas Needing Further Research
- Creator willingness to pay for AI-powered effects vs free platform alternatives
- Optimal suggestion frequency to maximize engagement without overwhelming creators
- Integration complexity with emerging platform APIs and policy changes
- Competitive landscape evolution in real-time creator tools space

---

## Next Steps

### Immediate Actions
1. **Technical Architecture Review:** Validate technical feasibility of sub-500ms latency targets across mobile/web
2. **Platform API Research:** Confirm streaming integration capabilities for TikTok Live, Twitch, YouTube
3. **Creator User Research:** Validate assumptions through interviews with target creator segments
4. **Competitive Analysis:** Deep dive into existing solutions and differentiation opportunities
5. **Resource Planning:** Finalize development team structure for mobile-first, AI-integrated product
6. **Prototype Development:** Build proof-of-concept for speech→suggestion→render pipeline

### PM Handoff

This Project Brief provides comprehensive context for **VibeLayerAI** as a conversation-aware, mobile-first live effects platform. The next phase requires detailed PRD development focusing on:

- Technical architecture specifications for real-time AI processing
- Mobile app development requirements for iOS and Android
- WebSocket infrastructure for low-latency effect synchronization
- Integration specifications for major streaming platforms
- AI model fine-tuning requirements for creator-specific intents

Please review this brief thoroughly and proceed with PRD generation, working section by section to validate technical feasibility, refine user stories, and establish detailed acceptance criteria for the development team.

---

*This brief distills a comprehensive PRD into strategic foundation elements. Full technical specifications, API contracts, and implementation details are documented in the accompanying PRD v2.1.*