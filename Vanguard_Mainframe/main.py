import os
import shutil
import asyncio
import httpx
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai

# ENGINE OPTIMIZATION
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# INITIALIZE AI ENGINES
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

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

async def run_omni_sequence(req: EngineeringMissionRequest):
    try:
        print(f"⚡ IGNITION: Deep Swarm Analysis for: {req.objective}")
        
        # 1. CORE 1: GOOGLE NEURAL ANALYSIS (High-Entropy Reasoning)
        model = genai.GenerativeModel('gemini-pro')
        prompt = (
            f"Act as a Vanguard Swarm Intelligence Worker. Objective: {req.objective}. "
            "Analyze cellular entropy and provide a theoretical 13-tier regeneration blueprint "
            "focusing on molecular stability and 0.0 entropy achieved through synthetic biology."
        )
        
        response = await asyncio.to_thread(model.generate_content, prompt)
        analysis_report = response.text

        # 2. GENERATE THE DATA PACKET
        file_name = f"{req.project_name}_Analysis.txt"
        file_path = os.path.join(PROJECT_DIR, file_name)
        with open(file_path, "w") as f:
            f.write(f"--- VANGUARD DEEP INTELLIGENCE REPORT ---\n")
            f.write(f"MISSION TARGET: {req.objective}\n")
            f.write(f"SWARM ANALYSIS:\n{analysis_report}\n")
            f.write(f"\n[FINAL STATUS: ZENITH ACHIEVED]")

        # 3. COMPRESS FOR EXTRACTION
        shutil.make_archive("Omni_Release", 'zip', PROJECT_DIR)
        print("💎 ZENITH REACHED: Deep Analysis Secured.")

        # 4. CALLBACK PING
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
            except:
                print("📡 Ping failed - dashboard update will rely on polling/manual check.")

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
        return FileResponse(zip_path, filename="Vanguard_Deep_Analysis.zip")
    raise HTTPException(status_code=404, detail="Analysis in progress...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
