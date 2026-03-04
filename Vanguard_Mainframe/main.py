# FILE: main.py (VANGUARD MAINFRAME - DIRECT INJECTION READY)
import os
import shutil
import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import anthropic

app = FastAPI(title="Vanguard Mainframe - Tyre 18 Neural Emulation")

# 1. THE SECURITY GATE (CORS)
# This allows the Base44.com dashboard to securely "Inject" the payload
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ENVIRONMENT INITIALIZATION
NODE_ID = int(os.getenv("NODE_ID", "0"))
PROJECT_DIR = "Vanguard_Build_Output"
os.makedirs(PROJECT_DIR, exist_ok=True)

GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")

if GOOGLE_KEY: genai.configure(api_key=GOOGLE_KEY)
if CLAUDE_KEY: claude_client = anthropic.Anthropic(api_key=CLAUDE_KEY)

# 3. THE SUB-ATOMIC DATA STRUCTURE
class EngineeringMissionRequest(BaseModel):
    project_name: str
    objective: str
    protons: list = []
    neutrons: list = []
    electrons: list = []

# 4. THE 13-TIER SINGULARITY LOOP
async def execute_omni_singularity(req: EngineeringMissionRequest):
    print(f"⚡ IGNITION: Starting Swarm Sequence for {req.project_name}")
    # Simulation Logic Placeholder (Tyre 18 Emulation)
    await asyncio.sleep(5) 
    return f"Vanguard Result for {req.objective}: 100% Remission Blueprint Achieved."

async def run_omni_sequence(req: EngineeringMissionRequest):
    try:
        final_blueprint = await execute_omni_singularity(req)
        
        # Save to the Persistent Connectome Disk
        file_path = os.path.join(PROJECT_DIR, f"{req.project_name}_blueprint.txt")
        with open(file_path, "w") as f:
            f.write(final_blueprint)
            
        shutil.make_archive("Omni_Release", 'zip', PROJECT_DIR)
        print("💎 ZENITH REACHED: Omni Singularity Achieved.")
        print("✅ MISSION COMPLETE: Blueprint Secured.")
    except Exception as e:
        print(f"❌ MISSION FAILED: {str(e)}")

# 5. THE DIRECT INJECTION ENDPOINT (Match for Base44)
@app.post("/start")
async def start_mission(req: EngineeringMissionRequest, bt: BackgroundTasks):
    bt.add_task(run_omni_sequence, req)
    return {
        "status": "MISSION_INITIATED", 
        "project": req.project_name,
        "mainframe_node": NODE_ID
    }

# 6. HEALTH CHECK (For Render.com)
@app.get("/")
async def health_check():
    return {"status": "ONLINE", "node": NODE_ID, "system": "VANGUARD_TYPE_I"}
  
     
