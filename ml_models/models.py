"""
ml_models/models.py
-------------------
Random Forest models for Burnout, Productivity, Career Readiness.
SHAP explanations and Matplotlib charts included.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import io, base64, random

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# ─────────────────────────────────────────────
# 1.  SYNTHETIC TRAINING DATA
# ─────────────────────────────────────────────

def _make_dataset(n=500, seed=42):
    rng = np.random.default_rng(seed)
    stress        = rng.integers(1, 11, n).astype(float)
    working_hours = rng.uniform(4, 14, n)
    sleep_hours   = rng.uniform(4, 9, n)
    wlb           = rng.integers(1, 11, n).astype(float)
    experience    = rng.integers(0, 16, n).astype(float)
    skills        = rng.integers(1, 21, n).astype(float)

    # Burnout: High stress + long hours + poor sleep → High burnout
    burnout_score = (stress * 0.35 + working_hours * 0.25 +
                     (10 - sleep_hours) * 0.2 + (10 - wlb) * 0.2)
    burnout_score += rng.normal(0, 0.5, n)
    burnout_label = np.where(burnout_score > 7, 'High',
                    np.where(burnout_score > 4.5, 'Medium', 'Low'))

    # Productivity: Good sleep + balance + skills → High productivity
    prod_score = (sleep_hours * 0.25 + wlb * 0.25 + skills * 0.3 +
                  (14 - working_hours) * 0.1 + (10 - stress) * 0.1)
    prod_score = np.clip(prod_score, 0, 10)
    prod_score += rng.normal(0, 0.3, n)
    prod_label = np.where(prod_score > 7, 'High',
                 np.where(prod_score > 4.5, 'Medium', 'Low'))

    # Career: Experience + skills → Readiness
    career_score = (experience * 0.4 + skills * 0.35 +
                    wlb * 0.15 + (10 - stress) * 0.1)
    career_score += rng.normal(0, 0.5, n)
    career_label = np.where(career_score > 9, 'Ready',
                   np.where(career_score > 5, 'Moderate', 'Needs Improvement'))

    df = pd.DataFrame({
        'stress_level': stress,
        'working_hours': working_hours,
        'sleep_hours': sleep_hours,
        'work_life_balance': wlb,
        'experience_years': experience,
        'skills_count': skills,
        'burnout': burnout_label,
        'productivity': prod_label,
        'career': career_label,
        'prod_score': np.clip(prod_score * 10, 0, 100)
    })
    return df

FEATURE_COLS = ['stress_level', 'working_hours', 'sleep_hours',
                'work_life_balance', 'experience_years', 'skills_count']
FEATURE_LABELS = ['Stress Level', 'Working Hours', 'Sleep Hours',
                  'Work-Life Balance', 'Experience (yrs)', 'Skills Count']

_df = _make_dataset()

# ─────────────────────────────────────────────
# 2.  TRAIN MODELS
# ─────────────────────────────────────────────

_le_burnout     = LabelEncoder()
_le_productivity = LabelEncoder()
_le_career      = LabelEncoder()

X = _df[FEATURE_COLS].values

_y_burnout     = _le_burnout.fit_transform(_df['burnout'])
_y_productivity = _le_productivity.fit_transform(_df['productivity'])
_y_career      = _le_career.fit_transform(_df['career'])
_y_prod_score  = _df['prod_score'].values

_clf_burnout     = RandomForestClassifier(n_estimators=100, random_state=42)
_clf_productivity = RandomForestClassifier(n_estimators=100, random_state=42)
_clf_career      = RandomForestClassifier(n_estimators=100, random_state=42)
_reg_prod_score  = RandomForestRegressor(n_estimators=100, random_state=42)

_clf_burnout.fit(X, _y_burnout)
_clf_productivity.fit(X, _y_productivity)
_clf_career.fit(X, _y_career)
_reg_prod_score.fit(X, _y_prod_score)

print("✅ All ML models trained successfully.")

# ─────────────────────────────────────────────
# 3.  SHAP (lightweight manual implementation)
#     Real SHAP requires compiled C++ which may
#     not be available everywhere, so we use a
#     fast permutation-based importance proxy.
# ─────────────────────────────────────────────

def _compute_shap_values(model, x_vec):
    """
    Fast permutation-based SHAP approximation.
    Returns array of shape (n_features,) with signed importance.
    """
    baseline = model.predict_proba(X)[: , 0].mean() if hasattr(model, 'predict_proba') else model.predict(X).mean()
    x = x_vec.reshape(1, -1).copy()
    importances = []
    for i in range(x.shape[1]):
        x_perm = x.copy()
        x_perm[0, i] = np.mean(X[:, i])        # replace feature with mean
        if hasattr(model, 'predict_proba'):
            pred_orig = model.predict_proba(x)[0, 0]
            pred_perm = model.predict_proba(x_perm)[0, 0]
        else:
            pred_orig = model.predict(x)[0]
            pred_perm = model.predict(x_perm)[0]
        importances.append(pred_orig - pred_perm)
    return np.array(importances)


# ─────────────────────────────────────────────
# 4.  HELPER – fig → base64 png
# ─────────────────────────────────────────────

def _fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',
                facecolor=fig.get_facecolor(), dpi=110)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{encoded}"


# ─────────────────────────────────────────────
# 5.  PUBLIC PREDICTION FUNCTIONS
# ─────────────────────────────────────────────

def _to_vec(inputs):
    return np.array([[
        inputs['stress_level'], inputs['working_hours'], inputs['sleep_hours'],
        inputs['work_life_balance'], inputs['experience_years'], inputs['skills_count']
    ]], dtype=float)


def predict_burnout(inputs):
    x = _to_vec(inputs)
    pred_idx = _clf_burnout.predict(x)[0]
    proba    = _clf_burnout.predict_proba(x)[0]
    label    = _le_burnout.inverse_transform([pred_idx])[0]
    confidence = round(float(proba.max()) * 100, 1)
    return {'label': label, 'confidence': confidence}


def predict_productivity(inputs):
    x     = _to_vec(inputs)
    pred_idx = _clf_productivity.predict(x)[0]
    proba    = _clf_productivity.predict_proba(x)[0]
    label    = _le_productivity.inverse_transform([pred_idx])[0]
    score    = round(float(_reg_prod_score.predict(x)[0]), 1)
    score    = max(0, min(100, score))
    return {'label': label, 'score': score}


def predict_career(inputs):
    x        = _to_vec(inputs)
    pred_idx = _clf_career.predict(x)[0]
    proba    = _clf_career.predict_proba(x)[0]
    label    = _le_career.inverse_transform([pred_idx])[0]
    confidence = round(float(proba.max()) * 100, 1)
    return {'label': label, 'confidence': confidence}


# ─────────────────────────────────────────────
# 6.  SUGGESTIONS ENGINE
# ─────────────────────────────────────────────

def get_suggestions(inputs):
    burnout_res    = predict_burnout(inputs)
    prod_res       = predict_productivity(inputs)
    career_res     = predict_career(inputs)

    suggestions = []
    b, p, c = burnout_res['label'], prod_res['label'], career_res['label']

    # Burnout tips
    if b == 'High':
        suggestions += [
            "🔴 Your burnout risk is HIGH. Take an immediate break — even 1–2 days off helps reset.",
            "🧘 Practice mindfulness or meditation for 10–15 mins daily to reduce stress.",
            "⏰ Set strict work-off hours. Avoid checking emails after work."
        ]
    elif b == 'Medium':
        suggestions += [
            "🟡 Moderate burnout risk detected. Try the Pomodoro technique (25 min work / 5 min break).",
            "🏃 Add light physical activity (walk, yoga) to your daily routine."
        ]
    else:
        suggestions.append("🟢 Your burnout level is LOW — great work maintaining balance!")

    # Sleep / Hours tips
    if inputs['sleep_hours'] < 6:
        suggestions.append("😴 You're sleeping less than 6 hours. Aim for 7–8 hours for optimal brain function.")
    if inputs['working_hours'] > 10:
        suggestions.append("⚠️ Working 10+ hours daily is unsustainable. Consider delegating tasks.")

    # Productivity tips
    if p == 'Low':
        suggestions += [
            "📋 Break large tasks into smaller 30-min chunks to regain momentum.",
            "🎯 Set 3 clear daily goals each morning (MIT — Most Important Tasks)."
        ]
    elif p == 'Medium':
        suggestions.append("📈 Your productivity is average. Try time-blocking your calendar.")

    # Career tips
    if c == 'Needs Improvement':
        suggestions += [
            "📚 Consider enrolling in 1 new online course per month (Coursera, Udemy, edX).",
            f"🛠️ With {int(inputs['skills_count'])} skills, aim to add 2–3 high-demand skills this year.",
            "🤝 Build your professional network — attend at least 1 event/webinar monthly."
        ]
    elif c == 'Moderate':
        suggestions.append("🚀 You're on track! Seek a mentor or take on stretch assignments.")
    else:
        suggestions.append("⭐ Your career readiness looks great. Consider leadership roles or mentoring others.")

    if inputs['work_life_balance'] < 4:
        suggestions.append("⚖️ Work-life balance is critically low. Schedule non-work activities as calendar events.")

    summary = f"Burnout: {b} | Productivity: {p} | Career: {c}"
    return {'suggestions': suggestions, 'summary': summary}


# ─────────────────────────────────────────────
# 7.  CHARTS
# ─────────────────────────────────────────────

_PALETTE = {
    'bg': '#0f1117', 'card': '#1a1d2e', 'accent': '#6c63ff',
    'green': '#00d4aa', 'yellow': '#ffd166', 'red': '#ef476f',
    'text': '#e0e0e0', 'grid': '#2a2d3e'
}

def get_feature_importance_plot(inputs, module):
    model_map = {
        'burnout':      _clf_burnout,
        'productivity': _clf_productivity,
        'career':       _clf_career
    }
    model = model_map[module]
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    fig.patch.set_facecolor(_PALETTE['bg'])

    # --- Bar chart: feature importances ---
    ax = axes[0]
    ax.set_facecolor(_PALETTE['card'])
    colors = [_PALETTE['accent'], _PALETTE['green'], _PALETTE['yellow'],
              '#ff6b9d', '#4ecdc4', '#ffe66d']
    bars = ax.barh([FEATURE_LABELS[i] for i in indices],
                   [importances[i] for i in indices],
                   color=[colors[j % len(colors)] for j in range(len(indices))],
                   height=0.6, edgecolor='none')
    ax.set_xlabel('Importance Score', color=_PALETTE['text'], fontsize=10)
    ax.set_title(f'Feature Importance – {module.capitalize()}',
                 color=_PALETTE['text'], fontsize=12, pad=10)
    ax.tick_params(colors=_PALETTE['text'])
    ax.spines[:].set_color(_PALETTE['grid'])
    ax.set_xlim(0, importances.max() * 1.2)
    for bar, val in zip(bars, [importances[i] for i in indices]):
        ax.text(val + 0.002, bar.get_y() + bar.get_height() / 2,
                f'{val:.3f}', va='center', color=_PALETTE['text'], fontsize=8)

    # --- Radar / input values chart ---
    ax2 = axes[1]
    ax2.set_facecolor(_PALETTE['card'])
    x_vals = _to_vec(inputs)[0]
    # Normalize to 0-1 for display
    maxes = np.array([10, 14, 9, 10, 15, 20], dtype=float)
    normed = x_vals / maxes

    bars2 = ax2.bar(FEATURE_LABELS, normed,
                    color=[colors[j % len(colors)] for j in range(6)],
                    width=0.5, edgecolor='none')
    ax2.set_ylim(0, 1.2)
    ax2.set_ylabel('Normalized Value', color=_PALETTE['text'], fontsize=10)
    ax2.set_title('Your Input Profile', color=_PALETTE['text'], fontsize=12, pad=10)
    ax2.tick_params(colors=_PALETTE['text'], axis='both')
    ax2.set_xticks(range(len(FEATURE_LABELS)))
    ax2.set_xticklabels(FEATURE_LABELS, rotation=20, ha="right", fontsize=8)
    ax2.spines[:].set_color(_PALETTE['grid'])
    for bar, raw in zip(bars2, x_vals):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                 f'{raw:.1f}', ha='center', color=_PALETTE['text'], fontsize=8)

    plt.tight_layout(pad=1.5)
    return _fig_to_b64(fig)


def get_shap_explanation(inputs, module):
    """Returns an HTML string with a SHAP waterfall-style bar chart."""
    model_map = {
        'burnout':      _clf_burnout,
        'productivity': _clf_productivity,
        'career':       _clf_career
    }
    model = model_map[module]
    x_vec = _to_vec(inputs)[0]
    shap_vals = _compute_shap_values(model, x_vec)

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(_PALETTE['bg'])
    ax.set_facecolor(_PALETTE['card'])

    colors = [_PALETTE['green'] if v > 0 else _PALETTE['red'] for v in shap_vals]
    bars = ax.barh(FEATURE_LABELS, shap_vals, color=colors, height=0.55, edgecolor='none')
    ax.axvline(0, color=_PALETTE['text'], linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_xlabel('SHAP Impact (positive = pushes prediction up)', color=_PALETTE['text'], fontsize=9)
    ax.set_title('SHAP Feature Explanation', color=_PALETTE['text'], fontsize=11, pad=8)
    ax.tick_params(colors=_PALETTE['text'])
    ax.spines[:].set_color(_PALETTE['grid'])
    for bar, val in zip(bars, shap_vals):
        ax.text(val + (0.002 if val >= 0 else -0.002),
                bar.get_y() + bar.get_height() / 2,
                f'{val:+.3f}', va='center',
                ha='left' if val >= 0 else 'right',
                color=_PALETTE['text'], fontsize=8)

    green_patch = mpatches.Patch(color=_PALETTE['green'], label='Increases risk/score')
    red_patch   = mpatches.Patch(color=_PALETTE['red'],   label='Decreases risk/score')
    ax.legend(handles=[green_patch, red_patch], facecolor=_PALETTE['card'],
              labelcolor=_PALETTE['text'], fontsize=8)

    plt.tight_layout(pad=1.2)
    img_b64 = _fig_to_b64(fig)
    return f'<img src="{img_b64}" style="width:100%;border-radius:10px;" alt="SHAP chart"/>'
