"""
Pydantic schema definitions for API inputs, outputs, and calculations.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class PromptAuditRequest(BaseModel):
    prompt: str = Field(..., description="Prompt text to analyze and optimize")
    model_tier: str = Field("medium_balanced", description="Model tier identifier (small_compact, medium_balanced, large_frontier, giant_reasoning)")
    quantization: str = Field("fp16", description="Quantization precision (fp16, int8, int4)")
    region: str = Field("global_avg", description="Region key from GRID_CARBON_INTENSITY")
    expected_calls_per_month: int = Field(10000, description="Estimated monthly frequency of this prompt")


class PromptAuditResponse(BaseModel):
    original_prompt: str
    optimized_prompt: str
    original_token_count: int
    optimized_token_count: int
    token_reduction_pct: float
    original_kwh_per_call: float
    optimized_kwh_per_call: float
    energy_saved_kwh_per_call: float
    original_gco2_per_call: float
    optimized_gco2_per_call: float
    gco2_saved_per_call: float
    monthly_gco2_saved: float
    monthly_kwh_saved: float
    eco_grade: str
    readability_and_clarity_score: float
    suggestions: List[str]
    equivalents: Dict[str, Any]


class FootprintCalculationRequest(BaseModel):
    model_tier: str = "medium_balanced"
    quantization: str = "fp16"
    region: str = "global_avg"
    input_tokens: int = 1500
    output_tokens: int = 500
    monthly_requests: int = 50000
    pue: float = 1.15


class FootprintCalculationResponse(BaseModel):
    region_name: str
    grid_intensity_gco2_kwh: float
    clean_energy_share: int
    total_tokens_per_request: int
    kwh_per_request: float
    gco2_per_request: float
    monthly_kwh: float
    monthly_kg_co2: float
    annual_kg_co2: float
    equivalents: Dict[str, Any]
    regional_comparisons: List[Dict[str, Any]]


class CloudFootprintRequest(BaseModel):
    instance_type: str = "gpu_single_a100"
    hours_per_day: float = 8.0
    days_per_month: int = 22
    instance_count: int = 1
    region: str = "us_east_virginia"


class CloudFootprintResponse(BaseModel):
    instance_name: str
    region_name: str
    total_hours_month: float
    monthly_kwh: float
    monthly_kg_co2: float
    annual_kg_co2: float
    green_alternative_region: str
    potential_co2_savings_pct: float
    potential_kg_co2_saved_annual: float
    equivalents: Dict[str, Any]


class LifestyleFootprintRequest(BaseModel):
    commute_km_weekly: float = 100.0
    commute_mode: str = "petrol_car"  # petrol_car, electric_car, public_transit, bicycle
    home_electricity_kwh_monthly: float = 300.0
    diet_type: str = "omnivore"       # meat_heavy, omnivore, pescatarian, vegetarian, vegan
    region: str = "global_avg"


class LifestyleFootprintResponse(BaseModel):
    monthly_transport_kg_co2: float
    monthly_home_energy_kg_co2: float
    monthly_diet_kg_co2: float
    total_monthly_kg_co2: float
    total_annual_tons_co2: float
    eco_grade: str
    key_recommendations: List[str]
    breakdown_percentages: Dict[str, float]
