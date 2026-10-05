/**
 * EcoPrompt AI - Client Application Logic
 */

let metaConfig = null;
let regionalChart = null;
let lifestyleChart = null;

const VERBOSE_SAMPLE_PROMPT = 
`Please could you kindly act as an expert senior machine learning engineer and please give me a comprehensive, detailed and exhaustive summary of this paper due to the fact that I need it for the purpose of a meeting at the present moment in time. Make sure to be sure to write a response that is easy to understand, and take note that it is important to include key metrics. Thank you so much in advance for your kind help!`;

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  initTabs();
  initCounters();
  await loadMetadata();
  initSampleButton();
  initCopyButton();
  initEventListeners();
  
  // Run initial calculations with defaults
  runPromptAudit();
  runCalculator();
  runCloudAudit();
  runLifestyleAudit();
  runSimulation();
  loadAdvisorCards();
});

// Setup tab navigation
function initTabs() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-tab');
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add('active');
    });
  });
}

// Live character and estimated token counter
function initCounters() {
  const textarea = document.getElementById('prompt-input');
  const counter = document.getElementById('char-token-counter');

  function update() {
    const text = textarea.value.trim();
    if (!text) {
      counter.textContent = 'Estimated Tokens: 0';
      return;
    }
    const words = text.match(/\w+|[^\w\s]/g) || [];
    const tokens = Math.max(1, Math.round(words.length * 1.15));
    counter.textContent = `Estimated Tokens: ~${tokens} (${text.length} chars)`;
  }

  textarea.addEventListener('input', update);
}

function initSampleButton() {
  const btn = document.getElementById('btn-load-sample');
  const textarea = document.getElementById('prompt-input');
  btn.addEventListener('click', () => {
    textarea.value = VERBOSE_SAMPLE_PROMPT;
    textarea.dispatchEvent(new Event('input'));
  });
}

function initCopyButton() {
  const copyBtn = document.getElementById('btn-copy-prompt');
  const outputTextarea = document.getElementById('optimized-prompt-output');

  copyBtn.addEventListener('click', async () => {
    if (!outputTextarea.value) return;
    try {
      await navigator.clipboard.writeText(outputTextarea.value);
      const originalText = copyBtn.textContent;
      copyBtn.textContent = '✓ Copied!';
      copyBtn.style.color = '#34d399';
      setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.color = '';
      }, 1800);
    } catch (e) {
      console.error('Clipboard copy failed:', e);
    }
  });
}

// Load metadata and populate select elements
async function loadMetadata() {
  try {
    const res = await fetch('/api/config/meta');
    metaConfig = await res.json();

    populateRegionDropdown('audit-region', 'global_avg');
    populateRegionDropdown('calc-region', 'global_avg');
    populateRegionDropdown('cloud-region', 'us_east_virginia');
    populateRegionDropdown('life-region', 'global_avg');
    populateRegionDropdown('sim-curr-region', 'us_east_virginia');
    populateRegionDropdown('sim-targ-region', 'us_west_oregon');

    populateModelDropdown('calc-model-tier', 'medium_balanced');
    populateCloudDropdown('cloud-instance', 'gpu_single_a100');
  } catch (err) {
    console.error('Failed to load configuration metadata:', err);
  }
}

function populateRegionDropdown(selectId, defaultKey) {
  const el = document.getElementById(selectId);
  if (!el || !metaConfig || !metaConfig.regions) return;
  el.innerHTML = '';
  for (const [key, val] of Object.entries(metaConfig.regions)) {
    const opt = document.createElement('option');
    opt.value = key;
    opt.textContent = `${val.name} (${val.intensity} gCO₂/kWh)`;
    if (key === defaultKey) opt.selected = true;
    el.appendChild(opt);
  }
}

function populateModelDropdown(selectId, defaultKey) {
  const el = document.getElementById(selectId);
  if (!el || !metaConfig || !metaConfig.models) return;
  el.innerHTML = '';
  for (const [key, val] of Object.entries(metaConfig.models)) {
    const opt = document.createElement('option');
    opt.value = key;
    opt.textContent = `${val.name}`;
    if (key === defaultKey) opt.selected = true;
    el.appendChild(opt);
  }
}

