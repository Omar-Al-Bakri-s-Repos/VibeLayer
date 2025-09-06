# VibeLayer Project Overview

## Purpose
VibeLayer is a real-time AI-powered visual effects and interaction system that enables dynamic, intelligent overlay generation and management. It combines AI agents with visual effects to create an interactive platform.

## Key Components
- **AI Agents**: Intelligent agents for real-time interactions and content generation
- **Visual Overlays**: Dynamic visual effects and overlay system with WebGL support
- **Control Panel**: Modern web interface for managing agents and overlays
- **Mobile Apps**: Native Android (Kotlin) and iOS (Swift) applications
- **Shared Utilities**: Common types, utilities, and configurations

## Architecture
- **Type**: Monorepo with pnpm workspaces
- **Build System**: Turbo for fast, incremental builds
- **Backend**: Convex for real-time data synchronization
- **Authentication**: Better Auth for user management

## Main Applications
1. **Control Panel** (`apps/control-panel/`) - Next.js 15 web application
2. **Mobile Android** (`apps/mobile-android/`) - Kotlin with Vulkan/OpenGL ES rendering
3. **Mobile iOS** (`apps/mobile-ios/`) - Swift with Metal rendering

## Core Packages
- `@vibelayer/shared` - Common utilities, types, and configurations
- `@vibelayer/agents` - AI agent functionality
- `@vibelayer/overlay` - Visual effects system
- `@vibelayer/effects-engine` - Core effects processing
- `@vibelayer/protocol` - Communication protocols
- `@vibelayer/config` - Configuration management
- `@vibelayer/brand-kit` - Brand assets and styling