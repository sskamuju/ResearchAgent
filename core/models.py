


from pydantic import BaseModel
from typing import List, Dict, Any

class PlanStep(BaseModel):
    """
    Represents a single step in a multi-step research plan.

    Attributes:
        id (str): A unique identifier for this step (e.g., "step1").
        tool (str): The name of the tool to be used (must match a registered tool in the executor).
        args (Dict[str, Any]): A dictionary of arguments to pass to the tool during execution.
        rationale (str): A brief explanation of why this step is useful for answering the user’s question.
    """
    id: str
    tool: str
    query: str
    rationale: str

class Plan(BaseModel):
    """
    Represents the full research plan, consisting of multiple steps.

    Attributes:
        steps (List[PlanStep]): A list of PlanStep objects defining the full execution strategy.
    """
    steps: List[PlanStep]