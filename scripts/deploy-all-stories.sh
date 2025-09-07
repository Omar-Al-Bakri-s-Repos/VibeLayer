#!/bin/bash

# Deploy All Stories - Automated multi-agent deployment using Depot build framework
# Creates 8 Claude Code agents for stories 1.1 through 1.8

set -euo pipefail

DEPOT_PROJECT_ID="frhsr3strf"
REPO_URL="https://github.com/Omar-Al-Bakri-s-Repos/VibeLayer.git"
BASE_SESSION_ID="vibelayer-depot-$(date +%Y%m%d-%H%M%S)"

echo "🚀 VibeLayer Multi-Agent Deployment"
echo "📂 Repository: $REPO_URL"
echo "🔧 Depot Project: $DEPOT_PROJECT_ID"
echo "🆔 Base Session: $BASE_SESSION_ID"
echo ""

# Validate depot CLI and authentication
if ! command -v depot &>/dev/null; then
    echo "❌ Error: depot CLI not found. Install from depot.dev"
    exit 1
fi

if [[ ! -f "depot.json" ]]; then
    echo "❌ Error: depot.json not found. Run from VibeLayer root directory"
    exit 1
fi

# Deploy agents for stories 1.1 through 1.8
STORIES=("1.1" "1.2" "1.3" "1.4" "1.5" "1.6" "1.7" "1.8")
DEPLOYED_AGENTS=()

echo "📋 Deploying ${#STORIES[@]} Claude Code agents using Depot infrastructure..."
echo ""

for STORY in "${STORIES[@]}"; do
    echo "🤖 Deploying Agent for Story ${STORY}..."
    
    SESSION_ID="${BASE_SESSION_ID}-story-${STORY}"
    
    # Verify story file exists
    STORY_FILE=$(find docs/stories -name "${STORY}.*.md" | head -1)
    if [[ -z "$STORY_FILE" ]]; then
        echo "⚠️  Warning: Story ${STORY} not found in docs/stories/ - skipping"
        continue
    fi
    
    # Create Depot-integrated agent prompt
    AGENT_PROMPT=$(cat <<EOF
You are James, Full Stack Developer for VibeLayer Story ${STORY}, running in Depot build infrastructure.

🎯 DEPOT BUILD INTEGRATION MISSION:
1. Read CLAUDE.md (your complete configuration and persona)
2. Read ${STORY_FILE} (your assigned story requirements)
3. Implement using the existing Depot build framework
4. Update Dev Agent Record sections in story file with your progress

🏗️ VIBELAYER DEPOT BUILD FRAMEWORK:
- depot.json is configured (project: ${DEPOT_PROJECT_ID})
- Use 'depot build' commands instead of 'docker build'
- Available targets: control-panel, monorepo, dev, claude-agent
- Multi-platform builds: linux/amd64, linux/arm64
- Depot caching pre-configured for faster builds

🔧 DEPOT COMMANDS TO USE:
- \`depot build --project ${DEPOT_PROJECT_ID} -t vibelayer:test .\` (build monorepo)
- \`depot build --project ${DEPOT_PROJECT_ID} --target control-panel\` (build control panel)
- \`depot build --project ${DEPOT_PROJECT_ID} --target claude-agent\` (development build)
- \`depot build --project ${DEPOT_PROJECT_ID} --load\` (build and load locally)

🚀 EXISTING INFRASTRUCTURE:
- Dockerfile optimized for Depot builds with multi-stage caching
- pnpm workspaces with Turbo monorepo setup
- Next.js control panel in apps/control-panel/
- TypeScript + Tailwind + Convex backend
- GitHub Container Registry integration
- GitHub Actions workflows in .github/workflows/

🛠️ MCP TOOLS AVAILABLE:
- Serena: Semantic code analysis, symbol-level editing, project understanding
- Desktop Commander: File operations, process management, system interactions
- Enhanced development workflow with intelligent code assistance

⚠️ CRITICAL RULES:
- Use Depot build acceleration, not regular Docker
- Follow existing depot.json configuration exactly  
- Update Dev Agent Record sections in your story file
- Implement comprehensive testing before marking complete
- Use MCP tools for enhanced development efficiency
- Follow VibeLayer coding patterns and architectural decisions

🎯 SUCCESS CRITERIA:
- Story requirements fully implemented
- All tests passing
- Code follows VibeLayer patterns
- Documentation updated
- Dev Agent Record shows completion status

START: Read CLAUDE.md and ${STORY_FILE}, then implement using Depot build framework.
EOF
    )
    
    echo "   📄 Story file: $STORY_FILE"
    echo "   🆔 Session ID: $SESSION_ID"
    
    # Deploy using Depot infrastructure
    if depot claude \
        --session-id "$SESSION_ID" \
        --repository "$REPO_URL" \
        --branch "main" \
        --git-secret "GIT_CREDENTIALS" \
        "$AGENT_PROMPT"; then
        
        DEPLOYED_AGENTS+=("${STORY}:${SESSION_ID}")
        echo "   ✅ Agent ${STORY} deployed successfully"
        echo "   🔗 Monitor: https://depot.dev/orgs/h0wmrqw8rk/claude/${SESSION_ID}"
    else
        echo "   ❌ Failed to deploy agent for story ${STORY}"
    fi
    
    echo ""
    
    # Brief pause between deployments
    sleep 2
done

echo ""
echo "📊 DEPLOYMENT SUMMARY"
echo "=================="
echo "Total Stories: ${#STORIES[@]}"
echo "Successfully Deployed: ${#DEPLOYED_AGENTS[@]}"
echo ""

if [[ ${#DEPLOYED_AGENTS[@]} -gt 0 ]]; then
    echo "🤖 ACTIVE AGENTS:"
    for agent in "${DEPLOYED_AGENTS[@]}"; do
        IFS=':' read -r story session <<< "$agent"
        echo "   Story ${story}: https://depot.dev/orgs/h0wmrqw8rk/claude/${session}"
    done
    echo ""
    echo "✅ Multi-agent deployment completed successfully!"
    echo "🏗️ All agents integrated with Depot build framework (project: $DEPOT_PROJECT_ID)"
    echo "📊 Monitor all agents at: https://depot.dev/orgs/h0wmrqw8rk/claude"
else
    echo "❌ No agents were deployed successfully"
    exit 1
fi