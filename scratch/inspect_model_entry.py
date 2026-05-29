import inspect
from google.antigravity.types import ModelEntry

# Get fields and constructor signature of ModelEntry
sig = inspect.signature(ModelEntry)
print("Constructor parameters:")
for name, param in sig.parameters.items():
    print(f"  {name}: {param.annotation} (default: {param.default})")
