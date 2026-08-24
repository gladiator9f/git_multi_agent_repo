#!/bin/bash
# GitHub Sync Script for git_multi_agent_repo
# Usage: ./sync_github.sh [push] ["custom commit message"]

set -e

# Configuration
GITHUB_REPO="gladiator9f/git_multi_agent_repo"
LOCAL_DIR="/home/ec2-user/environment/my_projects/git_multi_agent_repo"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
CUSTOM_MESSAGE=""
if [ "$1" == "push" ] && [ -n "$2" ]; then
    CUSTOM_MESSAGE="$2"
fi

# Retrieve PAT from SSM
GITHUB_PAT=$(aws ssm get-parameter --name "/orchestraprime/github/pat_multi_agent_repo" --with-decryption --query "Parameter.Value" --output text 2>/dev/null)
if [ -z "$GITHUB_PAT" ]; then
    echo -e "${RED}ERROR: Failed to retrieve GitHub PAT from SSM Parameter Store.${NC}"
    echo -e "${RED}Run: aws ssm put-parameter --name '/orchestraprime/github/pat_multi_agent_repo' --type SecureString --value '<YOUR_PAT>' --overwrite${NC}"
    exit 1
fi

GITHUB_URL="https://${GITHUB_PAT}@github.com/${GITHUB_REPO}.git"

echo -e "${GREEN}===== Multi-Agent Repo GitHub Sync =====${NC}"
echo -e "${BLUE}Repository: ${GITHUB_REPO}${NC}"
echo -e "${BLUE}Local: ${LOCAL_DIR}${NC}"
echo -e "${BLUE}Date: $(date)${NC}"
echo ""

cd "$LOCAL_DIR"

# Configure git
git config user.email "multi-agent-bot@orchestraprime.ai"
git config user.name "Multi-Agent Bot"

# Set remote URL with PAT
if git remote | grep -q origin; then
    git remote set-url origin "$GITHUB_URL"
else
    git remote add origin "$GITHUB_URL"
fi

# Show status
echo -e "${YELLOW}Current status:${NC}"
git status --short

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
echo -e "${BLUE}Current branch: ${CURRENT_BRANCH}${NC}"

if [ "$1" == "push" ]; then
    # Count changes
    CHANGES=$(git status --porcelain | wc -l)
    if [ "$CHANGES" -eq 0 ]; then
        echo -e "${GREEN}✓ Working directory clean, nothing to commit${NC}"
    else
        echo -e "${YELLOW}Found $CHANGES changes${NC}"

        git add -A

        if [ -n "$CUSTOM_MESSAGE" ]; then
            COMMIT_MSG="$CUSTOM_MESSAGE"
        else
            COMMIT_MSG="sync: update $(date '+%Y-%m-%d %H:%M:%S UTC')"
        fi

        git commit -m "$COMMIT_MSG"
        echo -e "${GREEN}✓ Changes committed${NC}"
    fi

    # Push
    echo -e "${YELLOW}Pushing to GitHub (branch: ${CURRENT_BRANCH})...${NC}"
    if git push origin "$CURRENT_BRANCH" --force-with-lease 2>/dev/null; then
        echo -e "${GREEN}✓ Pushed to GitHub${NC}"
    else
        echo -e "${YELLOW}Force-with-lease failed, force pushing...${NC}"
        git push origin "$CURRENT_BRANCH" --force
        echo -e "${GREEN}✓ Force pushed to GitHub${NC}"
    fi

    echo ""
    echo -e "${BLUE}Latest commits:${NC}"
    git log --oneline -5
fi

echo ""
echo -e "${GREEN}===== Sync Complete =====${NC}"
echo -e "${BLUE}GitHub: https://github.com/${GITHUB_REPO}${NC}"
echo -e "${BLUE}Branch: ${CURRENT_BRANCH}${NC}"
