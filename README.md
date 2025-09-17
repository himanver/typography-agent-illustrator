# Typography Agent for Adobe Illustrator

A comprehensive AI assistant that serves as a **critic, guide, and tedious work helper** for professional creative designers working with typography in Adobe Illustrator.

## 🎯 Vision

Transform typography workflows in Adobe Illustrator by providing:
- **Intelligent Critique**: AI-powered feedback on typography choices
- **Educational Guidance**: Learn typography principles through practical application  
- **Workflow Automation**: Eliminate tedious manual typography tasks

## 🚀 Key Features

### Core Issues Addressed
1. **Manual Text Adjustment**: Automated text box positioning and sizing for multi-page layouts
2. **Advanced Typesetting**: Professional-level control over kerning, hyphenation, optical margin alignment
3. **Special Characters**: Intelligent handling of ligatures, dash types, and typography symbols
4. **Workflow Efficiency**: Reducing tedious manual tasks through intelligent automation

### Agent Capabilities

#### 🎨 Typography Analysis
- **Font Pairing Analysis**: Evaluates font combinations for harmony and contrast
- **Readability Assessment**: Measures text legibility across different contexts
- **Hierarchy Evaluation**: Analyzes visual hierarchy and information flow
- **Brand Consistency Check**: Ensures alignment with brand guidelines

#### 🔧 Illustrator Integration
- **CEP Panel Integration**: Native Illustrator panel for seamless workflow
- **ExtendScript Automation**: Direct manipulation of Illustrator objects
- **Batch Processing**: Multi-document and multi-artboard operations
- **Template Management**: Smart template creation and application

#### ⚡ Professional Typesetting
- **Advanced Kerning**: Optical and metric kerning optimization
- **Hyphenation Engine**: Intelligent word breaking and flow control
- **Margin Alignment**: Optical margin alignment for professional polish
- **Special Character Management**: Ligature, dash, and symbol optimization

## 🏗️ Architecture

### Multi-Modal LLM Core
- **Role-Based Responses**: Critic, Guide, and Helper modes
- **Visual Analysis**: Understanding of typography layouts and design principles
- **Context Awareness**: Project-specific recommendations

### MCP Server Components
1. **Typography Analysis Server**: Font analysis, readability, hierarchy evaluation
2. **Illustrator Integration Server**: Direct Adobe Illustrator API integration
3. **Professional Typesetting Server**: Advanced typography algorithms
4. **Design Workflow Server**: Project management and collaboration tools

## 🛠️ Installation

### Prerequisites
- Adobe Illustrator CC 2019 or later
- Python 3.9+
- Node.js 16+ (for CEP panel development)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/typography-agent-illustrator.git
   cd typography-agent-illustrator
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (Anthropic, OpenAI, etc.)
   ```

4. **Install Adobe CEP Extension**
   ```bash
   # Copy CEP extension to Illustrator extensions folder
   # macOS: ~/Library/Application Support/Adobe/CEP/extensions/
   # Windows: C:\Users\[username]\AppData\Roaming\Adobe\CEP\extensions\
   ```

## 🚦 Quick Start

### Basic Usage

```python
import asyncio
from src.typography_agent import TypographyAgent, TypographyContext, AgentMode

async def main():
    # Initialize the agent
    agent = TypographyAgent()
    await agent.initialize_mcp_servers()
    
    # Set up project context
    context = TypographyContext(
        project_name="Brand Identity Design",
        document_specs={"width": 8.5, "height": 11, "units": "inches"},
        brand_guidelines=None,
        target_audience="Professional designers",
        medium="print",
        current_artboard="Main Layout",
        selected_elements=[]
    )
    
    agent.update_context(context)
    
    # Use as a Guide
    agent.set_mode(AgentMode.GUIDE)
    recommendation = await agent.get_typography_recommendations(
        "What are the best practices for kerning in logo design?"
    )
    print(recommendation)
    
    # Use as a Critic
    agent.set_mode(AgentMode.CRITIC)
    # ... analyze current typography
    
    # Use as a Helper
    agent.set_mode(AgentMode.HELPER)
    # ... apply automated fixes

if __name__ == "__main__":
    asyncio.run(main())
```

### Adobe Illustrator Integration

The agent integrates directly with Illustrator through:

1. **CEP Panel**: Native user interface within Illustrator
2. **ExtendScript**: Automated text manipulation and formatting
3. **Batch Operations**: Process multiple documents simultaneously

## 📚 Usage Examples

### Automated Text Box Adjustment
```python
# Fix the most common Illustrator typography pain point
await agent.batch_process_documents(
    document_paths=["design1.ai", "design2.ai"],
    operations=["adjust_text_boxes", "apply_optical_kerning"]
)
```

### Professional Typography Critique
```python
agent.set_mode(AgentMode.CRITIC)
feedback = await agent.analyze_typography(selected_elements)
for item in feedback:
    print(f"{item.severity}: {item.message}")
    if item.auto_fix_available:
        await agent.auto_fix_typography(item)
```

### Educational Typography Guidance
```python
agent.set_mode(AgentMode.GUIDE)
guidance = await agent.get_typography_recommendations(
    "How do I create better visual hierarchy in this poster design?"
)
```

## 🔧 Configuration

### Agent Modes
- **CRITIC**: Provides constructive, professional criticism
- **GUIDE**: Educational mentor with typography principles
- **HELPER**: Practical solutions and automation focus

### MCP Server Configuration
Each MCP server can be configured independently:

```python
# Typography Analysis Server
servers_config = {
    "typography_analysis": {
        "readability_threshold": 0.7,
        "hierarchy_strictness": "medium",
        "font_database": "extended"
    }
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black src/
flake8 src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Adobe for the Creative SDK and CEP framework
- Typography experts and design community for best practices
- Open source typography tools and libraries

## 🗺️ Roadmap

### Version 1.0 (Current)
- [x] Core agent architecture
- [x] Typography analysis engine
- [x] Basic Illustrator integration
- [ ] CEP panel development
- [ ] Advanced kerning algorithms

### Version 2.0 (Planned)
- [ ] Machine learning personalization
- [ ] Cross-platform support (InDesign, Photoshop)
- [ ] Advanced collaboration features
- [ ] Typography performance analytics

### Future Enhancements
- [ ] Web-based typography tools
- [ ] Mobile companion app
- [ ] Integration with design systems
- [ ] API ecosystem for third-party tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/typography-agent-illustrator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/typography-agent-illustrator/discussions)
- **Email**: support@typography-agent.com

---

**Typography Agent** - Elevating design through intelligent typography assistance.
