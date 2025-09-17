"""
Typography Agent - Basic Usage Example
Demonstrates the core functionality of the Typography Agent for Adobe Illustrator.
"""

import asyncio
import json
from typing import List, Dict
from src.typography_agent import (
    TypographyAgent, 
    TypographyContext, 
    AgentMode,
    TypographyTask
)

async def demonstrate_typography_analysis():
    """Demonstrate typography analysis capabilities"""
    print("🔍 Typography Analysis Demo")
    print("=" * 50)
    
    # Sample typography elements (as they would come from Illustrator)
    sample_elements = [
        {
            "family": "Helvetica",
            "fontSize": 24,
            "fontWeight": "bold",
            "lineHeight": 1.2,
            "characterSpacing": 0.0,
            "color": "#000000",
            "text": "Main Heading",
            "lineLength": 45
        },
        {
            "family": "Times New Roman", 
            "fontSize": 12,
            "fontWeight": "regular",
            "lineHeight": 1.4,
            "characterSpacing": 0.02,
            "color": "#333333",
            "text": "Body text content that provides detailed information about the topic.",
            "lineLength": 65
        },
        {
            "family": "Helvetica",
            "fontSize": 14,
            "fontWeight": "medium", 
            "lineHeight": 1.3,
            "characterSpacing": 0.01,
            "color": "#666666",
            "text": "Subheading",
            "lineLength": 35
        }
    ]
    
    # Initialize agent (mock mode - without actual MCP servers)
    agent = TypographyAgent()
    
    # Set up project context
    context = TypographyContext(
        project_name="Corporate Brochure Design",
        document_specs={"width": 8.5, "height": 11, "units": "inches"},
        brand_guidelines={
            "primary_font": "Helvetica",
            "secondary_font": "Times New Roman",
            "brand_colors": ["#000000", "#333333", "#666666"]
        },
        target_audience="Business professionals",
        medium="print",
        current_artboard="Page 1",
        selected_elements=sample_elements
    )
    
    agent.update_context(context)
    
    # Demonstrate different agent modes
    modes = [AgentMode.GUIDE, AgentMode.CRITIC, AgentMode.HELPER]
    
    for mode in modes:
        agent.set_mode(mode)
        print(f"\n📝 {mode.value.upper()} MODE")
        print("-" * 30)
        
        # Simulate typography analysis (without actual MCP server)
        mock_analysis_results = await simulate_typography_analysis(sample_elements, mode)
        
        for result in mock_analysis_results:
            print(f"Task: {result['task_type']}")
            print(f"Severity: {result['severity']}")
            print(f"Message: {result['message']}")
            if result['suggestions']:
                print("Suggestions:")
                for suggestion in result['suggestions']:
                    print(f"  • {suggestion}")
            print(f"Confidence: {result['confidence_score']:.1%}")
            print()

