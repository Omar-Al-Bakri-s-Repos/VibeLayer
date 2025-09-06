# 7.1. AI Layer Architecture (Agent Orchestra)

The AI Layer represents the core intelligence system that transforms real-time audio into conversation-aware effect suggestions. This layer employs a sophisticated multi-agent architecture using LangGraph for orchestration and PydanticAI for agent definitions.

## AI Agent Architecture

**Agent Orchestra Pattern:**
The system uses a hierarchical agent architecture where specialized agents handle specific aspects of the AI pipeline, coordinated by a central orchestrator.

```typescript
// AI Agent State Management
interface AgentOrchestrationState {
  // Session Management
  session: {
    id: string;
    creatorId: string;
    platform: string;
    status: 'initializing' | 'active' | 'paused' | 'ended';
    startTime: Date;
    metadata: SessionMetadata;
  };

  // Audio Processing State
  audioProcessing: {
    isActive: boolean;
    inputLevel: number;
    speakerInfo: SpeakerInfo[];
    backgroundMusicDetected: boolean;
    processingLatency: LatencyMetrics;
  };

  // Intent Classification State
  intentClassification: {
    currentTranscript: string;
    previousTranscripts: string[];
    detectedIntents: ClassifiedIntent[];
    confidenceScores: number[];
    processingTime: number;
  };

  // Effect Suggestion State
  effectSuggestion: {
    rankedEffects: RankedEffect[];
    brandFiltering: BrandFilterResult;
    cooldownStates: CooldownState[];
    suggestionHistory: EffectSuggestion[];
    generationLatency: number;
  };

  // System Health State
  systemHealth: {
    sttServiceHealth: HealthStatus;
    geminiServiceHealth: HealthStatus;
    overallLatency: LatencyMetrics;
    errorRates: ErrorRateMetrics;
    activeConnections: number;
  };
}
```

## Core AI Agents

### 1. Audio Processing Agent (STT Coordinator)
**Responsibility:** Manages Google Cloud STT v2 streaming connection and audio preprocessing

```python
# PydanticAI Agent Definition
from pydantic_ai import Agent, RunContext
from typing import Dict, List, Optional

class AudioProcessingAgent(Agent):
    """Manages real-time audio processing and speech-to-text conversion"""
    
    async def process_audio_stream(
        self,
        audio_chunk: bytes,
        context: RunContext[AgentOrchestrationState]
    ) -> AudioProcessingResult:
        """
        Process incoming audio chunk and return STT results
        
        Features:
        - Voice Activity Detection (VAD)
        - Speaker diarization
        - Music/speech separation
        - Quality assessment
        """
        
        # Voice activity detection
        has_speech = await self._detect_voice_activity(audio_chunk)
        if not has_speech:
            return AudioProcessingResult(
                transcript="",
                confidence=0.0,
                speaker_info=None,
                processing_time=0
            )
        
        # Music detection and filtering
        music_detected = await self._detect_background_music(audio_chunk)
        if music_detected:
            audio_chunk = await self._filter_music(audio_chunk)
        
        # Send to Google STT
        stt_result = await self._process_with_stt(audio_chunk)
        
        # Update state
        context.deps.update_audio_state({
            'isActive': True,
            'backgroundMusicDetected': music_detected,
            'processingLatency': stt_result.processing_time
        })
        
        return stt_result

    async def _process_with_stt(self, audio_chunk: bytes) -> STTResult:
        """Process audio with Google Cloud STT v2"""
        # Implementation details for STT integration
        pass
```

### 2. Intent Classification Agent (Gemini Coordinator)
**Responsibility:** Analyzes conversation context and classifies speaker intent

```python
class IntentClassificationAgent(Agent):
    """Analyzes conversation context for intent classification"""
    
    async def classify_intent(
        self,
        transcript: str,
        speaker_info: SpeakerInfo,
        context: RunContext[AgentOrchestrationState]
    ) -> IntentClassificationResult:
        """
        Classify conversational intent using Gemini 2.5 Flash
        
        Intent Categories:
        - celebration: Achievement, success, victory
        - hype: Excitement, energy, anticipation
        - gratitude: Thanks, appreciation, acknowledgment
        - romance: Affection, love, intimate moments
        - general: Default category for unclear intents
        """
        
        # Build context window from recent transcripts
        conversation_context = self._build_context_window(
            transcript, 
            context.deps.intentClassification.previousTranscripts
        )
        
        # Create optimized prompt for Gemini
        classification_prompt = self._create_classification_prompt(
            conversation_context,
            speaker_info
        )
        
        # Call Gemini API
        gemini_result = await self._classify_with_gemini(classification_prompt)
        
        # Validate and score result
        validated_result = self._validate_classification(gemini_result)
        
        # Update state
        context.deps.update_intent_state({
            'currentTranscript': transcript,
            'detectedIntents': [validated_result],
            'confidenceScores': [validated_result.confidence],
            'processingTime': validated_result.processing_time
        })
        
        return validated_result

    def _create_classification_prompt(
        self, 
        context: str, 
        speaker_info: SpeakerInfo
    ) -> str:
        """Create optimized prompt for intent classification"""
        return f"""
        Analyze this live stream conversation for emotional intent:
        
        Context: {context}
        Speaker: {"Host" if speaker_info.is_host else "Guest"}
        
        Classify the primary intent (respond with JSON):
        {{
            "intent": "celebration|hype|gratitude|romance|general",
            "confidence": 0.0-1.0,
            "reasoning": "brief explanation",
            "trigger_worthy": boolean
        }}
        
        Focus on genuine emotional moments that would benefit from visual effects.
        """
```

