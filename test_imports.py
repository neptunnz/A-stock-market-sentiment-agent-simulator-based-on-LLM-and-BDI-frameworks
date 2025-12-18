"""Test all modules can be imported normally"""
try:
    print("Testing import config...")
    import config
    print("[OK] config imported successfully")
    
    print("Testing import llm_client...")
    import llm_client
    print("[OK] llm_client imported successfully")
    
    print("Testing import market...")
    import market
    print("[OK] market imported successfully")
    
    print("Testing import agent...")
    import agent
    print("[OK] agent imported successfully")
    
    print("Testing import simulator...")
    import simulator
    print("[OK] simulator imported successfully")
    
    print("Testing import app...")
    import app
    print("[OK] app imported successfully")
    
    print("\nAll modules imported successfully!")
    
except Exception as e:
    print(f"\n[ERROR] Import error: {e}")
    import traceback
    traceback.print_exc()

