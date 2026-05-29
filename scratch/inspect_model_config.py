import inspect
from google.antigravity.types import ModelConfig

# Get fields and constructor signature of ModelConfig
sig = inspect.signature(ModelConfig)
print("Constructor parameters:")
for name, param in sig.parameters.items():
    print(f"  {name}: {param.annotation} (default: {param.default})")