function populateCloudDropdown(selectId, defaultKey) {
  const el = document.getElementById(selectId);
  if (!el || !metaConfig || !metaConfig.cloud_instances) return;
  el.innerHTML = '';
  for (const [key, val] of Object.entries(metaConfig.cloud_instances)) {
    const opt = document.createElement('option');
    opt.value = key;
    opt.textContent = `${val.name} (~${val.kwh} kWh/hr)`;
    if (key === defaultKey) opt.selected = true;
    el.appendChild(opt);
  }
}

function initEventListeners() {
  document.getElementById('btn-run-audit').addEventListener('click', runPromptAudit);
  document.getElementById('btn-run-calculator').addEventListener('click', runCalculator);
  document.getElementById('btn-run-cloud').addEventListener('click', runCloudAudit);
  document.getElementById('btn-run-lifestyle').addEventListener('click', runLifestyleAudit);
  document.getElementById('btn-run-sim').addEventListener('click', runSimulation);
}

// 1. EcoPrompt Audit Action
async function runPromptAudit() {
  let promptText = document.getElementById('prompt-input').value.trim();
  if (!promptText) {
    promptText = VERBOSE_SAMPLE_PROMPT;
    document.getElementById('prompt-input').value = promptText;
    document.getElementById('prompt-input').dispatchEvent(new Event('input'));
  }

  const payload = {
    prompt: promptText,
    model_tier: document.getElementById('audit-model-tier').value,
    quantization: document.getElementById('audit-quantization').value,
    region: document.getElementById('audit-region').value,
    expected_calls_per_month: parseInt(document.getElementById('audit-monthly-calls').value, 10) || 10000
  };

  try {
    const res = await fetch('/api/audit/prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    document.getElementById('res-token-reduction').textContent = `${data.token_reduction_pct}%`;
    document.getElementById('res-token-diff').textContent = `${data.original_token_count} → ${data.optimized_token_count} tokens`;
    
    // Carbon saved formatting
    const gco2 = data.monthly_gco2_saved;
    if (gco2 > 1000) {
      document.getElementById('res-co2-saved').textContent = `${(gco2 / 1000).toFixed(2)} kg`;
    } else {
      document.getElementById('res-co2-saved').textContent = `${gco2.toFixed(1)} g`;
    }
    document.getElementById('res-kwh-saved').textContent = `${data.monthly_kwh_saved.toFixed(3)} kWh/mo`;
    document.getElementById('res-clarity-score').textContent = `${data.readability_and_clarity_score}/100`;
    document.getElementById('audit-eco-grade-badge').textContent = `Eco Grade: ${data.eco_grade}`;

    document.getElementById('optimized-prompt-output').value = data.optimized_prompt;

    // Suggestions list
    const list = document.getElementById('audit-suggestions-list');
    list.innerHTML = '';
    data.suggestions.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      list.appendChild(li);
    });

    // Equivalents
    document.getElementById('eq-phones').textContent = data.equivalents.smartphone_charges.toLocaleString();
    document.getElementById('eq-car-km').textContent = `${data.equivalents.km_car_driven} km`;
    document.getElementById('eq-tree-days').textContent = `${data.equivalents.tree_days_needed} days`;

  } catch (err) {
    console.error('Audit failed:', err);
  }
}

