"""
Configuration and scientific constants for carbon footprint and energy estimation.
Emission factors sourced from IEA, EPA, and ML Green AI benchmarks.
"""

from typing import Dict, Any

# Regional electricity grid carbon intensity in grams of CO2e per kWh (gCO2e/kWh)
# Based on national grid averages and renewable energy shares
GRID_CARBON_INTENSITY: Dict[str, Dict[str, Any]] = {
    "global_avg": {
        "name": "Global Average",
        "intensity": 440.0,
        "clean_energy_share": 38,
        "region_group": "Global",
    },
    "us_avg": {
        "name": "US National Average",
        "intensity": 380.0,
        "clean_energy_share": 41,
        "region_group": "North America",
    },
    "us_west_oregon": {
        "name": "US West (Oregon - Hydro heavy)",
        "intensity": 115.0,
        "clean_energy_share": 78,
        "region_group": "North America",
    },
    "us_east_virginia": {
        "name": "US East (N. Virginia - Tech Alley)",
        "intensity": 340.0,
        "clean_energy_share": 35,
        "region_group": "North America",
    },
    "us_central_iowa": {
        "name": "US Central (Iowa - Wind heavy)",
        "intensity": 220.0,
        "clean_energy_share": 62,
        "region_group": "North America",
    },
    "eu_avg": {
        "name": "EU Average",
        "intensity": 230.0,
        "clean_energy_share": 52,
        "region_group": "Europe",
    },
    "se_sweden": {
        "name": "Sweden (Hydro & Nuclear)",
        "intensity": 25.0,
        "clean_energy_share": 96,
        "region_group": "Europe",
    },
    "fr_france": {
        "name": "France (Nuclear)",
        "intensity": 55.0,
        "clean_energy_share": 92,
        "region_group": "Europe",
    },
    "de_germany": {
        "name": "Germany (Renewables + Transition)",
        "intensity": 360.0,
        "clean_energy_share": 52,
        "region_group": "Europe",
    },
    "uk_britain": {
        "name": "United Kingdom (Wind + Gas)",
        "intensity": 185.0,
        "clean_energy_share": 58,
        "region_group": "Europe",
    },
    "in_india": {
        "name": "India (National Grid)",
        "intensity": 710.0,
        "clean_energy_share": 24,
        "region_group": "Asia-Pacific",
    },
    "cn_china": {
        "name": "China (National Grid)",
        "intensity": 530.0,
        "clean_energy_share": 34,
        "region_group": "Asia-Pacific",
    },
    "jp_japan": {
        "name": "Japan (LNG + Nuclear)",
        "intensity": 465.0,
        "clean_energy_share": 28,
        "region_group": "Asia-Pacific",
    },
    "au_australia": {
        "name": "Australia (National Grid)",
        "intensity": 490.0,
        "clean_energy_share": 36,
        "region_group": "Asia-Pacific",
    },
    "br_brazil": {
        "name": "Brazil (Hydro dominant)",
        "intensity": 105.0,
        "clean_energy_share": 85,
        "region_group": "South America",
    },
}

# Standard Datacenter Power Usage Effectiveness (PUE)
DEFAULT_DATACENTER_PUE = 1.15  # Modern hyperscaler PUE (Google/AWS/Azure average)

# AI Models & Approximate Energy Profiles (kWh per 1,000 tokens)
# Accounts for forward pass computation on modern accelerator clusters (H100/A100/TPUv5)
AI_MODEL_ENERGY_PROFILES: Dict[str, Dict[str, Any]] = {
    "small_compact": {
        "name": "Compact Edge / Flash (< 8B params)",
        "examples": "Gemini 1.5/2.0 Flash, LLaMA-3 8B, Mistral 7B",
        "kwh_per_1k_tokens": 0.00015,
        "avg_latency_ms": 180,
    },
    "medium_balanced": {
        "name": "Balanced General (8B - 35B params)",
        "examples": "Gemma 2 27B, Mixtral 8x7B (active), Command R",
        "kwh_per_1k_tokens": 0.00065,
        "avg_latency_ms": 420,
    },
    "large_frontier": {
        "name": "Large Frontier (70B - 120B params)",
        "examples": "LLaMA-3 70B, Qwen 72B",
        "kwh_per_1k_tokens": 0.00160,
        "avg_latency_ms": 850,
    },
    "giant_reasoning": {
        "name": "Heavy Reasoning / Giant MoE (200B+ params)",
        "examples": "Claude 3.5 Sonnet, GPT-4o, DeepSeek R1, Gemini 1.5 Pro",
        "kwh_per_1k_tokens": 0.00340,
        "avg_latency_ms": 1600,
    },
}

# Quantization energy reduction multipliers
QUANTIZATION_MULTIPLIERS = {
    "fp16": 1.0,     # Full precision baseline
    "int8": 0.62,    # ~38% power reduction
    "int4": 0.38,    # ~62% power reduction
}

# Cloud Server and Dev Workload Energy Estimates (kWh per hour)
CLOUD_INSTANCE_HOURLY_KWH = {
    "dev_vm_small": {"name": "Small Dev VM (2 vCPU, 4GB RAM)", "kwh": 0.035},
    "dev_vm_large": {"name": "High-CPU Build Server (16 vCPU, 32GB RAM)", "kwh": 0.220},
    "gpu_single_a10": {"name": "Single GPU Node (A10G / L4)", "kwh": 0.260},
    "gpu_single_a100": {"name": "Single High-End GPU (A100 80GB)", "kwh": 0.480},
    "gpu_cluster_8xh100": {"name": "8x H100 Training Node", "kwh": 6.800},
}

# Equivalency factors for tangible eco-impact communication
EQUIVALENTS = {
    "smartphone_charge_kwh": 0.012,       # 1 smartphone full charge = 12 Wh
    "car_km_gco2": 185.0,                  # 1 km driven in average passenger vehicle (gCO2)
    "tree_day_gco2_absorption": 55.0,      # grams of CO2 absorbed per day by mature tree (~20kg/year)
    "led_light_hour_kwh": 0.010,           # 10W LED bulb for 1 hour = 0.010 kWh
    "boil_water_cup_kwh": 0.018,           # Boiling 250ml water kettle = 0.018 kWh
}
