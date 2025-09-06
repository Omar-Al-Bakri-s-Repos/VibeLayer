# 6. Components

## Agent Orchestra (Core AI Processing)
**Responsibility:** Coordinates the real-time AI pipeline from speech input to effect suggestions using LangGraph orchestration

**Key Interfaces:**
- WebSocket message ingestion from clients
- Google Cloud STT v2 streaming integration
- Gemini 2.5 Flash intent classification
- Effect ranking and suggestion generation
- Real-time metrics collection and telemetry

**Dependencies:** Google Cloud STT, Gemini API, Effect Library, Brand Kit Service
**Technology Stack:** Python + LangGraph + PydanticAI, deployed on Google Cloud Run with auto-scaling

## Effects Engine (Cross-Platform Rendering)
**Responsibility:** Renders visual effects across web (WebGL) and native mobile (Metal/OpenGL) platforms with deterministic output

**Key Interfaces:**
- Effect activation API with render parameters
- Cross-platform rendering abstraction layer
- Performance monitoring and thermal management
- Asset caching and optimization

**Dependencies:** Effect Library, File Storage, Performance Monitor
**Technology Stack:** TypeScript core with platform-specific rendering engines (WebGL/Metal/OpenGL)

## WebSocket Hub (Real-Time Communication)
**Responsibility:** Manages real-time bidirectional communication between clients and backend services with scaling

**Key Interfaces:**
- Client connection management and authentication
- Message routing and protocol handling
- Connection scaling across multiple regions
- Heartbeat and reconnection logic

**Dependencies:** Authentication Service, Session Management, Load Balancer
**Technology Stack:** Node.js + Fastify + WebSocket, deployed on Convex for scaling

## Brand Kit Service (Visual Consistency)
**Responsibility:** Enforces creator brand consistency across all effect activations and provides customization interface

**Key Interfaces:**
- Brand Kit CRUD operations
- Effect compatibility scoring
- Real-time brand validation
- Template management and inheritance

**Dependencies:** Creator Service, Effect Library, File Storage
**Technology Stack:** Node.js microservice with Convex for real-time updates

## Mobile Native Apps (iOS/Android)
**Responsibility:** Provides native mobile interface with one-handed operation, RTMP streaming, and platform-specific optimizations

**Key Interfaces:**
- Native UI with ambidextrous design
- RTMP streaming integration where supported
- Audio processing and WebSocket communication
- Thermal management and battery optimization

**Dependencies:** Agent Orchestra (via WebSocket), Effects Engine, Platform APIs
**Technology Stack:** Swift/SwiftUI (iOS) + Metal, Kotlin/Compose (Android) + OpenGL/Vulkan

## Web Control Panel (Desktop Interface)
**Responsibility:** Comprehensive web-based interface for desktop streamers with full feature parity and professional controls

**Key Interfaces:**
- Live suggestion queue and manual effect library
- Comprehensive settings and brand kit management
- Analytics dashboard and ROI tracking
- OBS/streaming software integration

**Dependencies:** All backend services via REST + WebSocket
**Technology Stack:** Next.js 15 + React + TypeScript + shadcn/ui, deployed on Vercel

---
