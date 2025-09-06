/**
 * VibeLayer Config
 * Shared configuration and environment management
 */

import { z } from 'zod';

// Environment schema
export const EnvironmentSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(Number).default(3000),
  
  // Database
  CONVEX_DEPLOYMENT: z.string().optional(),
  CONVEX_URL: z.string().url().optional(),
  
  // Authentication
  BETTER_AUTH_SECRET: z.string().min(32).optional(),
  BETTER_AUTH_URL: z.string().url().optional(),
  
  // External Services
  OPENAI_API_KEY: z.string().optional(),
  GOOGLE_AI_API_KEY: z.string().optional(),
  
  // Security
  DOPPLER_TOKEN: z.string().optional(),
  RATE_LIMIT_MAX: z.string().transform(Number).default(100),
  
  // WebSocket
  WS_PORT: z.string().transform(Number).default(3001),
  WS_HOST: z.string().default('localhost'),
});

export type Environment = z.infer<typeof EnvironmentSchema>;

// App configuration schema
export const AppConfigSchema = z.object({
  app: z.object({
    name: z.string().default('VibeLayer'),
    version: z.string().default('1.0.0'),
    description: z.string().default('AI-powered visual effects platform'),
  }),
  
  api: z.object({
    baseUrl: z.string().url(),
    timeout: z.number().default(30000),
    retries: z.number().default(3),
  }),
  
  websocket: z.object({
    host: z.string(),
    port: z.number(),
    reconnectInterval: z.number().default(5000),
    maxReconnectAttempts: z.number().default(10),
  }),
  
  effects: z.object({
    maxIntensity: z.number().default(1.0),
    defaultDuration: z.number().default(3000),
    renderFps: z.number().default(60),
  }),
  
  brand: z.object({
    scoreThreshold: z.number().default(0.7),
    strictMode: z.boolean().default(false),
  }),
  
  security: z.object({
    rateLimit: z.object({
      windowMs: z.number().default(60000), // 1 minute
      maxRequests: z.number().default(100),
    }),
    csp: z.object({
      enabled: z.boolean().default(true),
      reportOnly: z.boolean().default(false),
    }),
    cors: z.object({
      origins: z.array(z.string()).default(['http://localhost:3000']),
      credentials: z.boolean().default(true),
    }),
  }),
});

export type AppConfig = z.infer<typeof AppConfigSchema>;

// Configuration manager
export class ConfigManager {
  private static instance: ConfigManager;
  private env: Environment;
  private config: AppConfig;

  private constructor() {
    this.env = this.loadEnvironment();
    this.config = this.loadAppConfig();
  }

  public static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }

  private loadEnvironment(): Environment {
    return EnvironmentSchema.parse(process.env);
  }

  private loadAppConfig(): AppConfig {
    const baseUrl = this.env.NODE_ENV === 'production' 
      ? 'https://api.vibelayer.com' 
      : `http://localhost:${this.env.PORT}`;

    return AppConfigSchema.parse({
      app: {
        name: 'VibeLayer',
        version: '1.0.0',
        description: 'AI-powered visual effects platform',
      },
      api: {
        baseUrl: `${baseUrl}/api`,
        timeout: 30000,
        retries: 3,
      },
      websocket: {
        host: this.env.WS_HOST,
        port: this.env.WS_PORT,
        reconnectInterval: 5000,
        maxReconnectAttempts: 10,
      },
      effects: {
        maxIntensity: 1.0,
        defaultDuration: 3000,
        renderFps: 60,
      },
      brand: {
        scoreThreshold: 0.7,
        strictMode: this.env.NODE_ENV === 'production',
      },
      security: {
        rateLimit: {
          windowMs: 60000,
          maxRequests: this.env.RATE_LIMIT_MAX,
        },
        csp: {
          enabled: true,
          reportOnly: this.env.NODE_ENV === 'development',
        },
        cors: {
          origins: this.env.NODE_ENV === 'production' 
            ? ['https://vibelayer.com', 'https://app.vibelayer.com']
            : ['http://localhost:3000', 'http://localhost:3001'],
          credentials: true,
        },
      },
    });
  }

  public getEnvironment(): Environment {
    return this.env;
  }

  public getConfig(): AppConfig {
    return this.config;
  }

  public get(key: keyof AppConfig): AppConfig[keyof AppConfig] {
    return this.config[key];
  }

  public getEnv(key: keyof Environment): Environment[keyof Environment] {
    return this.env[key];
  }

  public isDevelopment(): boolean {
    return this.env.NODE_ENV === 'development';
  }

  public isProduction(): boolean {
    return this.env.NODE_ENV === 'production';
  }

  public isTest(): boolean {
    return this.env.NODE_ENV === 'test';
  }
}

// Export singleton instance
export const config = ConfigManager.getInstance();

// Export helper functions
export const getConfig = () => config.getConfig();
export const getEnvironment = () => config.getEnvironment();
export const isDev = () => config.isDevelopment();
export const isProd = () => config.isProduction();
export const isTest = () => config.isTest();

// Default configurations
export const defaultAppConfig: AppConfig = {
  app: {
    name: 'VibeLayer',
    version: '1.0.0',
    description: 'AI-powered visual effects platform',
  },
  api: {
    baseUrl: 'http://localhost:3000/api',
    timeout: 30000,
    retries: 3,
  },
  websocket: {
    host: 'localhost',
    port: 3001,
    reconnectInterval: 5000,
    maxReconnectAttempts: 10,
  },
  effects: {
    maxIntensity: 1.0,
    defaultDuration: 3000,
    renderFps: 60,
  },
  brand: {
    scoreThreshold: 0.7,
    strictMode: false,
  },
  security: {
    rateLimit: {
      windowMs: 60000,
      maxRequests: 100,
    },
    csp: {
      enabled: true,
      reportOnly: false,
    },
    cors: {
      origins: ['http://localhost:3000'],
      credentials: true,
    },
  },
};