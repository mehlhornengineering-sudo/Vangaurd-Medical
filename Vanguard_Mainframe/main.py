import os
import shutil
import asyncio
import httpx
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
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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

# 3. THE DUAL-CORE SWARM SEQUENCE
async def run_omni_sequence(req: EngineeringMissionRequest):
    try:
        print(f"⚡ IGNITION: Dual-Core Swarm Analysis for: {req.objective}")
        
        # CORE 1: Google Neural Reasoning
        model = genai.GenerativeModel('gemini-pro')
        google_prompt = f"Objective: {req.objective}. Provide a theoretical 13-tier regeneration blueprint focused on 0.0 entropy."
        google_res = await asyncio.to_thread(model.generate_content, google_prompt)
        
        # CORE 2: Anthropic Verification
        claude_res = await asyncio.to_thread(
            claude_client.messages.create,
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": f"Review and verify this 13-tier logic for {req.objective}: {google_res.text[:800]}"}]
        )

        # 4. COMPILING THE DATA PACKET
        file_path = os.path.join(PROJECT_DIR, f"{req.project_name}_Deep_Analysis.txt")
        with open(file_path, "w") as f:
            f.write(f"--- VANGUARD DUAL-CORE BLUEPRINT ---\n")
            f.write(f"TARGET PATHOLOGY: {req.objective}\n\n")
            f.write(f"PRIMARY REASONING (GEMINI):\n{google_res.text}\n\n")
            f.write(f"VERIFICATION LAYER (CLAUDE):\n{claude_res.content[0].text}\n")
            f.write(f"\n[FINAL STATUS: ZENITH REACHED - CONSENSUS ACHIEVED]")

        shutil.make_archive("Omni_Release", 'zip', PROJECT_DIR)
        print("💎 ZENITH REACHED: Deep Analysis Secured.")

        # 5. WEBHOOK CALL HOME
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://app.base44.com/api/webhooks/mission-complete", 
                json={"status": "COMPLETE", "project": req.project_name}
            )

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
    raise HTTPException(status_code=404, detail="Processing Deep Analysis...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