async def simulate_typography_analysis(elements: List[Dict], mode: AgentMode) -> List[Dict]:
    """Simulate typography analysis results"""
    results = []
    
    # Font pairing analysis
    fonts_used = list(set(element["family"] for element in elements))
    if len(fonts_used) > 1:
        if mode == AgentMode.CRITIC:
            message = "Font pairing shows potential issues. Helvetica and Times New Roman create strong contrast but may lack cohesion in formal contexts."
        elif mode == AgentMode.GUIDE:
            message = "You're using a classic sans-serif + serif combination. This creates good contrast for hierarchy, following the principle that contrasting fonts should be distinctly different."
        else:  # HELPER
            message = "Font pairing detected. I can help optimize the combination or suggest alternatives that maintain your design intent."
        
        results.append({
            "task_type": "consistency",
            "severity": "info",
            "message": message,
            "suggestions": [
                "Consider using Helvetica Light for body text instead of Times New Roman",
                "Ensure sufficient size contrast between fonts",
                "Test readability at final print size"
            ],
            "auto_fix_available": True,
            "confidence_score": 0.8
        })
    
    # Readability analysis
    body_elements = [e for e in elements if e["fontSize"] < 18]
    if body_elements:
        avg_line_length = sum(e.get("lineLength", 60) for e in body_elements) / len(body_elements)
        
        if avg_line_length > 75:
            if mode == AgentMode.CRITIC:
                message = "Line length exceeds optimal reading comfort. This will strain readers and reduce comprehension."
            elif mode == AgentMode.GUIDE:
                message = "Line length is a crucial readability factor. The optimal range is 45-75 characters per line, with 60 being ideal for most contexts."
            else:  # HELPER
                message = "Line length needs adjustment. I can automatically resize text boxes to optimize reading comfort."
            
            results.append({
                "task_type": "readability",
                "severity": "warning",
                "message": message,
                "suggestions": [
                    f"Reduce line length from {avg_line_length:.0f} to 60-65 characters",
                    "Increase line height to 1.4-1.6 for longer lines",
                    "Consider multi-column layout for long text blocks"
                ],
                "auto_fix_available": True,
                "confidence_score": 0.9
            })
    
    # Hierarchy analysis
    font_sizes = [e["fontSize"] for e in elements]
    font_sizes.sort(reverse=True)
    
    if len(font_sizes) > 1:
        ratios = [font_sizes[i] / font_sizes[i+1] for i in range(len(font_sizes)-1)]
        poor_ratios = [r for r in ratios if r < 1.15 or r > 3.0]
        
        if poor_ratios:
            if mode == AgentMode.CRITIC:
                message = "Visual hierarchy lacks clarity. Size relationships between elements don't follow typographic scale principles."
            elif mode == AgentMode.GUIDE:
                message = "Effective hierarchy uses consistent scale ratios. Common ratios include 1.25 (major third), 1.5 (perfect fifth), or 1.618 (golden ratio)."
            else:  # HELPER
                message = "Hierarchy can be improved with better size relationships. I can apply a consistent typographic scale."
            
            results.append({
                "task_type": "hierarchy",
                "severity": "info",
                "message": message,
                "suggestions": [
                    "Use consistent scale ratios (1.25x, 1.5x, 2x)",
                    "Ensure minimum 1.2x difference between hierarchy levels",
                    "Consider weight and color for additional hierarchy cues"
                ],
                "auto_fix_available": False,
                "confidence_score": 0.75
            })
    
    return results

async def demonstrate_illustrator_automation():
    """Demonstrate Illustrator automation capabilities"""
    print("\n🤖 Illustrator Automation Demo")
    print("=" * 50)
    
    # Sample automation tasks
    automation_tasks = [
        {
            "name": "Text Box Auto-Adjustment",
            "description": "Automatically resize and position text boxes for optimal layout",
            "script_type": "adjust_text_boxes",
            "parameters": {
                "adjustments": [
                    {"width": 300, "height": 100, "autoFit": True},
                    {"width": 250, "height": 150, "autoFit": True}
                ]
            }
        },
        {
            "name": "Advanced Kerning",
            "description": "Apply professional kerning to improve text appearance",
            "script_type": "apply_kerning",
            "parameters": {
                "optical_kerning": True,
                "kerning_pairs": [
                    {"characters": "AV", "adjustment": -50},
                    {"characters": "To", "adjustment": -30},
                    {"characters": "We", "adjustment": -20}
                ]
            }
        },
        {
            "name": "Batch Text Formatting",
            "description": "Apply consistent formatting across multiple text elements",
            "script_type": "batch_format",
            "parameters": {
                "format_rules": [
                    {
                        "selector": "heading",
                        "fontFamily": "Helvetica Bold",
                        "fontSize": 24,
                        "lineHeight": 1.2,
                        "color": "#000000"
                    },
                    {
                        "selector": "body",
                        "fontFamily": "Helvetica",
                        "fontSize": 12,
                        "lineHeight": 1.4,
                        "color": "#333333"
                    }
                ]
            }
        }
    ]
    
    for task in automation_tasks:
        print(f"📋 {task['name']}")
        print(f"   {task['description']}")
        print(f"   Script: {task['script_type']}")
        print(f"   Parameters: {len(task['parameters'])} settings configured")
        print("   Status: ✅ Ready for execution")
        print()

