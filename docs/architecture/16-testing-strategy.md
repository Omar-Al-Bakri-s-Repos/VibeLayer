# 16. Testing Strategy

## Testing Pyramid

```
        E2E Tests (10%)
       /                \
    Integration Tests (20%)
   /                        \
Frontend Unit (35%)    Backend Unit (35%)
```

## Test Organization

**Frontend Tests:**
```
apps/control-panel/tests/
├── unit/                   # Component and hook tests
│   ├── components/
│   ├── hooks/
│   └── services/
├── integration/            # Feature integration tests
│   ├── auth-flow.test.ts
│   ├── effect-selection.test.ts
│   └── real-time-suggestions.test.ts
└── e2e/                   # End-to-end user journeys
    ├── streaming-workflow.spec.ts
    ├── brand-kit-creation.spec.ts
    └── mobile-responsive.spec.ts
```

**Backend Tests:**
```
apps/api-services/tests/
├── unit/                  # Service and utility tests
│   ├── services/
│   ├── models/
│   └── utils/
├── integration/           # API endpoint tests
│   ├── auth-api.test.ts
│   ├── effects-api.test.ts
│   └── websocket-api.test.ts
└── load/                  # Performance and load tests
    ├── websocket-load.test.ts
    └── ai-pipeline-load.test.ts
```

## Test Examples

**Frontend Component Test:**
```typescript
// tests/unit/components/SuggestionQueue.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { SuggestionQueue } from '@/components/organisms/SuggestionQueue';

describe('SuggestionQueue', () => {
  const mockSuggestions = [
    { id: '1', name: 'Celebration', confidence: 0.9 },
    { id: '2', name: 'Hype', confidence: 0.7 }
  ];

  it('renders suggestions with confidence indicators', () => {
    render(
      <SuggestionQueue 
        suggestions={mockSuggestions}
        onSelect={jest.fn()}
      />
    );

    expect(screen.getByText('Celebration')).toBeInTheDocument();
    expect(screen.getByText('90%')).toBeInTheDocument();
  });

  it('triggers selection callback on click', () => {
    const onSelect = jest.fn();
    render(
      <SuggestionQueue 
        suggestions={mockSuggestions}
        onSelect={onSelect}
      />
    );

    fireEvent.click(screen.getByText('Celebration'));
    expect(onSelect).toHaveBeenCalledWith('1');
  });
});
```

**Backend API Test:**
```typescript
// tests/integration/effects-api.test.ts
import request from 'supertest';
import { app } from '@/app';
import { createTestUser, generateAuthToken } from '@/tests/helpers';

describe('Effects API', () => {
  let authToken: string;

  beforeEach(async () => {
    const user = await createTestUser();
    authToken = generateAuthToken(user.id);
  });

  describe('GET /api/effects', () => {
    it('returns effects list for authenticated user', async () => {
      const response = await request(app)
        .get('/api/effects')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body).toHaveProperty('effects');
      expect(Array.isArray(response.body.effects)).toBe(true);
    });

    it('filters effects by category', async () => {
      const response = await request(app)
        .get('/api/effects?category=celebration')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      response.body.effects.forEach(effect => {
        expect(effect.category).toBe('celebration');
      });
    });
  });
});
```

**E2E Test:**
```typescript
// tests/e2e/streaming-workflow.spec.ts
import { test, expect } from '@playwright/test';

test('Complete streaming workflow', async ({ page }) => {
  // Login
  await page.goto('/auth/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-button"]');

  // Start stream session
  await page.click('[data-testid="start-stream"]');
  await page.selectOption('[data-testid="platform"]', 'tiktok');
  await page.click('[data-testid="confirm-start"]');

  // Verify streaming interface
  await expect(page.locator('[data-testid="suggestion-queue"]')).toBeVisible();
  await expect(page.locator('[data-testid="panic-button"]')).toBeVisible();

  // Simulate effect trigger
  await page.click('[data-testid="effect-suggestion"]:first-child');
  
  // Verify effect activation
  await expect(page.locator('[data-testid="active-effect"]')).toBeVisible();
  
  // End session
  await page.click('[data-testid="end-stream"]');
  await expect(page.locator('[data-testid="session-summary"]')).toBeVisible();
});
```

---
