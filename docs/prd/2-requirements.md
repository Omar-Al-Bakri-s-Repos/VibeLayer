# 2. Requirements

## Functional Requirements

**FR1: Real-Time Speech Processing** - The system SHALL provide continuous speech-to-text processing using Google STT v2 with voice activity detection, speaker diarization, and music/speech separation to enable conversation-aware effect triggering.

**FR2: AI Intent Classification** - The system SHALL use Gemini 2.5 Flash to classify conversational intent from speech transcripts, identifying celebration, wins, losses, gratitude, hype, romance, and other trigger-worthy moments with confidence scoring.

**FR3: Smart Suggestion Engine** - The system SHALL present ranked effect suggestions within 500ms p95 latency, incorporating intent confidence, brand scoring, speaker routing, cooldowns, and diversity factors in the ranking algorithm.

**FR4: Brand Consistency System** - The system SHALL enforce Brand Kit controls including color palette, fonts, allowed categories, and motion intensity to ensure visual consistency across all effect activations.

**FR5: Emergency Controls** - The system SHALL provide prominent Panic functionality accessible via UI button, hotkey, and optional voice command that stops all active effects within 200ms and prevents new activations for 10 seconds.

**FR6: Cross-Platform Rendering** - The system SHALL render effects via WebGL overlays for web browsers and native Metal/OpenGL overlays for mobile platforms, maintaining visual consistency and 60fps target performance.

**FR7: Multi-Speaker Awareness** - The system SHALL distinguish between speakers using diarization and provide Host-only mode that prevents guest speakers from triggering auto-effects while maintaining suggestion visibility.

**FR8: Background Music Filtering** - The system SHALL filter background music from speech processing using music/speech classification, preventing lyric-based false triggers while maintaining speech recognition accuracy.

**FR9: Manual Effect Library** - The system SHALL provide searchable manual effect library with instant search (≤150ms), tag filtering, thumbnails, and one-tap activation with ≤100ms response time.

**FR10: ROI Analytics** - The system SHALL track effect activation correlation with creator income through platform connectors, manual logging, and CSV import, providing dashboard visualization of effect-to-income relationships.

## Non-Functional Requirements

**NFR1: Performance Latency** - Speech transcript to UI suggestion display SHALL achieve p50 ≤300ms and p95 ≤500ms across web and mobile platforms under normal network conditions.

**NFR2: Rendering Performance** - Effect rendering SHALL maintain 60fps target with 30fps minimum floor, keeping dropped frames ≤1% at p95 across target device matrix.

**NFR3: System Reliability** - Platform uptime SHALL exceed 99.5% for overlay, WebSocket hub, and companion app aggregate availability with automated failover capabilities.

**NFR4: Mobile Optimization** - First frame rendering SHALL occur within 120ms on mobile devices, with thermal throttling events occurring in <5% of sessions on target hardware.

**NFR5: Cost Efficiency** - AI processing costs SHALL remain ≤$0.06 per active creator hour through optimized API usage, caching strategies, and intelligent batching.

**NFR6: Security Compliance** - All data transmission SHALL use JWT tokens with replay prevention, CSP headers, SRI validation, and secret management via Doppler with 90-day rotation cycles.

**NFR7: Scalability** - System SHALL support 500 concurrent overlays and 1,000 concurrent mobile listeners per region with auto-scaling WebSocket connections.

**NFR8: Cross-Platform Consistency** - Effect rendering with identical seeds and parameters SHALL produce bit-identical output for 30 seconds on the same device type and engine version.

---
