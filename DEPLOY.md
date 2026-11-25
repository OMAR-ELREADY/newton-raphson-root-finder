# 🚀 Deployment Guide

## Option 1: GitHub + Streamlit Cloud (Recommended - Free)

### Step 1: Create GitHub Repository
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `newton-raphson-root-finder`
3. Public (required for free Streamlit Cloud)
4. Don't initialize with README (we already have one)
5. Click **Create repository**

### Step 2: Push from Local
```bash
cd "D:\math project"
git remote add origin https://github.com/YOUR_USERNAME/newton-raphson-root-finder.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Repository: `yourusername/newton-raphson-root-finder`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **Deploy!**

Your app will be live at: `https://newton-raphson-root-finder.streamlit.app`

---

## Option 2: GitHub Pages (Static - Not for Streamlit)

Streamlit apps need a Python server, so GitHub Pages won't work directly. Use Streamlit Cloud, Render, or Railway instead.

---

## Option 3: Render (Free Tier)

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect your GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Free tier: 750 hours/month

---

## Option 4: Railway

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select repo
4. Auto-detects Streamlit
5. Free tier: $5 credit/month

---

## Quick Test Locally

```bash
cd "D:\math project"
streamlit run app.py
```

Opens at `http://localhost:8501`