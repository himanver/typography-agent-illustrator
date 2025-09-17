"""
Typography Agent for Adobe Illustrator
A comprehensive AI assistant for professional typography design.
"""

import asyncio
import json
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import logging

# LLM and MCP imports
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class AgentMode(Enum):
    """Agent operational modes"""
    CRITIC = "critic"
    GUIDE = "guide" 
    HELPER = "helper"

class TypographyTask(Enum):
    """Typography task categories"""
    KERNING = "kerning"
    ALIGNMENT = "alignment"
    HIERARCHY = "hierarchy"
    CONSISTENCY = "consistency"
    READABILITY = "readability"
    AUTOMATION = "automation"

@dataclass
class TypographyContext:
    """Current typography project context"""
    project_name: str
    document_specs: Dict
    brand_guidelines: Optional[Dict]
    target_audience: str
    medium: str  # print, digital, etc.
    current_artboard: Optional[str]
    selected_elements: List[Dict]

@dataclass
class TypographyFeedback:
    """Structured feedback from the agent"""
    mode: AgentMode
    task_type: TypographyTask
    severity: str  # info, warning, error
    message: str
    suggestions: List[str]
    auto_fix_available: bool
    confidence_score: float

class TypographyAgent:
    """Main Typography Agent class"""
    
    def __init__(self):
        self.anthropic = Anthropic()
        self.mode = AgentMode.GUIDE
        self.context: Optional[TypographyContext] = None
        self.mcp_servers = {}
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("TypographyAgent")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def initialize_mcp_servers(self):
        """Initialize all MCP servers"""
        servers_config = {
            "typography_analysis": {
                "command": "python",
                "args": ["src/mcp_servers/typography_analysis_server.py"]
            },
            "illustrator_integration": {
                "command": "python", 
                "args": ["src/mcp_servers/illustrator_integration_server.py"]
            },
            "typesetting_engine": {
                "command": "python",
                "args": ["src/mcp_servers/typesetting_engine_server.py"]
            },
            "workflow_automation": {
                "command": "python",
                "args": ["src/mcp_servers/workflow_automation_server.py"]
            }
        }
        
        for server_name, config in servers_config.items():
            try:
                server_params = StdioServerParameters(
                    command=config["command"],
                    args=config["args"]
                )
                
                session = await stdio_client(server_params)
                await session.initialize()
                self.mcp_servers[server_name] = session
                self.logger.info(f"Initialized MCP server: {server_name}")
                
            except Exception as e:
                self.logger.error(f"Failed to initialize {server_name}: {e}")

    def set_mode(self, mode: AgentMode):
        """Set the agent's operational mode"""
        self.mode = mode
        self.logger.info(f"Agent mode set to: {mode.value}")

    def update_context(self, context: TypographyContext):
        """Update the current typography context"""
        self.context = context
        self.logger.info(f"Context updated for project: {context.project_name}")

    async def analyze_typography(self, elements: List[Dict]) -> List[TypographyFeedback]:
        """Analyze typography elements and provide feedback"""
        if not self.mcp_servers.get("typography_analysis"):
            raise RuntimeError("Typography analysis server not initialized")
            
        feedback_list = []
        
        try:
            # Call typography analysis MCP server
            analysis_result = await self.mcp_servers["typography_analysis"].call_tool(
                "analyze_elements",
                arguments={
                    "elements": elements,
                    "context": self.context.__dict__ if self.context else {},
                    "mode": self.mode.value
                }
            )
            
            # Process results based on agent mode
            for result in analysis_result.content:
                feedback = self._process_analysis_result(result)
                feedback_list.append(feedback)
                
        except Exception as e:
            self.logger.error(f"Typography analysis failed: {e}")
            
        return feedback_list

    def _process_analysis_result(self, result: Dict) -> TypographyFeedback:
        """Process analysis result into structured feedback"""
        task_type = TypographyTask(result.get("task_type", "readability"))
        
        # Customize feedback based on agent mode
        if self.mode == AgentMode.CRITIC:
            message = self._generate_critical_feedback(result)
        elif self.mode == AgentMode.GUIDE:
            message = self._generate_educational_feedback(result)
        else:  # HELPER mode
            message = self._generate_action_feedback(result)
            
        return TypographyFeedback(
            mode=self.mode,
            task_type=task_type,
            severity=result.get("severity", "info"),
            message=message,
            suggestions=result.get("suggestions", []),
            auto_fix_available=result.get("auto_fix_available", False),
            confidence_score=result.get("confidence_score", 0.8)
        )

    def _generate_critical_feedback(self, result: Dict) -> str:
        """Generate critical, professional feedback"""
        base_message = result.get("message", "")
        return f"Critical Assessment: {base_message} This impacts the overall design quality and should be addressed for professional standards."

    def _generate_educational_feedback(self, result: Dict) -> str:
        """Generate educational, guiding feedback"""
        base_message = result.get("message", "")
        principle = result.get("typography_principle", "")
        return f"Typography Guidance: {base_message} {principle} This is an opportunity to enhance your typography skills."

    def _generate_action_feedback(self, result: Dict) -> str:
        """Generate action-oriented, helpful feedback"""
        base_message = result.get("message", "")
        action = result.get("suggested_action", "")
        return f"Quick Fix Available: {base_message} {action} I can help automate this adjustment."

    async def auto_fix_typography(self, feedback: TypographyFeedback) -> bool:
        """Automatically fix typography issues when possible"""
        if not feedback.auto_fix_available:
            return False
            
        if not self.mcp_servers.get("illustrator_integration"):
            raise RuntimeError("Illustrator integration server not initialized")
            
        try:
            fix_result = await self.mcp_servers["illustrator_integration"].call_tool(
                "apply_typography_fix",
                arguments={
                    "task_type": feedback.task_type.value,
                    "suggestions": feedback.suggestions,
                    "context": self.context.__dict__ if self.context else {}
                }
            )
            
            success = fix_result.content[0].get("success", False)
            if success:
                self.logger.info(f"Auto-fix applied for {feedback.task_type.value}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Auto-fix failed: {e}")
            return False

    async def batch_process_documents(self, document_paths: List[str], operations: List[str]) -> Dict:
        """Process multiple documents with batch operations"""
        if not self.mcp_servers.get("workflow_automation"):
            raise RuntimeError("Workflow automation server not initialized")
            
        try:
            batch_result = await self.mcp_servers["workflow_automation"].call_tool(
                "batch_process",
                arguments={
                    "document_paths": document_paths,
                    "operations": operations,
                    "context": self.context.__dict__ if self.context else {}
                }
            )
            
            return batch_result.content[0]
            
        except Exception as e:
            self.logger.error(f"Batch processing failed: {e}")
            return {"success": False, "error": str(e)}

    async def get_typography_recommendations(self, query: str) -> str:
        """Get typography recommendations using LLM"""
        system_prompt = self._build_system_prompt()
        
        try:
            response = await self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"Typography question: {query}\nContext: {self.context.__dict__ if self.context else 'No specific context'}"
                }]
            )
            
            return response.content[0].text
            
        except Exception as e:
            self.logger.error(f"LLM recommendation failed: {e}")
            return "I'm unable to provide recommendations at this time. Please try again."

    def _build_system_prompt(self) -> str:
        """Build system prompt based on current mode and context"""
        base_prompt = """You are a professional Typography Agent for Adobe Illustrator. You have deep expertise in typography, layout design, and professional typesetting standards."""
        
        mode_prompts = {
            AgentMode.CRITIC: "You provide constructive, professional criticism of typography choices. Be direct but helpful in identifying issues and their impact on design quality.",
            AgentMode.GUIDE: "You are an educational mentor, helping designers learn typography principles and best practices. Explain the 'why' behind recommendations.",
            AgentMode.HELPER: "You focus on practical solutions and automation. Provide actionable steps and offer to help with tedious tasks."
        }
        
        context_prompt = ""
        if self.context:
            context_prompt = f"""
            Current Project Context:
            - Project: {self.context.project_name}
            - Medium: {self.context.medium}
            - Target Audience: {self.context.target_audience}
            - Brand Guidelines: {'Available' if self.context.brand_guidelines else 'Not specified'}
            """
        
        return f"{base_prompt}\n\n{mode_prompts[self.mode]}\n{context_prompt}"

    async def shutdown(self):
        """Cleanup and shutdown all MCP servers"""
        for server_name, session in self.mcp_servers.items():
            try:
                await session.close()
                self.logger.info(f"Closed MCP server: {server_name}")
            except Exception as e:
                self.logger.error(f"Error closing {server_name}: {e}")

# Example usage and testing
async def main():
    """Example usage of the Typography Agent"""
    agent = TypographyAgent()
    
    try:
        # Initialize the agent
        await agent.initialize_mcp_servers()
        
        # Set up context
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
        agent.set_mode(AgentMode.GUIDE)
        
        # Get recommendations
        recommendation = await agent.get_typography_recommendations(
            "What are the best practices for kerning in logo design?"
        )
        
        print("Typography Recommendation:")
        print(recommendation)
        
    finally:
        await agent.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
