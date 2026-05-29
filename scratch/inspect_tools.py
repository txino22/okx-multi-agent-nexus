import asyncio
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import get_agent_config
from google.antigravity import Agent

async def main():
    cfg = get_agent_config(
        system_instructions="Test",
        modules="market",
        model_name="gemini-2.5-flash",
        read_only=True
    )
    async with Agent(cfg) as agent:
        print("Registered tools for 'market' module:")
        connection = agent.conversation.connection
        if hasattr(connection, '_tool_runner') and connection._tool_runner:
            for name, tool in connection._tool_runner.tools.items():
                print(f"  Tool: {name}")
                print(f"    Description: {tool.__doc__}")
        else:
            print("No _tool_runner found on connection:", type(connection))

asyncio.run(main())
