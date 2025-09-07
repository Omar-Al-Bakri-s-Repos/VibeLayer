# VibeLayer Monorepo Dockerfile
# Optimized for Depot builds with multi-stage caching

FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Enable pnpm
RUN corepack enable
RUN corepack prepare pnpm@9.15.0 --activate

# Dependencies stage - cached unless package files change
FROM base AS deps
COPY pnpm-lock.yaml package.json pnpm-workspace.yaml ./
COPY apps/*/package.json ./apps/
COPY packages/*/package.json ./packages/

# Install dependencies with frozen lockfile for reproducibility
RUN pnpm install --frozen-lockfile

# Builder stage - builds all workspace packages
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps ./apps
COPY --from=deps /app/packages ./packages

# Copy source code
COPY . .

# Build all packages in the workspace
RUN pnpm build

# Production dependencies stage
FROM base AS prod-deps
COPY pnpm-lock.yaml package.json pnpm-workspace.yaml ./
COPY apps/*/package.json ./apps/
COPY packages/*/package.json ./packages/

# Install only production dependencies
RUN pnpm install --frozen-lockfile --prod

# Runner stage - final minimal image
FROM base AS runner
ENV NODE_ENV=production

# Copy production dependencies
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=prod-deps /app/apps ./apps
COPY --from=prod-deps /app/packages ./packages

# Copy built application
COPY --from=builder /app/apps/control-panel/.next ./apps/control-panel/.next
COPY --from=builder /app/apps/control-panel/public ./apps/control-panel/public
COPY --from=builder /app/packages/*/dist ./packages/

# Copy necessary config files
COPY package.json pnpm-workspace.yaml turbo.json ./

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

EXPOSE 3000

# Start the control panel by default
CMD ["pnpm", "--filter=control-panel", "start"]