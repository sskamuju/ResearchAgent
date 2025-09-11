


from pydantic import BaseModel
from typing import List, Dict, Any

class PlanStep(BaseModel):
    id: str
    tool: str
    query: str
    rationale: str

class Plan(BaseModel):
    steps: List[PlanStep]