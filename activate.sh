#!/bin/bash
# Typography Agent Development Environment Activation Script

echo "🎨 Typography Agent for Adobe Illustrator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "❌ Dependencies not found. Installing..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed."
fi

# Verify installation
echo "🧪 Verifying installation..."
python -c "import anthropic, openai, mcp, fastapi; print('✅ All dependencies verified')" 2>/dev/null || {
    echo "❌ Some dependencies missing. Installing..."
    pip install -r requirements.txt
}

echo ""
echo "🚀 Typography Agent Development Environment Ready!"
echo ""
echo "Available commands:"
echo "  • Start MCP Bridge Server: cd mcp_bridge_server && python server.py"
echo "  • Run example script: python examples/basic_usage.py"
echo "  • Run tests: pytest"
echo "  • Format code: black src/"
echo "  • Check linting: flake8 src/"
echo ""
echo "💡 Remember to install the CEP extension in Illustrator!"
echo "📖 See setup_guide.md for complete installation instructions"
echo ""
echo "Virtual environment activated. Happy coding! 🎯"
