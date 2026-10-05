"""
Scientific Carbon Footprint & Energy Calculation Engine.
Calculates energy consumption in kWh and carbon emissions in gCO2e/kgCO2e.
"""

from typing import Dict, Any, List
from app.config import (
    GRID_CARBON_INTENSITY,
    AI_MODEL_ENERGY_PROFILES,
    QUANTIZATION_MULTIPLIERS,
    CLOUD_INSTANCE_HOURLY_KWH,
    EQUIVALENTS,
    DEFAULT_DATACENTER_PUE,
)
from app.models import (
    FootprintCalculationRequest,
    FootprintCalculationResponse,
    CloudFootprintRequest,
    CloudFootprintResponse,
    LifestyleFootprintRequest,
    LifestyleFootprintResponse,
)


def calculate_ai_energy_kwh(
    tokens: int,
    model_tier: str = "medium_balanced",
    quantization: str = "fp16",
    pue: float = DEFAULT_DATACENTER_PUE,
) -> float:
    """Calculate raw electricity consumption (kWh) for generating/processing tokens."""
    tier_info = AI_MODEL_ENERGY_PROFILES.get(model_tier, AI_MODEL_ENERGY_PROFILES["medium_balanced"])
    base_kwh_per_1k = tier_info["kwh_per_1k_tokens"]
    q_multiplier = QUANTIZATION_MULTIPLIERS.get(quantization, 1.0)
    
    # IT equipment power * PUE (cooling + overhead)
    total_kwh = (tokens / 1000.0) * base_kwh_per_1k * q_multiplier * pue
    return max(total_kwh, 1e-8)


def calculate_ai_emissions_gco2(
    kwh: float,
    region: str = "global_avg",
) -> float:
    """Calculate grams of CO2e for a given kWh consumption in a specific region."""
    region_info = GRID_CARBON_INTENSITY.get(region, GRID_CARBON_INTENSITY["global_avg"])
    intensity = region_info["intensity"]  # gCO2e per kWh
    return kwh * intensity


def get_equivalents(gco2: float, kwh: float) -> Dict[str, Any]:
    """Convert emissions and energy into tangible everyday real-world metrics."""
    smartphone_charges = kwh / EQUIVALENTS["smartphone_charge_kwh"] if EQUIVALENTS["smartphone_charge_kwh"] > 0 else 0
    km_car_driven = gco2 / EQUIVALENTS["car_km_gco2"] if EQUIVALENTS["car_km_gco2"] > 0 else 0
    tree_days_needed = gco2 / EQUIVALENTS["tree_day_gco2_absorption"] if EQUIVALENTS["tree_day_gco2_absorption"] > 0 else 0
    led_hours = kwh / EQUIVALENTS["led_light_hour_kwh"] if EQUIVALENTS["led_light_hour_kwh"] > 0 else 0
    boil_cups = kwh / EQUIVALENTS["boil_water_cup_kwh"] if EQUIVALENTS["boil_water_cup_kwh"] > 0 else 0

    return {
        "smartphone_charges": round(smartphone_charges, 1),
        "km_car_driven": round(km_car_driven, 2),
        "tree_days_needed": round(tree_days_needed, 2),
        "led_light_hours": round(led_hours, 1),
        "cups_water_boiled": round(boil_cups, 1),
    }


def calculate_ai_footprint(req: FootprintCalculationRequest) -> FootprintCalculationResponse:
    """Compute detailed AI inference footprint and regional comparisons."""
    total_tokens = req.input_tokens + req.output_tokens
    kwh_single = calculate_ai_energy_kwh(total_tokens, req.model_tier, req.quantization, req.pue)
    gco2_single = calculate_ai_emissions_gco2(kwh_single, req.region)

    monthly_kwh = kwh_single * req.monthly_requests
    monthly_gco2 = gco2_single * req.monthly_requests
    monthly_kg_co2 = monthly_gco2 / 1000.0
    annual_kg_co2 = monthly_kg_co2 * 12.0

    region_data = GRID_CARBON_INTENSITY.get(req.region, GRID_CARBON_INTENSITY["global_avg"])

    # Compute comparative emissions across notable green and brown regions
    comparisons: List[Dict[str, Any]] = []
    for r_key, r_info in GRID_CARBON_INTENSITY.items():
        comp_gco2_single = kwh_single * r_info["intensity"]
        comp_annual_kg = (comp_gco2_single * req.monthly_requests * 12.0) / 1000.0
        comparisons.append({
            "region_key": r_key,
            "region_name": r_info["name"],
            "region_group": r_info["region_group"],
            "intensity_gco2_kwh": r_info["intensity"],
            "clean_energy_share": r_info["clean_energy_share"],
            "annual_kg_co2": round(comp_annual_kg, 2),
            "savings_vs_current_kg": round(annual_kg_co2 - comp_annual_kg, 2),
            "savings_vs_current_pct": round(((annual_kg_co2 - comp_annual_kg) / annual_kg_co2 * 100.0) if annual_kg_co2 > 0 else 0, 1),
        })

    comparisons.sort(key=lambda x: x["annual_kg_co2"])

    return FootprintCalculationResponse(
        region_name=region_data["name"],
        grid_intensity_gco2_kwh=region_data["intensity"],
        clean_energy_share=region_data["clean_energy_share"],
        total_tokens_per_request=total_tokens,
        kwh_per_request=round(kwh_single, 8),
        gco2_per_request=round(gco2_single, 6),
        monthly_kwh=round(monthly_kwh, 4),
        monthly_kg_co2=round(monthly_kg_co2, 3),
        annual_kg_co2=round(annual_kg_co2, 2),
        equivalents=get_equivalents(monthly_gco2, monthly_kwh),
        regional_comparisons=comparisons,
    )


