# 19. Monitoring and Observability

## Monitoring Stack

- **Frontend Monitoring:** Sentry for error tracking, Vercel Analytics for performance
- **Backend Monitoring:** Sentry for errors, Google Cloud Monitoring for infrastructure
- **Error Tracking:** Centralized in Sentry with custom context and user information
- **Performance Monitoring:** Real User Monitoring (RUM) via Sentry, synthetic monitoring via Pingdom

## Key Metrics

**Frontend Metrics:**
- Core Web Vitals (LCP, FID, CLS) with targets: LCP <2.5s, FID <100ms, CLS <0.1
- JavaScript errors with error boundary capture and user context
- API response times measured client-side with p95 targets
- User interactions and conversion funnels for effect usage

**Backend Metrics:**
- Request rate and error rate by endpoint with 99.9% success rate target
- Response time distribution with p50 <200ms, p95 <500ms targets
- Database query performance with slow query monitoring
- WebSocket connection health and message throughput
- AI pipeline latency and processing costs
- Resource utilization and auto-scaling triggers

**Business Metrics:**
- Effect suggestion acceptance rate (target: >35%)
- Creator session duration with effects enabled
- Platform integration success rates
- Revenue correlation with effect usage

---
