# 7. External APIs

## Google Cloud Speech-to-Text v2
- **Purpose:** Real-time speech transcription with speaker diarization and music filtering
- **Documentation:** https://cloud.google.com/speech-to-text/v2/docs
- **Base URL:** https://speech.googleapis.com/v2
- **Authentication:** Google Cloud Service Account with JSON key
- **Rate Limits:** 1000 requests/minute, streaming optimized

**Key Endpoints Used:**
- `POST /speech:streamingRecognize` - Real-time speech streaming
- `GET /operations/{operationId}` - Operation status monitoring

**Integration Notes:** Streaming connection maintained throughout session with automatic reconnection. Audio preprocessed to optimize for speech vs music distinction.

## Gemini 2.5 Flash API
- **Purpose:** Intent classification and conversational context understanding
- **Documentation:** https://ai.google.dev/gemini-api/docs
- **Base URL:** https://generativelanguage.googleapis.com/v1beta
- **Authentication:** Google API Key with quotas
- **Rate Limits:** 300 requests/minute with batching optimization

**Key Endpoints Used:**
- `POST /models/gemini-2.5-flash:generateContent` - Intent classification
- `GET /models/gemini-2.5-flash` - Model information and capabilities

**Integration Notes:** Optimized prompts for intent classification with confidence scoring. Caching strategy for similar conversation patterns to reduce costs.

## TikTok Live Studio API
- **Purpose:** RTMP streaming integration and overlay capabilities
- **Documentation:** https://developers.tiktok.com/doc/live-studio-api
- **Base URL:** https://open-api.tiktok.com
- **Authentication:** OAuth 2.0 with creator consent
- **Rate Limits:** 100 requests/minute per creator

**Key Endpoints Used:**
- `POST /live/stream/start` - Initiate live stream
- `GET /live/stream/status` - Stream health monitoring
- `POST /live/overlay/update` - Real-time overlay updates

**Integration Notes:** Limited availability requires fallback to web browser overlay method when API access unavailable.

---
