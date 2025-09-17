# Typography Agent Setup Guide

Complete setup guide for integrating the Typography Agent with Adobe Illustrator using CEP (Common Extensibility Platform) and MCP (Model Context Protocol) servers.

## 🎯 Overview

This guide will help you set up a complete Typography Agent system that integrates with Adobe Illustrator, based on the successful implementations from your colleague's repositories:

- [kg_mcp](https://github.com/heetp_adobe/kg_mcp) - Knowledge Graph MCP integration
- [agentic_retype](https://github.com/heetp_adobe/agentic_retype) - Agentic typography automation
- [typographyAgentMCP](https://github.com/heetp_adobe/typographyAgentMCP) - Core MCP server implementation
- [typographyAgentCEP](https://github.com/heetp_adobe/typographyAgentCEP) - CEP extension implementation
- [typographyChatAgent](https://github.com/heetp_adobe/typographyChatAgent) - Chat interface integration

## 📋 Prerequisites

### Software Requirements
- **Adobe Illustrator CC 2019 or later**
- **Python 3.9+**
- **Node.js 16+** (for CEP development)
- **Git** (for repository management)

### Development Tools
- **Visual Studio Code** (recommended IDE)
- **Adobe CEP SDK** (for extension development)
- **ExtendScript Toolkit** (for debugging, optional)

## 🚀 Installation Steps

### Step 1: Clone and Setup Project

```bash
# Clone from Adobe Corporate GitHub
git clone https://git.corp.adobe.com/YOUR_USERNAME/typography-agent-illustrator.git
cd typography-agent-illustrator

# If working with existing local files (current setup)
# You're already in the project directory, so just install dependencies

# Install Python dependencies
pip install -r requirements.txt

# Install additional dependencies for MCP bridge
pip install fastapi uvicorn websockets
```

### Step 2: CEP Extension Setup

Following the [CEP 12 HTML Extension Cookbook](https://github.com/Adobe-CEP/CEP-Resources/blob/master/CEP_12.x/Documentation/CEP%2012%20HTML%20Extension%20Cookbook.md#debugging-unsigned-extensions):

#### 2.1 Enable Extension Development Mode

**macOS:**
```bash
# Enable unsigned extensions for development
defaults write com.adobe.CSXS.12 PlayerDebugMode 1
defaults write com.adobe.CSXS.11 PlayerDebugMode 1
defaults write com.adobe.CSXS.10 PlayerDebugMode 1

# Set log level for debugging
defaults write com.adobe.CSXS.12 LogLevel 6
```

**Windows:**
```cmd
# Run as Administrator
REG ADD "HKEY_CURRENT_USER\Software\Adobe\CSXS.12" /v PlayerDebugMode /t REG_SZ /d 1
REG ADD "HKEY_CURRENT_USER\Software\Adobe\CSXS.12" /v LogLevel /t REG_SZ /d 6
```

#### 2.2 Install CEP Extension

```bash
# Create symbolic link to CEP extensions directory

# macOS:
ln -s "$(pwd)/cep_extension" ~/Library/Application\ Support/Adobe/CEP/extensions/TypographyAgent

# Windows:
mklink /D "%APPDATA%\Adobe\CEP\extensions\TypographyAgent" "%CD%\cep_extension"
```

### Step 3: MCP Bridge Server Setup

#### 3.1 Configure Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# MCP Bridge Server Configuration
MCP_BRIDGE_HOST=127.0.0.1
MCP_BRIDGE_PORT=3000

# Typography Agent Configuration
TYPOGRAPHY_AGENT_MODE=guide
AUTO_ANALYSIS_ENABLED=true

# Logging
LOG_LEVEL=INFO
```

#### 3.2 Start MCP Bridge Server

```bash
# Navigate to bridge server directory
cd mcp_bridge_server

# Start the bridge server
python server.py
```

The server will start on `http://127.0.0.1:3000` and provide the HTTP API bridge between your CEP extension and MCP servers.

### Step 4: Adobe Illustrator Integration

#### 4.1 Restart Adobe Illustrator

After installing the CEP extension, restart Adobe Illustrator to load the new extension.

#### 4.2 Enable Typography Agent Panel

1. Open Adobe Illustrator
2. Go to **Window → Extensions → Typography Agent**
3. The Typography Agent panel should appear

#### 4.3 Test Connection

1. In the Typography Agent panel, check the connection status indicator
2. It should show "Connected to MCP servers" if everything is set up correctly
3. Try asking a simple question like "What are good font pairings for a logo?"

## 🔧 Configuration

### CEP Extension Configuration

Edit `cep_extension/js/main.js` to customize:

```javascript
// Default MCP server URL
const DEFAULT_MCP_URL = 'http://localhost:3000';

// Auto-analysis settings
const AUTO_ANALYSIS_ENABLED = true;

// Default agent mode
const DEFAULT_MODE = 'guide'; // 'critic', 'guide', or 'helper'
```

### MCP Server Configuration

Edit `mcp_bridge_server/server.py` to customize server behavior:

```python
# Server configuration
HOST = "127.0.0.1"
PORT = 3000

# CORS settings for CEP
CORS_ORIGINS = ["*"]  # Restrict in production

# Typography analysis settings
READABILITY_THRESHOLD = 0.7
HIERARCHY_STRICTNESS = "medium"
```

## 🧪 Testing Your Setup

### Test 1: Basic Functionality

1. Create a new document in Illustrator
2. Add some text elements with different fonts and sizes
3. Select the text elements
4. In Typography Agent panel, click "Analyze Selection"
5. You should see analysis results and suggestions

### Test 2: Chat Interface

1. In the Typography Agent panel, type: "How can I improve the readability of this text?"
2. The agent should respond with specific recommendations
3. Try switching between Critic, Guide, and Helper modes

### Test 3: Quick Actions

1. Select text elements in your document
2. Try the quick action buttons:
   - **Fix Kerning**: Should apply professional kerning
   - **Adjust Hierarchy**: Should improve visual hierarchy
   - **Check Readability**: Should provide readability assessment

## 🐛 Troubleshooting

### Common Issues

#### CEP Extension Not Loading

**Problem**: Extension doesn't appear in Illustrator
**Solutions**:
1. Verify PlayerDebugMode is enabled
2. Check extension path and permissions
3. Restart Illustrator completely
4. Check CEP logs: `~/Library/Logs/CSXS/CEP12.log` (macOS)

#### MCP Connection Failed

**Problem**: "Connection failed" status in panel
**Solutions**:
1. Verify MCP bridge server is running on port 3000
2. Check firewall settings
3. Verify API keys in `.env` file
4. Check server logs for error messages

#### ExtendScript Errors

**Problem**: Illustrator automation fails
**Solutions**:
1. Check ExtendScript syntax in `jsx/hostscript.jsx`
2. Verify Illustrator security settings allow script execution
3. Test ExtendScript functions independently

### Debug Mode

Enable detailed logging:

```bash
# Set environment variable
export DEBUG=typography-agent:*

# Start bridge server with debug logging
python server.py --debug
```

### Log Locations

- **CEP Logs**: `~/Library/Logs/CSXS/` (macOS), `%APPDATA%\Adobe\CEP\logs\` (Windows)
- **Bridge Server Logs**: Console output where server is running
- **ExtendScript Logs**: Illustrator ExtendScript Toolkit console

## 🔄 Development Workflow

### Making Changes

1. **CEP Extension Changes**: Edit files in `cep_extension/`, then reload extension in Illustrator
2. **MCP Server Changes**: Restart the bridge server after changes
3. **ExtendScript Changes**: Restart Illustrator after modifying `.jsx` files

### Hot Reload

For faster development:

```bash
# Use nodemon for auto-restart (install with npm install -g nodemon)
nodemon mcp_bridge_server/server.py

# Or use uvicorn's reload feature
uvicorn mcp_bridge_server.server:app --reload --host 127.0.0.1 --port 3000
```

## 🚀 Advanced Configuration

### Custom Typography Rules

Add custom typography analysis rules in `src/mcp_servers/typography_analysis_server.py`:

```python
# Custom readability rules
CUSTOM_READABILITY_RULES = {
    "brand_fonts": ["Helvetica", "Times New Roman"],
    "min_contrast_ratio": 7.0,  # Higher than WCAG AA
    "optimal_line_length": 55,  # Shorter for better readability
}
```

### Brand-Specific Guidelines

Implement brand-specific typography guidelines:

```python
# Brand guidelines integration
BRAND_GUIDELINES = {
    "corporate": {
        "primary_font": "Helvetica Neue",
        "secondary_font": "Times New Roman", 
        "heading_sizes": [24, 18, 16, 14],
        "body_size": 12,
        "line_height": 1.4
    }
}
```

### Integration with Existing Repositories

To integrate insights from your colleague's repositories:

1. **Study the kg_mcp implementation** for knowledge graph integration patterns
2. **Review agentic_retype** for automation workflows
3. **Examine typographyAgentMCP** for MCP server architecture
4. **Analyze typographyAgentCEP** for CEP extension best practices
5. **Learn from typographyChatAgent** for chat interface implementation

## 📚 Additional Resources

- [Adobe CEP Documentation](https://adobe-cep.github.io/CEP-Resources/)
- [ExtendScript Toolkit Documentation](https://extendscript.docsforadobe.dev/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Typography Best Practices](https://practicaltypography.com/)

## 🤝 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review logs for error messages
3. Consult your colleague's repositories for implementation examples
4. Create issues in your project repository with detailed error information

---

**Success!** Your Typography Agent should now be fully integrated with Adobe Illustrator, providing intelligent typography assistance through the CEP extension interface.
