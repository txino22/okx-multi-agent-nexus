import inspect
from google.antigravity import LocalAgentConfig

# Get fields and constructor signature of LocalAgentConfig
sig = inspect.signature(LocalAgentConfig)
print("Constructor parameters:")
for name, param in sig.parameters.items():
    print(f"  {name}: {param.annotation} (default: {param.default})")

# Let's inspect class attributes or methods
print("\nClass attributes and methods:")
for name, member in inspect.getmembers(LocalAgentConfig):
    if not name.startswith('_'):
        print(f"  {name}: {member}")
