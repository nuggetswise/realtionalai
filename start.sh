#!/bin/bash

echo "🧠 Starting GraphOps Playground..."
echo "=================================="
echo ""
echo "This app is designed for RelationalAI PM interviews!"
echo ""
echo "Features:"
echo "  🏗️  Graph Schema Builder"
echo "  🔍 Query Executor" 
echo "  🧠 Semantic Inference Engine"
echo "  📋 PM Strategy Helper"
echo ""
echo "To use AI features, add your OpenAI API key in the sidebar."
echo ""

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Consider activating one."
fi

echo ""
echo "🚀 Launching app..."
echo "📱 App will open at: http://localhost:8502"
echo ""

# Run the app on port 8502 to avoid conflicts
streamlit run app.py --server.port 8502 