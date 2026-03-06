import os
import shutil
import asyncio
import httpx
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import anthropic

# 1. ENGINE OPTIMIZATION (High-Speed Request Handling)
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# 2. NEURAL INITIALIZATION
# Ensure these keys are set in your Render Environment Variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = FastAPI()

# SECURITY PROTOCOL (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THE VAULT SETUP ---
VAULT_DIR = "Vanguard_Vault"
os.makedirs(VAULT_DIR, exist_ok=True)

class EngineeringMissionRequest(BaseModel):
    project_name: str
    objective: str

# 3. THE DUAL-CORE SWARM SEQUENCE + PERSISTENCE
async def run_omni_sequence(req: EngineeringMissionRequest):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"⚡ VAULT IGNITION: Processing {req.project_name} at {timestamp}")
        
        # --- CORE A: Google Neural Reasoning ---
        model = genai.GenerativeModel('gemini-pro')
        google_prompt = (
            f"Act as a Vanguard Swarm Intelligence Worker. Objective: {req.objective}. "
            "Analyze cellular entropy and provide a theoretical 13-tier regeneration blueprint "
            "focusing on molecular stability and 0.0 entropy achieved through synthetic biology."
        )
        google_res = await asyncio.to_thread(model.generate_content, google_prompt)
        
        # --- CORE B: Anthropic Verification ---
        claude_res = await asyncio.to_thread(
            claude_client.messages.create,
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            messages=[{
                "role": "user", 
                "content": f"Review and verify this 13-tier molecular logic for {req.objective}: {google_res.text[:1000]}"
            }]
        )

        # --- SAVE TO PERSISTENT VAULT ---
        file_name = f"CURE_{req.project_name}_{timestamp}.txt"
        file_path = os.path.join(VAULT_DIR, file_name)
        
        with open(file_path, "w") as f:
            f.write(f"--- VANGUARD PERMANENT RECORD ---\n")
            f.write(f"TIMESTAMP: {timestamp}\n")
            f.write(f"MISSION TARGET: {req.objective}\n\n")
            f.write(f"PRIMARY ANALYSIS (GEMINI):\n{google_res.text}\n\n")
            f.write(f"VERIFICATION LAYER (CLAUDE):\n{claude_res.content[0].text}\n")
            f.write(f"\n[STATUS: STORED IN VAULT - ZENITH ACHIEVED]")

        # 4. UPDATE MASTER ARCHIVE
        shutil.make_archive("Omni_Release", 'zip', VAULT_DIR)
        print(f"💎 ZENITH SECURED: File saved to {file_path}")

        # 5. WEBHOOK CALL HOME (Ping Base44)
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    "https://app.base44.com/api/webhooks/mission-complete", 
                    json={
                        "status": "COMPLETE", 
                        "project": req.project_name,
                        "file_id": file_name,
                        "download_url": "https://vanguard-mainframe-trideca.onrender.com/download-vault"
                    },
                    timeout=10.0
                )
                print("📡 PING SENT: Base44 notified.")
            except:
                print("📡 Ping failed - dashboard update will rely on manual retrieval.")

    except Exception as e:
        print(f"❌ VAULT ERROR: {str(e)}")

@app.post("/start")
async def start_mission(req: EngineeringMissionRequest, bt: BackgroundTasks):
    bt.add_task(run_omni_sequence, req)
    return {"status": "VAULT_PROCESSING_STARTED", "vault_path": VAULT_DIR}

@app.get("/download-vault")
async def download_vault():
    zip_path = "Omni_Release.zip"
    if os.path.exists(zip_path):
        return FileResponse(zip_path, filename="Vanguard_Full_Vault.zip")
    raise HTTPException(status_code=404, detail="Vault is empty or processing.")

# --- BOOTSTRAP ---
if __name__ == "__main__":
    import uvicorn
    # Use port 10000 for Render
    uvicorn.run(app, host="0.0.0.0", port=10000)
