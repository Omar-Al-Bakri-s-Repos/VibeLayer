# 12. Unified Project Structure

```
vibelayer-ai/
├── .github/                    # CI/CD workflows and templates
│   └── workflows/
│       ├── ci.yaml            # Test and build validation
│       ├── deploy-web.yaml    # Web app deployment
│       ├── deploy-api.yaml    # API services deployment
│       └── mobile-builds.yaml # Mobile app builds
├── apps/                       # Application packages
│   ├── control-panel/         # Web PWA (Next.js)
│   │   ├── src/
│   │   │   ├── components/    # React components (Atomic Design)
│   │   │   ├── app/          # Next.js 15 App Router
│   │   │   ├── hooks/        # Custom React hooks
│   │   │   ├── services/     # API client services
│   │   │   ├── stores/       # Zustand state management
│   │   │   ├── styles/       # Tailwind + global styles
│   │   │   └── utils/        # Frontend utilities
│   │   ├── public/           # Static assets
│   │   ├── tests/            # Frontend tests (Vitest + Playwright)
│   │   ├── next.config.js    # Next.js configuration
│   │   └── package.json
│   ├── mobile-ios/           # Native iOS app (Swift + Metal)
│   │   ├── VibeLayerAI/
│   │   │   ├── Views/        # SwiftUI views
│   │   │   ├── Services/     # API and WebSocket services
│   │   │   ├── Models/       # Data models
│   │   │   ├── Rendering/    # Metal rendering engine
│   │   │   └── Utils/        # iOS utilities
│   │   ├── Tests/            # iOS unit tests
│   │   ├── UITests/          # iOS UI tests
│   │   └── VibeLayerAI.xcodeproj
│   ├── mobile-android/       # Native Android app (Kotlin + OpenGL)
│   │   ├── app/src/main/java/
│   │   │   ├── ui/           # Jetpack Compose UI
│   │   │   ├── services/     # API and WebSocket services
│   │   │   ├── models/       # Data models
│   │   │   ├── rendering/    # OpenGL rendering engine
│   │   │   └── utils/        # Android utilities
│   │   ├── app/src/test/     # Unit tests
│   │   ├── app/src/androidTest/ # Instrumented tests
│   │   └── build.gradle.kts
│   └── api-services/         # Backend microservices
│       ├── src/
│       │   ├── functions/    # Serverless functions (Vercel/Cloud)
│       │   │   ├── auth/     # Authentication endpoints
│       │   │   ├── effects/  # Effects management API
│       │   │   ├── sessions/ # Stream session API
│       │   │   └── websocket/# WebSocket handlers
│       │   ├── services/     # Business logic services
│       │   │   ├── ai/       # AI processing (Agent Orchestra)
│       │   │   ├── effects/  # Effects engine
│       │   │   ├── brand/    # Brand Kit service
│       │   │   └── analytics/# Analytics service
│       │   ├── models/       # Database models (Convex)
│       │   ├── middleware/   # Auth, CORS, validation
│       │   └── utils/        # Backend utilities
│       ├── tests/            # Backend tests (Vitest + Supertest)
│       └── package.json
├── packages/                   # Shared packages across apps
│   ├── shared-types/         # TypeScript interfaces and types
│   │   ├── src/
│   │   │   ├── api/          # API request/response types
│   │   │   ├── models/       # Domain model interfaces
│   │   │   ├── events/       # WebSocket message types
│   │   │   └── constants/    # Shared constants
│   │   └── package.json
│   ├── effects-engine/       # Cross-platform effects rendering
│   │   ├── src/
│   │   │   ├── core/         # Platform-agnostic logic
│   │   │   ├── web/          # WebGL implementation
│   │   │   ├── ios/          # Metal implementation interfaces
│   │   │   ├── android/      # OpenGL implementation interfaces
│   │   │   └── assets/       # Effect definitions and assets
│   │   └── package.json
│   ├── protocol/             # WebSocket protocol definitions
│   │   ├── src/
│   │   │   ├── messages/     # Message type definitions
│   │   │   ├── validation/   # Message validation schemas
│   │   │   └── handlers/     # Message routing logic
│   │   └── package.json
│   ├── brand-kit/            # Brand consistency system
│   │   ├── src/
│   │   │   ├── scoring/      # Brand compatibility algorithms
│   │   │   ├── validation/   # Brand rule validation
│   │   │   └── templates/    # Pre-built brand templates
│   │   └── package.json
│   ├── ui-components/        # Shared React components
│   │   ├── src/
│   │   │   ├── atoms/        # Basic components
│   │   │   ├── molecules/    # Composite components
│   │   │   └── themes/       # Design system tokens
│   │   └── package.json
│   └── config/               # Shared configuration packages
│       ├── eslint/          # ESLint configurations
│       ├── typescript/      # TypeScript configurations
│       ├── jest/            # Testing configurations
│       └── tailwind/        # Tailwind configurations
├── infrastructure/           # Infrastructure as Code (Pulumi)
│   ├── dev/                 # Development environment
│   ├── staging/             # Staging environment
│   ├── production/          # Production environment
│   └── shared/              # Shared infrastructure components
├── scripts/                  # Build, deployment, and utility scripts
│   ├── build.sh            # Cross-platform build script
│   ├── deploy.sh           # Deployment orchestration
│   ├── test.sh             # Comprehensive testing
│   └── setup-dev.sh        # Development environment setup
├── docs/                     # Project documentation
│   ├── prd.md               # Product Requirements Document
│   ├── architecture.md      # This document
│   ├── api/                # API documentation
│   ├── mobile/             # Mobile-specific documentation
│   └── deployment/         # Deployment guides
├── .env.example              # Environment variables template
├── package.json              # Root package.json with workspace config
├── pnpm-workspace.yaml      # pnpm workspace configuration
├── turbo.json               # Turbo build orchestration
├── tsconfig.json            # Root TypeScript configuration
└── README.md                # Project overview and setup
```

---
