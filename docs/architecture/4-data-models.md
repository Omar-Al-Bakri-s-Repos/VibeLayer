# 4. Data Models

## Core Business Entities

The following data models represent the key business entities shared between frontend and backend systems:

## Creator

**Purpose:** Represents a livestream creator using the VibeLayerAI platform

**Key Attributes:**
- id: string - Unique creator identifier
- email: string - Contact and authentication
- displayName: string - Public creator name
- brandKit: BrandKit - Visual identity configuration
- subscriptionTier: SubscriptionTier - Feature access level
- platforms: PlatformConnection[] - Connected streaming platforms
- settings: CreatorSettings - Personal preferences

```typescript
interface Creator {
  id: string;
  email: string;
  displayName: string;
  brandKit: BrandKit;
  subscriptionTier: 'free' | 'creator' | 'professional' | 'enterprise';
  platforms: PlatformConnection[];
  settings: CreatorSettings;
  createdAt: Date;
  updatedAt: Date;
}
```

**Relationships:**
- One-to-One with BrandKit
- One-to-Many with StreamSession
- One-to-Many with Effect activations

## StreamSession

**Purpose:** Represents an active or completed livestream session with VibeLayerAI

**Key Attributes:**
- id: string - Unique session identifier
- creatorId: string - Session owner
- platform: Platform - Streaming platform used
- status: SessionStatus - Current session state
- effectsTriggered: EffectActivation[] - Effects used during session
- metrics: SessionMetrics - Performance and engagement data

```typescript
interface StreamSession {
  id: string;
  creatorId: string;
  platform: 'tiktok' | 'twitch' | 'youtube' | 'other';
  status: 'active' | 'paused' | 'ended';
  startTime: Date;
  endTime?: Date;
  effectsTriggered: EffectActivation[];
  metrics: SessionMetrics;
  aiProcessingStats: AIProcessingStats;
}
```

**Relationships:**
- Many-to-One with Creator
- One-to-Many with EffectActivation
- One-to-One with SessionMetrics

## Effect

**Purpose:** Represents a visual effect that can be triggered during streams

**Key Attributes:**
- id: string - Unique effect identifier
- name: string - Human-readable effect name
- category: EffectCategory - Grouping for organization
- intentTriggers: IntentType[] - AI intents that can trigger this effect
- renderConfig: RenderConfig - Platform-specific rendering parameters
- brandCompatibility: BrandScoring - Brand Kit compatibility rules

```typescript
interface Effect {
  id: string;
  name: string;
  category: 'celebration' | 'hype' | 'gratitude' | 'romance' | 'general';
  intentTriggers: IntentType[];
  renderConfig: {
    web: WebGLConfig;
    ios: MetalConfig;
    android: OpenGLConfig;
  };
  brandCompatibility: BrandScoring;
  thumbnailUrl: string;
  duration: number; // milliseconds
  performanceCost: 'low' | 'medium' | 'high';
}
```

**Relationships:**
- Many-to-Many with IntentType
- One-to-Many with EffectActivation

## BrandKit

**Purpose:** Creator's visual identity and brand consistency configuration

**Key Attributes:**
- id: string - Unique brand kit identifier
- creatorId: string - Owner reference
- colorPalette: ColorPalette - Primary and accent colors
- typography: TypographySettings - Font choices and sizing
- motionIntensity: MotionLevel - Animation intensity preference
- allowedCategories: EffectCategory[] - Permitted effect types

```typescript
interface BrandKit {
  id: string;
  creatorId: string;
  name: string;
  colorPalette: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
  };
  typography: {
    fontFamily: string;
    fontSize: 'small' | 'medium' | 'large';
    fontWeight: 'light' | 'normal' | 'bold';
  };
  motionIntensity: 1 | 2 | 3 | 4 | 5;
  allowedCategories: EffectCategory[];
  customEffectIds: string[];
}
```

**Relationships:**
- One-to-One with Creator
- Influences Effect compatibility scoring

---
