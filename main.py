import asyncio
import json
import logging

from src.pipeline import run_all

# log to a file, overwriting it on each run
logging.basicConfig(filename="run.log", filemode="w", level=logging.INFO,
                    format="%(name)s %(levelname)s %(message)s")


async def main():
    with open("tickets.json") as f:
        tickets = json.load(f)
    results = await run_all(tickets)
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    # the ones the model could not sort go to a person
    unchecked = [r["id"] for r in results if not r["checked"]]
    print(f"Sorted {len(results)} tickets. For a person: {unchecked}")


if __name__ == "__main__":
    asyncio.run(main())