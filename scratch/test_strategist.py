import asyncio
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import get_agent_config, STRATEGIST_INSTRUCTIONS
from google.antigravity import Agent

async def main():
    cfg = get_agent_config(
        system_instructions=STRATEGIST_INSTRUCTIONS,
        modules="market,bot.grid,bot.dca",
        model_name="gemini-2.5-pro",
        read_only=True
    )
    async with Agent(cfg) as agent:
        print("--- RUNNING STRATEGIST ---")
        response = await agent.chat('{"action": "calculate_max_profit_strategy", "assets": ["BTC-USDT", "ETH-USDT"]}')
        print("RAW RESPONSE:")
        print(await response.text())
        print("\nTOTAL USAGE:")
        print(agent.conversation.total_usage)

asyncio.run(main())
