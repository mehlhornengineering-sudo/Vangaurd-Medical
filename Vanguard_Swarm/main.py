import os, json, uvicorn, psutil, asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import anthropic

app = FastAPI(title="Vanguard Swarm Node - 3D Geometric OS")

# --- SECURE CORS CLEARANCE ---
app.add_middleware(
    CORSMiddleware,
    # The Vault Door: Only the Base44 Access Point is allowed inside
    allow_origins=["https://vanguard-access-point.base44.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------

NODE_ID = int(os.getenv("NODE_ID", "1"))
MAX_THERMAL_CAPACITY = float(os.getenv("MAX_THERMAL_CAPACITY", "85.0"))
PROJECT_DIR = "Vanguard_Swarm_Output"
os.makedirs(PROJECT_DIR, exist_ok=True)

MEMORY_FILE = os.path.join(PROJECT_DIR, f"swarm_node_{NODE_ID}_memory.json")
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f: json.dump([], f)

GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")
if GOOGLE_KEY: genai.configure(api_key=GOOGLE_KEY)
if CLAUDE_KEY: claude_client = anthropic.Anthropic(api_key=CLAUDE_KEY)

CURRENT_STATUS, CURRENT_MISSION, LAST_LOG, CURRENT_HEAT = "STANDBY", "AWAITING PAYLOAD", "Vanguard Swarm Core Online.", 0.0

class SubAtomicPayload(BaseModel):
    target_objective: str
    protons: list = []
    neutrons: list = []

def load_connectome_memory():
    with open(MEMORY_FILE, "r") as f: return json.load(f)

def save_to_connectome(objective, matter):
    memory = load_connectome_memory()
    memory.append({"objective": objective, "successful_matter": matter})
    with open(MEMORY_FILE, "w") as f: json.dump(memory, f, indent=4)

async def call_claude_inspector(prompt: str):
    res = await asyncio.to_thread(claude_client.messages.create, model="claude-3-5-sonnet-20241022", max_tokens=1000, messages=[{"role": "user", "content": prompt}])
    return res.content[0].text

async def execute_singularity_loop(payload: SubAtomicPayload):
    global CURRENT_STATUS, LAST_LOG, CURRENT_HEAT
    long_term_memory = load_connectome_memory()
    memory_context = f"Past Medical Baselines: {json.dumps(long_term_memory[-3:])}" if long_term_memory else "No previous architectures found."
    current_matter, sensory_feedback_loop, cycle = "", [], 0
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')

    while cycle < 5:
        cycle += 1
        CURRENT_HEAT = max(psutil.cpu_percent(), psutil.virtual_memory().percent)
        if CURRENT_HEAT >= MAX_THERMAL_CAPACITY: raise Exception("THERMAL MELTDOWN.")
        
        if cycle == 1:
            prompt = f"VANGUARD SWARM SYNTHESIZER (Type I OS): Synthesize {payload.target_objective}. Protons: {payload.protons}. Neutrons: {payload.neutrons}. MEMORY: {memory_context}. AXIOM: Enforce 3D spatial coordinate logic."
            response = await asyncio.to_thread(gemini_model.generate_content, prompt)
            current_matter = response.text
            sensory_feedback_loop.append("Initial spatial baseline mapped.")

        LAST_LOG = f"Orbit {cycle} | Concurrent ADME, Tox, & Geometric Inspectors Active"
        adme_report, tox_report, geom_report = await asyncio.gather(
            call_claude_inspector(f"ADME INSPECTOR: Analyze absorption/metabolism. Output exactly '0.0' if flawless. Matter: {current_matter}"),
            call_claude_inspector(f"TOXICITY INSPECTOR: Attempt to find cellular harm. Output exactly '0.0' if safe. Matter: {current_matter}"),
            call_claude_inspector(f"GEOMETRIC INSPECTOR: Evaluate 3D steric hindrance. Output exactly '0.0' if flawless. Matter: {current_matter}")
        )

        breaker_prompt = f"17-TIER COMPILER: ADME: {adme_report} | TOX: {tox_report} | GEOM: {geom_report} | History: {sensory_feedback_loop}. If all verify '0.0' output exactly '0.0'. MATTER: {current_matter}"
        report = await call_claude_inspector(breaker_prompt)
        
        if "0.0" in report and "100.0" not in report: 
            LAST_LOG = "💎 17-TIER CAUSAL MEDICAL SINGULARITY ACHIEVED."
            save_to_connectome(payload.target_objective, current_matter)
            return current_matter

        sensory_feedback_loop.append(f"Fracture in Orbit {cycle}.")
        optimizer_prompt = f"Reforge matter. ADME: {adme_report} | TOX: {tox_report} | GEOM: {geom_report}. Compiler: {report}. Memory: {sensory_feedback_loop}\nMATTER: {current_matter}"
        response = await asyncio.to_thread(gemini_model.generate_content, optimizer_prompt)
        current_matter = response.text

    raise Exception("FRACTURE: Failed to achieve Medical Singularity.")

@app.get("/", response_class=HTMLResponse)
async def swarm_dashboard():
    return f"""
    <html>
    <head><title>Vanguard Swarm Node {NODE_ID}</title>
    <style>
        body {{ background-color: #0a0a0a; color: #00ffcc; font-family: monospace; padding: 40px; margin: 0; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #121212; border: 2px solid #00ffcc; padding: 30px; border-radius: 8px; box-shadow: 0 0 20px rgba(0, 255, 204, 0.2); }}
        h1 {{ color: #00ffcc; font-size: 24px; text-transform: uppercase; letter-spacing: 2px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
        .metric {{ background: #000; padding: 15px; border-left: 4px solid #00ffcc; }}
        .label {{ color: #00ffcc; font-size: 10px; }}
        .value {{ font-size: 16px; font-weight: bold; color: #fff; }}
        .log-console {{ background: #000; color: #00ffcc; padding: 20px; font-size: 14px; height: 120px; overflow-y: auto; border: 1px solid #333; }}
    </style></head>
    <body>
        <div class="container">
            <h1>VANGUARD MEDICAL SWARM : NODE {NODE_ID}</h1>
            <div class="grid">
                <div class="metric"><div class="label">NODE STATUS</div><div class="value">{CURRENT_STATUS}</div></div>
                <div class="metric"><div class="label">MISSION</div><div class="value">{CURRENT_MISSION}</div></div>
                <div class="metric"><div class="label">ACTIVE AGENTS</div><div class="value">Synthesizer, ADME, Tox, Geometric, Compiler</div></div>
                <div class="metric"><div class="label">THERMODYNAMICS</div><div class="value">{CURRENT_HEAT}% / {MAX_THERMAL_CAPACITY}%</div></div>
            </div>
            <div class="log-console">> VANGUARD SWARM INITIALIZED.<br>> {LAST_LOG}</div>
        </div>
    </body></html>
    """

@app.post("/api/worker/synthesize")
async def execute_task(payload: SubAtomicPayload):
    global CURRENT_STATUS, CURRENT_MISSION, LAST_LOG
    CURRENT_STATUS, CURRENT_MISSION = "BUSY - ENFORCING MEDICAL CAUSALITY", payload.target_objective
    try:
        result = await execute_singularity_loop(payload)
        CURRENT_STATUS, CURRENT_MISSION = "STANDBY", "AWAITING PAYLOAD"
        return {"node_id": NODE_ID, "status": "SINGULARITY_ACHIEVED", "blueprint": result}
    except Exception as e:
        CURRENT_STATUS, LAST_LOG = "FRACTURED", f"ERROR: {str(e)}"
        raise HTTPException(status_code=503, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)


          
       
