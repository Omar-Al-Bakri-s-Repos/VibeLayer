# VibeLayer BMAD-Depot Integration

This directory contains the complete integration between BMAD-METHOD™ and Depot Remote Agent Sandboxes for the VibeLayer project.

## 🌉 Architecture Overview

The integration follows the principle of **hybrid execution**:

- **Local Agents**: BMAD orchestrator, ScrumMaster, Analyst, PM, Architect run locally for fast planning
- **Sandboxed Agents**: Only development agents run in secure Depot sandboxes for code implementation
- **Story-Driven**: Each development agent receives only their specific story with full context

## 📁 Files Structure

```
scripts/depot/
├── README.md                     # This documentation
├── bmad_depot_bridge.md          # BMAD agent definition following BMAD patterns
├── bmad_depot_bridge.py          # Python implementation bridge
├── spawn_dev_agent.py            # Individual development agent spawning  
├── session_coordinator.py        # Multi-session coordination and monitoring
├── test-integration.py           # Integration test suite
├── vibelayer-scrum-config.md     # ScrumMaster configuration for comprehensive story output
├── tasks/
│   └── validate-story-task.md    # Story validation task following BMAD pattern
└── templates/
    └── story-validation-tmpl.yaml # Validation result template
```

## 🚀 Quick Start

### 1. Prerequisites

- Depot CLI installed (automatically done during setup)
- Python 3.11+
- BMAD-METHOD™ already installed in project
- GitHub Actions access (for CI/CD integration)

### 2. Test the Integration

Run the integration test suite:

```bash
python3 scripts/depot/test-integration.py
```

This validates:
- Depot CLI accessibility  
- Story validation functionality
- Session management
- Story discovery and coordination

### 3. Basic Usage

#### Validate a Story Before Development
```bash
python3 scripts/depot/bmad_depot_bridge.py validate-story --story-file path/to/story.md
```

#### Spawn Development Agent for Single Story  
```bash
python3 scripts/depot/bmad_depot_bridge.py spawn-dev --story-file path/to/story.md
```

#### Coordinate Parallel Development
```bash  
python3 scripts/depot/bmad_depot_bridge.py coordinate --stories-dir .bmad/stories/ --max-concurrent 5
```

#### Monitor Active Sessions
```bash
python3 scripts/depot/bmad_depot_bridge.py monitor --timeout 30
```

## 🎭 BMAD Agent Integration

### Using the BMAD Depot Bridge Agent

The integration includes a proper BMAD agent that follows BMAD patterns:

```bash
# Activate the BMAD Depot Bridge agent
# Load: scripts/depot/bmad_depot_bridge.md

# Available commands (with * prefix):
*help                  # Show available commands  
*spawn-dev            # Spawn development agent for story
*coordinate           # Coordinate parallel development
*monitor              # Monitor active sessions  
*validate-story       # Validate story before spawning
*depot-status         # Check Depot CLI status
```

### Story-Driven Development Workflow

1. **Planning Phase (Local)**:
   - BMAD orchestrator coordinates local agents
   - ScrumMaster generates comprehensive VibeLayer story backlog
   - Analyst, PM, Architect create specifications locally

2. **Development Phase (Sandboxed)**:
   - Stories contain full context and implementation guidance
   - Development agents spawn in isolated Depot sandboxes
   - Each agent receives only their story (no cross-story artifacts)
   - Multiple agents work in parallel on different stories

3. **Integration Phase**:
   - Completed code collected from sandboxes
   - Local QA agents review implementations
   - Orchestrator coordinates final integration

## 🔧 Configuration

### Environment Variables

```bash
# Required for Depot authentication
export DEPOT_TOKEN="your-depot-token"

# Optional for Claude Code integration  
export CLAUDE_CODE_OAUTH_TOKEN="your-claude-token"

# Optional for custom configuration
export VIBELAYER_STORIES_DIR=".bmad/stories"
export VIBELAYER_MAX_CONCURRENT="5"
```

### GitHub Secrets

