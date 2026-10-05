"""
Unit tests for EcoPrompt AI modules and REST API.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.calculator import (
    calculate_ai_energy_kwh,
    calculate_ai_emissions_gco2,
    calculate_ai_footprint,
    calculate_cloud_footprint,
    calculate_lifestyle_footprint,
    get_equivalents,
)
from app.auditor import optimize_prompt_text, estimate_tokens, audit_prompt
from app.models import (
    PromptAuditRequest,
    FootprintCalculationRequest,
    CloudFootprintRequest,
    LifestyleFootprintRequest,
)

client = TestClient(app)


def test_token_estimation():
    text = "Hello world, this is a test prompt."
    tokens = estimate_tokens(text)
    assert 8 <= tokens <= 12


def test_prompt_optimizer_fluff_removal():
    verbose = "Please could you kindly act as an expert and give me a detailed summary. Thank you so much!"
    optimized, suggestions = optimize_prompt_text(verbose)
    assert "Please" not in optimized
    assert "kindly" not in optimized
    assert "Thank you" not in optimized
    assert len(suggestions) > 0


def test_ai_energy_calculation():
    kwh = calculate_ai_energy_kwh(tokens=1000, model_tier="medium_balanced", quantization="fp16")
    assert kwh > 0
    # INT4 should consume less energy than FP16
    kwh_int4 = calculate_ai_energy_kwh(tokens=1000, model_tier="medium_balanced", quantization="int4")
    assert kwh_int4 < kwh


def test_ai_emissions_regional():
    kwh = 1.0
    gco2_sweden = calculate_ai_emissions_gco2(kwh, region="se_sweden")
    gco2_india = calculate_ai_emissions_gco2(kwh, region="in_india")
    assert gco2_sweden < gco2_india


def test_equivalents():
    eq = get_equivalents(gco2=185.0, kwh=0.12)
    assert eq["km_car_driven"] == 1.0
    assert eq["smartphone_charges"] == 10.0


def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "prompt_auditor" in data["features"]


def test_api_config_meta():
    res = client.get("/api/config/meta")
    assert res.status_code == 200
    data = res.json()
    assert "regions" in data
    assert "models" in data
    assert "quantizations" in data


def test_api_audit_prompt():
    req = {
        "prompt": "Could you please kindly explain how photosynthesis works in plants? Thank you!",
        "model_tier": "medium_balanced",
        "quantization": "fp16",
        "region": "global_avg",
        "expected_calls_per_month": 5000,
    }
    res = client.post("/api/audit/prompt", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["token_reduction_pct"] > 0
    assert data["monthly_kwh_saved"] > 0
    assert "optimized_prompt" in data


def test_api_calculate_footprint():
    req = {
        "model_tier": "large_frontier",
        "quantization": "fp16",
        "region": "us_east_virginia",
        "input_tokens": 1500,
        "output_tokens": 500,
        "monthly_requests": 20000,
    }
    res = client.post("/api/calculate/footprint", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["annual_kg_co2"] > 0
    assert len(data["regional_comparisons"]) > 0


def test_api_calculate_lifestyle():
    req = {
        "commute_km_weekly": 80.0,
        "commute_mode": "petrol_car",
        "home_electricity_kwh_monthly": 250.0,
        "diet_type": "omnivore",
        "region": "global_avg",
    }
    res = client.post("/api/calculate/lifestyle", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["total_annual_tons_co2"] > 0
    assert "Transport" in data["breakdown_percentages"]


def test_api_simulate_migration():
    req = {
        "current_tier": "giant_reasoning",
        "target_tier": "small_compact",
        "current_region": "us_east_virginia",
        "target_region": "us_west_oregon",
        "monthly_tokens": 10000000,
    }
    res = client.post("/api/simulate/migration", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["annual_savings"]["co2_reduction_pct"] > 50.0
