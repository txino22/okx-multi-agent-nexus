import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from google.antigravity import Agent, LocalAgentConfig

async def test_model(model_name, use_vertex):
    config = LocalAgentConfig(
        model=model_name,
        vertex=use_vertex,
        project=os.environ.get("GCP_PROJECT") if use_vertex else None,
        location=os.environ.get("GCP_LOCATION") if use_vertex else None,
        api_key=os.environ.get("GEMINI_API_KEY") if not use_vertex else None
    )
    try:
        async with Agent(config) as agent:
            response = await agent.chat("Dí hola en una palabra.")
            text = ""
            async for chunk in response:
                text += chunk
            print(f"SUCCESS model={model_name} (vertex={use_vertex}): {text.strip()}")
            return True
    except Exception as e:
        print(f"FAILED model={model_name} (vertex={use_vertex}): {e}")
        return False

async def main():
    print("Testing Vertex AI models...")
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro",
        "gemini-1.5-pro-001",
        "gemini-1.5-pro-002",
        "gemini-2.5-flash"
    ]
    for m in models_to_test:
        await test_model(m, use_vertex=True)

asyncio.run(main())
