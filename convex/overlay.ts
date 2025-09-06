import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const createLayer = mutation({
  args: {
    userId: v.id("users"),
    name: v.string(),
    zIndex: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    return await ctx.db.insert("overlayLayers", {
      userId: args.userId,
      name: args.name,
      zIndex: args.zIndex ?? 0,
      visible: true,
      effects: [],
      createdAt: now,
      updatedAt: now,
    });
  },
});

export const addEffect = mutation({
  args: {
    layerId: v.id("overlayLayers"),
    type: v.union(v.literal("particle"), v.literal("filter"), v.literal("animation"), v.literal("transition")),
    parameters: v.any(),
    duration: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    return await ctx.db.insert("overlayEffects", {
      ...args,
      enabled: true,
      createdAt: now,
      updatedAt: now,
    });
  },
});

export const getUserLayers = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("overlayLayers")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("asc")
      .collect();
  },
});

export const getLayerEffects = query({
  args: { layerId: v.id("overlayLayers") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("overlayEffects")
      .withIndex("by_layer", (q) => q.eq("layerId", args.layerId))
      .collect();
  },
});

export const updateLayerVisibility = mutation({
  args: {
    layerId: v.id("overlayLayers"),
    visible: v.boolean(),
  },
  handler: async (ctx, args) => {
    return await ctx.db.patch(args.layerId, {
      visible: args.visible,
      updatedAt: Date.now(),
    });
  },
});