async def demonstrate_recommendations():
    """Demonstrate AI-powered typography recommendations"""
    print("\n💡 AI Recommendations Demo")
    print("=" * 50)
    
    # Sample questions a designer might ask
    typography_questions = [
        "What's the best font pairing for a luxury brand identity?",
        "How do I improve readability in small print sizes?",
        "What kerning adjustments are needed for this logo?",
        "How can I create better visual hierarchy in my poster?",
        "What are the typography best practices for web vs print?"
    ]
    
    # Mock responses for different agent modes
    mock_responses = {
        AgentMode.CRITIC: [
            "Your current pairing lacks the sophistication required for luxury branding. The fonts don't convey premium quality.",
            "Small print readability is compromised by insufficient line height and character spacing. This fails accessibility standards.",
            "Logo kerning shows amateur execution. Professional logos require precise optical adjustments, not default spacing.",
            "Hierarchy is weak and confusing. Readers won't understand the information priority, harming communication effectiveness.",
            "You're applying print typography rules to web design, which creates readability issues on screens."
        ],
        AgentMode.GUIDE: [
            "Luxury brands often use serif fonts like Didot or Bodoni for elegance, paired with clean sans-serifs like Avenir. The contrast creates sophistication while maintaining readability.",
            "For small print, increase line height to 1.4-1.6, use medium font weights instead of light, and ensure 4.5:1 contrast ratio. Consider fonts designed for small sizes like Verdana.",
            "Logo kerning requires optical, not metric spacing. Focus on letter pairs like 'AV', 'To', 'We' which often need tightening. Test at multiple sizes to ensure consistency.",
            "Create hierarchy through size (use 1.5x ratios), weight (regular/bold), and color. Establish clear information order: headline → subhead → body → captions.",
            "Web typography needs different considerations: system fonts for speed, larger sizes for screens (16px minimum), and shorter line lengths (45-65 characters) for mobile."
        ],
        AgentMode.HELPER: [
            "I can analyze your current fonts and suggest luxury alternatives. Would you like me to apply a sophisticated serif + sans-serif combination automatically?",
            "I'll scan your small text and apply optimal settings: increase line height, adjust character spacing, and ensure proper contrast ratios. Ready to proceed?",
            "I can automatically apply professional kerning to your logo. I'll identify problem letter pairs and apply precise adjustments based on optical spacing principles.",
            "Let me restructure your hierarchy with consistent scale ratios. I'll apply size, weight, and spacing adjustments to create clear information flow.",
            "I'll optimize your typography for web: convert to web-safe fonts, adjust sizes for screen reading, and ensure mobile responsiveness. Shall I start?"
        ]
    }
    
    agent = TypographyAgent()
    
    for mode in [AgentMode.GUIDE, AgentMode.CRITIC, AgentMode.HELPER]:
        agent.set_mode(mode)
        print(f"\n🎯 {mode.value.upper()} MODE RESPONSES")
        print("-" * 40)
        
        for i, question in enumerate(typography_questions):
            print(f"Q: {question}")
            print(f"A: {mock_responses[mode][i]}")
            print()

async def main():
    """Run all demonstration examples"""
    print("🎨 Typography Agent for Adobe Illustrator")
    print("=" * 60)
    print("Comprehensive AI assistant for professional typography design")
    print("Serving as your critic, guide, and tedious work helper")
    print()
    
    try:
        await demonstrate_typography_analysis()
        await demonstrate_illustrator_automation()
        await demonstrate_recommendations()
        
        print("\n🎉 Demo Complete!")
        print("=" * 50)
        print("The Typography Agent is ready to:")
        print("• Analyze and critique your typography choices")
        print("• Guide you through typography best practices")  
        print("• Automate tedious typography tasks in Illustrator")
        print("• Provide intelligent recommendations for any typography challenge")
        print()
        print("Next steps:")
        print("1. Install Adobe Illustrator integration")
        print("2. Configure your API keys")
        print("3. Start using the agent in your design workflow")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("This is expected in demo mode without full MCP server setup.")

if __name__ == "__main__":
    asyncio.run(main())
