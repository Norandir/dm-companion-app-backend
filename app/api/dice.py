from fastapi import APIRouter
from app.schemas.dice import DiceRollRequest, DiceRollResult
import random
import re

router = APIRouter()

dice_pattern = re.compile(r"(\d*)d(\d+)")  # matches "2d6", "d20", etc.

@router.post("/roll/", response_model=DiceRollResult)
def roll_dice(request: DiceRollRequest):
    rolls = []
    breakdown_parts = []

    for dice in request.dice:
        match = dice_pattern.fullmatch(dice)
        if not match:
            continue  # skip invalid formats

        num, sides = match.groups()
        num = int(num) if num else 1
        sides = int(sides)

        current_rolls = [random.randint(1, sides) for _ in range(num)]
        rolls.extend(current_rolls)
        breakdown_parts.append(f"{dice}: {current_rolls}")

    total = sum(rolls) + request.modifier
    if request.modifier:
        breakdown_parts.append(f"Modifier: {request.modifier}")

    return DiceRollResult(
        individual_rolls=rolls,
        total=total,
        breakdown=" | ".join(breakdown_parts)
    )
