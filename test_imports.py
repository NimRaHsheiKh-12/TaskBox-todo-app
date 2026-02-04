import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test just the imports and basic functionality
try:
    from backend.src.api.chat import router
    print("[OK] Chat API router imported successfully")
except Exception as e:
    print(f"[ERR] Error importing chat API: {e}")
    import traceback
    traceback.print_exc()

try:
    from backend.src.services.chat_service import ChatService
    print("[OK] ChatService imported successfully")
except Exception as e:
    print(f"[ERR] Error importing ChatService: {e}")
    import traceback
    traceback.print_exc()

try:
    from backend.src.utils.message_parser import MessageParser
    print("[OK] MessageParser imported successfully")
except Exception as e:
    print(f"[ERR] Error importing MessageParser: {e}")
    import traceback
    traceback.print_exc()

try:
    from backend.src.utils.task_enums import TaskAction
    print("[OK] TaskAction imported successfully")
except Exception as e:
    print(f"[ERR] Error importing TaskAction: {e}")
    import traceback
    traceback.print_exc()