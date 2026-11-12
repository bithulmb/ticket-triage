import os

from openai import AsyncOpenAI

# groq speaks the openai api, so the same client works against its url
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
INSTRUCTIONS = ("Sort the support ticket into billing, shipping or other, with a priority "
                'from 1 (low) to 5 (urgent). Reply with JSON only, like {"category": "billing", "priority": 4}.')


async def ask_model(text: str) -> str:
    reply = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "system", "content": INSTRUCTIONS},
                  {"role": "user", "content": text}],
    )
    return reply.choices[0].message.content