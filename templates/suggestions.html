<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>AI Suggestions – CareerHealth.AI</title>
  <link rel="stylesheet" href="/static/css/style.css"/>
</head>
<body>

<nav class="navbar">
  <a class="navbar-brand" href="/dashboard">⚡ <span>CareerHealth</span>.AI</a>
  <div class="navbar-links">
    <a class="nav-link" href="/dashboard">← Dashboard</a>
    <a class="nav-link" href="/burnout">Burnout</a>
    <a class="nav-link" href="/productivity">Productivity</a>
    <a class="nav-link" href="/career">Career</a>
    <a class="btn-nav" href="/logout">Logout</a>
  </div>
</nav>

<div class="page-wrapper" style="padding-top:40px;padding-bottom:60px;">

  <div class="section-header" style="margin-bottom:32px;">
    <div class="section-icon warn">💡</div>
    <div>
      <div class="section-heading display">Personalized AI Suggestions</div>
      <div class="section-sub">Rule-based + ML hybrid engine · Combines Burnout, Productivity & Career predictions</div>
    </div>
  </div>

  <div class="predict-layout">

    <!-- INPUT -->
    <div>
      <div style="display:flex;gap:10px;margin-bottom:20px;">
        <button id="btn-manual" class="btn btn-primary" onclick="setMode('manual')">✏️ Manual Input</button>
        <button id="btn-auto"   class="btn btn-secondary" onclick="autoPredict()">⚡ Auto (Last Inputs)</button>
      </div>

      <div class="card">
        <div style="font-family:'Source Code Pro',monospace;font-size:.75rem;color:var(--muted);margin-bottom:18px;text-transform:uppercase;letter-spacing:.1em;">Your Profile</div>

        <div class="form-group">
          <label class="form-label">Stress Level</label>
          <div class="range-row">
            <input type="range" id="stress_level" min="1" max="10" value="5" step="1" style="flex:1;"/>
            <span class="range-val" id="stress_level_val">5</span>
            <span style="font-size:.78rem;color:var(--muted);">/ 10</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Working Hours / Day</label>
          <div class="range-row">
            <input type="range" id="working_hours" min="1" max="16" value="9" step="0.5" style="flex:1;"/>
            <span class="range-val" id="working_hours_val">9</span>
            <span style="font-size:.78rem;color:var(--muted);">hrs</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Sleep Hours / Day</label>
          <div class="range-row">
            <input type="range" id="sleep_hours" min="2" max="10" value="6" step="0.5" style="flex:1;"/>
            <span class="range-val" id="sleep_hours_val">6</span>
            <span style="font-size:.78rem;color:var(--muted);">hrs</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Work-Life Balance</label>
          <div class="range-row">
            <input type="range" id="work_life_balance" min="1" max="10" value="4" step="1" style="flex:1;"/>
            <span class="range-val" id="work_life_balance_val">4</span>
            <span style="font-size:.78rem;color:var(--muted);">/ 10</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Experience (Years)</label>
          <div class="range-row">
            <input type="range" id="experience_years" min="0" max="20" value="2" step="1" style="flex:1;"/>
            <span class="range-val" id="experience_years_val">2</span>
            <span style="font-size:.78rem;color:var(--muted);">yrs</span>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Number of Skills</label>
          <div class="range-row">
            <input type="range" id="skills_count" min="1" max="25" value="5" step="1" style="flex:1;"/>
            <span class="range-val" id="skills_count_val">5</span>
            <span style="font-size:.78rem;color:var(--muted);">skills</span>
          </div>
        </div>

        <button class="btn btn-primary btn-full" style="margin-top:8px;background:var(--warn);color:#080b14;" onclick="runPredict(false)">
          💡 Get AI Suggestions
        </button>
      </div>

      <div class="card" style="margin-top:16px;padding:16px 20px;">
        <div style="font-size:.8rem;color:var(--muted);line-height:1.8;">
          <strong style="color:var(--text);">How suggestions work:</strong><br/>
          This module runs all three ML models (burnout, productivity, career) on your input simultaneously,
          then generates personalized recommendations based on the combined results.
        </div>
      </div>
    </div>

    <!-- RESULT -->
    <div>
      <div class="loading-overlay" id="loading">
        <div class="spinner"></div>
        <div style="color:var(--muted);font-size:.9rem;">Running all 3 ML models + generating suggestions…</div>
      </div>

      <div id="placeholder" class="card" style="text-align:center;padding:60px 28px;color:var(--muted);">
        <div style="font-size:3rem;margin-bottom:16px;">💡</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;margin-bottom:8px;">No Suggestions Yet</div>
        <div style="font-size:.85rem;">Enter your profile data and click <strong>Get AI Suggestions</strong>.</div>
      </div>

      <div id="result-area" style="display:none;">

        <!-- SUMMARY ROW -->
        <div class="card" style="padding:20px 24px;margin-bottom:16px;">
          <div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">ML Analysis Summary</div>
          <div id="summary-row" style="font-family:'Source Code Pro',monospace;font-size:.88rem;color:var(--accent2);line-height:1.8;"></div>
        </div>

        <!-- SUGGESTIONS LIST -->
        <div class="card" style="padding:24px;">
          <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:18px;">
            📋 Your Personalized Action Plan
          </div>
          <div id="suggestions-list"></div>
        </div>

        <!-- INPUT ECHO -->
        <div class="card" style="margin-top:16px;padding:18px 22px;">
          <div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px;">Profile Analyzed</div>
          <div id="input-echo" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.85rem;"></div>
        </div>

      </div>
    </div>
  </div>
