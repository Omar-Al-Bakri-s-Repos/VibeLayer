/**
 * VibeLayer Protocol
 * WebSocket message definitions and communication layer
 */

import { z } from 'zod';

// Base message schema
export const BaseMessageSchema = z.object({
  id: z.string(),
  timestamp: z.number(),
  type: z.string(),
});

// Effect trigger message
export const EffectTriggerSchema = BaseMessageSchema.extend({
  type: z.literal('effect:trigger'),
  payload: z.object({
    effectId: z.string(),
    intensity: z.number().min(0).max(1),
    duration: z.number().optional(),
    parameters: z.record(z.unknown()).optional(),
  }),
});

// System status message
export const SystemStatusSchema = BaseMessageSchema.extend({
  type: z.literal('system:status'),
  payload: z.object({
    connected: z.boolean(),
    services: z.record(z.enum(['online', 'offline', 'error'])),
    performance: z.object({
      fps: z.number(),
      latency: z.number(),
      memoryUsage: z.number(),
    }),
  }),
});

// Creator connection message
export const CreatorConnectionSchema = BaseMessageSchema.extend({
  type: z.literal('creator:connect'),
  payload: z.object({
    creatorId: z.string(),
    displayName: z.string(),
    subscriptionTier: z.enum(['free', 'creator', 'professional', 'enterprise']),
  }),
});

// AI suggestion message
export const AISuggestionSchema = BaseMessageSchema.extend({
  type: z.literal('ai:suggestion'),
  payload: z.object({
    effectId: z.string(),
    confidence: z.number().min(0).max(1),
    context: z.string(),
    reasoning: z.string(),
  }),
});

// Union of all message types
export const MessageSchema = z.discriminatedUnion('type', [
  EffectTriggerSchema,
  SystemStatusSchema,
  CreatorConnectionSchema,
  AISuggestionSchema,
]);

// Type exports
export type BaseMessage = z.infer<typeof BaseMessageSchema>;
export type EffectTriggerMessage = z.infer<typeof EffectTriggerSchema>;
export type SystemStatusMessage = z.infer<typeof SystemStatusSchema>;
export type CreatorConnectionMessage = z.infer<typeof CreatorConnectionSchema>;
export type AISuggestionMessage = z.infer<typeof AISuggestionSchema>;
export type Message = z.infer<typeof MessageSchema>;

// Message factory functions
export const createEffectTrigger = (
  effectId: string,
  intensity: number,
  duration?: number,
  parameters?: Record<string, unknown>
): EffectTriggerMessage => ({
  id: crypto.randomUUID(),
  timestamp: Date.now(),
  type: 'effect:trigger',
  payload: {
    effectId,
    intensity,
    duration,
    parameters,
  },
});

export const createSystemStatus = (
  connected: boolean,
  services: Record<string, 'online' | 'offline' | 'error'>,
  performance: { fps: number; latency: number; memoryUsage: number }
): SystemStatusMessage => ({
  id: crypto.randomUUID(),
  timestamp: Date.now(),
  type: 'system:status',
  payload: {
    connected,
    services,
    performance,
  },
});

// Message validation
export const validateMessage = (data: unknown): Message => {
  return MessageSchema.parse(data);
};

export const isValidMessage = (data: unknown): data is Message => {
  return MessageSchema.safeParse(data).success;
};