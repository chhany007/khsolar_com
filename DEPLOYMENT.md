# 🚀 KHSolar Deployment Guide

## Streamlit Community Cloud (FREE - Recommended)

### Why Streamlit Cloud?
- ✅ **100% FREE forever**
- ✅ **No credit card required**
- ✅ **Unlimited apps**
- ✅ **Auto-deploy from GitHub**
- ✅ **Custom domain support**
- ✅ **Official Streamlit platform**

### Deployment Steps:

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Repository: `chhany007/khsolar_com`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Your App URL**
   - Will be: `https://chhany007-khsolar.streamlit.app`
   - Or custom: `https://khsolar.streamlit.app` (if available)

4. **Add Custom Domain (solarkh.com)**
   - Go to app settings
   - Click "Custom domain"
   - Add: `solarkh.com`
   - Follow DNS instructions

### DNS Settings for Namecheap:

Once deployed, add these DNS records in Namecheap:

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME | www | `chhany007-khsolar.streamlit.app` | Automatic |
| URL Redirect | @ | `https://www.solarkh.com` | Automatic |

---

## Alternative: Hugging Face Spaces (FREE)

### Steps:

1. Go to https://huggingface.co/spaces
2. Create new Space
3. Choose "Streamlit" as SDK
4. Connect GitHub repo or upload files
5. Your app will be at: `https://huggingface.co/spaces/[username]/khsolar`

---

## Alternative: Railway (Better Free Tier)

### Steps:

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `chhany007/khsolar_com`
5. Railway auto-detects Streamlit
6. Get $5 free credit monthly

---

## Files Already Configured ✅

Your repository already has:
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version (3.11)
- ✅ `packages.txt` - System dependencies
- ✅ `app.py` - Main application

---

## Comparison:

| Platform | Free Tier | Custom Domain | Ease |
|----------|-----------|---------------|------|
| **Streamlit Cloud** | ✅ Unlimited | ✅ Yes | ⭐⭐⭐⭐⭐ |
| Hugging Face | ✅ Unlimited | ❌ No | ⭐⭐⭐⭐ |
| Railway | $5/month credit | ✅ Yes | ⭐⭐⭐⭐ |
| Render | Very limited | ✅ Yes | ⭐⭐⭐ |

---

## 🎯 Recommended: Streamlit Cloud

**Deploy now:** https://share.streamlit.io

Your app will be live in 2-3 minutes! 🚀
