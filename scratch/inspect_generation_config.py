import inspect
from google.antigravity.types import GenerationConfig

# Get fields and constructor signature of GenerationConfig
sig = inspect.signature(GenerationConfig)
print("Constructor parameters:")
for name, param in sig.parameters.items():
    print(f"  {name}: {param.annotation} (default: {param.default})")
