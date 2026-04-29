from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import numpy as np
import pandas as pd
import json
import os
import base64
import io
import random

from ml_models.models import (
    predict_burnout, predict_productivity, predict_career,
    get_suggestions, get_feature_importance_plot, get_shap_explanation
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'career_health_secret_2024')

# ─────────────────────────────────────────────
# OPEN USER STORE — any username can register
# Format: { 'username': 'password' }
# Stored in memory (resets on server restart)
# ─────────────────────────────────────────────
USER_DB = {}

# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()
        action   = request.form.get('action', 'login')   # 'login' or 'register'

        if not username or not password:
            return render_template('login.html', error='Username and password cannot be empty.')
        if len(username) < 3:
            return render_template('login.html', error='Username must be at least 3 characters.')
        if len(password) < 4:
            return render_template('login.html', error='Password must be at least 4 characters.')

        if action == 'register':
            if username in USER_DB:
                return render_template('login.html',
                    error=f'Username "{username}" is already taken. Please log in instead.')
            USER_DB[username] = password
            session['logged_in'] = True
            session['username']  = username
            return redirect(url_for('dashboard'))

        else:  # login
            if username not in USER_DB:
                return render_template('login.html',
                    error=f'No account for "{username}". Use Register to create one.')
            if USER_DB[username] != password:
                return render_template('login.html', error='Incorrect password. Please try again.')
            session['logged_in'] = True
            session['username']  = username
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username', 'User'))

# ─────────────────────────────────────────────
# MODULE PAGES
# ─────────────────────────────────────────────

@app.route('/burnout')
def burnout_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('burnout.html')

@app.route('/productivity')
def productivity_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('productivity.html')

@app.route('/career')
def career_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('career.html')

@app.route('/suggestions')
def suggestions_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('suggestions.html')

# ─────────────────────────────────────────────
# API ENDPOINTS
# ─────────────────────────────────────────────

def parse_input(data, auto=False):
    if auto:
        return {
            'stress_level':      random.randint(1, 10),
            'working_hours':     round(random.uniform(4, 14), 1),
            'sleep_hours':       round(random.uniform(4, 9), 1),
            'work_life_balance': random.randint(1, 10),
            'experience_years':  random.randint(0, 15),
            'skills_count':      random.randint(1, 20)
        }
    return {
        'stress_level':      float(data.get('stress_level', 5)),
        'working_hours':     float(data.get('working_hours', 8)),
        'sleep_hours':       float(data.get('sleep_hours', 7)),
        'work_life_balance': float(data.get('work_life_balance', 5)),
        'experience_years':  float(data.get('experience_years', 2)),
        'skills_count':      float(data.get('skills_count', 5))
    }


@app.route('/predict-burnout', methods=['POST'])
def api_burnout():
    data   = request.get_json()
    auto   = data.get('auto', False)
    inputs = parse_input(data, auto)
    result = predict_burnout(inputs)
    chart  = get_feature_importance_plot(inputs, 'burnout')
    shap_html = get_shap_explanation(inputs, 'burnout')
    session['last_inputs'] = inputs
    return jsonify({'prediction': result['label'], 'confidence': result['confidence'],
                    'inputs': inputs, 'chart': chart, 'shap': shap_html})


@app.route('/predict-productivity', methods=['POST'])
def api_productivity():
    data   = request.get_json()
    auto   = data.get('auto', False)
    inputs = parse_input(data, auto)
    result = predict_productivity(inputs)
    chart  = get_feature_importance_plot(inputs, 'productivity')
    shap_html = get_shap_explanation(inputs, 'productivity')
    session['last_inputs'] = inputs
    return jsonify({'prediction': result['label'], 'score': result['score'],
                    'inputs': inputs, 'chart': chart, 'shap': shap_html})


@app.route('/predict-career', methods=['POST'])
def api_career():
    data   = request.get_json()
    auto   = data.get('auto', False)
    inputs = parse_input(data, auto)
    result = predict_career(inputs)
    chart  = get_feature_importance_plot(inputs, 'career')
    shap_html = get_shap_explanation(inputs, 'career')
    session['last_inputs'] = inputs
    return jsonify({'prediction': result['label'], 'confidence': result['confidence'],
                    'inputs': inputs, 'chart': chart, 'shap': shap_html})


@app.route('/suggestions', methods=['POST'])
def api_suggestions():
    data   = request.get_json()
    auto   = data.get('auto', False)
    if auto and session.get('last_inputs'):
        inputs = session['last_inputs']
    else:
        inputs = parse_input(data, auto)
    result = get_suggestions(inputs)
    return jsonify({'suggestions': result['suggestions'], 'summary': result['summary'],
                    'inputs': inputs})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