### 3. Effect Suggestion Agent (Ranking Coordinator)
**Responsibility:** Generates and ranks effect suggestions based on intent and brand settings

```python
class EffectSuggestionAgent(Agent):
    """Generates ranked effect suggestions based on classified intent"""
    
    async def generate_suggestions(
        self,
        classified_intent: IntentClassificationResult,
        context: RunContext[AgentOrchestrationState]
    ) -> EffectSuggestionResult:
        """
        Generate and rank effect suggestions
        
        Ranking Factors:
        1. Intent relevance (40%)
        2. Brand compatibility (30%)
        3. Cooldown status (15%)
        4. Diversity factor (10%)
        5. Performance cost (5%)
        """
        
        # Get applicable effects for intent
        candidate_effects = await self._get_effects_by_intent(
            classified_intent.intent
        )
        
        # Apply brand filtering
        brand_compatible_effects = await self._apply_brand_filtering(
            candidate_effects,
            context.deps.session.creatorId
        )
        
        # Check cooldown states
        available_effects = self._filter_by_cooldown(
            brand_compatible_effects,
            context.deps.effectSuggestion.cooldownStates
        )
        
        # Rank effects using weighted algorithm
        ranked_effects = self._rank_effects(
            available_effects,
            classified_intent,
            context.deps.effectSuggestion.suggestionHistory
        )
        
        # Apply diversity filtering to prevent repetition
        diverse_suggestions = self._apply_diversity_filter(
            ranked_effects,
            max_suggestions=3
        )
        
        # Update state
        context.deps.update_suggestion_state({
            'rankedEffects': diverse_suggestions,
            'generationLatency': time.time() - start_time
        })
        
        return EffectSuggestionResult(
            suggestions=diverse_suggestions,
            intent_source=classified_intent,
            generation_time=time.time() - start_time
        )

    def _rank_effects(
        self,
        effects: List[Effect],
        intent: IntentClassificationResult,
        history: List[EffectSuggestion]
    ) -> List[RankedEffect]:
        """Multi-factor ranking algorithm for effects"""
        
        scored_effects = []
        for effect in effects:
            # Intent relevance scoring
            intent_score = self._calculate_intent_relevance(effect, intent)
            
            # Brand compatibility scoring
            brand_score = self._calculate_brand_compatibility(effect)
            
            # Diversity scoring (penalize recent usage)
            diversity_score = self._calculate_diversity_score(effect, history)
            
            # Performance scoring (favor low-cost effects on mobile)
            performance_score = self._calculate_performance_score(effect)
            
            # Weighted final score
            final_score = (
                intent_score * 0.40 +
                brand_score * 0.30 +
                diversity_score * 0.15 +
                performance_score * 0.15
            )
            
            scored_effects.append(RankedEffect(
                effect=effect,
                score=final_score,
                intent_relevance=intent_score,
                brand_compatibility=brand_score
            ))
        
        return sorted(scored_effects, key=lambda x: x.score, reverse=True)
```

### 4. System Health Monitor Agent
**Responsibility:** Monitors system health and manages fallback strategies

