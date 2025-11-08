# 🚀 KHSolar - Render.com Deployment Guide

Complete guide to deploy KHSolar to Render.com with **FREE hosting + Custom Domain + SSL**

---

## ✅ Why Render.com?

- ✅ **FREE Tier** - 750 hours/month (enough for most use cases)
- ✅ **Full Streamlit Support** - No limitations
- ✅ **Custom Domain** - FREE (bring your own domain)
- ✅ **SSL Certificate** - FREE automatic HTTPS
- ✅ **Auto-Deploy** - Push to GitHub = Auto-deploy
- ✅ **512MB RAM** - Sufficient for KHSolar
- ✅ **No Credit Card Required** for free tier

---

## 📋 Prerequisites

1. **GitHub Account** - Your code is already on GitHub ✅
2. **Render Account** - Free (we'll create this)
3. **Domain Name** - Optional (for custom domain)

---

## 🎯 Step-by-Step Deployment

### Step 1: Create Render Account

1. Go to **https://render.com**
2. Click **Get Started for Free**
3. Sign up with **GitHub** (recommended)
4. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. **In Render Dashboard**:
   - Click **New +** button (top right)
   - Select **Web Service**

2. **Connect Repository**:
   - Find and select **chhany007/khsolar**
   - Click **Connect**

### Step 3: Configure Web Service

Fill in these settings:

```
Name: khsolar
Region: Singapore (closest to Cambodia)
Branch: main
Runtime: Python 3
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
```

**Instance Type:**
```
Free
```

### Step 4: Environment Variables (Optional)

Click **Advanced** and add these if needed:

```
PYTHON_VERSION = 3.11.6
STREAMLIT_SERVER_HEADLESS = true
STREAMLIT_SERVER_PORT = 10000
```

### Step 5: Deploy!

1. Click **Create Web Service**
2. Render will start building your app
3. Wait 3-5 minutes for the build to complete
4. Your app will be live at: `https://khsolar.onrender.com`

---

## 🌐 Add Custom Domain (FREE)

### Step 1: Add Domain in Render

1. **In your Render service dashboard**:
   - Go to **Settings** tab
   - Scroll to **Custom Domain** section
   - Click **Add Custom Domain**
   - Enter your domain (e.g., `khsolar.com` or `www.khsolar.com`)
   - Click **Save**

2. **Render will provide DNS instructions**:
   ```
   Type: CNAME
   Name: www (or your subdomain)
   Value: khsolar.onrender.com
   ```

### Step 2: Configure DNS in Namecheap

#### For Root Domain (khsolar.com):

1. **Login to Namecheap**
2. Go to **Domain List** → **Manage**
3. Click **Advanced DNS** tab
4. **Add/Update Records**:

   **Option A: Using CNAME (Recommended for www)**
   ```
   Type: CNAME Record
   Host: www
   Value: khsolar.onrender.com
   TTL: Automatic
   ```

   **Option B: Using ANAME/ALIAS (For root domain)**
   ```
   Type: ALIAS Record (if available)
   Host: @
   Value: khsolar.onrender.com
   TTL: Automatic
   ```

   **If ALIAS not available, use A Record:**
   ```
   Type: A Record
   Host: @
   Value: [IP from Render - check Render dashboard]
   TTL: Automatic
   ```

5. **Add URL Redirect** (optional - redirect root to www):
   ```
   Type: URL Redirect Record
   Host: @
   Value: https://www.khsolar.com
   ```

6. Click **Save All Changes**

### Step 3: Verify Domain in Render

1. **Back in Render dashboard**:
   - Go to **Settings** → **Custom Domain**
   - Click **Verify DNS Configuration**
   - Wait for DNS propagation (usually 15 minutes - 24 hours)

2. **SSL Certificate**:
   - Render automatically provisions FREE SSL certificate
   - Once DNS is verified, SSL is enabled automatically
   - Your site will be accessible via HTTPS

---

## 🔍 Monitor Your Deployment

### Check Build Logs

1. Go to your service dashboard
2. Click **Logs** tab
3. Monitor build and runtime logs

### Check Service Status

- **Deploying**: Build in progress
- **Live**: App is running successfully
- **Failed**: Check logs for errors

---

## ⚙️ Auto-Deploy Setup

Render automatically deploys when you push to GitHub:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Render automatically detects the push and redeploys
4. Wait 2-3 minutes for deployment

---

## 🐛 Troubleshooting

### Build Fails

**Error: Module not found**
```bash
Solution: Check requirements.txt has all dependencies
```

**Error: Python version**
```bash
Solution: Ensure runtime.txt has: 3.11
```

**Error: Port binding**
```bash
Solution: Use $PORT variable in start command (already configured)
```

### App Crashes

**Check Logs**:
1. Go to Logs tab
2. Look for error messages
3. Common issues:
   - Missing dependencies
   - File path errors
   - Database connection issues

**Memory Issues**:
- Free tier has 512MB RAM
- Optimize your app if needed
- Consider upgrading to paid tier ($7/month for 2GB RAM)

### Domain Not Working

**DNS Not Propagated**:
- Wait 24-48 hours for full propagation
- Check with: https://dnschecker.org

**SSL Certificate Not Issued**:
- Ensure DNS is fully propagated
- Click "Verify DNS Configuration" in Render
- Wait a few hours and try again

---

## 💰 Free Tier Limits

| Feature | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **RAM** | 512 MB | 2-8 GB |
| **CPU** | Shared | Dedicated |
| **Bandwidth** | Unlimited | Unlimited |
| **Hours** | 750/month | Unlimited |
| **Sleep** | After 15 min inactivity | Always on |
| **Custom Domain** | ✅ FREE | ✅ FREE |
| **SSL** | ✅ FREE | ✅ FREE |
| **Price** | $0 | $7+/month |

**Note**: Free tier apps sleep after 15 minutes of inactivity. First request after sleep takes 30-60 seconds to wake up.

---

## 🚀 Upgrade to Paid (Optional)

If you need always-on service:

1. Go to **Settings** → **Instance Type**
2. Select **Starter** ($7/month) or higher
3. Benefits:
   - No sleep
   - More RAM (2GB)
   - Faster performance
   - Priority support

---

## 📊 Performance Tips

### Optimize for Free Tier

1. **Use Caching**:
   ```python
   @st.cache_data
   def load_data():
       # Your data loading code
   ```

2. **Lazy Load Images**:
   - Load images only when needed
   - Compress images before uploading

3. **Minimize Dependencies**:
   - Only include necessary packages in requirements.txt

4. **Database Optimization**:
   - Use efficient queries
   - Index frequently accessed data

---

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Your GitHub Repo**: https://github.com/chhany007/khsolar

---

## ✅ Deployment Checklist

### Before Deploying:
- [x] Code pushed to GitHub
- [x] render.yaml created
- [x] start.sh created
- [x] requirements.txt complete
- [ ] Render account created
- [ ] Repository connected

### During Deployment:
- [ ] Web service created
- [ ] Build command configured
- [ ] Start command configured
- [ ] Environment variables set (if needed)
- [ ] Build successful
- [ ] App is live

### After Deployment:
- [ ] Test all features
- [ ] Add custom domain (optional)
- [ ] Configure DNS in Namecheap
- [ ] Verify SSL certificate
- [ ] Share live URL
- [ ] Monitor performance

---

## 🎯 Quick Commands Reference

### Local Testing:
```bash
# Test locally before deploying
streamlit run app.py
```

### Push Updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

### Check Logs:
```bash
# In Render dashboard → Logs tab
# Or use Render CLI (optional)
```

---

## 📞 Support

### Render Support:
- **Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

### KHSolar Issues:
- **GitHub Issues**: https://github.com/chhany007/khsolar/issues
- **Check Logs**: Render dashboard → Logs tab

---

## 🎉 Success!

Once deployed, your KHSolar app will be:
- ✅ Live at `https://khsolar.onrender.com`
- ✅ Accessible via your custom domain (if configured)
- ✅ Secured with FREE SSL certificate
- ✅ Auto-deploying on every GitHub push

**Your app is production-ready!** 🚀

---

## 🔄 Next Steps

1. **Deploy Now**: Follow Step 1-5 above
2. **Test Thoroughly**: Verify all features work
3. **Add Custom Domain**: Configure your domain
4. **Share**: Give your URL to users
5. **Monitor**: Check logs and performance

**Need help?** Check the troubleshooting section or Render documentation.

---

**Ready to Deploy?** Go to https://render.com and follow the steps above! 🚀
