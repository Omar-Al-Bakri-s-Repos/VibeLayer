# 4. Technical Assumptions

## Repository Structure: Monorepo
**Decision**: pnpm workspace monorepo with apps/ and services/ separation plus comprehensive fallback architecture
**Rationale**: Enables shared packages (effects-engine, protocol, brand-kit, config) while maintaining clear separation between web, mobile, and backend services. Includes graceful degradation protocols for Google API failures and multi-vendor AI provider evaluation framework for Phase 2.

## Service Architecture
**CRITICAL DECISION**: Microservices with agentic orchestration plus resilience patterns
- **Control Panel**: Next.js 15 + React + TypeScript + shadcn/ui (PWA architecture) with offline-capable fallback modes
- **WebSocket Hub**: Node.js/Fastify with JWT authentication, room-based scaling, and multi-region deployment with intelligent creator-to-region routing
- **Agent Orchestra**: LangGraph + PydanticAI coordinating STT ↔ Gemini ↔ rendering pipeline with comprehensive telemetry and fallback protocols
- **Mobile Apps**: Native iOS (Swift/Metal) + Android (Kotlin/OpenGL/Vulkan) with device-specific thermal profiling and progressive web app fallback for restricted environments
- **Data Layer**: Convex for real-time queries with automated scaling triggers and performance monitoring

## Testing Requirements
**CRITICAL DECISION**: Comprehensive testing pyramid with performance focus plus automated regression prevention
- **Unit Testing**: Core agents, ranker logic, effect determinism validation, and thermal management algorithms
- **Integration Testing**: Cross-service communication, real-time data flow, and multi-vendor AI provider compatibility
- **Performance Testing**: Latency benchmarks across web/mobile with thermal simulation, device lab infrastructure, and automated performance regression detection in CI/CD
- **Security Testing**: Automated security scanning, penetration testing, and dependency vulnerability management
- **End-to-End Testing**: Creator workflows with automated suggestion validation and cross-platform visual consistency verification

## Additional Technical Assumptions and Security Hardening

**AI Architecture (Google-Exclusive with Fallback Planning)**:
- Google Cloud Speech-to-Text v2 with streaming, speaker diarization, and end-to-end audio encryption
- Gemini 2.5 Flash for intent classification with <300ms p50 latency target and caching strategies for cost optimization
- Multi-vendor AI provider evaluation framework for Phase 2 risk mitigation
- Cost target: ≤$0.06 per active creator hour through API optimization and intelligent batching

**Enhanced Security & Compliance**:
- BetterAuth with JWT/EdDSA tokens (180s expiration) and comprehensive replay prevention
- Doppler secret management with 90-day rotation cycles and automated compliance monitoring
- CSP headers with no unsafe-inline, SRI validation, mobile app code obfuscation, and certificate pinning
- End-to-end encryption for audio streams and comprehensive audit logging for compliance
- Privacy-first design with explicit data deletion workflows and GDPR compliance validation

**Performance Constraints with Thermal Management**:
- Mobile hardware: iOS A15+, Android Snapdragon 8 Gen1+ with device-specific thermal profiling
- Network optimization: STT uplink ≤100 kbit/s with cellular resilience, RTMP ≤3 Mbps at 1080p@30
- Rendering budgets: Web overlay ≤1.5MB gzipped, mobile textures ≤8MB, VRAM ≤256MB with dynamic adjustment
- Latency targets: p95 ≤500ms suggestion with comprehensive telemetry, first frame ≤120ms mobile with thermal adaptation

**Platform Integration with Resilience**:
- Native RTMP encoding for mobile where stream keys available, with progressive web app fallback for restricted environments
- OBS/TikTok Live Studio overlay integration with signed URLs and platform policy change monitoring
- Cross-platform effect determinism via identical seeds/parameters with automated visual consistency validation

**Maintenance & Sustainability Planning**:
- Dedicated maintenance engineering capacity (30% of team) for cross-platform updates and security patches
- Comprehensive documentation standards for custom protocols and performance optimizations
- Feature flag infrastructure for rapid problem isolation and resolution
- Long-term technical debt monitoring with automated refactoring recommendations

---