</div>

<script src="/static/js/main.js"></script>
<script>
const FIELDS = ['stress_level','working_hours','sleep_hours','work_life_balance','experience_years','skills_count'];

document.querySelectorAll('input[type=range]').forEach(s => {
  const out = document.getElementById(s.id + '_val');
  if (out) { out.textContent = s.value; s.addEventListener('input', () => out.textContent = s.value); }
});

function setMode(m) {
  document.getElementById('btn-manual').className = m === 'manual' ? 'btn btn-primary' : 'btn btn-secondary';
  document.getElementById('btn-auto').className   = m === 'auto'   ? 'btn btn-primary' : 'btn btn-secondary';
}

function autoPredict() {
  setMode('auto');
  const ranges = { stress_level:[1,10,0], working_hours:[4,14,1], sleep_hours:[4,9,1],
                   work_life_balance:[1,10,0], experience_years:[0,15,0], skills_count:[1,20,0] };
  Object.entries(ranges).forEach(([id,[mn,mx,dec]]) => {
    const el = document.getElementById(id);
    const val = dec ? (Math.random()*(mx-mn)+mn).toFixed(dec) : Math.floor(Math.random()*(mx-mn+1)+mn);
    el.value = val;
    const out = document.getElementById(id+'_val');
    if (out) out.textContent = val;
  });
  runPredict(true);
}

async function runPredict(auto) {
  const payload = auto ? {auto:true} : {auto:false, ...collectFormData(FIELDS)};
  document.getElementById('placeholder').style.display = 'none';
  document.getElementById('result-area').style.display = 'none';
  showLoading('loading');
  try {
    const data = await apiPost('/suggestions', payload);
    hideLoading('loading');
    renderResult(data);
  } catch(e) { hideLoading('loading'); alert('Error: '+e.message); }
}

function renderResult(d) {
  document.getElementById('summary-row').textContent = d.summary;

  const list = document.getElementById('suggestions-list');
  list.innerHTML = d.suggestions.map((s, i) =>
    `<div class="suggestion-item" style="animation-delay:${i * 0.06}s;">
       <div style="font-size:1.2rem;flex-shrink:0;">${s.charAt(0)}</div>
       <div>${s.slice(2)}</div>
     </div>`
  ).join('');

  const labels = { stress_level:'Stress', working_hours:'Working Hrs', sleep_hours:'Sleep Hrs',
                   work_life_balance:'Work-Life Bal.', experience_years:'Experience', skills_count:'Skills' };
  document.getElementById('input-echo').innerHTML = Object.entries(d.inputs).map(([k,v]) =>
    `<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--border);">
       <span style="color:var(--muted);">${labels[k]||k}</span>
       <span style="color:var(--accent2);font-weight:600;">${v}</span></div>`).join('');

  document.getElementById('result-area').style.display = 'block';
  document.getElementById('result-area').scrollIntoView({behavior:'smooth', block:'start'});
}
</script>
</body>
</html>
