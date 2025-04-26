from pydantic import BaseModel
from typing import List, Optional

class DiceRollRequest(BaseModel):
    dice: List[str]  # e.g., ["2d6", "1d4"]
    modifier: Optional[int] = 0  # flat bonus to add to total

class DiceRollResult(BaseModel):
    individual_rolls: List[int]
    total: int
    breakdown: str
