import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from google.antigravity import Agent, LocalAgentConfig

async def test():
    config = LocalAgentConfig(
        model="gemini-1.5-flash",
        vertex=False,
        api_key=os.environ.get("GEMINI_API_KEY")
    )
    try:
        async with Agent(config) as agent:
            response = await agent.chat("Hola")
            print("Response:", await response.text())
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
