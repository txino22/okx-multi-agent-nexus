import inspect
from google.antigravity.types import GeminiConfig

# Get fields and constructor signature of GeminiConfig
sig = inspect.signature(GeminiConfig)
print("Constructor parameters:")
for name, param in sig.parameters.items():
    print(f"  {name}: {param.annotation} (default: {param.default})")
