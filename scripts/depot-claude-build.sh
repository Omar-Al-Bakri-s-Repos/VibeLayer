#!/bin/bash

# Depot Claude Build Script - Integrates with existing Depot build framework
# Uses depot.json configuration and Depot runners for proper build acceleration

set -euo pipefail

# Configuration from existing depot.json
DEPOT_PROJECT_ID="frhsr3strf"
REPO_URL="https://github.com/Omar-Al-Bakri-s-Repos/VibeLayer.git"
STORY="${1:-1.1}"
SESSION_ID="vibelayer-depot-story-${STORY}-$(date +%Y%m%d-%H%M%S)"

# Validate depot CLI and authentication
if ! command -v depot &>/dev/null; then
    echo "❌ Error: depot CLI not found. Install from depot.dev"
    exit 1
fi

# Verify depot.json exists and is configured
if [[ ! -f "depot.json" ]]; then
    echo "❌ Error: depot.json not found. Run 'depot init' first"
    exit 1
fi

echo "🏗️ Depot Claude Build - Story ${STORY}"
echo "📂 Repository: $REPO_URL"
echo "🔧 Depot Project: $DEPOT_PROJECT_ID"
echo "🆔 Session ID: $SESSION_ID"
echo "📋 Using existing depot.json configuration"

# Verify story file exists
STORY_FILE=$(find docs/stories -name "${STORY}.*.md" | head -1)
if [[ -z "$STORY_FILE" ]]; then
    echo "❌ Error: Story ${STORY} not found in docs/stories/"
    exit 1
fi

echo "📄 Story file: $STORY_FILE"

# Create Depot-integrated agent prompt
AGENT_PROMPT=$(cat <<EOF
You are James, Full Stack Developer for VibeLayer Story ${STORY}, running in Depot build infrastructure.

🎯 DEPOT BUILD INTEGRATION MISSION:
1. Read CLAUDE.md (your complete configuration)
2. Read ${STORY_FILE} (your assigned story)
3. Implement using the existing Depot build framework

🏗️ DEPOT BUILD FRAMEWORK (CRITICAL):
- depot.json is already configured (project: ${DEPOT_PROJECT_ID})
- Use 'depot build' commands instead of 'docker build'
- Available targets: control-panel, monorepo, dev
- Multi-platform builds: linux/amd64, linux/arm64
- Depot caching is pre-configured for faster builds

🔧 DEPOT COMMANDS TO USE:
- \`depot build --project ${DEPOT_PROJECT_ID} -t vibelayer:test .\` (build monorepo)
- \`depot build --project ${DEPOT_PROJECT_ID} --target control-panel\` (build control panel)
- \`depot build --project ${DEPOT_PROJECT_ID} --load\` (build and load locally)
- Follow existing GitHub Actions patterns in .github/workflows/depot-build.yml

🚀 EXISTING INFRASTRUCTURE:
- Dockerfile is already optimized for Depot builds
- pnpm workspaces configured
- Turbo monorepo setup complete
- Multi-stage builds with caching layers
- GitHub Container Registry integration

⚠️ IMPORTANT RULES:
- Use Depot build acceleration, not regular Docker
- Follow existing depot.json configuration
- Update Dev Agent Record sections in story files
- Implement comprehensive testing before marking complete
- Use MCP tools (Serena, Desktop Commander) for enhanced development

START: Read CLAUDE.md and ${STORY_FILE}, then implement using Depot build framework.
EOF
)

echo "🤖 Deploying Depot-integrated Claude Agent..."
echo "📋 Agent configured for Depot build acceleration"

# Deploy using existing Depot infrastructure
depot claude \
    --session-id "$SESSION_ID" \
    --repository "$REPO_URL" \
    --branch "main" \
    --git-secret "GIT_CREDENTIALS" \
    "$AGENT_PROMPT"

echo ""
echo "✅ Depot Claude Agent deployed successfully!"
echo "🔗 Session ID: $SESSION_ID"
echo "🏗️ Integrated with Depot build framework (project: $DEPOT_PROJECT_ID)"
echo "📊 Monitor at: https://depot.dev/orgs/h0wmrqw8rk/claude/$SESSION_ID"
echo ""
echo "🎯 Agent is configured to:"
echo "   - Use depot build commands for container builds"
echo "   - Follow existing depot.json configuration" 
echo "   - Leverage Depot's build acceleration"
echo "   - Implement Story ${STORY} with proper testing"