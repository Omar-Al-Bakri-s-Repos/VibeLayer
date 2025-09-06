// Overlay specific types for WebGL (Pixi/regl) + Lottie
import type { OverlayEffect, OverlayLayer } from '@vibelayer/shared';
import type { Application as PixiApplication, Container } from 'pixi.js';
import type { AnimationItem } from 'lottie-web';

export interface WebGLRenderer {
  pixi?: PixiApplication;
  regl?: any; // regl context
  canvas: HTMLCanvasElement;
  width: number;
  height: number;
}

export interface PixiEffect extends OverlayEffect {
  container: Container;
  update(deltaTime: number): void;
  destroy(): void;
}

export interface LottieEffect extends OverlayEffect {
  animation: AnimationItem;
  path: string;
  autoplay: boolean;
  loop: boolean;
}

export interface ReglShaderEffect extends OverlayEffect {
  vertexShader: string;
  fragmentShader: string;
  uniforms: Record<string, any>;
}

export interface EffectConfig {
  intensity: number;
  speed: number;
  color?: string;
  size?: number;
  duration?: number;
  easing?: string;
}

export interface AnimationFrame {
  timestamp: number;
  deltaTime: number;
}

// Re-export shared types
export { OverlayEffect, OverlayLayer };