```python
class SystemHealthAgent(Agent):
    """Monitors AI pipeline health and manages fallbacks"""
    
    async def monitor_system_health(
        self,
        context: RunContext[AgentOrchestrationState]
    ) -> SystemHealthResult:
        """
        Monitor health of all AI components
        
        Health Checks:
        - Google STT service availability and latency
        - Gemini API service availability and quota
        - Overall pipeline latency
        - Error rate monitoring
        - Connection quality assessment
        """
        
        # Check STT service health
        stt_health = await self._check_stt_health()
        
        # Check Gemini service health
        gemini_health = await self._check_gemini_health()
        
        # Calculate overall latency
        overall_latency = self._calculate_pipeline_latency(context)
        
        # Check error rates
        error_rates = self._calculate_error_rates(context)
        
        # Determine overall health status
        overall_health = self._determine_overall_health(
            stt_health, gemini_health, overall_latency, error_rates
        )
        
        # Trigger fallbacks if necessary
        if overall_health.status == 'degraded':
            await self._trigger_fallback_mode(context)
        
        return SystemHealthResult(
            stt_health=stt_health,
            gemini_health=gemini_health,
            overall_latency=overall_latency,
            error_rates=error_rates,
            status=overall_health.status
        )

    async def _trigger_fallback_mode(
        self, 
        context: RunContext[AgentOrchestrationState]
    ):
        """Implement fallback strategies during service degradation"""
        
        # Fallback strategies:
        # 1. Increase caching for similar conversation patterns
        # 2. Reduce suggestion frequency to decrease API load
        # 3. Use simpler intent classification rules
        # 4. Prioritize manual effect library over AI suggestions
        pass
```

## LangGraph Orchestration

The agents are orchestrated using LangGraph to create a robust, fault-tolerant pipeline:

```python
from langgraph.graph import StateGraph, END

def create_ai_pipeline_graph() -> StateGraph:
    """Create the main AI processing pipeline using LangGraph"""
    
    # Create state graph
    workflow = StateGraph(AgentOrchestrationState)
    
    # Add agents as nodes
    workflow.add_node("audio_processing", AudioProcessingAgent())
    workflow.add_node("intent_classification", IntentClassificationAgent())
    workflow.add_node("effect_suggestion", EffectSuggestionAgent())
    workflow.add_node("health_monitor", SystemHealthAgent())
    
    # Define the processing flow
    workflow.add_edge("audio_processing", "intent_classification")
    workflow.add_edge("intent_classification", "effect_suggestion")
    workflow.add_edge("effect_suggestion", END)
    
    # Add conditional edges for error handling
    workflow.add_conditional_edges(
        "audio_processing",
        should_continue_processing,
        {
            True: "intent_classification",
            False: END
        }
    )
    
    # Add health monitoring as parallel process
    workflow.add_edge("health_monitor", END)
    
    # Set entry point
    workflow.set_entry_point("audio_processing")
    
    return workflow.compile()

def should_continue_processing(state: AgentOrchestrationState) -> bool:
    """Determine if processing should continue based on audio quality"""
    return (
        state.audioProcessing.isActive and
        len(state.intentClassification.currentTranscript.strip()) > 0
    )
```

## AI State Management

**State Persistence and Synchronization:**

```typescript
// AI State Store (Zustand)
interface AIState {
  // Agent Orchestration State
  orchestration: AgentOrchestrationState;
  
  // Real-time Updates
  updateAudioState: (update: Partial<AudioProcessingState>) => void;
  updateIntentState: (update: Partial<IntentClassificationState>) => void;
  updateSuggestionState: (update: Partial<EffectSuggestionState>) => void;
  updateHealthState: (update: Partial<SystemHealthState>) => void;
  
  // Action Handlers
  startProcessing: (sessionId: string) => Promise<void>;
  stopProcessing: () => Promise<void>;
  processAudioChunk: (audioChunk: ArrayBuffer) => Promise<void>;
  triggerManualSuggestion: (query: string) => Promise<void>;
  
  // Error Handling
  lastError: AIError | null;
  handleError: (error: AIError) => void;
  clearError: () => void;
  
  // Performance Metrics
  metrics: {
    avgLatency: number;
    successRate: number;
    suggestionsGenerated: number;
    effectsTriggered: number;
  };
  updateMetrics: (metrics: Partial<AIMetrics>) => void;
}

// AI State Store Implementation
export const useAIStore = create<AIState>((set, get) => ({
  orchestration: {
    session: null,
    audioProcessing: {
      isActive: false,
      inputLevel: 0,
      speakerInfo: [],
      backgroundMusicDetected: false,
      processingLatency: { p50: 0, p95: 0 }
    },
    intentClassification: {
      currentTranscript: '',
      previousTranscripts: [],
      detectedIntents: [],
      confidenceScores: [],
      processingTime: 0
    },
    effectSuggestion: {
      rankedEffects: [],
      brandFiltering: null,
      cooldownStates: [],
      suggestionHistory: [],
      generationLatency: 0
    },
    systemHealth: {
      sttServiceHealth: 'unknown',
      geminiServiceHealth: 'unknown',
      overallLatency: { p50: 0, p95: 0 },
      errorRates: { stt: 0, gemini: 0, overall: 0 },
      activeConnections: 0
    }
  },

  updateAudioState: (update) => set((state) => ({
    orchestration: {
      ...state.orchestration,
      audioProcessing: { ...state.orchestration.audioProcessing, ...update }
    }
  })),

  updateIntentState: (update) => set((state) => ({
    orchestration: {
      ...state.orchestration,
      intentClassification: { ...state.orchestration.intentClassification, ...update }
    }
  })),

  updateSuggestionState: (update) => set((state) => ({
    orchestration: {
      ...state.orchestration,
      effectSuggestion: { ...state.orchestration.effectSuggestion, ...update }
    }
  })),

  processAudioChunk: async (audioChunk: ArrayBuffer) => {
    const state = get();
    try {
      // Send to AI pipeline via WebSocket
      const result = await aiPipelineService.processAudio({
        sessionId: state.orchestration.session?.id,
        audioChunk,
        timestamp: Date.now()
      });
      
      // Update state based on results
      if (result.transcript) {
        state.updateIntentState({
          currentTranscript: result.transcript,
          processingTime: result.processingTime
        });
      }
      
      if (result.suggestions?.length > 0) {
        state.updateSuggestionState({
          rankedEffects: result.suggestions,
          generationLatency: result.suggestionLatency
        });
      }
      
    } catch (error) {
      state.handleError(error as AIError);
    }
  },

  // Additional methods...
}));
```

