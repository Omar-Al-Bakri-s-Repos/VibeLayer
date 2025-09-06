# 3. Tech Stack

The following represents the definitive technology selection for the entire VibeLayerAI project. All development must use these exact versions and technologies.

| Category | Technology | Version | Purpose | Rationale |
|----------|-----------|---------|---------|-----------|
| Frontend Language | TypeScript | 5.6.3 | Type-safe development across all platforms | Prevents runtime errors, enables better AI agent code generation |
| Frontend Framework | Next.js | 15.x | Web PWA with SSR/SSG capabilities | Best-in-class React framework with Vercel optimization |
| UI Component Library | shadcn/ui | Latest | Accessible, customizable component system | Reduces development time while maintaining brand flexibility |
| State Management | Zustand | 5.x | Lightweight state management | Simpler than Redux, perfect for real-time updates |
| Backend Language | Node.js | 20.x LTS | JavaScript ecosystem consistency | Enables code sharing and faster development |
| Backend Framework | Fastify | 5.x | High-performance WebSocket server | Superior performance for real-time communication |
| API Style | WebSocket + REST | - | Real-time + traditional API patterns | WebSocket for live updates, REST for CRUD operations |
| Database | Convex | Latest | Real-time database with live queries | Purpose-built for real-time applications |
| Cache | Redis | 7.x | High-performance caching | Essential for effect asset caching and session management |
| File Storage | Google Cloud Storage | - | Scalable file storage for effects | Integrates with Google AI stack |
| Authentication | BetterAuth | Latest | Modern auth with JWT + EdDSA | Security-first with replay prevention |
| Frontend Testing | Vitest | 2.x | Fast unit testing | Better performance than Jest |
| Backend Testing | Vitest + Supertest | 2.x | API testing framework | Consistent testing across frontend/backend |
| E2E Testing | Playwright | 1.x | Cross-platform testing | Best mobile and desktop testing support |
| Build Tool | Turbo | 2.x | Monorepo build orchestration | Optimal caching and parallel builds |
| Bundler | Next.js built-in | - | Webpack-based bundling | Integrated with Next.js optimizations |
| IaC Tool | Pulumi | 3.x | Infrastructure as Code | TypeScript-based infrastructure |
| CI/CD | GitHub Actions | - | Automated testing and deployment | Seamless integration with repository |
| Monitoring | Sentry | Latest | Error tracking and performance | Real-time error monitoring |
| Logging | Pino | 9.x | High-performance logging | Structured logging for debugging |
| CSS Framework | Tailwind CSS | 4.x | Utility-first styling | Rapid UI development with consistency |

---
