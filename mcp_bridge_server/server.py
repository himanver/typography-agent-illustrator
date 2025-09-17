"""
MCP Bridge Server for Typography Agent CEP Extension
Provides HTTP API bridge between CEP extension and MCP servers
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager

# Import our Typography Agent MCP components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from typography_agent import TypographyAgent, TypographyContext, AgentMode

# Pydantic models for API
class QueryRequest(BaseModel):
    message: str
    mode: str = "guide"
    context: Optional[Dict] = None

class ToolCallRequest(BaseModel):
    arguments: Dict[str, Any]
    timestamp: Optional[int] = None

class ServerInitRequest(BaseModel):
    config: Optional[Dict] = None

# Global agent instance
typography_agent: Optional[TypographyAgent] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown"""
    global typography_agent
    
    # Startup
    logging.info("Starting Typography Agent MCP Bridge Server...")
    typography_agent = TypographyAgent()
    
    try:
        await typography_agent.initialize_mcp_servers()
        logging.info("Typography Agent initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize Typography Agent: {e}")
        # Continue anyway - some features may work without all servers
    
    yield
    
    # Shutdown
    if typography_agent:
        await typography_agent.shutdown()
    logging.info("Typography Agent MCP Bridge Server stopped")

# Create FastAPI app
app = FastAPI(
    title="Typography Agent MCP Bridge",
    description="HTTP API bridge for Typography Agent MCP servers",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for CEP extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # CEP extensions need broad CORS access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_initialized": typography_agent is not None,
        "servers_connected": len(typography_agent.mcp_servers) if typography_agent else 0
    }

@app.post("/servers/{server_name}/initialize")
async def initialize_server(server_name: str, request: ServerInitRequest):
    """Initialize a specific MCP server"""
    if not typography_agent:
        raise HTTPException(status_code=503, detail="Typography agent not initialized")
    
    try:
        # Server initialization is handled during agent startup
        # This endpoint provides status information
        server_status = server_name in typography_agent.mcp_servers
        
        return {
            "server_name": server_name,
            "initialized": server_status,
            "capabilities": await get_server_capabilities(server_name) if server_status else None
        }
    except Exception as e:
        logger.error(f"Error initializing server {server_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/servers/{server_name}/capabilities")
async def get_server_capabilities(server_name: str):
    """Get capabilities of a specific MCP server"""
    if not typography_agent or server_name not in typography_agent.mcp_servers:
        raise HTTPException(status_code=404, detail=f"Server {server_name} not found")
    
    # Return mock capabilities - in real implementation, this would query the MCP server
    capabilities = {
        "typography-analysis": {
            "tools": ["analyze_elements", "font_pairing_analysis", "readability_assessment", "hierarchy_evaluation"],
            "description": "Typography analysis and feedback"
        },
        "illustrator-integration": {
            "tools": ["apply_typography_fix", "adjust_text_boxes", "batch_format_text", "apply_advanced_kerning", "optical_margin_alignment"],
            "description": "Direct Illustrator automation"
        },
        "typesetting-engine": {
            "tools": ["professional_kerning", "hyphenation_control", "margin_optimization"],
            "description": "Professional typesetting algorithms"
        },
        "workflow-automation": {
            "tools": ["batch_process", "template_apply", "style_sync"],
            "description": "Workflow automation and batch processing"
        }
    }
    
    return capabilities.get(server_name, {"tools": [], "description": "Unknown server"})

@app.get("/servers/{server_name}/tools")
async def list_server_tools(server_name: str):
    """List available tools for a server"""
    capabilities = await get_server_capabilities(server_name)
    return capabilities.get("tools", [])

