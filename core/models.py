# Define schema using Pydantic


from pydantic import BaseModel
from typing import List, Dict, Any

class PlanStep(BaseModel):
    id: str
    tool: str
    args: Dict[str, Any]
    rationale: str

class Plan(BaseModel):
    steps: List[PlanStep]