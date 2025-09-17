"""
Typography Analysis MCP Server
Provides advanced typography analysis capabilities including font pairing, 
readability assessment, and hierarchy evaluation.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
import math
import re

class TypographyAnalyzer:
    """Core typography analysis engine"""
    
    def __init__(self):
        self.font_compatibility_matrix = self._load_font_compatibility()
        self.readability_rules = self._load_readability_rules()
        self.hierarchy_principles = self._load_hierarchy_principles()
    
    def _load_font_compatibility(self) -> Dict:
        """Load font pairing compatibility matrix"""
        return {
            "serif": {
                "compatible": ["sans-serif", "script", "monospace"],
                "avoid": ["decorative"],
                "best_pairs": ["Helvetica", "Arial", "Futura"]
            },
            "sans-serif": {
                "compatible": ["serif", "monospace", "script"],
                "avoid": ["decorative"],
                "best_pairs": ["Times New Roman", "Georgia", "Minion Pro"]
            },
            "script": {
                "compatible": ["serif", "sans-serif"],
                "avoid": ["script", "decorative"],
                "best_pairs": ["Times New Roman", "Helvetica"]
            },
            "monospace": {
                "compatible": ["serif", "sans-serif"],
                "avoid": ["script", "decorative"],
                "best_pairs": ["Helvetica", "Times New Roman"]
            }
        }
    
    def _load_readability_rules(self) -> Dict:
        """Load readability assessment rules"""
        return {
            "line_length": {"min": 45, "max": 75, "optimal": 60},
            "line_height": {"min": 1.2, "max": 1.8, "optimal": 1.4},
            "font_size": {
                "body_min": 9, "body_max": 14, "body_optimal": 11,
                "heading_min": 14, "heading_max": 72
            },
            "contrast_ratio": {"min": 4.5, "optimal": 7.0},
            "character_spacing": {"min": -0.05, "max": 0.2, "optimal": 0.0}
        }
    
    def _load_hierarchy_principles(self) -> Dict:
        """Load visual hierarchy principles"""
        return {
            "size_ratios": [1, 1.125, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 3],
            "weight_progression": ["light", "regular", "medium", "semibold", "bold"],
            "spacing_multipliers": {"tight": 0.8, "normal": 1.0, "loose": 1.2}
        }
    
    def analyze_font_pairing(self, fonts: List[Dict]) -> Dict:
        """Analyze font pairing compatibility"""
        if len(fonts) < 2:
            return {"score": 1.0, "feedback": "Single font detected", "suggestions": []}
        
        primary_font = fonts[0]
        secondary_fonts = fonts[1:]
        
        compatibility_score = 0.0
        feedback = []
        suggestions = []
        
        primary_category = self._categorize_font(primary_font.get("family", ""))
        
        for secondary_font in secondary_fonts:
            secondary_category = self._categorize_font(secondary_font.get("family", ""))
            
            # Check compatibility
            if secondary_category in self.font_compatibility_matrix[primary_category]["compatible"]:
                compatibility_score += 0.8
                feedback.append(f"Good pairing: {primary_font.get('family')} with {secondary_font.get('family')}")
            elif secondary_category in self.font_compatibility_matrix[primary_category]["avoid"]:
                compatibility_score += 0.2
                feedback.append(f"Potentially problematic pairing: {primary_font.get('family')} with {secondary_font.get('family')}")
                suggestions.append(f"Consider replacing {secondary_font.get('family')} with a {primary_category}-compatible font")
            else:
                compatibility_score += 0.5
                feedback.append(f"Neutral pairing: {primary_font.get('family')} with {secondary_font.get('family')}")
        
        compatibility_score = min(1.0, compatibility_score / len(secondary_fonts))
        
        return {
            "score": compatibility_score,
            "feedback": feedback,
            "suggestions": suggestions,
            "primary_category": primary_category,
            "recommended_pairs": self.font_compatibility_matrix[primary_category]["best_pairs"]
        }
    
    def assess_readability(self, text_elements: List[Dict]) -> Dict:
        """Assess text readability based on typography rules"""
        total_score = 0.0
        feedback = []
        suggestions = []
        element_count = len(text_elements)
        
        for element in text_elements:
            element_score = 0.0
            element_feedback = []
            
            # Check font size
            font_size = element.get("fontSize", 12)
            if self.readability_rules["font_size"]["body_min"] <= font_size <= self.readability_rules["font_size"]["body_max"]:
                element_score += 0.25
            else:
                element_feedback.append(f"Font size {font_size}pt may impact readability")
                if font_size < self.readability_rules["font_size"]["body_min"]:
                    suggestions.append(f"Increase font size to at least {self.readability_rules['font_size']['body_min']}pt")
                else:
                    suggestions.append(f"Consider reducing font size to {self.readability_rules['font_size']['body_optimal']}pt for body text")
            
            # Check line height
            line_height = element.get("lineHeight", 1.2)
            if self.readability_rules["line_height"]["min"] <= line_height <= self.readability_rules["line_height"]["max"]:
                element_score += 0.25
            else:
                element_feedback.append(f"Line height {line_height} is outside optimal range")
                suggestions.append(f"Adjust line height to {self.readability_rules['line_height']['optimal']}")
            
            # Check character spacing
            char_spacing = element.get("characterSpacing", 0.0)
            if self.readability_rules["character_spacing"]["min"] <= char_spacing <= self.readability_rules["character_spacing"]["max"]:
                element_score += 0.25
            else:
                element_feedback.append(f"Character spacing {char_spacing} may affect readability")
                suggestions.append("Adjust character spacing to improve text flow")
            
            # Check line length (if available)
            line_length = element.get("lineLength", 60)
            if self.readability_rules["line_length"]["min"] <= line_length <= self.readability_rules["line_length"]["max"]:
                element_score += 0.25
            else:
                element_feedback.append(f"Line length {line_length} characters is outside optimal range")
                suggestions.append(f"Aim for {self.readability_rules['line_length']['optimal']} characters per line")
            
            total_score += element_score
            feedback.extend(element_feedback)
        
        average_score = total_score / element_count if element_count > 0 else 0.0
        
        return {
            "score": average_score,
            "feedback": feedback,
            "suggestions": list(set(suggestions)),  # Remove duplicates
            "elements_analyzed": element_count
        }
    
    def evaluate_hierarchy(self, text_elements: List[Dict]) -> Dict:
        """Evaluate visual hierarchy effectiveness"""
        if len(text_elements) < 2:
            return {"score": 0.5, "feedback": ["Insufficient elements for hierarchy analysis"], "suggestions": []}
        
        # Sort elements by font size (assuming larger = more important)
        sorted_elements = sorted(text_elements, key=lambda x: x.get("fontSize", 12), reverse=True)
        
        hierarchy_score = 0.0
        feedback = []
        suggestions = []
        
        # Check size progression
        size_ratios = []
        for i in range(len(sorted_elements) - 1):
            current_size = sorted_elements[i].get("fontSize", 12)
            next_size = sorted_elements[i + 1].get("fontSize", 12)
            ratio = current_size / next_size if next_size > 0 else 1.0
            size_ratios.append(ratio)
        
        # Evaluate size ratios
        good_ratios = [r for r in size_ratios if r in self.hierarchy_principles["size_ratios"] or 1.1 <= r <= 3.0]
        if len(good_ratios) == len(size_ratios):
            hierarchy_score += 0.4
            feedback.append("Font size hierarchy is well-established")
        else:
            feedback.append("Font size hierarchy could be improved")
            suggestions.append("Use consistent size ratios (1.25x, 1.5x, 2x) between hierarchy levels")
        
        # Check weight variation
        weights = [element.get("fontWeight", "regular") for element in text_elements]
        unique_weights = set(weights)
        if len(unique_weights) > 1:
            hierarchy_score += 0.3
            feedback.append("Font weight variation supports hierarchy")
        else:
            feedback.append("Consider using different font weights to enhance hierarchy")
            suggestions.append("Add weight variation (regular, medium, bold) to create clear hierarchy")
        
        # Check color/contrast variation
        colors = [element.get("color", "#000000") for element in text_elements]
        unique_colors = set(colors)
        if len(unique_colors) > 1:
            hierarchy_score += 0.3
            feedback.append("Color variation enhances hierarchy")
        else:
            feedback.append("Color variation could strengthen hierarchy")
            suggestions.append("Consider using different shades or colors for hierarchy levels")
        
        return {
            "score": hierarchy_score,
            "feedback": feedback,
            "suggestions": suggestions,
            "size_ratios": size_ratios,
            "hierarchy_levels": len(set(element.get("fontSize", 12) for element in text_elements))
        }
    
    def _categorize_font(self, font_family: str) -> str:
        """Categorize font into basic categories"""
        font_family_lower = font_family.lower()
        
        # Common serif fonts
        serif_fonts = ["times", "georgia", "minion", "garamond", "baskerville", "caslon"]
        if any(serif in font_family_lower for serif in serif_fonts):
            return "serif"
        
        # Common sans-serif fonts
        sans_serif_fonts = ["helvetica", "arial", "futura", "avenir", "proxima", "gotham"]
        if any(sans in font_family_lower for sans in sans_serif_fonts):
            return "sans-serif"
        
        # Script/handwriting fonts
        script_fonts = ["script", "brush", "handwriting", "calligraphy"]
        if any(script in font_family_lower for script in script_fonts):
            return "script"
        
        # Monospace fonts
        mono_fonts = ["courier", "monaco", "consolas", "menlo", "monospace"]
        if any(mono in font_family_lower for mono in mono_fonts):
            return "monospace"
        
        # Default to sans-serif for unknown fonts
        return "sans-serif"

# Initialize MCP Server
server = Server("typography-analysis")
analyzer = TypographyAnalyzer()

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available typography analysis tools"""
    return [
        Tool(
            name="analyze_elements",
            description="Analyze typography elements for font pairing, readability, and hierarchy",
            inputSchema={
                "type": "object",
                "properties": {
                    "elements": {
                        "type": "array",
                        "description": "Typography elements to analyze",
                        "items": {
                            "type": "object",
                            "properties": {
                                "family": {"type": "string"},
                                "fontSize": {"type": "number"},
                                "fontWeight": {"type": "string"},
                                "lineHeight": {"type": "number"},
                                "characterSpacing": {"type": "number"},
                                "color": {"type": "string"},
                                "text": {"type": "string"},
                                "lineLength": {"type": "number"}
                            }
                        }
                    },
                    "context": {
                        "type": "object",
                        "description": "Project context for analysis"
                    },
                    "mode": {
                        "type": "string",
                        "description": "Agent mode (critic, guide, helper)"
                    }
                },
                "required": ["elements"]
            }
        ),
        Tool(
            name="font_pairing_analysis",
            description="Analyze font pairing compatibility",
            inputSchema={
                "type": "object",
                "properties": {
                    "fonts": {
                        "type": "array",
                        "description": "Fonts to analyze for pairing",
                        "items": {
                            "type": "object",
                            "properties": {
                                "family": {"type": "string"},
                                "category": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["fonts"]
            }
        ),
        Tool(
            name="readability_assessment",
            description="Assess text readability based on typography principles",
            inputSchema={
                "type": "object",
                "properties": {
                    "text_elements": {
                        "type": "array",
                        "description": "Text elements to assess for readability"
                    }
                },
                "required": ["text_elements"]
            }
        ),
        Tool(
            name="hierarchy_evaluation",
            description="Evaluate visual hierarchy effectiveness",
            inputSchema={
                "type": "object",
                "properties": {
                    "text_elements": {
                        "type": "array",
                        "description": "Text elements to evaluate for hierarchy"
                    }
                },
                "required": ["text_elements"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for typography analysis"""
    
    if name == "analyze_elements":
        elements = arguments.get("elements", [])
        context = arguments.get("context", {})
        mode = arguments.get("mode", "guide")
        
        # Perform comprehensive analysis
        font_analysis = analyzer.analyze_font_pairing(elements)
        readability_analysis = analyzer.assess_readability(elements)
        hierarchy_analysis = analyzer.evaluate_hierarchy(elements)
        
        # Combine results
        results = []
        
        # Font pairing feedback
        if font_analysis["score"] < 0.7:
            results.append({
                "task_type": "consistency",
                "severity": "warning" if font_analysis["score"] < 0.5 else "info",
                "message": "Font pairing needs attention",
                "suggestions": font_analysis["suggestions"],
                "auto_fix_available": True,
                "confidence_score": font_analysis["score"],
                "typography_principle": "Effective font pairing creates harmony while maintaining distinction between text elements."
            })
        
        # Readability feedback
        if readability_analysis["score"] < 0.7:
            results.append({
                "task_type": "readability",
                "severity": "warning" if readability_analysis["score"] < 0.5 else "info",
                "message": "Readability could be improved",
                "suggestions": readability_analysis["suggestions"],
                "auto_fix_available": True,
                "confidence_score": readability_analysis["score"],
                "typography_principle": "Optimal readability ensures your message reaches the audience effectively."
            })
        
        # Hierarchy feedback
        if hierarchy_analysis["score"] < 0.7:
            results.append({
                "task_type": "hierarchy",
                "severity": "info",
                "message": "Visual hierarchy can be strengthened",
                "suggestions": hierarchy_analysis["suggestions"],
                "auto_fix_available": False,
                "confidence_score": hierarchy_analysis["score"],
                "typography_principle": "Clear hierarchy guides readers through content in order of importance."
            })
        
        return [TextContent(type="text", text=json.dumps(results, indent=2))]
    
    elif name == "font_pairing_analysis":
        fonts = arguments.get("fonts", [])
        result = analyzer.analyze_font_pairing(fonts)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "readability_assessment":
        text_elements = arguments.get("text_elements", [])
        result = analyzer.assess_readability(text_elements)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "hierarchy_evaluation":
        text_elements = arguments.get("text_elements", [])
        result = analyzer.evaluate_hierarchy(text_elements)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the typography analysis MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="typography-analysis",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
