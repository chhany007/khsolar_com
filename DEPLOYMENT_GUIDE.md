# 🚀 KHSolar Deployment Guide

This guide will help you deploy KHSolar to various free hosting platforms.

---

## 🌟 Option 1: Hugging Face Spaces (RECOMMENDED)

**Best for:** Streamlit apps, completely free, unlimited usage

### Steps:

1. **Create Account**
   - Go to https://huggingface.co
   - Sign up for free account
   - Verify your email

2. **Create New Space**
   - Click "New" → "Space"
   - Name: `khsolar` (or your preferred name)
   - License: MIT
   - SDK: **Streamlit**
   - Hardware: CPU (free)
   - Visibility: Public

3. **Upload Files**
   
   Upload these files to your Space:
   ```
   ✅ app.py
   ✅ models.py
   ✅ calculations.py
   ✅ product_manager.py
   ✅ visualization.py
   ✅ export_utils.py
   ✅ requirements.txt
   ✅ README.md
   ✅ product_prices.txt
   ✅ logo/logo.png (create logo folder)
   ✅ vip_users.db (if you have it)
   ```

4. **Auto-Deploy**
   - Hugging Face will automatically build and deploy
   - Wait 2-3 minutes for build to complete
   - Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/khsolar`

5. **Optional: Connect GitHub**
   - Go to Space Settings
   - Connect to GitHub repository
   - Auto-deploy on every git push

### Benefits:
- ✅ Completely FREE
- ✅ No credit card required
- ✅ 16GB RAM, 8 CPU cores
- ✅ Persistent storage
- ✅ Custom domains available
- ✅ Always on (no sleep)
- ✅ Unlimited usage

---

## 🚂 Option 2: Railway.app

**Best for:** GitHub integration, auto-deploy

### Steps:

1. **Sign Up**
   - Go to https://railway.app
   - Sign up with GitHub
   - Get $5 free credit monthly

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `khsolar` repository

3. **Configure**
   - Railway auto-detects Python
   - Start command is set automatically from `Procfile`
   - Environment variables (if needed):
     ```
     PORT=8080
     ```

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Get your URL: `https://khsolar-production.up.railway.app`

5. **Custom Domain (Optional)**
   - Settings → Domains
   - Add your custom domain

### Benefits:
- ✅ $5/month free credit
- ✅ GitHub auto-deploy
- ✅ Custom domains
- ✅ Easy scaling
- ⚠️ Limited to ~500 hours/month on free tier

---

## 🎨 Option 3: Render.com

**Best for:** Simple deployment, good free tier

### Steps:

1. **Sign Up**
   - Go to https://render.com
   - Sign up with GitHub

2. **New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `khsolar` repo

3. **Configure**
   ```
   Name: khsolar
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Get URL: `https://khsolar.onrender.com`

### Benefits:
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ Custom domains
- ✅ SSL certificates
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 750 hours/month free

---

## 📊 Comparison Table

| Feature | Hugging Face | Railway | Render | Streamlit Cloud |
|---------|-------------|---------|--------|-----------------|
| **Free Tier** | ✅ Unlimited | $5 credit | 750h/mo | 1 app |
| **Always On** | ✅ Yes | ⚠️ Limited | ❌ Sleeps | ✅ Yes |
| **RAM** | 16GB | 8GB | 512MB | 1GB |
| **Build Time** | 2-3 min | 1-2 min | 3-5 min | 2-3 min |
| **Custom Domain** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **GitHub Sync** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Best For** | Streamlit | Any app | Any app | Streamlit |

---

## 🔧 Troubleshooting

### Build Fails

**Problem:** Requirements installation fails
```bash
Solution:
1. Check requirements.txt versions
2. Remove version pins if needed
3. Use compatible versions
```

**Problem:** Module not found
```bash
Solution:
1. Ensure all .py files are uploaded
2. Check file names match imports
3. Verify folder structure
```

### App Crashes

**Problem:** Port binding error
```bash
Solution:
Use environment variable $PORT:
streamlit run app.py --server.port=$PORT
```

**Problem:** Database file not found
```bash
Solution:
1. Upload vip_users.db
2. Or let app create it automatically
```

### Performance Issues

**Problem:** App is slow
```bash
Solution:
1. Optimize image loading (use caching)
2. Reduce data processing
3. Upgrade to paid tier if needed
```

---

## 📝 Environment Variables

If you need to set environment variables:

### Hugging Face Spaces
- Go to Settings → Repository secrets
- Add variables

### Railway
- Settings → Variables
- Add key-value pairs

### Render
- Environment → Environment Variables
- Add variables

Common variables:
```bash
STREAMLIT_SERVER_PORT=8080
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

---

## 🎯 Recommended Workflow

### For Development:
```bash
1. Work locally
2. Test thoroughly
3. Push to GitHub
4. Auto-deploy to hosting
```

### For Production:
```bash
1. Use Hugging Face Spaces (best free option)
2. Connect GitHub for auto-deploy
3. Monitor usage and performance
4. Upgrade if needed
```

---

## 🔗 Useful Links

- **Hugging Face Docs:** https://huggingface.co/docs/hub/spaces
- **Railway Docs:** https://docs.railway.app
- **Render Docs:** https://render.com/docs
- **Streamlit Deployment:** https://docs.streamlit.io/streamlit-community-cloud/get-started

---

## 💡 Tips

1. **Use Git for deployment**
   - Push changes to GitHub
   - Let platform auto-deploy
   - Track versions easily

2. **Monitor resources**
   - Check memory usage
   - Monitor build times
   - Watch free tier limits

3. **Optimize for free tier**
   - Use caching (@st.cache_data)
   - Lazy load images
   - Minimize dependencies

4. **Backup your data**
   - Export database regularly
   - Keep local copies
   - Use version control

---

## ✅ Quick Start Checklist

- [ ] Choose hosting platform (Hugging Face recommended)
- [ ] Create account
- [ ] Upload/connect repository
- [ ] Verify all files are present
- [ ] Wait for build to complete
- [ ] Test deployed app
- [ ] Share URL with users
- [ ] Set up custom domain (optional)

---

**Need Help?**
- Check platform documentation
- Review error logs in deployment dashboard
- Test locally first before deploying

**Ready to Deploy?**
Start with Hugging Face Spaces - it's the easiest and most generous free tier!
