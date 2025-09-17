@echo off
REM Typography Agent Development Environment Activation Script (Windows)

echo 🎨 Typography Agent for Adobe Illustrator
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv venv
    echo ✅ Virtual environment created.
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check and install dependencies
echo 🧪 Verifying installation...
python -c "import anthropic, openai, mcp, fastapi; print('✅ All dependencies verified')" 2>nul || (
    echo ❌ Some dependencies missing. Installing...
    pip install --upgrade pip
    pip install -r requirements.txt
)

echo.
echo 🚀 Typography Agent Development Environment Ready!
echo.
echo Available commands:
echo   • Start MCP Bridge Server: cd mcp_bridge_server ^&^& python server.py
echo   • Run example script: python examples/basic_usage.py
echo   • Run tests: pytest
echo   • Format code: black src/
echo   • Check linting: flake8 src/
echo.
echo 💡 Remember to install the CEP extension in Illustrator!
echo 📖 See setup_guide.md for complete installation instructions
echo.
echo Virtual environment activated. Happy coding! 🎯
