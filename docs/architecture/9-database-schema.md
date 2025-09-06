# 9. Database Schema

Based on Convex real-time database with TypeScript schema definitions:

```typescript
// Convex Schema Definition
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  creators: defineTable({
    email: v.string(),
    displayName: v.string(),
    subscriptionTier: v.union(
      v.literal("free"),
      v.literal("creator"), 
      v.literal("professional"),
      v.literal("enterprise")
    ),
    settings: v.object({
      autoTriggerEnabled: v.boolean(),
      suggestionThreshold: v.number(),
      panicHotkeyEnabled: v.boolean(),
    }),
    platforms: v.array(v.object({
      platform: v.string(),
      connected: v.boolean(),
      apiKey: v.optional(v.string()),
    })),
  })
    .index("by_email", ["email"]),

  brandKits: defineTable({
    creatorId: v.id("creators"),
    name: v.string(),
    colorPalette: v.object({
      primary: v.string(),
      secondary: v.string(),
      accent: v.string(),
      background: v.string(),
    }),
    typography: v.object({
      fontFamily: v.string(),
      fontSize: v.union(v.literal("small"), v.literal("medium"), v.literal("large")),
      fontWeight: v.union(v.literal("light"), v.literal("normal"), v.literal("bold")),
    }),
    motionIntensity: v.union(
      v.literal(1), v.literal(2), v.literal(3), v.literal(4), v.literal(5)
    ),
    allowedCategories: v.array(v.string()),
  })
    .index("by_creator", ["creatorId"]),

  streamSessions: defineTable({
    creatorId: v.id("creators"),
    platform: v.union(
      v.literal("tiktok"),
      v.literal("twitch"),
      v.literal("youtube"),
      v.literal("other")
    ),
    status: v.union(
      v.literal("active"),
      v.literal("paused"),
      v.literal("ended")
    ),
    startTime: v.number(), // Unix timestamp
    endTime: v.optional(v.number()),
    metrics: v.object({
      effectsTriggered: v.number(),
      averageLatency: v.number(),
      totalViewers: v.optional(v.number()),
      revenueGenerated: v.optional(v.number()),
    }),
  })
    .index("by_creator", ["creatorId"])
    .index("by_status", ["status"]),

  effects: defineTable({
    name: v.string(),
    category: v.union(
      v.literal("celebration"),
      v.literal("hype"),
      v.literal("gratitude"),
      v.literal("romance"),
      v.literal("general")
    ),
    intentTriggers: v.array(v.string()),
    renderConfig: v.object({
      duration: v.number(),
      performanceCost: v.union(
        v.literal("low"),
        v.literal("medium"),
        v.literal("high")
      ),
    }),
    thumbnailUrl: v.string(),
    assetUrls: v.object({
      web: v.string(),
      ios: v.string(),
      android: v.string(),
    }),
  })
    .index("by_category", ["category"]),

  effectActivations: defineTable({
    sessionId: v.id("streamSessions"),
    effectId: v.id("effects"),
    trigger: v.union(v.literal("auto"), v.literal("manual")),
    timestamp: v.number(),
    intentDetected: v.optional(v.string()),
    confidence: v.optional(v.number()),
    renderLatency: v.number(),
  })
    .index("by_session", ["sessionId"])
    .index("by_timestamp", ["timestamp"]),
});
```

**Performance Optimizations:**
- Strategic indexing on frequently queried fields
- Real-time subscriptions for live data updates
- Automatic data synchronization across clients
- Built-in caching and edge distribution

---
