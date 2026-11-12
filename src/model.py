import asyncio


async def ask_model_mock(text: str) -> str:
    """Stand-in model. Swap this one function for a real client in production."""
    await asyncio.sleep(0.1)
    text = text.lower()
    if "charged" in text or "refund" in text:
        return '{"category": "billing", "priority": 4}'
    if "parcel" in text or "arrived" in text:
        return '{"category": "shipping", "priority": 3}'
    # a deliberate miss: plain text, not json, so the pipeline has to cope
    return "I am not sure how to sort this one."