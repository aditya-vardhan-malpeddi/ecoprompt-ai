"""
Green AI Advisor & Sustainability Intelligence Engine.
Provides actionable strategies, carbon-aware compute scheduling,
and green architectural recommendations.
"""

from typing import List, Dict, Any
from app.config import (
    GRID_CARBON_INTENSITY,
    AI_MODEL_ENERGY_PROFILES,
    QUANTIZATION_MULTIPLIERS,
)


def get_green_ai_recommendations() -> List[Dict[str, Any]]:
    """Return categorized, high-impact Green AI and sustainability actions."""
    return [
        {
            "category": "Model Routing & Distillation",
            "title": "Use Small Specialized Models First",
            "impact": "High (Up to 85% energy reduction)",
            "description": "Route simple queries (classification, extraction, summarization) to compact edge/flash models (<8B parameters) rather than large frontier models.",
            "action_items": [
                "Deploy a lightweight classifier or router to determine query complexity.",
                "Use models like Gemini Flash or LLaMA-3 8B for 80% of routine workloads.",
                "Reserve heavy frontier models strictly for complex reasoning or code generation.",
            ]
        },
        {
            "category": "Prompt Efficiency & Caching",
            "title": "Prompt Token Compression & Context Caching",
            "impact": "Medium-High (40% - 60% token savings)",
            "description": "Trim polite pleasantries, repeated preamble, and use Context Caching for static system instructions or documentation.",
            "action_items": [
                "Leverage Prompt Caching so prefix tokens are only computed once.",
                "Set strict max_tokens limits and enforce structured output formats (JSON/Pydantic schemas).",
                "Audit prompt templates regularly with EcoPrompt AI.",
            ]
        },
        {
            "category": "Hardware & Precision",
            "title": "Adopt 4-bit / 8-bit Quantization (INT4 / INT8)",
            "impact": "High (35% - 62% energy cut per token)",
            "description": "Quantized weights significantly reduce memory bandwidth bottlenecks, DRAM activation energy, and compute power.",
            "action_items": [
                "Utilize AWQ, GPTQ, or bitsandbytes INT4 quantization for local deployments.",
                "Use high-efficiency tensor accelerators (e.g. Google TPU v5e or NVIDIA L4/H100).",
                "Employ speculative decoding to maximize FLOP utilization during inference.",
            ]
        },
        {
            "category": "Spatial & Temporal Scheduling",
            "title": "Carbon-Aware Cloud Routing & Batch Scheduling",
            "impact": "Very High (Up to 90% CO2 reduction)",
            "description": "Run background training, batch inference, or embedding generation in clean-energy grid regions during peak solar/wind hours.",
            "action_items": [
                "Migrate batch workloads to low-carbon cloud regions (e.g., US-West/Oregon or Europe-North/Sweden).",
                "Schedule offline batch jobs during local midday (peak solar) or nighttime (high wind).",
                "Integrate Carbon-Aware SDK or Electricity Maps API for real-time marginal carbon signals.",
            ]
        },
        {
            "category": "System Architecture",
            "title": "Semantic Vector Caching",
            "impact": "Medium-High (100% savings on cache hits)",
            "description": "Cache embeddings and LLM responses for similar questions using vector similarity (e.g., GPTCache).",
            "action_items": [
                "Store question-answer pairs in a fast vector cache with a 0.92+ cosine similarity threshold.",
                "Bypass LLM generation entirely for frequently asked customer questions.",
            ]
        }
    ]


def simulate_green_migration(
    current_tier: str = "giant_reasoning",
    target_tier: str = "small_compact",
    current_region: str = "us_east_virginia",
    target_region: str = "us_west_oregon",
    monthly_tokens: int = 50_000_000,
    current_quantization: str = "fp16",
    target_quantization: str = "int4",
) -> Dict[str, Any]:
    """Simulate the energy and carbon savings of adopting green architectural recommendations."""
    curr_tier_kwh = AI_MODEL_ENERGY_PROFILES.get(current_tier, AI_MODEL_ENERGY_PROFILES["giant_reasoning"])["kwh_per_1k_tokens"]
    targ_tier_kwh = AI_MODEL_ENERGY_PROFILES.get(target_tier, AI_MODEL_ENERGY_PROFILES["small_compact"])["kwh_per_1k_tokens"]

    curr_q = QUANTIZATION_MULTIPLIERS.get(current_quantization, 1.0)
    targ_q = QUANTIZATION_MULTIPLIERS.get(target_quantization, 0.38)

    curr_intensity = GRID_CARBON_INTENSITY.get(current_region, GRID_CARBON_INTENSITY["us_east_virginia"])["intensity"]
    targ_intensity = GRID_CARBON_INTENSITY.get(target_region, GRID_CARBON_INTENSITY["us_west_oregon"])["intensity"]

    # Current consumption
    curr_kwh_month = (monthly_tokens / 1000.0) * curr_tier_kwh * curr_q * 1.15
    curr_kg_co2_month = (curr_kwh_month * curr_intensity) / 1000.0
    curr_kg_co2_annual = curr_kg_co2_month * 12.0

    # Target green consumption
    targ_kwh_month = (monthly_tokens / 1000.0) * targ_tier_kwh * targ_q * 1.15
    targ_kg_co2_month = (targ_kwh_month * targ_intensity) / 1000.0
    targ_kg_co2_annual = targ_kg_co2_month * 12.0

    saved_annual_kg = max(0.0, curr_kg_co2_annual - targ_kg_co2_annual)
    saved_kwh_annual = max(0.0, (curr_kwh_month - targ_kwh_month) * 12.0)
    co2_reduction_pct = round((saved_annual_kg / curr_kg_co2_annual * 100.0) if curr_kg_co2_annual > 0 else 0.0, 1)

    return {
        "monthly_tokens": monthly_tokens,
        "current_scenario": {
            "model_tier": current_tier,
            "quantization": current_quantization,
            "region": current_region,
            "monthly_kwh": round(curr_kwh_month, 2),
            "annual_kg_co2": round(curr_kg_co2_annual, 2),
        },
        "green_scenario": {
            "model_tier": target_tier,
            "quantization": target_quantization,
            "region": target_region,
            "monthly_kwh": round(targ_kwh_month, 2),
            "annual_kg_co2": round(targ_kg_co2_annual, 2),
        },
        "annual_savings": {
            "kg_co2_saved": round(saved_annual_kg, 2),
            "metric_tons_co2_saved": round(saved_annual_kg / 1000.0, 3),
            "kwh_saved": round(saved_kwh_annual, 2),
            "co2_reduction_pct": co2_reduction_pct,
            "equivalent_trees_planted_10yr": round(saved_annual_kg / 60.0, 1),
            "equivalent_car_miles_avoided": round((saved_annual_kg * 1000.0) / 310.0, 1),
        }
    }
