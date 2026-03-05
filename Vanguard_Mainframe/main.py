import os
import shutil
import asyncio
import httpx  
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# --- ENGINE OPTIMIZATION ---
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

app = FastAPI()

# SECURITY PROTOCOL (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_DIR = "Vanguard_Build_Output"
os.makedirs(PROJECT_DIR, exist_ok=True)

class EngineeringMissionRequest(BaseModel):
    project_name: str
    objective: str

# --- THE SWARM SEQUENCE WITH WEBHOOK ---
async def run_omni_sequence(req: EngineeringMissionRequest):
    try:
        print(f"⚡ IGNITION: Starting Swarm Sequence...")
        await asyncio.sleep(15) 
        
        file_path = os.path.join(PROJECT_DIR, "blueprint.txt")
        with open(file_path, "w") as f:
            f.write(f"Vanguard Mission: {req.objective}\nStatus: Achievement Unlocked.")
            
        shutil.make_archive("Omni_Release", 'zip', PROJECT_DIR)
        print("💎 ZENITH REACHED.")

        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    "https://app.base44.com/api/webhooks/mission-complete", 
                    json={
                        "status": "COMPLETE",
                        "project": req.project_name,
                        "download_url": "https://vanguard-mainframe-trideca.onrender.com/download-results"
                    },
                    timeout=10.0
                )
                print("📡 PING SENT: Base44 notified.")
            except Exception as ping_error:
                print(f"⚠️ Webhook failed (Base44 might not be listening): {ping_error}")

    except Exception as e:
        print(f"❌ SWARM ERROR: {str(e)}")

@app.post("/start")
async def start_mission(req: EngineeringMissionRequest, bt: BackgroundTasks):
    bt.add_task(run_omni_sequence, req)
    return {"status": "MISSION_INITIATED", "mainframe_node": 0}

@app.get("/download-results")
async def download_results():
    zip_path = "Omni_Release.zip"
    if os.path.exists(zip_path):
        return FileResponse(zip_path, filename="Vanguard_Blueprint.zip")
    raise HTTPException(status_code=404, detail="Processing...")

# --- BOOTSTRAP ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

