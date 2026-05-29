import inspect
from google.antigravity import Agent

# Get fields and methods of Agent class
print("Agent class methods/attributes:")
for name, member in inspect.getmembers(Agent):
    if not name.startswith('_'):
        print(f"  {name}: {member}")