@app.post("/servers/{server_name}/tools/{tool_name}")
async def call_tool(server_name: str, tool_name: str, request: ToolCallRequest):
    """Call a specific tool on a server"""
    if not typography_agent:
        raise HTTPException(status_code=503, detail="Typography agent not initialized")
    
    try:
        # Map server and tool names to our agent methods
        if server_name == "typography-analysis":
            result = await handle_typography_analysis_tool(tool_name, request.arguments)
        elif server_name == "illustrator-integration":
            result = await handle_illustrator_integration_tool(tool_name, request.arguments)
        elif server_name == "typesetting-engine":
            result = await handle_typesetting_tool(tool_name, request.arguments)
        elif server_name == "workflow-automation":
            result = await handle_workflow_tool(tool_name, request.arguments)
        else:
            raise HTTPException(status_code=404, detail=f"Server {server_name} not found")
        
        return result
        
    except Exception as e:
        logger.error(f"Error calling tool {tool_name} on {server_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process a natural language query"""
    if not typography_agent:
        raise HTTPException(status_code=503, detail="Typography agent not initialized")
    
    try:
        # Set agent mode
        mode = AgentMode(request.mode.lower())
        typography_agent.set_mode(mode)
        
        # Update context if provided
        if request.context:
            context = TypographyContext(
                project_name=request.context.get("project_name", "Untitled"),
                document_specs=request.context.get("document_specs", {}),
                brand_guidelines=request.context.get("brand_guidelines"),
                target_audience=request.context.get("target_audience", "General"),
                medium=request.context.get("medium", "print"),
                current_artboard=request.context.get("current_artboard"),
                selected_elements=request.context.get("selected_elements", [])
            )
            typography_agent.update_context(context)
        
        # Get LLM response
        response = await typography_agent.get_typography_recommendations(request.message)
        
        # Analyze if the query suggests specific actions
        suggested_actions = analyze_query_for_actions(request.message)
        
        return {
            "message": response,
            "type": "info",
            "mode": request.mode,
            "actions": suggested_actions
        }
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Tool handlers

async def handle_typography_analysis_tool(tool_name: str, arguments: Dict):
    """Handle typography analysis tool calls"""
    if tool_name == "analyze_elements":
        elements = arguments.get("elements", [])
        context = arguments.get("context", {})
        mode = arguments.get("mode", "guide")
        
        # Mock analysis results - in real implementation, this would call the actual MCP server
        return {
            "success": True,
            "results": [
                {
                    "task_type": "readability",
                    "severity": "info",
                    "message": "Text readability is within acceptable range",
                    "suggestions": ["Consider increasing line height for better readability"],
                    "auto_fix_available": True,
                    "confidence_score": 0.8
                }
            ]
        }
    
    elif tool_name == "font_pairing_analysis":
        fonts = arguments.get("fonts", [])
        return {
            "success": True,
            "score": 0.8,
            "feedback": ["Good font pairing detected"],
            "suggestions": []
        }
    
    else:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")

async def handle_illustrator_integration_tool(tool_name: str, arguments: Dict):
    """Handle Illustrator integration tool calls"""
    # These would interface with the actual ExtendScript execution
    return {
        "success": True,
        "message": f"Tool {tool_name} executed successfully",
        "processed": arguments.get("element_count", 1)
    }

async def handle_typesetting_tool(tool_name: str, arguments: Dict):
    """Handle professional typesetting tool calls"""
    return {
        "success": True,
        "message": f"Typesetting tool {tool_name} applied",
        "improvements": ["Kerning optimized", "Spacing adjusted"]
    }

async def handle_workflow_tool(tool_name: str, arguments: Dict):
    """Handle workflow automation tool calls"""
    return {
        "success": True,
        "message": f"Workflow tool {tool_name} completed",
        "batch_size": arguments.get("batch_size", 1)
    }

def analyze_query_for_actions(query: str) -> List[Dict]:
    """Analyze query text to suggest relevant actions"""
    query_lower = query.lower()
    actions = []
    
    if any(word in query_lower for word in ["kerning", "spacing", "letter spacing"]):
        actions.append({"type": "kerning", "description": "Apply kerning fixes"})
    
    if any(word in query_lower for word in ["hierarchy", "heading", "title"]):
        actions.append({"type": "hierarchy", "description": "Adjust visual hierarchy"})
    
    if any(word in query_lower for word in ["readability", "readable", "legible"]):
        actions.append({"type": "readability", "description": "Improve readability"})
    
    if any(word in query_lower for word in ["align", "alignment", "margin"]):
        actions.append({"type": "alignment", "description": "Fix alignment and margins"})
    
    return actions

# Additional utility endpoints

@app.get("/servers")
async def list_servers():
    """List all available MCP servers"""
    if not typography_agent:
        return {"servers": [], "error": "Typography agent not initialized"}
    
    return {
        "servers": list(typography_agent.mcp_servers.keys()),
        "total": len(typography_agent.mcp_servers)
    }

@app.get("/status")
async def get_status():
    """Get detailed status information"""
    if not typography_agent:
        return {
            "agent_status": "not_initialized",
            "servers": {},
            "mode": None
        }
    
    return {
        "agent_status": "ready",
        "servers": {
            name: "connected" for name in typography_agent.mcp_servers.keys()
        },
        "mode": typography_agent.mode.value,
        "context_available": typography_agent.context is not None
    }

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=3000,
        reload=True,
        log_level="info"
    )
