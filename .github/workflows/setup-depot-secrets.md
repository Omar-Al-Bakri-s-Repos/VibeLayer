# Setting up Depot Secrets for GitHub Actions

## Required Secrets

1. **DEPOT_TOKEN** - Your Depot authentication token
   - Get from: https://depot.dev/orgs/h0wmrqw8rk/settings/tokens
   - Add to: Repository Settings → Secrets and variables → Actions → New repository secret

## Steps to Configure

1. Go to your GitHub repository: https://github.com/OmarA1-Bakri/VibeLayer
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add the following secret:
   - Name: `DEPOT_TOKEN`
   - Value: Your Depot token from the dashboard

## Running the Workflow

1. Go to Actions tab in GitHub
2. Find "Depot Story Runner" workflow
3. Click "Run workflow"
4. Options:
   - **stories**: Enter story numbers (e.g., "1.1,1.2,1.3") or "all" for all stories
   - **parallel**: Check to run stories in parallel (recommended)
5. Click "Run workflow"

The workflow will:
- Spawn Depot Claude agents for each selected story
- Each agent reads the story requirements from `.bmad/stories/`
- Agents implement the story autonomously
- Create pull requests with the changes

## Monitoring

- Each story runs in its own job
- View progress in the Actions tab
- Session IDs are shown in logs for debugging
- PRs are created automatically if changes are made