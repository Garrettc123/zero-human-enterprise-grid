#!/bin/bash

echo "============================================================"
echo "ZERO-HUMAN ENTERPRISE GRID - SETUP"
echo "============================================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi
echo "✓ Python 3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r orchestrator/requirements.txt
pip install -r revenue-engine/requirements.txt
echo "✓ Dependencies installed"

# Check environment
echo ""
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN not set"
    echo "   Set with: export GITHUB_TOKEN='your_token'"
else
    echo "✓ GITHUB_TOKEN found"
fi

echo ""
echo "============================================================"
echo "SETUP COMPLETE"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Set: export GITHUB_TOKEN='your_token'"
echo "2. Run: python3 orchestrator/autonomous_orchestrator.py"
echo ""
echo "Payment Hub: gwc2780@gmail.com"
echo "============================================================"