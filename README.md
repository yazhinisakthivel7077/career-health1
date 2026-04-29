# AI-Driven Career Health and Productivity Decision System

A complete full-stack ML web application built with Python Flask, scikit-learn Random Forest, and SHAP explainability.

---

## 📁 Folder Structure

```
career_health_system/
│
├── app.py                    ← Flask backend (main entry point)
├── requirements.txt          ← Python dependencies
│
├── ml_models/
│   ├── __init__.py
│   └── models.py             ← Random Forest models + SHAP + Matplotlib charts
│
├── templates/                ← Jinja2 HTML pages
│   ├── home.html             ← Landing page (before login)
│   ├── login.html            ← Login page
│   ├── logout.html           ← Logout confirmation
│   ├── dashboard.html        ← Navigation hub (menu cards)
│   ├── burnout.html          ← Burnout Prediction module
│   ├── productivity.html     ← Productivity Analysis module
│   ├── career.html           ← Career Readiness module
│   └── suggestions.html      ← Personalized Suggestions module
│
└── static/
    ├── css/
    │   └── style.css         ← Dark futuristic theme
    └── js/
        └── main.js           ← Shared JS utilities
```

---

## ⚙️ Step-by-Step Setup & Run Instructions

### Step 1 — Install Python (3.9 or higher)
Download from: https://python.org

### Step 2 — Open Terminal / Command Prompt
Navigate to the project folder:
```bash
cd career_health_system
```

### Step 3 — (Recommended) Create a Virtual Environment
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run the Application
```bash
python app.py
```
You should see:
```
✅ All ML models trained successfully.
 * Running on http://127.0.0.1:5000
```

### Step 6 — Open in Browser
Go to: **http://localhost:5000**

---

## 🔑 Demo Login Credentials

| Username | Password     |
|----------|-------------|
| admin    | password123 |
| student  | college2024 |
| user     | demo123     |

---

## 🧭 Navigation Flow

```
Home Page → Login → Dashboard
                       ├── Burnout Prediction    (/burnout)
                       ├── Productivity Analysis (/productivity)
                       ├── Career Readiness      (/career)
                       ├── AI Suggestions        (/suggestions)
                       └── Logout                (/logout)
```

---

## 🤖 Machine Learning Details

### Algorithm: Random Forest
- **Burnout Model**: RandomForestClassifier → Low / Medium / High
- **Productivity Model**: RandomForestClassifier (level) + RandomForestRegressor (score 0–100%)
- **Career Model**: RandomForestClassifier → Ready / Moderate / Needs Improvement

### Training Data
- 500 synthetic samples generated with NumPy
- Features: stress_level, working_hours, sleep_hours, work_life_balance, experience_years, skills_count
- Labels generated using realistic weighted formulas

### SHAP Explainability
- Uses permutation-based SHAP approximation (no C++ dependencies required)
- Generates waterfall-style bar charts showing each feature's positive/negative impact

---

## 📡 API Endpoints

| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | /predict-burnout     | Predict burnout level + SHAP chart   |
| POST   | /predict-productivity| Predict productivity score + chart   |
| POST   | /predict-career      | Predict career readiness + chart     |
| POST   | /suggestions         | Generate personalized suggestions    |

### Sample Request Body (Manual Mode):
```json
{
  "auto": false,
  "stress_level": 7,
  "working_hours": 10,
  "sleep_hours": 5,
  "work_life_balance": 3,
  "experience_years": 2,
  "skills_count": 5
}
```

### Auto Predict Mode:
```json
{ "auto": true }
```

---

## 🎨 Features

- ✅ Dark futuristic UI with grid background
- ✅ 4 fully independent ML modules
- ✅ Manual input (sliders) + Auto Predict button
- ✅ Random Forest Classifier & Regressor
- ✅ SHAP waterfall explanation charts
- ✅ Matplotlib feature importance + input profile charts
- ✅ Confidence scores with animated progress bars
- ✅ Session-based login/logout
- ✅ Responsive design

---

## 🛠 Troubleshooting

**Port already in use?**
```bash
python app.py  # Flask uses port 5000 by default
# Or change port in app.py: app.run(port=5001)
```

**ModuleNotFoundError?**
```bash
pip install flask numpy pandas scikit-learn matplotlib seaborn
```

**Blank charts?**
Make sure you're using Python 3.9+ and matplotlib 3.7+.

---

Built as a college project demonstrating full-stack ML development.
