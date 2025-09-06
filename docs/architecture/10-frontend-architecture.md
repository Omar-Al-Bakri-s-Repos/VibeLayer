# 10. Frontend Architecture

## Component Architecture

**Organization Pattern:** Atomic Design with domain-specific groupings

```
src/
├── components/
│   ├── atoms/           # Basic building blocks
│   │   ├── Button/
│   │   ├── Input/
│   │   └── Icon/
│   ├── molecules/       # Simple combinations
│   │   ├── EffectCard/
│   │   ├── SuggestionBadge/
│   │   └── BrandColorPicker/
│   ├── organisms/       # Complex UI sections  
│   │   ├── EffectLibrary/
│   │   ├── SuggestionQueue/
│   │   └── StreamControls/
│   └── templates/       # Page layouts
│       ├── DashboardLayout/
│       └── StreamingLayout/
├── hooks/               # Reusable React logic
│   ├── useWebSocket.ts
│   ├── useEffects.ts
│   └── useBrandKit.ts
└── services/           # API communication
    ├── api.ts
    ├── websocket.ts
    └── auth.ts
```

**Component Template:**
```typescript
// Standard component structure
interface ComponentProps {
  // Props definition with TypeScript
}

export const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Hooks for state and effects
  const [state, setState] = useState();
  const { data, loading } = useCustomHook();

  // Event handlers
  const handleAction = useCallback(() => {
    // Action logic
  }, [dependencies]);

  // Render with accessibility
  return (
    <div role="region" aria-label="Component description">
      {/* Component JSX */}
    </div>
  );
};
```

## State Management Architecture

**State Structure with Zustand:**
```typescript
interface AppState {
  // Authentication state
  auth: {
    user: Creator | null;
    isAuthenticated: boolean;
    login: (credentials: LoginCredentials) => Promise<void>;
    logout: () => void;
  };
  
  // Real-time suggestions
  suggestions: {
    current: RankedEffect[];
    confidence: number;
    isLoading: boolean;
    clearSuggestions: () => void;
  };
  
  // Effect library
  effects: {
    library: Effect[];
    favorites: string[];
    searchTerm: string;
    selectedCategory: EffectCategory | null;
    toggleFavorite: (effectId: string) => void;
    setSearchTerm: (term: string) => void;
  };
  
  // Brand kit
  brandKit: {
    current: BrandKit | null;
    isEditing: boolean;
    updateColors: (colors: ColorPalette) => void;
    updateSettings: (settings: Partial<BrandKit>) => void;
  };
  
  // Stream session
  session: {
    current: StreamSession | null;
    status: SessionStatus;
    metrics: SessionMetrics;
    startSession: (platform: Platform) => Promise<void>;
    endSession: () => Promise<void>;
  };
}
```

**State Management Patterns:**
- Zustand stores for each major domain (auth, suggestions, effects, etc.)
- Immer integration for immutable state updates  
- Subscription patterns for real-time WebSocket data
- Persistence layer for offline functionality
- Optimistic updates for better UX

## Routing Architecture

**Route Organization (Next.js App Router):**
```
app/
├── (dashboard)/         # Dashboard group
│   ├── layout.tsx      # Dashboard-specific layout
│   ├── page.tsx        # Dashboard home
│   ├── effects/        # Effect library
│   ├── brand-kit/      # Brand customization
│   └── analytics/      # Performance analytics
├── (streaming)/        # Streaming interface group
│   ├── layout.tsx      # Minimal streaming layout
│   ├── mobile/         # Mobile-optimized interface
│   └── desktop/        # Desktop streaming controls
├── auth/               # Authentication flows
│   ├── login/
│   ├── register/
│   └── callback/       # OAuth callbacks
├── api/                # API routes
│   ├── auth/
│   ├── effects/
│   └── websocket/
└── globals.css         # Global styles
```

**Protected Route Pattern:**
```typescript
// Middleware for route protection
export function withAuth<T extends object>(Component: React.ComponentType<T>) {
  return function AuthenticatedComponent(props: T) {
    const { isAuthenticated, user } = useAuthStore();
    const router = useRouter();

    useEffect(() => {
      if (!isAuthenticated) {
        router.push('/auth/login');
      }
    }, [isAuthenticated, router]);

    if (!isAuthenticated || !user) {
      return <LoadingSpinner />;
    }

    return <Component {...props} />;
  };
}
```

## Frontend Services Layer

**API Client Setup:**
```typescript
// API client with authentication and error handling
class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  setToken(token: string) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
      ...options.headers,
    };

    const response = await fetch(url, { ...options, headers });
    
    if (!response.ok) {
      throw new ApiError(response.status, await response.json());
    }

    return response.json();
  }

  // CRUD methods
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint);
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient(process.env.NEXT_PUBLIC_API_URL!);
```

**Service Example:**
```typescript
// Effects service with caching and optimistic updates
export class EffectsService {
  private static cache = new Map<string, Effect[]>();

  static async getEffects(category?: EffectCategory): Promise<Effect[]> {
    const cacheKey = category || 'all';
    
    // Return cached data if available
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!;
    }

    // Fetch from API
    const effects = await apiClient.get<Effect[]>(
      `/effects${category ? `?category=${category}` : ''}`
    );
    
    // Cache for future use
    this.cache.set(cacheKey, effects);
    
    return effects;
  }

  static async triggerEffect(effectId: string): Promise<void> {
    // Optimistic update
    useEffectsStore.getState().addActivation(effectId);
    
    try {
      await apiClient.post('/effects/trigger', { effectId });
    } catch (error) {
      // Revert optimistic update on failure
      useEffectsStore.getState().removeActivation(effectId);
      throw error;
    }
  }
}
```

---
