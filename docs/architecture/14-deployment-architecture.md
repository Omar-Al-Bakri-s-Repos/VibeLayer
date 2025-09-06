# 14. Deployment Architecture

## Deployment Strategy

**Frontend Deployment:**
- **Platform:** Vercel with Edge Runtime
- **Build Command:** `turbo build --filter=control-panel`
- **Output Directory:** `apps/control-panel/dist`
- **CDN/Edge:** Vercel Edge Network with global distribution

**Backend Deployment:**
- **Platform:** Google Cloud Run + Vercel Serverless Functions
- **Build Command:** `turbo build --filter=api-services`
- **Deployment Method:** Container-based with auto-scaling
- **AI Services:** Google Cloud Run for Agent Orchestra

**Mobile Deployment:**
- **iOS:** App Store Connect with TestFlight for beta
- **Android:** Google Play Console with Internal Testing

## CI/CD Pipeline

```yaml
# .github/workflows/ci.yaml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 9.15.0
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm type-check
      - run: pnpm test:unit
      - run: pnpm build
      
      # E2E tests with Playwright
      - run: pnpm test:e2e
        env:
          PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD: false

  deploy-preview:
    needs: test
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: vercel deploy --token=${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## Environments

| Environment | Frontend URL | Backend URL | Purpose |
|-------------|-------------|-------------|---------|
| Development | http://localhost:3000 | http://localhost:3001 | Local development |
| Staging | https://staging.vibelayer.ai | https://api-staging.vibelayer.ai | Pre-production testing |
| Production | https://app.vibelayer.ai | https://api.vibelayer.ai | Live environment |

---
