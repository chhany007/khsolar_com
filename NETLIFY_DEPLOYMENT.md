# 🚀 KHSolar - Netlify Deployment Guide

## ⚠️ Important Notice

**KHSolar is a Streamlit Python application** that requires a persistent Python runtime server. While we've prepared Netlify configuration files, please note:

### Limitations on Netlify:
- ❌ Streamlit requires a long-running server (not serverless)
- ❌ Netlify Functions have 10-second timeout limits
- ❌ Full Streamlit interactivity won't work properly
- ⚠️ The deployment will show a landing page with deployment instructions

### ✅ Better Alternatives (Free + Custom Domain):

1. **Render.com** (RECOMMENDED)
   - ✅ Free tier with custom domains
   - ✅ Perfect for Streamlit apps
   - ✅ No timeout limits
   - ✅ SSL certificates included

2. **Hugging Face Spaces**
   - ✅ Unlimited free hosting
   - ✅ Custom domains supported
   - ✅ Built for Streamlit

3. **Railway.app**
   - ✅ $5/month free credit
   - ✅ Custom domains
   - ✅ Easy deployment

---

## 📦 Files Created for Netlify

We've prepared the following files for you:

```
khsolar/
├── netlify.toml                    # Netlify configuration
├── netlify/functions/
│   └── streamlit.py               # Serverless function (landing page)
├── requirements-netlify.txt        # Netlify-compatible dependencies
└── runtime.txt                     # Python version (3.11.6)
```

---

## 🔧 Option 1: Deploy to Netlify (Limited Functionality)

If you still want to try Netlify, follow these steps:

### Step 1: Prepare Repository

1. **Push to GitHub** (if not already done):
```bash
cd C:\Users\chhan\CascadeProjects\khsolar
git init
git add .
git commit -m "Prepare for Netlify deployment"
git remote add origin https://github.com/YOUR_USERNAME/khsolar.git
git push -u origin main
```

### Step 2: Deploy to Netlify

1. **Go to Netlify**: https://app.netlify.com
2. **Sign up/Login** with GitHub
3. **New Site from Git**:
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub
   - Select your `khsolar` repository
4. **Build Settings**:
   ```
   Build command: pip install -r requirements-netlify.txt
   Publish directory: .
   Functions directory: netlify/functions
   ```
5. **Environment Variables**:
   ```
   PYTHON_VERSION = 3.11
   ```
6. **Deploy Site**

### Step 3: Custom Domain (FREE)

1. **In Netlify Dashboard**:
   - Go to Site Settings → Domain Management
   - Click "Add custom domain"
   - Enter your domain (e.g., `khsolar.com`)

2. **Update DNS at your domain registrar**:
   ```
   Type: CNAME
   Name: www (or @)
   Value: YOUR-SITE-NAME.netlify.app
   ```

3. **SSL Certificate**:
   - Netlify automatically provisions FREE SSL
   - Wait 1-2 minutes for activation

### What You'll Get:
- ⚠️ A landing page explaining the deployment limitations
- ⚠️ Links to better hosting alternatives
- ⚠️ Not a fully functional Streamlit app

---

## 🎯 Option 2: Deploy to Render.com (RECOMMENDED)

For full Streamlit functionality with free hosting + custom domain:

### Step 1: Sign Up

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 2: Create Web Service

1. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your `khsolar` repository

2. **Configure**:
   ```
   Name: khsolar
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
   ```

3. **Environment Variables** (if needed):
   ```
   PYTHON_VERSION=3.11.6
   STREAMLIT_SERVER_HEADLESS=true
   ```

### Step 3: Deploy

1. Click "Create Web Service"
2. Wait 3-5 minutes for build
3. Your app will be live at: `https://khsolar.onrender.com`

### Step 4: Custom Domain (FREE)

1. **In Render Dashboard**:
   - Go to your service → Settings
   - Scroll to "Custom Domain"
   - Click "Add Custom Domain"
   - Enter your domain

2. **Update DNS**:
   ```
   Type: CNAME
   Name: www (or subdomain)
   Value: PROVIDED_BY_RENDER
   ```

3. **SSL**: Automatically provisioned (FREE)

---

## 🌟 Option 3: Hugging Face Spaces

Perfect for Streamlit apps, completely free:

### Step 1: Create Space

1. Go to https://huggingface.co
2. Sign up for free
3. Click "New" → "Space"
4. Configure:
   ```
   Name: khsolar
   SDK: Streamlit
   Hardware: CPU (free)
   Visibility: Public
   ```

### Step 2: Upload Files

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
✅ All other .py files
```

### Step 3: Auto-Deploy

- Hugging Face automatically builds and deploys
- Wait 2-3 minutes
- Live at: `https://huggingface.co/spaces/YOUR_USERNAME/khsolar`

### Step 4: Custom Domain

1. **In Space Settings**:
   - Go to Settings → Custom Domain
   - Add your domain
   - Follow DNS instructions

---

## 📊 Comparison: Which to Choose?

| Feature | Netlify | Render.com | Hugging Face |
|---------|---------|------------|--------------|
| **Streamlit Support** | ❌ Limited | ✅ Full | ✅ Full |
| **Free Tier** | ✅ Yes | ✅ Yes | ✅ Unlimited |
| **Custom Domain** | ✅ Free | ✅ Free | ✅ Free |
| **SSL Certificate** | ✅ Free | ✅ Free | ✅ Free |
| **Build Time** | 1-2 min | 3-5 min | 2-3 min |
| **Always On** | ✅ Yes | ⚠️ Sleeps | ✅ Yes |
| **Best For** | Static sites | Python apps | ML/Streamlit |
| **Recommendation** | ❌ Not ideal | ✅ Best choice | ✅ Great choice |

---

## 🎯 Our Recommendation

### For KHSolar, we recommend:

1. **First Choice: Render.com**
   - Full Streamlit support
   - Free custom domain
   - Easy deployment
   - Professional hosting

2. **Second Choice: Hugging Face Spaces**
   - Unlimited free hosting
   - Perfect for Streamlit
   - Great community

3. **Netlify**: Only for static sites
   - Not suitable for full Streamlit apps
   - Use for landing pages only

---

## 🔗 Quick Links

- **Render.com**: https://render.com
- **Hugging Face**: https://huggingface.co
- **Netlify**: https://netlify.com
- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app

---

## 📞 Need Help?

1. **For Render deployment**: See `DEPLOYMENT_GUIDE.md`
2. **For Hugging Face**: See `DEPLOY_STREAMLIT_CLOUD.txt`
3. **For issues**: Check the deployment logs in your hosting dashboard

---

## ✅ Deployment Checklist

### Before Deploying:
- [ ] Choose hosting platform (Render.com recommended)
- [ ] Create account on chosen platform
- [ ] Push code to GitHub (if using Git deployment)
- [ ] Verify all Python files are present
- [ ] Check requirements.txt is complete

### After Deploying:
- [ ] Test all features work correctly
- [ ] Set up custom domain (optional)
- [ ] Configure SSL certificate (automatic)
- [ ] Share your live URL
- [ ] Monitor performance and usage

---

**Ready to Deploy?**

We recommend **Render.com** for the best experience with KHSolar. It's free, supports custom domains, and works perfectly with Streamlit!

**Questions?** Check the platform-specific documentation or review the error logs in your deployment dashboard.
