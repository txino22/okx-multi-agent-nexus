import os
import google.antigravity

path = os.path.dirname(google.antigravity.__file__)
print("Searching in:", path)

for root, dirs, files in os.walk(path):
    for f in files:
        if f.endswith('.py'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', errors='ignore') as f_obj:
                content = f_obj.read()
                if 'cache' in content.lower():
                    print(f"Found in {os.path.relpath(filepath, path)}")
                    # print some lines
                    for line in content.splitlines():
                        if 'cache' in line.lower():
                            print("  ", line.strip())