// 2. AI Carbon Calculator Action
async function runCalculator() {
  const payload = {
    model_tier: document.getElementById('calc-model-tier').value || 'medium_balanced',
    quantization: document.getElementById('calc-quantization').value,
    region: document.getElementById('calc-region').value || 'global_avg',
    input_tokens: parseInt(document.getElementById('calc-input-tokens').value, 10) || 2000,
    output_tokens: parseInt(document.getElementById('calc-output-tokens').value, 10) || 600,
    monthly_requests: parseInt(document.getElementById('calc-monthly-reqs').value, 10) || 100000,
  };

  try {
    const res = await fetch('/api/calculate/footprint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    document.getElementById('calc-clean-energy-share').textContent = `Clean Grid: ${data.clean_energy_share}%`;
    document.getElementById('calc-monthly-kwh').textContent = `${data.monthly_kwh.toLocaleString()} kWh`;
    document.getElementById('calc-per-req-kwh').textContent = `${(data.kwh_per_request * 1000).toFixed(4)} Wh / req`;
    document.getElementById('calc-monthly-kg-co2').textContent = `${data.monthly_kg_co2.toLocaleString()} kg CO₂`;
    document.getElementById('calc-annual-kg-co2').textContent = `Annual: ${(data.annual_kg_co2 / 1000).toFixed(2)} metric tons`;

    renderRegionalChart(data.regional_comparisons, data.region_name);
  } catch (err) {
    console.error('Calculator failed:', err);
  }
}

function renderRegionalChart(comparisons, currentRegionName) {
  const ctx = document.getElementById('regionalComparisonChart').getContext('2d');
  
  // Select top 6 interesting regions
  const topRegions = comparisons.slice(0, 7);
  const labels = topRegions.map(r => r.region_name.split(' (')[0]);
  const dataValues = topRegions.map(r => r.annual_kg_co2);
  const backgroundColors = topRegions.map(r => 
    r.region_name.includes(currentRegionName) ? '#06b6d4' : (r.intensity_gco2_kwh < 150 ? '#10b981' : '#f59e0b')
  );

  if (regionalChart) {
    regionalChart.destroy();
  }

  regionalChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Annual kg CO₂e',
        data: dataValues,
        backgroundColor: backgroundColors,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Annual: ${ctx.raw.toLocaleString()} kg CO₂`
          }
        }
      },
      scales: {
        x: {
          ticks: { color: '#94a3b8', font: { size: 10 } },
          grid: { display: false }
        },
        y: {
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        }
      }
    }
  });
}

// 3. Cloud & GPU Footprint Action
async function runCloudAudit() {
  const payload = {
    instance_type: document.getElementById('cloud-instance').value || 'gpu_single_a100',
    region: document.getElementById('cloud-region').value || 'us_east_virginia',
    instance_count: parseInt(document.getElementById('cloud-count').value, 10) || 1,
    hours_per_day: parseFloat(document.getElementById('cloud-hours').value) || 12,
    days_per_month: parseInt(document.getElementById('cloud-days').value, 10) || 22,
  };

  try {
    const res = await fetch('/api/calculate/cloud', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    document.getElementById('cloud-savings-chip').textContent = `Save up to ${data.potential_co2_savings_pct}%`;
    document.getElementById('cloud-res-kwh').textContent = `${data.monthly_kwh.toLocaleString()} kWh`;
    document.getElementById('cloud-res-hours').textContent = `${data.total_hours_month} hrs / mo`;
    document.getElementById('cloud-res-annual-kg').textContent = `${data.annual_kg_co2.toLocaleString()} kg`;
    document.getElementById('cloud-res-monthly-kg').textContent = `${data.monthly_kg_co2} kg/mo`;

    document.getElementById('cloud-green-alt-region').textContent = data.green_alternative_region;
    document.getElementById('cloud-green-savings-pct').textContent = `${data.potential_co2_savings_pct}%`;
    document.getElementById('cloud-green-saved-kg').textContent = `${data.potential_kg_co2_saved_annual.toLocaleString()} kg`;

    document.getElementById('cloud-eq-trees').textContent = `${data.equivalents.tree_days_needed} days`;
    document.getElementById('cloud-eq-car').textContent = `${data.equivalents.km_car_driven} km`;
  } catch (err) {
    console.error('Cloud audit failed:', err);
  }
}

// 4. Lifestyle & Commute Audit Action
async function runLifestyleAudit() {
  const payload = {
    commute_mode: document.getElementById('life-commute-mode').value,
    commute_km_weekly: parseFloat(document.getElementById('life-commute-km').value) || 120,
    home_electricity_kwh_monthly: parseFloat(document.getElementById('life-home-kwh').value) || 320,
    diet_type: document.getElementById('life-diet').value,
    region: document.getElementById('life-region').value || 'global_avg'
  };

  try {
    const res = await fetch('/api/calculate/lifestyle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    document.getElementById('life-grade-badge').textContent = `Score: ${data.eco_grade.split(' ')[0]}`;
    document.getElementById('life-annual-tons').textContent = `${data.total_annual_tons_co2} t`;
    document.getElementById('life-monthly-kg').textContent = `${data.total_monthly_kg_co2} kg/mo`;

    const recList = document.getElementById('life-recommendations-list');
    recList.innerHTML = '';
    data.key_recommendations.forEach(rec => {
      const li = document.createElement('li');
      li.textContent = rec;
      recList.appendChild(li);
    });

    renderLifestyleChart(data.breakdown_percentages);
  } catch (err) {
    console.error('Lifestyle audit failed:', err);
  }
}

function renderLifestyleChart(percentages) {
  const ctx = document.getElementById('lifestyleDonutChart').getContext('2d');
  const labels = Object.keys(percentages);
  const values = Object.values(percentages);

  if (lifestyleChart) {
    lifestyleChart.destroy();
  }

  lifestyleChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: ['#06b6d4', '#10b981', '#f59e0b'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { color: '#94a3b8', font: { size: 11 } }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.label}: ${ctx.raw}%`
          }
        }
      },
      cutout: '70%'
    }
  });
}

