#!/bin/bash

# VibeLayer Doppler Setup Script
echo "🔐 Setting up Doppler for VibeLayer..."

# Check if Doppler CLI is installed
if ! command -v doppler &> /dev/null; then
    echo "❌ Doppler CLI not found. Installing..."
    
    # Install Doppler CLI based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install dopplerhq/cli/doppler
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh | sudo sh
    else
        echo "❌ Unsupported OS. Please install Doppler CLI manually: https://docs.doppler.com/docs/install-cli"
        exit 1
    fi
fi

# Login to Doppler (if not already logged in)
if ! doppler auth status &> /dev/null; then
    echo "🔑 Please login to Doppler..."
    doppler login
fi

# Setup project
echo "📁 Setting up Doppler project..."
doppler projects create vibelayer --description "VibeLayer AI Platform secrets" || true

# Setup environments
echo "🌍 Creating environments..."
doppler environments create dev --project vibelayer --name "Development" || true
doppler environments create stg --project vibelayer --name "Staging" || true
doppler environments create prd --project vibelayer --name "Production" || true

# Setup configs
echo "⚙️ Creating configs..."
doppler configs create dev --project vibelayer --environment dev --name "Development Config" || true
doppler configs create stg --project vibelayer --environment stg --name "Staging Config" || true
doppler configs create prd --project vibelayer --environment prd --name "Production Config" || true

# Set default config for local development
echo "🏠 Setting up local development..."
cd "$(dirname "$0")/.."
doppler setup --project vibelayer --config dev

echo "✅ Doppler setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'doppler secrets set' to add your secrets"
echo "2. Use 'doppler run -- npm run dev' to run with secrets"
echo "3. For production: 'doppler run --config prd -- npm start'"
