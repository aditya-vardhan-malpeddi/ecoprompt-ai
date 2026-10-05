# 🌿 EcoPrompt AI

> **Green AI Intelligence & Carbon Footprint Auditor**
> *Audit token waste, measure LLM & cloud carbon footprints, and deploy resource-efficient AI systems.*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-10b981.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0-059669.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-06b6d4.svg)](LICENSE)

---

## 📖 Overview

**EcoPrompt AI** is a comprehensive sustainability and Green AI suite designed to quantify and minimize the environmental impact of modern artificial intelligence and digital operations. 

Modern Large Language Models (LLMs) consume significant electrical energy and water resources during inference. A significant portion of this energy is wasted on redundant conversational pleasantries, circular reasoning, unoptimized prompts, and running compute in carbon-heavy grid regions.

**EcoPrompt AI** solves this by offering:
1. **✨ EcoPrompt Auditor**: Analyzes prompts for token bloat, conversational fluff, and redundant preamble. Generates optimized, high-efficiency Green AI prompt rewrites and calculates saved energy (kWh) and $CO_2e$ emissions.
2. **⚡ AI Workload Carbon Calculator**: Models energy consumption and grid carbon emissions across LLM parameter scales (Edge/Flash to Giant Frontier models), quantization levels (FP16, INT8, INT4), and regional electricity grids.
3. **☁️ Cloud & GPU Auditor**: Measures carbon emissions for cloud VMs and dedicated GPU accelerators (e.g. A100, H100 clusters), identifying green datacenter relocation savings (e.g., migrating to hydro/nuclear-powered regions like Sweden or Oregon).
4. **🌍 Lifestyle & Commute Sustainability Scorecard**: Computes day-to-day commute, home energy, and dietary footprints with a personal eco-scorecard and Paris Agreement benchmark tracking.
5. **💡 Green AI Architecture Advisor & Migration Simulator**: Simulates the compounding environmental savings of switching model tiers, adopting quantization, and routing batch workloads to low-carbon grid hours.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone and Setup Environment

```bash
git clone https://github.com/aditya-vardhan-malpeddi/ecoprompt-ai.git
cd ecoprompt-ai

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Application

```bash
python run.py
```

Open your browser at:
- **Interactive Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger REST API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health Check**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 🛠️ Project Structure

```
ecoprompt-ai/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI REST API & routes
│   ├── config.py            # Regional emission factors, model energy profiles, constants
│   ├── models.py            # Pydantic schema validation models
│   ├── calculator.py        # Carbon calculation engine & real-world equivalents
│   ├── auditor.py           # EcoPrompt prompt trimmer & Green AI optimizer
│   ├── advisor.py           # Green AI guidelines & migration scenario simulator
│   └── static/
│       ├── index.html       # Responsive, modern dashboard UI
│       ├── style.css        # Eco-modern glassmorphism CSS
│       └── app.js           # Client reactivity, Chart.js integrations, API calls
├── tests/
│   ├── __init__.py
│   └── test_core.py         # Pytest test suite (11 unit tests)
├── requirements.txt         # Pinned production and test dependencies
├── run.py                   # One-click application runner
└── README.md
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/health` | `GET` | Health check and feature capability registry |
| `/api/config/meta` | `GET` | Retrieves regional grid intensities, model profiles, and hardware specs |
| `/api/audit/prompt` | `POST` | Audits a prompt, returns token reduction, clean rewrite, and saved $CO_2$ |
| `/api/calculate/footprint` | `POST` | Calculates AI inference kWh, $CO_2e$, and regional comparative benchmarks |
| `/api/calculate/cloud` | `POST` | Computes cloud VM / GPU cluster carbon footprints and green migration savings |
| `/api/calculate/lifestyle` | `POST` | Computes personal lifestyle footprint, breakdown, and eco-grade |
| `/api/simulate/migration` | `POST` | Simulates compounding savings of architectural changes (model, quantization, region) |
| `/api/recommendations` | `GET` | Returns prioritized Green AI best practice guidelines |

---

## 🧪 Running Tests

To run the unit test suite:

```bash
pytest tests/ -v
```

All 11 tests validate token estimation, regex optimization rules, energy consumption models, regional grid intensities, equivalents calculations, and REST API endpoints.

---

## 📊 Scientific Methodology & Emission Factors

- **Grid Carbon Intensity ($gCO_2e/\text{kWh}$)**: Sourced from national grid averages and the International Energy Agency (IEA). E.g., Sweden (~25 $gCO_2e/\text{kWh}$), US West Hydro (~115 $gCO_2e/\text{kWh}$), Global Average (~440 $gCO_2e/\text{kWh}$).
- **Datacenter PUE**: Accounts for hyperscale cooling and facility power overhead using an industry standard baseline PUE of 1.15.
- **AI Model Energy Profiles**: Inference FLOP-to-kWh conversions calibrated on state-of-the-art accelerator benchmarks (TPU v5e, NVIDIA H100/A100) across model parameter tiers:
  - Compact Edge / Flash (<8B params): ~0.00015 kWh / 1,000 tokens
  - Balanced General (8B–35B params): ~0.00065 kWh / 1,000 tokens
  - Large Frontier (70B–120B params): ~0.00160 kWh / 1,000 tokens
  - Giant Frontier / Reasoning (200B+ params): ~0.00340 kWh / 1,000 tokens
- **Quantization Efficiency**: INT8 delivers ~38% power reduction; INT4 delivers ~62% power reduction over standard FP16.

---

## 📄 License

This project is licensed under the MIT License.