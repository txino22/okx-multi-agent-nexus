import asyncio
import inspect
from google.antigravity import Agent, LocalAgentConfig

async def main():
    cfg = LocalAgentConfig(model="gemini-2.5-flash", api_key="dummy")
    async with Agent(cfg) as agent:
        conv = agent.conversation
        print("Conversation class:", conv.__class__)
        print("\nConversation attributes/methods:")
        for name, member in inspect.getmembers(conv):
            if not name.startswith('_'):
                print(f"  {name}: {member}")
            
asyncio.run(main())
