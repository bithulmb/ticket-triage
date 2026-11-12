import asyncio
import logging
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from src.model import ask_model_mock
from src.llm import ask_model

logger = logging.getLogger("triage")


class Triage(BaseModel):
    # Literal pins the category to three values; priority has to sit in 1..5
    category: Literal["billing", "shipping", "other"]
    priority: int = Field(ge=1, le=5)

async def triage(ticket: dict) -> dict:
    answer1 = await ask_model_mock(ticket["text"])
    answer = await ask_model(ticket["text"])    
    
    try:
        result = Triage.model_validate_json(answer)
    except ValidationError:
        # a bad answer is set aside for a person rather than crashing the batch
        logger.warning("ticket %s needs a person", ticket["id"])
        return {"id": ticket["id"], "category": None, "priority": None, "checked": False}
    logger.info("ticket %s sorted as %s", ticket["id"], result.category)
    return {"id": ticket["id"], **result.model_dump(), "checked": True}


async def run_all(tickets: list) -> list:
    # fire every ticket off at once instead of waiting for each in turn
    return await asyncio.gather(*[triage(t) for t in tickets])