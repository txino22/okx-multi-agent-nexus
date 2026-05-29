import asyncio
import os
from google.antigravity import Agent
from agents import get_interface_config
from dotenv import load_dotenv

load_dotenv()

async def test():
    cfg = get_interface_config()
    print("Starting agent...")
    async with Agent(cfg) as agent:
        print("Agent started. Sending message to get balance...")
        response = await agent.chat("Cuál es mi balance en la cuenta demo de OKX?")
        print("Response:")
        async for chunk in response:
            print(chunk, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(test())
