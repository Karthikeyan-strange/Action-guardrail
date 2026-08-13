from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class ToolAction(BaseModel):
    agent_id: str
    tool_name: str
    operation: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    session_id: Optional[str] = None