def calculate_cloud_footprint(req: CloudFootprintRequest) -> CloudFootprintResponse:
    """Calculate cloud infrastructure carbon emissions."""
    instance_info = CLOUD_INSTANCE_HOURLY_KWH.get(
        req.instance_type,
        {"name": "Generic Compute", "kwh": 0.150}
    )
    
    total_hours = req.hours_per_day * req.days_per_month * req.instance_count
    monthly_kwh = total_hours * instance_info["kwh"] * DEFAULT_DATACENTER_PUE
    
    current_region = GRID_CARBON_INTENSITY.get(req.region, GRID_CARBON_INTENSITY["us_east_virginia"])
    monthly_gco2 = monthly_kwh * current_region["intensity"]
    monthly_kg_co2 = monthly_gco2 / 1000.0
    annual_kg_co2 = monthly_kg_co2 * 12.0

    # Best green alternative region (e.g., Sweden or US Oregon)
    green_region_key = "se_sweden" if "eu" in req.region or "se" in req.region else "us_west_oregon"
    green_region = GRID_CARBON_INTENSITY[green_region_key]
    green_annual_kg = (monthly_kwh * green_region["intensity"] * 12.0) / 1000.0
    
    saved_kg = max(0.0, annual_kg_co2 - green_annual_kg)
    savings_pct = (saved_kg / annual_kg_co2 * 100.0) if annual_kg_co2 > 0 else 0.0

    return CloudFootprintResponse(
        instance_name=instance_info["name"],
        region_name=current_region["name"],
        total_hours_month=round(total_hours, 1),
        monthly_kwh=round(monthly_kwh, 2),
        monthly_kg_co2=round(monthly_kg_co2, 2),
        annual_kg_co2=round(annual_kg_co2, 2),
        green_alternative_region=green_region["name"],
        potential_co2_savings_pct=round(savings_pct, 1),
        potential_kg_co2_saved_annual=round(saved_kg, 2),
        equivalents=get_equivalents(monthly_gco2, monthly_kwh),
    )


def calculate_lifestyle_footprint(req: LifestyleFootprintRequest) -> LifestyleFootprintResponse:
    """Calculate personal sustainability & lifestyle carbon emissions."""
    # Transport emission factors (kg CO2 per km)
    transport_factors = {
        "petrol_car": 0.192,
        "electric_car": 0.050,
        "public_transit": 0.040,
        "bicycle": 0.000,
    }
    car_factor = transport_factors.get(req.commute_mode, 0.192)
    monthly_transport_kg = (req.commute_km_weekly * 4.33) * car_factor

    # Home electricity
    region_info = GRID_CARBON_INTENSITY.get(req.region, GRID_CARBON_INTENSITY["global_avg"])
    monthly_home_kg = (req.home_electricity_kwh_monthly * region_info["intensity"]) / 1000.0

    # Dietary monthly emissions (kg CO2e per month)
    diet_factors = {
        "meat_heavy": 220.0,
        "omnivore": 140.0,
        "pescatarian": 105.0,
        "vegetarian": 85.0,
        "vegan": 60.0,
    }
    monthly_diet_kg = diet_factors.get(req.diet_type, 140.0)

    total_monthly_kg = monthly_transport_kg + monthly_home_kg + monthly_diet_kg
    total_annual_tons = (total_monthly_kg * 12.0) / 1000.0

    # Determine Eco Grade
    if total_annual_tons < 2.5:
        grade = "A+ (Outstanding Eco Champion)"
    elif total_annual_tons < 4.5:
        grade = "A (Low Carbon Footprint)"
    elif total_annual_tons < 7.5:
        grade = "B (Moderate Impact - Near Paris Goal)"
    elif total_annual_tons < 12.0:
        grade = "C (High Footprint)"
    else:
        grade = "D (Urgent Action Needed)"

    recommendations = []
    if req.commute_mode == "petrol_car":
        recommendations.append("Switching 2 days/week to remote work or transit saves ~250 kg CO2/year.")
    if req.diet_type in ["meat_heavy", "omnivore"]:
        recommendations.append("Incorporating 'Meatless Mondays' can lower personal dietary carbon by ~15-20%.")
    if req.home_electricity_kwh_monthly > 250:
        recommendations.append("Auditing standby power and upgrading to smart climate controls cuts home kWh by up to 18%.")

    pct_transport = round((monthly_transport_kg / total_monthly_kg * 100.0) if total_monthly_kg > 0 else 0, 1)
    pct_home = round((monthly_home_kg / total_monthly_kg * 100.0) if total_monthly_kg > 0 else 0, 1)
    pct_diet = round((monthly_diet_kg / total_monthly_kg * 100.0) if total_monthly_kg > 0 else 0, 1)

    return LifestyleFootprintResponse(
        monthly_transport_kg_co2=round(monthly_transport_kg, 2),
        monthly_home_energy_kg_co2=round(monthly_home_kg, 2),
        monthly_diet_kg_co2=round(monthly_diet_kg, 2),
        total_monthly_kg_co2=round(total_monthly_kg, 2),
        total_annual_tons_co2=round(total_annual_tons, 2),
        eco_grade=grade,
        key_recommendations=recommendations,
        breakdown_percentages={
            "Transport": pct_transport,
            "Home Energy": pct_home,
            "Diet": pct_diet,
        }
    )
