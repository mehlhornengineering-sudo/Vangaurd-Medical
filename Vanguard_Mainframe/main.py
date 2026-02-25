import os, json, shutil, asyncio, psutil
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import anthropic

app = FastAPI(title="Vanguard Medical Mainframe - 3D Geometric OS")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

NODE_ID = int(os.getenv("NODE_ID", "0"))
MAX_THERMAL_CAPACITY = float(os.getenv("MAX_THERMAL_CAPACITY", "85.0"))
PROJECT_DIR = "Vanguard_Build_Output"
os.makedirs(PROJECT_DIR, exist_ok=True)

MEMORY_FILE = os.path.join(PROJECT_DIR, "vanguard_connectome_memory.json")
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f: json.dump([], f)

GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")
if GOOGLE_KEY: genai.configure(api_key=GOOGLE_KEY)
if CLAUDE_KEY: claude_client = anthropic.Anthropic(api_key=CLAUDE_KEY)

class MedicalMissionRequest(BaseModel):
    project_name: str
    objective: str
    protons: list = []    
    neutrons: list = []   

def load_connectome_memory():
    with open(MEMORY_FILE, "r") as f: return json.load(f)

def save_to_connectome(project_name, objective, matter):
    memory = load_connectome_memory()
    memory.append({"project": project_name, "objective": objective, "successful_matter": matter})
    with open(MEMORY_FILE, "w") as f: json.dump(memory, f, indent=4)

async def call_claude_inspector(prompt: str):
    res = await asyncio.to_thread(claude_client.messages.create, model="claude-3-5-sonnet-20241022", max_tokens=1000, messages=[{"role": "user", "content": prompt}])
    return res.content[0].text

async def execute_advanced_medical_singularity(req: MedicalMissionRequest):
    print(f"\n🧬 IGNITING VANGUARD 3D GEOMETRIC SWARM FOR: {req.project_name}")
    long_term_memory = load_connectome_memory()
    memory_context = f"Past 3D Baselines: {json.dumps(long_term_memory[-3:])}" if long_term_memory else "No previous 3D architectures found."
    current_matter, sensory_feedback_loop, cycle = "", [], 0
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')

    while cycle < 5:
        cycle += 1
        heat = max(psutil.cpu_percent(), psutil.virtual_memory().percent)
        if heat >= MAX_THERMAL_CAPACITY: raise Exception("THERMAL MELTDOWN.")
        
        if cycle == 1:
            prompt = f"VANGUARD SYNTHESIZER (Type I OS - EGNN Emulation). Objective: {req.objective}. CONNECTOME MEMORY: {memory_context}. AXIOM: Engineer using 3D rotational symmetry and spatial coordinate logic."
            response = await asyncio.to_thread(gemini_model.generate_content, prompt)
            current_matter = response.text
            sensory_feedback_loop.append("Orbit 1 Spatial Synthesis Completed.")

        adme_report, tox_report, geom_report = await asyncio.gather(
            call_claude_inspector(f"ADME INSPECTOR: Analyze absorption/metabolism. Output exactly '0.0' if flawless. Matter: {current_matter}"),
            call_claude_inspector(f"TOXICITY INSPECTOR: Attempt to find cellular harm. Output exactly '0.0' if safe. Matter: {current_matter}"),
            call_claude_inspector(f"GEOMETRIC INSPECTOR: Evaluate 3D steric hindrance and geometric docking. Output exactly '0.0' if flawless. Matter: {current_matter}")
        )

        compiler_prompt = f"17-TIER COMPILER: ADME: {adme_report} | TOX: {tox_report} | GEOM: {geom_report} | History: {sensory_feedback_loop}. If all are exactly '0.0' and deterministic, output exactly '0.0'. MATTER: {current_matter}"
        final_report = await call_claude_inspector(compiler_prompt)
        
        if "0.0" in final_report and "100.0" not in final_report: 
            save_to_connectome(req.project_name, req.objective, current_matter)
            break

        sensory_feedback_loop.append(f"Orbit {cycle} Fracture: Inspectors rejected payload.") 
        optimizer_prompt = f"Reforge matter. ADME: {adme_report}. TOX: {tox_report}. GEOM: {geom_report}. Compiler: {final_report}.\nMATTER: {current_matter}"
        response = await asyncio.to_thread(gemini_model.generate_content, optimizer_prompt)
        current_matter = response.text

    return current_matter

@app.post("/api/mainframe/start")
async def start_mission(req: MedicalMissionRequest, bt: BackgroundTasks):
    bt.add_task(execute_advanced_medical_singularity, req)
    return {"status": "VANGUARD_3D_SWARM_INITIATED", "project": req.project_name}