// 5. Green AI Advisor & Migration Simulator
async function runSimulation() {
  const payload = {
    current_tier: document.getElementById('sim-curr-tier').value,
    target_tier: document.getElementById('sim-targ-tier').value,
    current_region: document.getElementById('sim-curr-region').value,
    target_region: document.getElementById('sim-targ-region').value,
    current_quantization: document.getElementById('sim-curr-quant').value,
    target_quantization: document.getElementById('sim-targ-quant').value,
    monthly_tokens: parseInt(document.getElementById('sim-tokens').value, 10) || 50000000
  };

  try {
    const res = await fetch('/api/simulate/migration', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    const sav = data.annual_savings;

    document.getElementById('sim-saved-pct').textContent = `${sav.co2_reduction_pct}%`;
    document.getElementById('sim-saved-kg').textContent = `${sav.kg_co2_saved.toLocaleString()} kg CO₂ / yr`;
    document.getElementById('sim-saved-kwh').textContent = `${sav.kwh_saved.toLocaleString()} kWh / yr`;
    document.getElementById('sim-tons-metric').textContent = `${sav.metric_tons_co2_saved} metric tons avoided`;
    document.getElementById('sim-trees-equiv').textContent = `${sav.equivalent_trees_planted_10yr.toLocaleString()} 🌲`;
    document.getElementById('sim-car-equiv').textContent = `${sav.equivalent_car_miles_avoided.toLocaleString()} miles avoided`;
  } catch (err) {
    console.error('Simulation failed:', err);
  }
}

async function loadAdvisorCards() {
  try {
    const res = await fetch('/api/recommendations');
    const data = await res.json();
    const container = document.getElementById('advisor-cards-container');
    container.innerHTML = '';

    data.recommendations.forEach(rec => {
      const card = document.createElement('div');
      card.className = 'advisor-card';
      
      let itemsHtml = '';
      rec.action_items.forEach(item => {
        itemsHtml += `<li>${item}</li>`;
      });

      card.innerHTML = `
        <div class="advisor-card-top">
          <span class="advisor-category">${rec.category}</span>
          <span class="advisor-impact-badge">${rec.impact}</span>
        </div>
        <h3>${rec.title}</h3>
        <p>${rec.description}</p>
        <ul class="styled-list">
          ${itemsHtml}
        </ul>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error('Failed to load advisor cards:', err);
  }
}
