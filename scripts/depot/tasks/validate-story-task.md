# Validate Story Task

## Purpose
Validate a BMAD story file before spawning a development agent in Depot sandbox.

## Context
Stories must contain sufficient context and implementation details for development agents to work in isolation.

## Process

### Step 1: File Validation
- [ ] Story file exists and is readable
- [ ] Story file has proper naming convention (story_[id].md)
- [ ] File size is reasonable (not empty, not too large)

### Step 2: Content Validation
Check for essential sections:
- [ ] **Context Section**: Background and business requirements
- [ ] **Implementation Section**: Technical details and architecture guidance  
- [ ] **Acceptance Criteria**: Clear success criteria
- [ ] **Story ID**: Unique identifier for tracking

### Step 3: Dependency Validation
- [ ] Extract any dependencies listed in story
- [ ] Check if dependency stories are completed (if applicable)
- [ ] Validate dependency chain is not circular

### Step 4: Context Sufficiency
- [ ] Story contains enough technical context for isolated development
- [ ] Architecture decisions are clearly documented
- [ ] Implementation approach is specified
- [ ] Code patterns and conventions are referenced

### Validation Criteria
**PASS**: Story contains all essential sections and sufficient implementation context
**WARN**: Minor issues but development can proceed
**FAIL**: Missing critical information or dependencies not met

## Output
Return validation result with:
- Overall pass/fail status
- List of identified issues
- Dependency information
- Recommendations for improvement

## Usage
```bash
python3 scripts/depot/bmad_depot_bridge.py validate-story --story-file path/to/story.md
```