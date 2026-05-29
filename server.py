from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uvicorn
import uuid
import time
from agents import get_interface_config
from google.antigravity import Agent
from request_context import logs_var
from okx_client import get_okx_balance, get_okx_active_bots
from delegation import auto_delegate

# Initialize Cloud Firestore Client
db = None
try:
    from google.cloud import firestore
    # Default to auto-detect project/location in Google Cloud
    db = firestore.Client()
except Exception as e:
    print(f"Warning: Could not initialize Firestore Client: {e}")

app = FastAPI(title="Neptune AI Command Center")

class ChatRequest(BaseModel):
    message: str
    user_id: str = "user_default"
    session_id: str = None

class ClearRequest(BaseModel):
    user_id: str = "user_default"
    session_id: str

@app.get("/api/chat/history")
async def chat_history(user_id: str = "user_default", session_id: str = None):
    if not session_id:
        return {"messages": [], "session_id": str(uuid.uuid4())}
    
    if db:
        try:
            doc_ref = db.collection("usuarios").document(user_id).collection("sesiones_chat").document(session_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                if not data.get("is_archived", False):
                    return {
                        "messages": data.get("messages", []),
                        "session_id": session_id
                    }
        except Exception as e:
            print(f"Error fetching history: {e}")
            
    return {"messages": [], "session_id": str(uuid.uuid4())}

@app.post("/api/chat/clear")
async def clear_chat(req: ClearRequest):
    if db and req.session_id:
        try:
            doc_ref = db.collection("usuarios").document(req.user_id).collection("sesiones_chat").document(req.session_id)
            if doc_ref.get().exists:
                doc_ref.update({"is_archived": True})
        except Exception as e:
            print(f"Error archiving session {req.session_id}: {e}")
            
    new_session_id = str(uuid.uuid4())
    return {"session_id": new_session_id}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    user_id = req.user_id or "user_default"
    session_id = req.session_id or str(uuid.uuid4())
    
    # Retrieve existing history first (before writing the new message)
    history_messages = []
    if db:
        try:
            session_ref = db.collection("usuarios").document(user_id).collection("sesiones_chat").document(session_id)
            doc = session_ref.get()
            if doc.exists:
                data = doc.to_dict()
                if not data.get("is_archived", False):
                    all_messages = data.get("messages", [])
                    # Slice to the last 10 messages (5 turns) — spec: ventana de 5-10 mensajes
                    history_messages = all_messages[-10:]
        except Exception as e:
            print(f"Error retrieving history from Firestore: {e}")
            
    # Format pruned history context block
    history_context = ""
    if history_messages:
        history_context = "HISTORIAL RECIENTE DEL CHAT (últimos mensajes):\n"
        for msg in history_messages:
            role = "Usuario" if msg["sender"] == "user" else "Agente"
            history_context += f"- {role}: {msg['content']}\n"
        history_context += "\nUsa este historial reciente únicamente para mantener el contexto de la conversación. No repitas saludos.\n\n"
        
    t0 = time.monotonic()
    analyst_output, strategist_output = await auto_delegate(req.message)
    delegation_ms = (time.monotonic() - t0) * 1000
    print(f"[Delegation] Parallel call completed in {delegation_ms:.0f}ms")

    extra_context = ""
    if analyst_output:
        extra_context += f"[DATOS DEL ANALISTA]\n{analyst_output}\n\n"
    if strategist_output:
        extra_context += f"[DATOS DEL ESTRATEGA]\n{strategist_output}\n\n"
    prompt = f"{extra_context}{history_context}Mensaje actual del usuario: {req.message}"
    
    # Pre-save raw user message to Firestore (without context)
    user_msg = {
        "sender": "user",
        "content": req.message,
        "timestamp": time.time(),
        "metadata": {}
    }
    
    if db:
        try:
            session_ref = db.collection("usuarios").document(user_id).collection("sesiones_chat").document(session_id)
            doc = session_ref.get()
            if not doc.exists:
                session_ref.set({
                    "user_id": user_id,
                    "session_id": session_id,
                    "created_at": time.time(),
                    "is_archived": False,
                    "messages": [user_msg]
                })
            else:
                session_ref.update({
                    "messages": firestore.ArrayUnion([user_msg])
                })
        except Exception as e:
            print(f"Error pre-saving user message to Firestore: {e}")

    request_logs = []
    token = logs_var.set(request_logs)
    try:
        cfg = get_interface_config()
        # Initialize Google Antigravity Agent
        async with Agent(cfg) as agent:
            response = await agent.chat(prompt)
            final_text = ""
            async for chunk in response:
                final_text += chunk
            
            # Post-save agent response to Firestore
            agent_msg = {
                "sender": "agent",
                "content": final_text,
                "timestamp": time.time(),
                "metadata": {
                    "logs": request_logs
                }
            }
            if db:
                try:
                    session_ref = db.collection("usuarios").document(user_id).collection("sesiones_chat").document(session_id)
                    session_ref.update({
                        "messages": firestore.ArrayUnion([agent_msg])
                    })
                except Exception as e:
                    print(f"Error saving agent response to Firestore: {e}")
                    
            return {
                "response": final_text,
                "logs": request_logs,
                "session_id": session_id
            }
    except Exception as e:
        err_msg = f"Error procesando solicitud con el agente en Vertex AI: {str(e)}"
        
        # Save error response as agent message for history sanity
        agent_err_msg = {
            "sender": "agent",
            "content": err_msg,
            "timestamp": time.time(),
            "metadata": {
                "logs": request_logs
            }
        }
        if db:
            try:
                session_ref = db.collection("usuarios").document(user_id).collection("sesiones_chat").document(session_id)
                session_ref.update({
                    "messages": firestore.ArrayUnion([agent_err_msg])
                })
            except Exception as fe:
                print(f"Error saving agent error response: {fe}")
                
        return {
            "response": err_msg,
            "logs": request_logs,
            "session_id": session_id
        }
    finally:
        logs_var.reset(token)

@app.get("/api/portfolio")
async def portfolio_endpoint():
    return get_okx_balance()

@app.get("/api/active-bots")
async def active_bots_endpoint():
    return get_okx_active_bots()

# Static routing matching the Stitch folder layouts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STITCH_DIR = os.path.join(BASE_DIR, "stitch_neptune_trading_nexus")

@app.get("/")
async def get_nexus():
    return FileResponse(os.path.join(STITCH_DIR, "the_nexus_ultra_fidelity_agent", "code.html"))

@app.get("/vault")
async def get_vault():
    return FileResponse(os.path.join(STITCH_DIR, "the_nexus_ultra_fidelity_agent", "code.html"))

@app.get("/fleet")
async def get_fleet():
    return FileResponse(os.path.join(STITCH_DIR, "the_nexus_ultra_fidelity_agent", "code.html"))

# Static asset mounts for screenshots/images
if os.path.exists(os.path.join(STITCH_DIR, "the_nexus_ultra_fidelity_agent")):
    app.mount("/the_nexus_ultra_fidelity_agent", StaticFiles(directory=os.path.join(STITCH_DIR, "the_nexus_ultra_fidelity_agent")), name="nexus_static")
if os.path.exists(os.path.join(STITCH_DIR, "vault_ultra_fidelity_portfolio")):
    app.mount("/vault_ultra_fidelity_portfolio", StaticFiles(directory=os.path.join(STITCH_DIR, "vault_ultra_fidelity_portfolio")), name="vault_static")
if os.path.exists(os.path.join(STITCH_DIR, "fleet_ultra_fidelity_monitoring")):
    app.mount("/fleet_ultra_fidelity_monitoring", StaticFiles(directory=os.path.join(STITCH_DIR, "fleet_ultra_fidelity_monitoring")), name="fleet_static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
