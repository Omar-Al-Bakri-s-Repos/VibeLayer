# 13. Development Workflow

## Local Development Setup

**Prerequisites:**
```bash
# Required software versions
node --version    # v20.x LTS
pnpm --version    # v9.15.0+
turbo --version   # v2.3.0+

# Mobile development (optional for web-only dev)
xcode-select --version      # Xcode 15+
java --version             # JDK 17+
```

**Initial Setup:**
```bash
# Clone and setup repository
git clone https://github.com/your-org/vibelayer-ai.git
cd vibelayer-ai

# Install all dependencies
pnpm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Setup development database (Convex)
pnpm convex dev --configure
pnpm convex push

# Setup Google Cloud credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# Initial build to validate setup
pnpm build
```

**Development Commands:**
```bash
# Start all services in development mode
pnpm dev

# Start specific applications
pnpm dev --filter=control-panel    # Web app only
pnpm dev --filter=api-services     # Backend services only

# Start mobile development
cd apps/mobile-ios && open VibeLayerAI.xcodeproj
cd apps/mobile-android && ./gradlew assembleDebug

# Run tests
pnpm test                          # All tests
pnpm test:unit                     # Unit tests only
pnpm test:e2e                      # End-to-end tests
pnpm test:mobile                   # Mobile tests

# Code quality
pnpm lint                          # ESLint + Prettier
pnpm type-check                    # TypeScript validation
pnpm format                        # Auto-format code
```

## Environment Configuration

**Required Environment Variables:**

```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:3000/api
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:3001
NEXT_PUBLIC_CONVEX_URL=https://your-convex-dev.convex.cloud
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn

# Backend (.env)
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
GEMINI_API_KEY=your-gemini-api-key
DOPPLER_TOKEN=your-doppler-token
REDIS_URL=redis://localhost:6379

# Shared (.env)
DATABASE_URL=your-convex-connection-string
JWT_SECRET=your-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key
NODE_ENV=development
```

---
