# VibeLayer Development Commands

## Essential Commands

### Development
```bash
pnpm dev                    # Start all development servers
pnpm build                  # Build all packages and apps
pnpm clean                  # Clean all build artifacts
```

### Quality Assurance
```bash
pnpm lint                   # Lint all packages
pnpm type-check             # Type check all packages
pnpm test                   # Run tests across all packages
pnpm format                 # Format code with Prettier
pnpm format:check           # Check formatting without changes
```

### Package Management
```bash
pnpm install                # Install all dependencies
pnpm changeset              # Create changeset for releases
pnpm version-packages       # Version packages with changesets
pnpm release                # Build and publish packages
```

### Individual Package Commands
```bash
# Control Panel (Next.js)
cd apps/control-panel
pnpm dev                    # Start development server
pnpm build                  # Build for production
pnpm start                  # Start production server
pnpm lint                   # Lint Next.js app
pnpm type-check             # Type check app

# Shared Package
cd packages/shared
pnpm build                  # Build package
pnpm dev                    # Watch mode build
pnpm test                   # Run tests
pnpm clean                  # Clean dist folder
```

### System Commands (Linux)
```bash
ls -la                      # List files with details
cd <directory>              # Change directory
grep -r "pattern" .         # Search for patterns
find . -name "*.ts"         # Find TypeScript files
git status                  # Check git status
git add .                   # Stage all changes
git commit -m "message"     # Commit changes
```

## Development URLs
- Control Panel: `http://localhost:3000`
- API endpoints: `/api/*` routes in Next.js app

## Build Pipeline
The project uses Turbo for orchestrated builds:
1. Packages build first (dependency order)
2. Applications build after their dependencies
3. Incremental builds for changed files only