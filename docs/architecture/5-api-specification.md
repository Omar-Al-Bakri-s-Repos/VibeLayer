# 5. API Specification

## WebSocket Real-Time API

The primary interface for real-time communication between clients and the AI processing pipeline:

```typescript
// WebSocket Message Protocol
interface WSMessage {
  type: 'suggestion' | 'activation' | 'status' | 'panic' | 'heartbeat';
  sessionId: string;
  timestamp: Date;
  payload: any;
}

// AI Suggestion Message
interface SuggestionMessage extends WSMessage {
  type: 'suggestion';
  payload: {
    effects: RankedEffect[];
    confidence: number;
    intentDetected: IntentType;
    speakerInfo: SpeakerInfo;
  };
}

// Effect Activation Message  
interface ActivationMessage extends WSMessage {
  type: 'activation';
  payload: {
    effectId: string;
    trigger: 'auto' | 'manual';
    renderParams: RenderParameters;
  };
}

// System Status Message
interface StatusMessage extends WSMessage {
  type: 'status';
  payload: {
    aiPipelineHealth: 'healthy' | 'degraded' | 'down';
    latency: LatencyMetrics;
    activeConnections: number;
  };
}
```

## REST API Endpoints

Standard REST endpoints for CRUD operations and configuration management:

```yaml
openapi: 3.0.0
info:
  title: VibeLayerAI REST API
  version: 1.0.0
  description: Configuration and management API for VibeLayerAI platform
servers:
  - url: https://api.vibelayer.ai/v1
    description: Production API

paths:
  /creators/profile:
    get:
      summary: Get creator profile
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Creator profile data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Creator'
    
  /brand-kits:
    post:
      summary: Create brand kit
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BrandKit'
      responses:
        '201':
          description: Brand kit created
  
  /effects:
    get:
      summary: List available effects
      parameters:
        - name: category
          in: query
          schema:
            type: string
        - name: brandCompatible
          in: query
          schema:
            type: boolean
      responses:
        '200':
          description: List of effects
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Effect'

  /sessions:
    post:
      summary: Start streaming session
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                platform:
                  type: string
                  enum: [tiktok, twitch, youtube]
                rtmpUrl:
                  type: string
      responses:
        '201':
          description: Session started
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StreamSession'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---
