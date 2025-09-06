import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    email: v.string(),
    name: v.string(),
    avatarUrl: v.optional(v.string()),
    isAdmin: v.optional(v.boolean()),
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_email", ["email"]),

  agentSessions: defineTable({
    userId: v.id("users"),
    agentId: v.string(),
    status: v.union(v.literal("active"), v.literal("paused"), v.literal("completed")),
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_user", ["userId"]).index("by_status", ["status"]),

  agentMessages: defineTable({
    sessionId: v.id("agentSessions"),
    role: v.union(v.literal("user"), v.literal("assistant"), v.literal("system")),
    content: v.string(),
    metadata: v.optional(v.any()),
    timestamp: v.number(),
  }).index("by_session", ["sessionId"]).index("by_timestamp", ["timestamp"]),

  overlayLayers: defineTable({
    userId: v.id("users"),
    name: v.string(),
    zIndex: v.number(),
    visible: v.boolean(),
    effects: v.array(v.any()),
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_user", ["userId"]).index("by_zIndex", ["zIndex"]),

  overlayEffects: defineTable({
    layerId: v.id("overlayLayers"),
    type: v.union(v.literal("particle"), v.literal("filter"), v.literal("animation"), v.literal("transition")),
    parameters: v.any(),
    duration: v.optional(v.number()),
    enabled: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number(),
  }).index("by_layer", ["layerId"]).index("by_type", ["type"]),

  apiKeys: defineTable({
    userId: v.id("users"),
    service: v.string(), // "google-speech", "google-gemini", etc.
    keyHash: v.string(),
    isActive: v.boolean(),
    createdAt: v.number(),
    expiresAt: v.optional(v.number()),
  }).index("by_user", ["userId"]).index("by_service", ["service"]),
});
