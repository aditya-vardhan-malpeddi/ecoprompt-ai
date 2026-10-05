"""
EcoPrompt AI - FastAPI Application Server.
Exposes RESTful endpoints for carbon auditing, prompt optimization, and sustainability insights.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import (
    GRID_CARBON_INTENSITY,
    AI_MODEL_ENERGY_PROFILES,
    QUANTIZATION_MULTIPLIERS,
    CLOUD_INSTANCE_HOURLY_KWH,
)
from app.models import (
    PromptAuditRequest,
    PromptAuditResponse,
    FootprintCalculationRequest,
    FootprintCalculationResponse,
    CloudFootprintRequest,
    CloudFootprintResponse,
    LifestyleFootprintRequest,
    LifestyleFootprintResponse,
)
from app.calculator import (
    calculate_ai_footprint,
    calculate_cloud_footprint,
    calculate_lifestyle_footprint,
)
from app.auditor import audit_prompt
from app.advisor import (
    get_green_ai_recommendations,
    simulate_green_migration,
)

app = FastAPI(
    title="EcoPrompt AI",
    description="Green AI and Sustainability Intelligence Suite for carbon auditing, prompt optimization, and eco-guidelines.",
    version="1.0.0",
)

# Enable CORS for local testing and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static directory setup
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "EcoPrompt AI API is active. Static UI not yet deployed."}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "EcoPrompt AI",
        "version": "1.0.0",
        "features": [
            "prompt_auditor",
            "ai_carbon_calculator",
            "cloud_footprint_calculator",
            "lifestyle_sustainability",
            "green_ai_advisor",
            "migration_simulator",
        ],
    }


@app.get("/api/config/meta")
async def get_metadata():
    """Retrieve all available configurations, regions, and model tiers for frontend dropdowns."""
    return {
        "regions": GRID_CARBON_INTENSITY,
        "models": AI_MODEL_ENERGY_PROFILES,
        "quantizations": QUANTIZATION_MULTIPLIERS,
        "cloud_instances": CLOUD_INSTANCE_HOURLY_KWH,
    }


@app.post("/api/audit/prompt", response_model=PromptAuditResponse)
async def post_prompt_audit(request: PromptAuditRequest):
    """Audit and optimize a user prompt to reduce tokens, energy, and emissions."""
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt text cannot be empty.")
    return audit_prompt(request)


@app.post("/api/calculate/footprint", response_model=FootprintCalculationResponse)
async def post_calculate_footprint(request: FootprintCalculationRequest):
    """Calculate AI workload energy consumption, carbon emissions, and regional alternatives."""
    return calculate_ai_footprint(request)


@app.post("/api/calculate/cloud", response_model=CloudFootprintResponse)
async def post_calculate_cloud(request: CloudFootprintRequest):
    """Calculate cloud compute and GPU instance emissions with green region alternatives."""
    return calculate_cloud_footprint(request)


@app.post("/api/calculate/lifestyle", response_model=LifestyleFootprintResponse)
async def post_calculate_lifestyle(request: LifestyleFootprintRequest):
    """Calculate personal lifestyle and commuting carbon footprint with an eco-scorecard."""
    return calculate_lifestyle_footprint(request)


@app.get("/api/recommendations")
async def get_recommendations():
    """Get prioritized Green AI recommendations and best practices."""
    return {"recommendations": get_green_ai_recommendations()}


@app.post("/api/simulate/migration")
async def post_simulate_migration(payload: dict):
    """Simulate the carbon and energy impact of switching models, precision, or cloud regions."""
    current_tier = payload.get("current_tier", "giant_reasoning")
    target_tier = payload.get("target_tier", "small_compact")
    current_region = payload.get("current_region", "us_east_virginia")
    target_region = payload.get("target_region", "us_west_oregon")
    monthly_tokens = int(payload.get("monthly_tokens", 50_000_000))
    current_quantization = payload.get("current_quantization", "fp16")
    target_quantization = payload.get("target_quantization", "int4")

    return simulate_green_migration(
        current_tier=current_tier,
        target_tier=target_tier,
        current_region=current_region,
        target_region=target_region,
        monthly_tokens=monthly_tokens,
        current_quantization=current_quantization,
        target_quantization=target_quantization,
    )
