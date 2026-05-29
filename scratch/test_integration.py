import asyncio
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add root folder to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from server import app

def test_chat():
    client = TestClient(app)
    
    # 1. Clear session
    session_id = "test-session-12345"
    client.post("/api/chat/clear", json={"user_id": "test_user", "session_id": session_id})
    
    # 2. First message: "Hola, me gustaría buscar oportunidades rentables en el mercado."
    print("\n--- SENDING FIRST MESSAGE ---")
    response = client.post("/api/chat", json={
        "message": "Hola, me gustaría buscar oportunidades rentables en el mercado hoy.",
        "user_id": "test_user",
        "session_id": session_id
    })
    print("STATUS:", response.status_code)
    data = response.json()
    print("RESPONSE:", data.get("response"))
    print("LOGS:")
    for log in data.get("logs", []):
        print(f"  [{log.get('role_from')} -> {log.get('role_to')}]: {log.get('message')} ({log.get('status')})")
        
    # 3. Second message: "Vale, cuéntame más sobre la opción recomendada."
    print("\n--- SENDING SECOND MESSAGE ---")
    response2 = client.post("/api/chat", json={
        "message": "Vale, cuéntame más sobre la opción recomendada.",
        "user_id": "test_user",
        "session_id": session_id
    })
    print("STATUS:", response2.status_code)
    data2 = response2.json()
    print("RESPONSE:", data2.get("response"))
    print("LOGS:")
    for log in data2.get("logs", []):
        print(f"  [{log.get('role_from')} -> {log.get('role_to')}]: {log.get('message')} ({log.get('status')})")

if __name__ == "__main__":
    test_chat()
