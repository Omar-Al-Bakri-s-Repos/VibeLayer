// VibeLayer AI Agents - Python-based LangGraph + PydanticAI integration types
// This package provides TypeScript type definitions for Python agents

export interface PythonAgentConfig {
  model: string;
  temperature: number;
  maxTokens: number;
  systemPrompt?: string;
}

export interface PythonAgentMessage {
  id: string;
  content: string;
  timestamp: string;
  role: 'user' | 'assistant' | 'system';
  metadata?: Record<string, unknown>;
}

export interface PythonAgentSession {
  id: string;
  userId: string;
  agentId: string;
  messages: PythonAgentMessage[];
  createdAt: string;
  updatedAt: string;
  status: 'active' | 'paused' | 'completed';
}

// Google AI service types
export interface SpeechToTextConfig {
  language: string;
  encoding: 'LINEAR16' | 'FLAC' | 'MULAW' | 'AMR' | 'AMR_WB' | 'OGG_OPUS' | 'SPEEX_WITH_HEADER_BYTE';
  sampleRateHertz: number;
  enableAutomaticPunctuation: boolean;
}

export interface GeminiFlashConfig {
  model: 'gemini-2.5-flash';
  temperature: number;
  maxOutputTokens: number;
}

export interface GeminiImageConfig extends GeminiFlashConfig {
  imageFormat: 'JPEG' | 'PNG' | 'WEBP';
  maxImageSize: number;
}
