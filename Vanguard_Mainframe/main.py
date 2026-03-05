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

# 2. NEURAL INITIALIZATION (Using Environment Variables)
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

PROJECT_DIR = "Vanguard_Build_Output"
os.makedirs(PROJECT_DIR, exist_ok=True)

class EngineeringMissionRequest(BaseModel):
    project_name: str
    objective: str

# 3. THE DUAL-CORE SWARM SEQUENCE + VALIDATION
async def run_omni_sequence(req: EngineeringMissionRequest):
    try:
        print(f"⚡ IGNITION: Dual-Core Swarm Analysis for: {req.objective}")
        
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
            max_tokens=1000,
            messages=[{
                "role": "user", 
                "content": f"Review and verify this 13-tier molecular logic for {req.objective}: {google_res.text[:800]}"
            }]
        )

        # --- VALIDATION LOGIC (Testing the Swarm's convergence) ---
        match_score = "HIGH" if (req.objective[:8].lower() in google_res.text.lower()) else "ANALYZING"
        
        file_name = f"{req.project_name}_Swarm_Validation.txt"
        file_path = os.path.join(PROJECT_DIR, file_name)
        
        with open(file_path, "w") as f:
            f.write(f"--- VANGUARD SWARM VALIDATION REPORT ---\n")
            f.write(f"MISSION TARGET: {req.objective}\n")
            f.write(f"TEST FEAT: Molecular Convergence Check\n")
            f.write(f"VALIDATION SCORE: {match_score}\n")
            f.write(f"----------------------------------------\n\n")
            f.write(f"CORE A (GEMINI) LOGIC SUMMARY:\n{google_res.text[:1000]}\n\n")
            f.write(f"CORE B (CLAUDE) VERIFICATION:\n{claude_res.content[0].text[:1000]}\n")
            f.write(f"\n[SWARM STATUS: OPERATIONAL - ZENITH ACHIEVED]")

        # 4. COMPRESS FOR EXTRACTION
        shutil.make_archive("Omni_Release", 'zip', PROJECT_DIR)
        print(f"💎 ZENITH REACHED: {req.project_name} Secured.")

        # 5. WEBHOOK CALL HOME (Ping Base44)
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
            except Exception as e:
                print(f"⚠️ Webhook failed: {e}")

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
        return FileResponse(zip_path, filename="Vanguard_Swarm_Analysis.zip")
    raise HTTPException(status_code=404, detail="Analysis still in progress...")

# --- BOOTSTRAP ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
