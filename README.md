# VibeLayer AI Platform

VibeLayer is a real-time AI-powered visual effects and interaction system that enables dynamic, intelligent overlay generation and management.

## 🚀 Features

- **AI Agents**: Intelligent agents for real-time interactions and content generation
- **Visual Overlays**: Dynamic visual effects and overlay system with WebGL support
- **Control Panel**: Modern web interface for managing agents and overlays
- **Shared Utilities**: Common types, utilities, and configurations

## 🏗️ Architecture

This is a monorepo built with:

- **Package Manager**: pnpm with workspaces
- **Build System**: Turbo for fast, incremental builds
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Development**: Hot reload and fast refresh across all packages

### Project Structure

```
VibeLayer/
├── apps/
│   └── control-panel/          # Next.js web application
├── packages/
│   ├── agents/                 # AI agent functionality
│   ├── overlay/                # Visual effects and overlays
│   └── shared/                 # Common utilities and types
├── package.json                # Root package configuration
├── pnpm-workspace.yaml         # Workspace configuration
├── turbo.json                  # Build pipeline configuration
└── tsconfig.json               # TypeScript configuration
```

## 🛠️ Development Setup

### Prerequisites

- Node.js >= 18.0.0
- pnpm >= 8.0.0

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd VibeLayer
```

2. Install dependencies:
```bash
pnpm install
```

3. Build all packages:
```bash
pnpm build
```

4. Start development servers:
```bash
pnpm dev
```

### Available Scripts

- `pnpm dev` - Start development servers for all apps
- `pnpm build` - Build all packages and apps
- `pnpm lint` - Lint all packages
- `pnpm type-check` - Type check all packages
- `pnpm test` - Run tests across all packages
- `pnpm clean` - Clean build artifacts
- `pnpm format` - Format code with Prettier

## 📦 Packages

### @vibelayer/shared

Common utilities, types, and configurations used across the platform.

### @vibelayer/agents

Core AI agent functionality including:
- Agent management and orchestration
- Session handling
- Message processing

### @vibelayer/overlay

Real-time visual effects system featuring:
- Layer-based rendering
- Multiple effect types (particles, filters, animations)
- WebGL acceleration support

### @vibelayer/control-panel

Next.js web application providing:
- Agent configuration interface
- Overlay editor
- Real-time monitoring dashboard

## 🚦 Getting Started

1. After installation, the control panel will be available at `http://localhost:3000`
2. Configure AI agents through the web interface
3. Create and customize visual overlays
4. Monitor system performance and interactions

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting: `pnpm lint && pnpm type-check`
4. Submit a pull request

## 📄 License

[License information to be added]
