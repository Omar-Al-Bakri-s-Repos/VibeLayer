# VibeLayer Code Style & Conventions

## TypeScript Configuration
- **Target**: ES2022
- **Module**: ESNext with bundler resolution
- **Strict mode**: Enabled
- **JSX**: Preserve (for Next.js)
- **Incremental**: Enabled for faster builds

## Prettier Configuration
- **Semi-colons**: Always (`;`)
- **Quotes**: Single quotes (`'`)
- **Print Width**: 80 characters
- **Tab Width**: 2 spaces
- **Trailing Commas**: ES5 style
- **Tabs**: Use spaces, not tabs

## Code Organization
- **Path Aliases**: 
  - `@/*` for local src files
  - `@/lib/*` for package sources
  - `@vibelayer/*` for workspace packages

## Package Structure
- Each package exports through `src/index.ts`
- Multiple entry points via package.json exports
- CommonJS and ESM dual build with tsup
- TypeScript declarations included

## Component Patterns (React)
- Use React.forwardRef for components needing refs
- Variant-based styling with class-variance-authority
- Props extend HTML element props when appropriate
- Display names set for better debugging

## File Naming
- **Components**: PascalCase (`Button.tsx`, `LoginForm.tsx`)
- **Utilities**: camelCase (`utils.ts`, `auth-client.ts`)
- **Pages**: lowercase with hyphens (`page.tsx`)
- **Tests**: `.test.ts` or `.spec.ts` suffix

## Import Organization
1. React imports first
2. Third-party libraries
3. Internal workspace packages (`@vibelayer/*`)
4. Relative imports (`.` and `..`)

## Mobile Conventions
- **Android**: Kotlin with PascalCase classes
- **iOS**: Swift with PascalCase classes
- Cross-platform consistency in API design