For CI/CD integration, configure these secrets:

- `DEPOT_TOKEN`: Your Depot organization token
- `CLAUDE_CODE_OAUTH_TOKEN`: Claude Code OAuth token (optional)

## 📊 GitHub Actions Integration

The integration includes a comprehensive GitHub Actions workflow:

### Triggers

- **Manual**: `workflow_dispatch` with action selection
- **Automatic**: Push/PR with story file changes

### Available Actions

1. **coordinate-development**: Coordinate parallel development of multiple stories
2. **spawn-single-agent**: Spawn development agent for specific story  
3. **monitor-sessions**: Monitor active development sessions
4. **cleanup-sessions**: Clean up old session files

### Example Usage

```bash
# Trigger via GitHub CLI
gh workflow run bmad-depot.yml \
  -f action=coordinate-development \
  -f max_concurrent=5 \
  -f stories_dir=.bmad/stories/
```

## 🎯 Story Requirements

For successful Depot integration, stories must contain:

### Required Sections
- **Context**: Business context and user needs
- **Implementation Details**: Technical approach and file locations
- **Architecture Guidance**: VibeLayer patterns and decisions
- **Acceptance Criteria**: Clear, testable success criteria
- **Testing Requirements**: Testing approach for TypeScript/React
- **Dependencies**: Other stories that must complete first

### Technical Context
- VibeLayer-specific code patterns and conventions
- Monorepo package organization (@vibelayer/*)
- Technology stack usage (TypeScript, React, Next.js, Tailwind)
- API contracts and communication patterns

## 🔍 Monitoring and Debugging

### Session Management

```bash
# List all active sessions
python3 scripts/depot/spawn_dev_agent.py --list

# Get specific session status
python3 scripts/depot/spawn_dev_agent.py --status session-id

# Monitor with auto-refresh
python3 scripts/depot/session_coordinator.py --monitor --monitor-timeout 60
```

### Log Files

- Session logs: `.depot/logs/`
- Session state: `.depot/sessions/`
- Artifacts: `.depot/artifacts/`

## 🧪 Testing

### Integration Test Suite

```bash
# Run full test suite
python3 scripts/depot/test-integration.py

# Individual component testing
python3 scripts/depot/bmad_depot_bridge.py depot-status
python3 scripts/depot/bmad_depot_bridge.py validate-story --story-file test.md
```

### Test Coverage

- Depot CLI accessibility
- Story validation functionality  
- Session management and coordination
- Story discovery and dependency resolution
- Error handling and recovery

## 🔒 Security Considerations

- Development agents run in isolated Depot sandboxes
- No cross-story artifact sharing in sandbox environments
- Session state managed securely in local storage
- GitHub Actions use organization secrets for authentication

## 🚀 Performance Optimization

- **Local Planning**: Fast execution for analysis and coordination
- **Parallel Development**: Up to 10 concurrent development agents
- **Smart Scheduling**: Dependency-aware story coordination  
- **Resource Management**: Automatic cleanup of old sessions

## 📈 Scaling Considerations

- **Concurrency**: Configurable via `max_concurrent` parameter
- **Story Batching**: Processes stories in manageable batches
- **Resource Limits**: Depot sandbox resource controls
- **Cost Management**: Monitor via Depot dashboard

## 🤝 Contributing

When extending this integration:

1. **Follow BMAD Patterns**: Use YAML configuration blocks and structured agent definitions
2. **Maintain Story Isolation**: Each development agent works independently
3. **Test Integration**: Run test suite after changes
4. **Update Documentation**: Keep README and configuration up to date

## 📚 References

- [BMAD-METHOD™ Documentation](https://github.com/bmad-code-org/BMAD-METHOD)
- [Depot Remote Agent Sandboxes](https://depot.dev/docs)
- [VibeLayer Architecture](../docs/architecture/)

---

✨ **Ready for Enterprise-Grade AI Development**: This integration enables scalable, secure, and efficient AI-assisted development workflows for the VibeLayer platform.