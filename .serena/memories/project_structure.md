# VibeLayer Project Structure

## Root Directory
```
VibeLayer/
├── apps/                   # Applications
├── packages/               # Shared packages
├── convex/                 # Convex backend functions
├── docs/                   # Documentation
├── scripts/                # Build and utility scripts
├── package.json            # Root package configuration
├── pnpm-workspace.yaml     # Workspace configuration
├── turbo.json              # Build pipeline configuration
└── tsconfig.json           # TypeScript configuration
```

## Applications (`apps/`)
```
apps/
├── control-panel/          # Next.js web application
│   ├── src/
│   │   ├── app/           # Next.js 13+ app router
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities and configurations
│   ├── tests/             # Test files
│   └── package.json       # App dependencies
├── mobile-android/         # Android Kotlin application
│   ├── src/main/java/     # Kotlin source code
│   │   └── com/vibelayer/mobile/
│   │       ├── core/      # Core functionality
│   │       └── overlay/   # Overlay management
│   └── build.gradle.kts   # Android build configuration
└── mobile-ios/            # iOS Swift application
    ├── Sources/           # Swift source code
    │   └── VibeLayerMobile/
    │       ├── Core/      # Core functionality
    │       └── Overlay/   # Overlay management
    └── Package.swift      # Swift package configuration
```

## Packages (`packages/`)
```
packages/
├── shared/                # Common utilities and types
│   └── src/
│       ├── types/         # TypeScript type definitions
│       └── utils/         # Utility functions
├── agents/                # AI agent functionality
├── overlay/               # Visual effects and overlay system
├── effects-engine/        # Core effects processing engine
├── protocol/              # Communication protocols
├── config/                # Configuration management
└── brand-kit/             # Brand assets and styling guidelines
```

## Control Panel Structure
```
apps/control-panel/src/
├── app/                   # Next.js app router
│   ├── api/              # API routes
│   ├── auth/             # Authentication pages
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Home page
│   └── globals.css       # Global styles
├── components/           # React components
│   ├── ui/              # Reusable UI components
│   ├── auth/            # Authentication components
│   └── microphone/      # Microphone-related components
└── lib/                 # Utilities
    ├── auth.ts          # Authentication logic
    ├── auth-client.ts   # Client-side auth
    └── utils.ts         # General utilities
```

## Key Configuration Files
- `turbo.json` - Build pipeline and caching
- `tsconfig.json` - TypeScript compiler options
- `pnpm-workspace.yaml` - Workspace package definitions
- `convex.json` - Convex backend configuration
- `.prettierrc` - Code formatting rules