## AI Pipeline Integration

**WebSocket Integration for Real-time AI Processing:**

```typescript
// AI Pipeline WebSocket Service
class AIPipelineService {
  private ws: WebSocket | null = null;
  private messageQueue: AIMessage[] = [];
  
  async connect(sessionId: string): Promise<void> {
    this.ws = new WebSocket(`${WS_URL}/ai-pipeline`);
    
    this.ws.onopen = () => {
      this.authenticate(sessionId);
      this.processMessageQueue();
    };
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data) as AIMessage;
      this.handleAIResponse(message);
    };
    
    this.ws.onerror = (error) => {
      logger.error('AI Pipeline WebSocket error', error);
      useAIStore.getState().handleError(new AIError('CONNECTION_ERROR', error.message));
    };
  }
  
  async processAudio(request: AudioProcessingRequest): Promise<void> {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.messageQueue.push({
        type: 'AUDIO_PROCESSING',
        payload: request
      });
      return;
    }
    
    this.ws.send(JSON.stringify({
      type: 'AUDIO_PROCESSING',
      payload: {
        ...request,
        audioChunk: Array.from(new Uint8Array(request.audioChunk))
      }
    }));
  }
  
  private handleAIResponse(message: AIMessage): void {
    const aiStore = useAIStore.getState();
    
    switch (message.type) {
      case 'AUDIO_PROCESSED':
        aiStore.updateAudioState(message.payload);
        break;
        
      case 'INTENT_CLASSIFIED':
        aiStore.updateIntentState(message.payload);
        break;
        
      case 'SUGGESTIONS_GENERATED':
        aiStore.updateSuggestionState(message.payload);
        // Notify UI components
        useSuggestionsStore.getState().updateSuggestions(message.payload.rankedEffects);
        break;
        
      case 'HEALTH_UPDATE':
        aiStore.updateHealthState(message.payload);
        break;
        
      case 'ERROR':
        aiStore.handleError(new AIError(message.payload.code, message.payload.message));
        break;
    }
  }
}
```

## Performance Optimization

**Caching and Optimization Strategies:**

```python
class AIOptimizationService:
    """Service for optimizing AI pipeline performance"""
    
    def __init__(self):
        self.intent_cache = TTLCache(maxsize=1000, ttl=300)  # 5 min TTL
        self.effect_cache = TTLCache(maxsize=500, ttl=600)   # 10 min TTL
        
    async def get_cached_intent(self, transcript_hash: str) -> Optional[IntentClassificationResult]:
        """Get cached intent classification for similar transcripts"""
        return self.intent_cache.get(transcript_hash)
    
    async def cache_intent_result(
        self, 
        transcript_hash: str, 
        result: IntentClassificationResult
    ):
        """Cache intent classification result"""
        self.intent_cache[transcript_hash] = result
    
    async def optimize_gemini_request(self, prompt: str) -> str:
        """Optimize Gemini API request to reduce token usage"""
        # Remove redundant words and optimize prompt structure
        optimized = self._compress_prompt(prompt)
        return optimized
    
    def _compress_prompt(self, prompt: str) -> str:
        """Compress prompt while maintaining classification accuracy"""
        # Implementation for prompt compression
        pass
```

This enhanced AI layer architecture provides:

1. **Multi-Agent Orchestration** using LangGraph and PydanticAI
2. **Comprehensive State Management** with Zustand stores
3. **Real-time Processing Pipeline** with WebSocket integration
4. **Performance Optimization** with caching and request optimization
5. **Health Monitoring** with fallback strategies
6. **Error Handling** with graceful degradation

The system is designed to achieve the critical sub-500ms latency targets while maintaining reliability and cost efficiency through intelligent caching and optimization strategies.

---
