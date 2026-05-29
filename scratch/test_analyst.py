import asyncio
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import get_agent_config, ANALYST_INSTRUCTIONS
from google.antigravity import Agent

async def main():
    cfg = get_agent_config(
        system_instructions=ANALYST_INSTRUCTIONS,
        modules="market",
        model_name="gemini-2.5-flash",
        read_only=True
    )
    async with Agent(cfg) as agent:
        print("--- RUNNING ANALYST ---")
        response = await agent.chat('{"action": "scan_market_top_opportunities"}')
        print("RAW RESPONSE:")
        print(await response.text())
        print("\nTOTAL USAGE:")
        print(agent.conversation.total_usage)

asyncio.run(main())
