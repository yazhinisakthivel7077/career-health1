# 🚀 Deployment Guide — Career Health System

You can deploy this Flask app on **Render** or **Railway** (or both). Both connect directly to GitHub and auto-deploy on every push.

---

## 🚂 OPTION A — Deploy on Railway (Easiest)

1. Go to [https://railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects Python and reads `railway.json`
5. Under **Variables**, add:
   - `SECRET_KEY` → any random string (e.g. `my-super-secret-key-123`)
6. Click **"Deploy"** — done in ~2 minutes
7. Go to **Settings → Networking → Generate Domain** to get your public URL

✅ No sleep on free tier. Auto-deploys every time you push to GitHub.

---

## 🟣 OPTION B — Deploy on Render

This Flask app is deployed in two steps:
1. **Render** → hosts the Python Flask backend (the actual app)
2. **Netlify** → acts as a frontend proxy that forwards traffic to Render

---

## STEP 1 — Push to GitHub

First, push this project to a GitHub repository.

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/career-health-system.git
git push -u origin main
```

---

## STEP 2 — Deploy Backend on Render

1. Go to [https://render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select your repository
4. Fill in the settings:

| Setting | Value |
|---|---|
| **Name** | `career-health-system` |
| **Environment** | `Python` |
| **Region** | Oregon (US West) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| **Plan** | Free |

5. Under **Environment Variables**, add:
   - `SECRET_KEY` → click "Generate" or type a random string

6. Click **"Create Web Service"**
7. Wait ~3–5 minutes for the build to finish
8. Copy your Render URL — it will look like:
   ```
   https://career-health-system.onrender.com
   ```

> ✅ Test by opening the Render URL in your browser — you should see the Career Health System home page.

---

## STEP 3 — Update netlify.toml with Your Render URL

Open `netlify.toml` and replace `YOUR_RENDER_URL` with your actual Render URL:

```toml
[[redirects]]
  from = "/*"
  to = "https://career-health-system.onrender.com/:splat"
  status = 200
  force = true
```

Commit and push the change:

```bash
git add netlify.toml
git commit -m "Add Render URL to Netlify proxy"
git push
```

---

## STEP 4 — Deploy Frontend on Netlify

1. Go to [https://netlify.com](https://netlify.com) and sign in
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect GitHub and select your repository
4. Fill in the build settings:

| Setting | Value |
|---|---|
| **Branch** | `main` |
| **Build command** | *(leave empty)* |
| **Publish directory** | `.` (a dot — the root) |

5. Click **"Deploy site"**
6. Netlify will give you a URL like:
   ```
   https://career-health-system.netlify.app
   ```

All traffic to your Netlify URL is automatically forwarded to Render.

---

## Architecture

```
User Browser
     │
     ▼
 Netlify URL  ──proxy──►  Render Flask App
(CDN / HTTPS)             (Python backend + ML models)
```

---

## ⚠️ Important Notes

### Free Tier Spin-Down (Render)
On Render's free plan, the server **sleeps after 15 minutes of inactivity**.
The first request after sleep takes ~30 seconds to wake up. This is normal.

To avoid this, upgrade to Render's paid plan ($7/month) or use a free uptime monitor like [UptimeRobot](https://uptimerobot.com) to ping your Render URL every 10 minutes.

### User Data is In-Memory
The app stores user accounts in `USER_DB = {}` in memory.
**All registered users are wiped when Render restarts the server.**

For persistent users, you would need to add a database (Render offers free PostgreSQL).

### Secret Key
The `SECRET_KEY` environment variable is set on Render and controls Flask sessions.
Never commit a real secret key to GitHub.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Render build fails | Check build logs; usually a missing dependency |
| `ModuleNotFoundError` | Make sure `gunicorn` is in `requirements.txt` |
| Netlify shows blank page | Make sure `netlify.toml` has the correct Render URL |
| App wakes up slowly | Normal on free tier — first request after inactivity takes ~30s |
| Login doesn't persist | Flask sessions require a consistent `SECRET_KEY` — set it as env var on Render |
