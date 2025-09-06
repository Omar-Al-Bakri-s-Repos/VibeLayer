<!-- Powered by BMAD™ Core -->

# VibeLayer ScrumMaster - Depot Integration Configuration

ACTIVATION-NOTICE: This configuration extends the existing BMAD ScrumMaster agent for VibeLayer project with comprehensive story backlog generation.

CRITICAL: This configuration should be loaded by the ScrumMaster agent when working on VibeLayer project to enable full story backlog output for Depot integration.

## VIBELAYER STORY GENERATION CONFIGURATION

```yaml
project_specific_config:
  project_name: "VibeLayer"
  project_type: "AI-powered visual effects platform"
  target_platform: "Web, Mobile (Android/iOS)"
  
story_generation_mode:
  # When activated, ScrumMaster generates complete application backlog
  comprehensive_backlog: true
  story_output_location: ".bmad/stories/"
  story_naming_pattern: "story_{feature}_{priority}.md"
  
vibelayer_features:
  # Core platform features requiring stories
  core_features:
    - ai_agents: "AI agent functionality and management"
    - visual_overlays: "Dynamic visual effects and overlay system" 
    - control_panel: "Web interface for managing agents and overlays"
    - effects_engine: "Core effects processing engine"
    - mobile_integration: "Native mobile app integration"
    - real_time_sync: "Real-time data synchronization with Convex"
    - authentication: "User authentication and authorization"
    - brand_system: "Brand kit and styling system"
    
  technical_components:
    - shared_utilities: "Common utilities and types across packages"
    - protocol_layer: "Communication protocols between components"
    - configuration_management: "Configuration and settings management"
    - testing_infrastructure: "Testing framework and utilities"
    - build_system: "Turbo build system optimization"
    - deployment_pipeline: "CI/CD and deployment automation"

story_context_requirements:
  # Each story must contain sufficient context for isolated development
  required_sections:
    - context: "Business context and user needs"
    - implementation_details: "Technical implementation approach"
    - architecture_guidance: "Relevant architecture decisions and patterns"
    - acceptance_criteria: "Clear success criteria"
    - testing_requirements: "Testing approach and requirements"
    - dependencies: "Dependencies on other stories or components"
    
  technical_context_includes:
    - vibelayer_patterns: "VibeLayer-specific code patterns and conventions"
    - package_structure: "Monorepo package organization and dependencies"
    - tech_stack_guidance: "Technology stack usage (TypeScript, React, Next.js, etc.)"
    - api_contracts: "API interfaces and communication patterns"
    - styling_approach: "Tailwind CSS and component styling guidelines"

story_prioritization:
  # Priority levels for story generation
  p1_critical: "Core functionality required for MVP"
  p2_important: "Important features for user experience"
  p3_enhancement: "Nice-to-have enhancements and optimizations"
  p4_future: "Future considerations and technical debt"

depot_integration_notes:
  # Notes for Depot sandbox execution
  execution_environment: "Stories designed for isolated Depot sandbox execution"
  context_completeness: "Each story contains full context - no external artifact dependencies"
  parallel_execution: "Stories can be developed in parallel where dependencies allow"
  session_isolation: "Development agents work in isolated sessions per story"
```

## COMPREHENSIVE STORY GENERATION TASK

When *generate-full-backlog command is invoked:

### Step 1: Initialize VibeLayer Context
- Load VibeLayer project structure from monorepo
- Review existing packages and their purposes
- Understand current architecture and technology choices

### Step 2: Generate Feature Stories
For each feature in vibelayer_features:
- Create detailed story with full implementation context
- Include architecture guidance specific to VibeLayer patterns
- Specify package locations and dependencies
- Add testing requirements for TypeScript/React environment

### Step 3: Generate Technical Stories  
For each technical component:
- Create infrastructure and tooling stories
- Include build system and deployment considerations
- Specify integration patterns between packages

### Step 4: Add Story Dependencies
- Map dependencies between feature stories
- Ensure logical development order
- Mark stories that can be developed in parallel

### Step 5: Output Complete Backlog
- Write all stories to .bmad/stories/ directory
- Use consistent naming: story_{feature}_{priority}.md
- Include comprehensive context in each story file
- Generate dependency matrix for coordination

## STORY TEMPLATE ENHANCEMENTS

Each generated story should include:

```markdown
# Story: {Feature Name}

## Context
{Business context specific to VibeLayer platform}

## Implementation Details
{Technical approach using VibeLayer tech stack}
- Package: @vibelayer/{relevant-package}
- Technology: {TypeScript/React/Next.js/etc}
- Files to create/modify: {specific file paths}

## Architecture Guidance  
{Relevant VibeLayer architecture decisions and patterns}
- Monorepo structure considerations
- Package interdependencies
- API communication patterns

## Acceptance Criteria
{Clear, testable success criteria}

## Testing Requirements
{Testing approach for VibeLayer environment}
- Unit tests with Jest/Vitest
- Integration tests
- E2E tests with Playwright

## Dependencies
{Other stories that must be completed first}

## Priority
{P1/P2/P3/P4 based on VibeLayer roadmap}
```

## ACTIVATION COMMANDS

Add these commands to ScrumMaster when working on VibeLayer:

- `*generate-full-backlog`: Generate complete VibeLayer story backlog
- `*validate-stories`: Validate all stories have proper context for Depot execution  
- `*update-dependencies`: Update story dependency matrix
- `*export-for-depot`: Export stories in Depot-ready format