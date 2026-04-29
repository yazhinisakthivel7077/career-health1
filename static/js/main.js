/* static/js/main.js — shared utilities */

// ── Range slider live value display ──────────────
document.querySelectorAll('input[type=range]').forEach(slider => {
  const out = document.getElementById(slider.id + '_val');
  if (out) {
    out.textContent = slider.value;
    slider.addEventListener('input', () => { out.textContent = slider.value; });
  }
});

// ── Fill form with auto-generated values ─────────
function fillAutoValues(ranges) {
  Object.entries(ranges).forEach(([id, [min, max, decimals]]) => {
    const el = document.getElementById(id);
    if (!el) return;
    const val = decimals
      ? (Math.random() * (max - min) + min).toFixed(decimals)
      : Math.floor(Math.random() * (max - min + 1) + min);
    el.value = val;
    const out = document.getElementById(id + '_val');
    if (out) out.textContent = val;
    el.dispatchEvent(new Event('input'));
  });
}

// ── Collect form values into object ──────────────
function collectFormData(fieldIds) {
  const data = {};
  fieldIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) data[id] = parseFloat(el.value);
  });
  return data;
}

// ── Render result badge ───────────────────────────
function resultClass(label) {
  const l = label.toLowerCase();
  if (l.includes('high'))   return 'result-high';
  if (l.includes('medium')) return 'result-medium';
  if (l.includes('low'))    return 'result-low';
  if (l.includes('ready') && !l.includes('not') && !l.includes('needs')) return 'result-ready';
  if (l.includes('moderate')) return 'result-moderate';
  if (l.includes('needs') || l.includes('improvement')) return 'result-needs';
  return '';
}

function badgeClass(label) {
  const l = label.toLowerCase();
  if (l.includes('high'))   return 'badge-high';
  if (l.includes('medium')) return 'badge-medium';
  if (l.includes('low'))    return 'badge-low';
  if (l.includes('ready') && !l.includes('needs')) return 'badge-ready';
  if (l.includes('moderate')) return 'badge-moderate';
  return 'badge-medium';
}

// ── API POST helper ───────────────────────────────
async function apiPost(endpoint, payload) {
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Network error');
  return res.json();
}

// ── Show / hide loading overlay ───────────────────
function showLoading(id)  { const el = document.getElementById(id); if (el) el.style.display = 'block'; }
function hideLoading(id)  { const el = document.getElementById(id); if (el) el.style.display = 'none'; }
function showEl(id)       { const el = document.getElementById(id); if (el) el.style.display = 'block'; }
function hideEl(id)       { const el = document.getElementById(id); if (el) el.style.display = 'none'; }
