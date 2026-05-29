import sys
import os

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Testing imports...")
try:
    import config
    print("  config imported successfully")
    import okx_client
    print("  okx_client imported successfully")
    import agents
    print("  agents imported successfully")
    import server
    print("  server imported successfully")
    import main
    print("  main imported successfully")
    print("\nSUCCESS: All files imported and parsed successfully with no errors!")
except Exception as e:
    print(f"\nERROR: Import failed with exception: {e}")
    sys.exit(1)
