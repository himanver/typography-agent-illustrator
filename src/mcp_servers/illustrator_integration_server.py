"""
Adobe Illustrator Integration MCP Server
Provides direct integration with Adobe Illustrator through CEP and ExtendScript.
Handles automated text adjustments, batch processing, and Illustrator API calls.
"""

import asyncio
import json
import subprocess
import tempfile
import os
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent

class IllustratorIntegration:
    """Core Illustrator integration engine"""
    
    def __init__(self):
        self.extendscript_path = self._find_extendscript_toolkit()
        self.temp_script_dir = tempfile.mkdtemp(prefix="typography_agent_")
        
    def _find_extendscript_toolkit(self) -> Optional[str]:
        """Find ExtendScript Toolkit installation"""
        possible_paths = [
            "/Applications/Adobe ExtendScript Toolkit CC/ExtendScript Toolkit.app/Contents/MacOS/ExtendScript Toolkit",
            "/Applications/Utilities/Adobe Utilities-CS6.localized/ExtendScript Toolkit CS6/ExtendScript Toolkit.app/Contents/MacOS/ExtendScript Toolkit",
            "C:\\Program Files (x86)\\Adobe\\Adobe Utilities - CS6\\ExtendScript Toolkit CS6\\ExtendScript Toolkit.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def generate_extendscript(self, operation: str, parameters: Dict) -> str:
        """Generate ExtendScript code for Illustrator operations"""
        
        if operation == "adjust_text_boxes":
            return self._generate_text_box_adjustment_script(parameters)
        elif operation == "apply_kerning":
            return self._generate_kerning_script(parameters)
        elif operation == "batch_format":
            return self._generate_batch_format_script(parameters)
        elif operation == "create_text_styles":
            return self._generate_text_styles_script(parameters)
        elif operation == "optical_margin_alignment":
            return self._generate_optical_margin_script(parameters)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def _generate_text_box_adjustment_script(self, parameters: Dict) -> str:
        """Generate script for automatic text box adjustment"""
        return f'''
// Typography Agent - Text Box Adjustment Script
#target illustrator

function adjustTextBoxes() {{
    if (app.documents.length === 0) {{
        alert("No document is open.");
        return;
    }}
    
    var doc = app.activeDocument;
    var textFrames = doc.textFrames;
    var adjustments = {json.dumps(parameters.get("adjustments", []))};
    var results = [];
    
    try {{
        for (var i = 0; i < textFrames.length; i++) {{
            var textFrame = textFrames[i];
            var adjustment = adjustments[i] || {{}};
            
            // Store original properties
            var original = {{
                width: textFrame.width,
                height: textFrame.height,
                left: textFrame.left,
                top: textFrame.top
            }};
            
            // Apply adjustments
            if (adjustment.width) {{
                textFrame.width = adjustment.width;
            }}
            if (adjustment.height) {{
                textFrame.height = adjustment.height;
            }}
            if (adjustment.left !== undefined) {{
                textFrame.left = adjustment.left;
            }}
            if (adjustment.top !== undefined) {{
                textFrame.top = adjustment.top;
            }}
            
            // Auto-fit if requested
            if (adjustment.autoFit) {{
                textFrame.textRange.characterAttributes.size = {parameters.get("baseFontSize", 12)};
                // Adjust font size to fit
                var maxIterations = 20;
                var iteration = 0;
                
                while (textFrame.overflowed && iteration < maxIterations) {{
                    textFrame.textRange.characterAttributes.size *= 0.95;
                    iteration++;
                }}
                
                while (!textFrame.overflowed && 
                       textFrame.textRange.characterAttributes.size < {parameters.get("maxFontSize", 72)} &&
                       iteration < maxIterations) {{
                    textFrame.textRange.characterAttributes.size *= 1.05;
                    iteration++;
                    if (textFrame.overflowed) {{
                        textFrame.textRange.characterAttributes.size *= 0.95;
                        break;
                    }}
                }}
            }}
            
            results.push({{
                index: i,
                success: true,
                original: original,
                final: {{
                    width: textFrame.width,
                    height: textFrame.height,
                    left: textFrame.left,
                    top: textFrame.top,
                    fontSize: textFrame.textRange.characterAttributes.size
                }}
            }});
        }}
        
        return JSON.stringify({{
            success: true,
            processed: results.length,
            results: results
        }});
        
    }} catch (error) {{
        return JSON.stringify({{
            success: false,
            error: error.toString()
        }});
    }}
}}

// Execute the function
adjustTextBoxes();
'''
    
    def _generate_kerning_script(self, parameters: Dict) -> str:
        """Generate script for advanced kerning adjustments"""
        return f'''
// Typography Agent - Advanced Kerning Script
#target illustrator

function applyAdvancedKerning() {{
    if (app.documents.length === 0) {{
        alert("No document is open.");
        return;
    }}
    
    var doc = app.activeDocument;
    var selection = doc.selection;
    var kerningAdjustments = {json.dumps(parameters.get("kerning_pairs", []))};
    var results = [];
    
    try {{
        if (selection.length === 0) {{
            // Apply to all text frames if nothing selected
            selection = doc.textFrames;
        }}
        
        for (var i = 0; i < selection.length; i++) {{
            var textFrame = selection[i];
            if (textFrame.typename !== "TextFrame") continue;
            
            var textRange = textFrame.textRange;
            var content = textRange.contents;
            
            // Apply kerning pairs
            for (var j = 0; j < kerningAdjustments.length; j++) {{
                var pair = kerningAdjustments[j];
                var searchPair = pair.characters;
                var kerningValue = pair.adjustment;
                
                // Find and adjust kerning for specific character pairs
                for (var k = 0; k < content.length - 1; k++) {{
                    var currentPair = content.substring(k, k + 2);
                    if (currentPair === searchPair) {{
                        try {{
                            var charRange = textRange.characters[k];
                            charRange.characterAttributes.tracking = kerningValue;
                        }} catch (e) {{
                            // Continue if character adjustment fails
                        }}
                    }}
                }}
            }}
            
            // Apply optical kerning if requested
            if ({str(parameters.get("optical_kerning", "false")).lower()}) {{
                textRange.characterAttributes.autoKernType = AutoKernType.OPTICAL;
            }}
            
            // Apply metric kerning if requested
            if ({str(parameters.get("metric_kerning", "false")).lower()}) {{
                textRange.characterAttributes.autoKernType = AutoKernType.METRICS;
            }}
            
            results.push({{
                index: i,
                success: true,
                kerning_pairs_applied: kerningAdjustments.length
            }});
        }}
        
        return JSON.stringify({{
            success: true,
            processed: results.length,
            results: results
        }});
        
    }} catch (error) {{
        return JSON.stringify({{
            success: false,
            error: error.toString()
        }});
    }}
}}

// Execute the function
applyAdvancedKerning();
'''
    
    def _generate_batch_format_script(self, parameters: Dict) -> str:
        """Generate script for batch text formatting"""
        return f'''
// Typography Agent - Batch Format Script
#target illustrator

function batchFormatText() {{
    if (app.documents.length === 0) {{
        alert("No document is open.");
        return;
    }}
    
    var doc = app.activeDocument;
    var textFrames = doc.textFrames;
    var formatRules = {json.dumps(parameters.get("format_rules", []))};
    var results = [];
    
    try {{
        for (var i = 0; i < textFrames.length; i++) {{
            var textFrame = textFrames[i];
            var textRange = textFrame.textRange;
            var applied_rules = [];
            
            // Apply each formatting rule
            for (var j = 0; j < formatRules.length; j++) {{
                var rule = formatRules[j];
                var shouldApply = false;
                
                // Check if rule applies to this text frame
                if (rule.selector === "all") {{
                    shouldApply = true;
                }} else if (rule.selector === "heading" && textRange.characterAttributes.size > {parameters.get("heading_threshold", 18)}) {{
                    shouldApply = true;
                }} else if (rule.selector === "body" && textRange.characterAttributes.size <= {parameters.get("heading_threshold", 18)}) {{
                    shouldApply = true;
                }} else if (rule.selector === "contains" && textRange.contents.indexOf(rule.text) !== -1) {{
                    shouldApply = true;
                }}
                
                if (shouldApply) {{
                    // Apply font family
                    if (rule.fontFamily) {{
                        textRange.characterAttributes.textFont = app.textFonts.getByName(rule.fontFamily);
                    }}
                    
                    // Apply font size
                    if (rule.fontSize) {{
                        textRange.characterAttributes.size = rule.fontSize;
                    }}
                    
                    // Apply font weight/style
                    if (rule.fontWeight) {{
                        // This is simplified - actual implementation would need font style mapping
                        if (rule.fontWeight === "bold") {{
                            textRange.characterAttributes.textFont = app.textFonts.getByName(textRange.characterAttributes.textFont.name + " Bold");
                        }}
                    }}
                    
                    // Apply line height
                    if (rule.lineHeight) {{
                        textRange.paragraphAttributes.leading = rule.lineHeight;
                    }}
                    
                    // Apply character spacing
                    if (rule.characterSpacing) {{
                        textRange.characterAttributes.tracking = rule.characterSpacing;
                    }}
                    
                    // Apply color
                    if (rule.color) {{
                        var color = new RGBColor();
                        color.red = parseInt(rule.color.substring(1, 3), 16);
                        color.green = parseInt(rule.color.substring(3, 5), 16);
                        color.blue = parseInt(rule.color.substring(5, 7), 16);
                        textRange.characterAttributes.fillColor = color;
                    }}
                    
                    applied_rules.push(rule.name || "unnamed_rule");
                }}
            }}
            
            results.push({{
                index: i,
                success: true,
                applied_rules: applied_rules
            }});
        }}
        
        return JSON.stringify({{
            success: true,
            processed: results.length,
            results: results
        }});
        
    }} catch (error) {{
        return JSON.stringify({{
            success: false,
            error: error.toString()
        }});
    }}
}}

// Execute the function
batchFormatText();
'''
    
    def _generate_optical_margin_script(self, parameters: Dict) -> str:
        """Generate script for optical margin alignment"""
        return f'''
// Typography Agent - Optical Margin Alignment Script
#target illustrator

function applyOpticalMarginAlignment() {{
    if (app.documents.length === 0) {{
        alert("No document is open.");
        return;
    }}
    
    var doc = app.activeDocument;
    var textFrames = doc.textFrames;
    var marginAdjustment = {parameters.get("margin_adjustment", 0.05)};
    var results = [];
    
    try {{
        for (var i = 0; i < textFrames.length; i++) {{
            var textFrame = textFrames[i];
            var textRange = textFrame.textRange;
            
            // Apply optical margin alignment
            // This is a simplified implementation
            var paragraphs = textRange.paragraphs;
            
            for (var j = 0; j < paragraphs.length; j++) {{
                var paragraph = paragraphs[j];
                var firstChar = paragraph.characters[0];
                var lastChar = paragraph.characters[paragraph.characters.length - 1];
                
                // Check for punctuation and adjust margins
                var punctuationChars = ['"', "'", "-", ".", ",", ";", ":", "!", "?"];
                
                if (firstChar && punctuationChars.indexOf(firstChar.contents) !== -1) {{
                    paragraph.paragraphAttributes.firstLineIndent -= marginAdjustment * 72; // Convert to points
                }}
                
                if (lastChar && punctuationChars.indexOf(lastChar.contents) !== -1) {{
                    // Adjust right margin for hanging punctuation
                    paragraph.paragraphAttributes.rightIndent -= marginAdjustment * 72;
                }}
            }}
            
            results.push({{
                index: i,
                success: true,
                paragraphs_processed: paragraphs.length
            }});
        }}
        
        return JSON.stringify({{
            success: true,
            processed: results.length,
            results: results
        }});
        
    }} catch (error) {{
        return JSON.stringify({{
            success: false,
            error: error.toString()
        }});
    }}
}}

// Execute the function
applyOpticalMarginAlignment();
'''
    
    def _generate_text_styles_script(self, parameters: Dict) -> str:
        """Generate script for creating and applying text styles"""
        return f'''
// Typography Agent - Text Styles Script
#target illustrator

function createAndApplyTextStyles() {{
    if (app.documents.length === 0) {{
        alert("No document is open.");
        return;
    }}
    
    var doc = app.activeDocument;
    var styles = {json.dumps(parameters.get("styles", []))};
    var results = [];
    
    try {{
        // Create character styles
        for (var i = 0; i < styles.length; i++) {{
            var styleDefinition = styles[i];
            var styleName = styleDefinition.name;
            
            // Check if style already exists
            var existingStyle = null;
            try {{
                existingStyle = doc.characterStyles.getByName(styleName);
            }} catch (e) {{
                // Style doesn't exist, create new one
                existingStyle = doc.characterStyles.add();
                existingStyle.name = styleName;
            }}
            
            // Apply style properties
            var charAttr = existingStyle.characterAttributes;
            
            if (styleDefinition.fontFamily) {{
                charAttr.textFont = app.textFonts.getByName(styleDefinition.fontFamily);
            }}
            if (styleDefinition.fontSize) {{
                charAttr.size = styleDefinition.fontSize;
            }}
            if (styleDefinition.characterSpacing) {{
                charAttr.tracking = styleDefinition.characterSpacing;
            }}
            if (styleDefinition.color) {{
                var color = new RGBColor();
                color.red = parseInt(styleDefinition.color.substring(1, 3), 16);
                color.green = parseInt(styleDefinition.color.substring(3, 5), 16);
                color.blue = parseInt(styleDefinition.color.substring(5, 7), 16);
                charAttr.fillColor = color;
            }}
            
            results.push({{
                style_name: styleName,
                created: true
            }});
        }}
        
        return JSON.stringify({{
            success: true,
            styles_created: results.length,
            results: results
        }});
        
    }} catch (error) {{
        return JSON.stringify({{
            success: false,
            error: error.toString()
        }});
    }}
}}

// Execute the function
createAndApplyTextStyles();
'''
    
    async def execute_extendscript(self, script_content: str) -> Dict:
        """Execute ExtendScript in Illustrator"""
        # Write script to temporary file
        script_file = os.path.join(self.temp_script_dir, f"script_{asyncio.current_task().get_name()}.jsx")
        
        try:
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Execute script using osascript on macOS or direct execution on Windows
            if os.name == 'posix':  # macOS/Linux
                applescript = f'''
                tell application "Adobe Illustrator"
                    do javascript file "{script_file}"
                end tell
                '''
                
                result = subprocess.run(
                    ['osascript', '-e', applescript],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    try:
                        return json.loads(result.stdout.strip())
                    except json.JSONDecodeError:
                        return {"success": True, "output": result.stdout.strip()}
                else:
                    return {"success": False, "error": result.stderr}
            
            else:  # Windows
                # For Windows, we'd use COM automation or direct ExtendScript execution
                return {"success": False, "error": "Windows execution not implemented yet"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        finally:
            # Clean up temporary file
            if os.path.exists(script_file):
                os.remove(script_file)

# Initialize MCP Server
server = Server("illustrator-integration")
illustrator = IllustratorIntegration()

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available Illustrator integration tools"""
    return [
        Tool(
            name="apply_typography_fix",
            description="Apply typography fixes directly in Illustrator",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_type": {
                        "type": "string",
                        "description": "Type of typography task (kerning, alignment, etc.)"
                    },
                    "suggestions": {
                        "type": "array",
                        "description": "Specific suggestions to apply"
                    },
                    "context": {
                        "type": "object",
                        "description": "Project context"
                    }
                },
                "required": ["task_type"]
            }
        ),
        Tool(
            name="adjust_text_boxes",
            description="Automatically adjust text box sizes and positions",
            inputSchema={
                "type": "object",
                "properties": {
                    "adjustments": {
                        "type": "array",
                        "description": "Text box adjustments to apply"
                    },
                    "autoFit": {
                        "type": "boolean",
                        "description": "Whether to auto-fit text to boxes"
                    }
                }
            }
        ),
        Tool(
            name="batch_format_text",
            description="Apply formatting rules to multiple text elements",
            inputSchema={
                "type": "object",
                "properties": {
                    "format_rules": {
                        "type": "array",
                        "description": "Formatting rules to apply"
                    }
                },
                "required": ["format_rules"]
            }
        ),
        Tool(
            name="apply_advanced_kerning",
            description="Apply advanced kerning adjustments",
            inputSchema={
                "type": "object",
                "properties": {
                    "kerning_pairs": {
                        "type": "array",
                        "description": "Character pairs and their kerning adjustments"
                    },
                    "optical_kerning": {
                        "type": "boolean",
                        "description": "Enable optical kerning"
                    },
                    "metric_kerning": {
                        "type": "boolean",
                        "description": "Enable metric kerning"
                    }
                }
            }
        ),
        Tool(
            name="optical_margin_alignment",
            description="Apply optical margin alignment for professional typography",
            inputSchema={
                "type": "object",
                "properties": {
                    "margin_adjustment": {
                        "type": "number",
                        "description": "Margin adjustment amount (in inches)"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for Illustrator integration"""
    
    try:
        if name == "apply_typography_fix":
            task_type = arguments.get("task_type", "")
            suggestions = arguments.get("suggestions", [])
            
            # Map task type to appropriate operation
            if task_type == "kerning":
                script = illustrator.generate_extendscript("apply_kerning", {
                    "optical_kerning": True,
                    "kerning_pairs": [{"characters": "AV", "adjustment": -50}]  # Example
                })
            elif task_type == "alignment":
                script = illustrator.generate_extendscript("optical_margin_alignment", {
                    "margin_adjustment": 0.05
                })
            else:
                script = illustrator.generate_extendscript("batch_format", {
                    "format_rules": [{"selector": "all", "name": "auto_fix"}]
                })
            
            result = await illustrator.execute_extendscript(script)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "adjust_text_boxes":
            adjustments = arguments.get("adjustments", [])
            auto_fit = arguments.get("autoFit", True)
            
            script = illustrator.generate_extendscript("adjust_text_boxes", {
                "adjustments": adjustments,
                "autoFit": auto_fit,
                "baseFontSize": 12,
                "maxFontSize": 72
            })
            
            result = await illustrator.execute_extendscript(script)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "batch_format_text":
            format_rules = arguments.get("format_rules", [])
            
            script = illustrator.generate_extendscript("batch_format", {
                "format_rules": format_rules,
                "heading_threshold": 18
            })
            
            result = await illustrator.execute_extendscript(script)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "apply_advanced_kerning":
            kerning_pairs = arguments.get("kerning_pairs", [])
            optical_kerning = arguments.get("optical_kerning", False)
            metric_kerning = arguments.get("metric_kerning", False)
            
            script = illustrator.generate_extendscript("apply_kerning", {
                "kerning_pairs": kerning_pairs,
                "optical_kerning": optical_kerning,
                "metric_kerning": metric_kerning
            })
            
            result = await illustrator.execute_extendscript(script)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "optical_margin_alignment":
            margin_adjustment = arguments.get("margin_adjustment", 0.05)
            
            script = illustrator.generate_extendscript("optical_margin_alignment", {
                "margin_adjustment": margin_adjustment
            })
            
            result = await illustrator.execute_extendscript(script)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        error_result = {"success": False, "error": str(e)}
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

async def main():
    """Run the Illustrator integration MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="illustrator-integration",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
