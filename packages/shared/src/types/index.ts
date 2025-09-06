// Common type definitions for VibeLayer platform
import { z } from 'zod';

// Base configuration schema
export const ConfigSchema = z.object({
  apiUrl: z.string().url(),
  version: z.string(),
  environment: z.enum(['development', 'staging', 'production']),
});

export type Config = z.infer<typeof ConfigSchema>;

// AI Agent types
export interface AgentMessage {
  id: string;
  content: string;
  timestamp: Date;
  role: 'user' | 'assistant' | 'system';
}

export interface AgentSession {
  id: string;
  userId: string;
  messages: AgentMessage[];
  createdAt: Date;
  updatedAt: Date;
}

// Visual overlay types
export interface OverlayEffect {
  id: string;
  type: 'particle' | 'filter' | 'animation' | 'transition';
  parameters: Record<string, unknown>;
  duration?: number;
  enabled: boolean;
}

export interface OverlayLayer {
  id: string;
  name: string;
  effects: OverlayEffect[];
  zIndex: number;
  visible: boolean;
}
