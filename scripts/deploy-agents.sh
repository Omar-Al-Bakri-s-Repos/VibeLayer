#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting VibeLayer Agent Deployment${NC}"

# 1. VERIFY ENVIRONMENT
echo -e "${YELLOW}Verifying environment...${NC}"

# Get GitHub PAT from Doppler
GITHUB_PAT=$(doppler secrets get GITHUB_PAT --plain --project vibelayer --config dev)
if [[ -z "$GITHUB_PAT" ]]; then
    echo -e "${RED}ERROR: Could not retrieve GITHUB_PAT from Doppler${NC}"
    echo -e "${YELLOW}Attempting to use environment variable...${NC}"
    GITHUB_PAT="${GITHUB_TOKEN}"
fi

if [[ -z "$GITHUB_PAT" ]]; then
    echo -e "${RED}ERROR: No GitHub PAT available${NC}"
    exit 1
fi

# Verify GitHub token is valid
if ! curl -s -H "Authorization: token $GITHUB_PAT" https://api.github.com/user > /dev/null; then
    echo -e "${RED}ERROR: GitHub PAT is invalid${NC}"
    exit 1
fi
echo -e "${GREEN}✓ GitHub PAT validated${NC}"

# Add to Depot secrets
~/.depot/bin/depot claude secrets add GITHUB_TOKEN --value "$GITHUB_PAT" 2>/dev/null || true

# Verify depot is working
if ! ~/.depot/bin/depot claude list-sessions >/dev/null 2>&1; then
    echo -e "${YELLOW}WARNING: Depot CLI claude