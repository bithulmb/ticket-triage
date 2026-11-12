import asyncio

from src.pipeline import triage


def test_billing_ticket_is_checked():
    # asyncio.run drives the async pipeline from a plain sync test
    row = asyncio.run(triage({"id": 1, "text": "I was charged twice"}))
    assert row["category"] == "billing"
    assert row["checked"] is True


def test_unclear_ticket_goes_to_a_person():
    row = asyncio.run(triage({"id": 4, "text": "How do I change my password?"}))
    assert row["checked"] is False
    assert row["category"] is None