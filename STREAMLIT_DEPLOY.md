# 🚀 Deploy to Streamlit Cloud - Quick Guide

## ✅ Your Repository: `chhany007/khsolar_com`

---

## 📋 Deployment Steps (2 Minutes)

### **Step 1: Go to Streamlit Cloud**
👉 **Click here:** https://share.streamlit.io

### **Step 2: Sign In**
- Click **"Sign in"** or **"Continue with GitHub"**
- Authorize Streamlit Cloud to access your GitHub

### **Step 3: Create New App**
1. Click **"New app"** button (top right)
2. Fill in the form:

```
Repository: chhany007/khsolar_com
Branch: main
Main file path: app.py
```

3. Click **"Deploy!"**

### **Step 4: Wait for Deployment**
- Takes 2-3 minutes
- You'll see build logs
- Once complete, your app is live! ✅

---

## 🌐 Your App URL

After deployment, your app will be available at:

**Primary URL:**
```
https://khsolar-com.streamlit.app
```

**Or:**
```
https://chhany007-khsolar-com.streamlit.app
```

---

## 🎯 Add Custom Domain (solarkh.com)

### **Option 1: Cloudflare (FREE - Recommended)**

Since Streamlit Cloud free tier doesn't support custom domains directly, use Cloudflare:

1. **Sign up at Cloudflare** (free)
   - Go to: https://cloudflare.com
   - Create free account

2. **Add Your Domain**
   - Click "Add a site"
   - Enter: `solarkh.com`
   - Choose FREE plan

3. **Change Nameservers in Namecheap**
   - Cloudflare will show you 2 nameservers
   - Go to Namecheap → Domain List → Manage
   - Change nameservers to Cloudflare's

4. **Add DNS Records in Cloudflare**

| Type | Name | Target | Proxy Status |
|------|------|--------|--------------|
| CNAME | www | `khsolar-com.streamlit.app` | Proxied (🟠) |
| CNAME | @ | `khsolar-com.streamlit.app` | Proxied (🟠) |

5. **Wait for DNS Propagation** (1-4 hours)

6. **Done!** Visit `https://solarkh.com` ✅

---

### **Option 2: Direct CNAME (If Namecheap Allows)**

In Namecheap Advanced DNS:

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME Record | www | `khsolar-com.streamlit.app` | Automatic |
| URL Redirect | @ | `https://www.solarkh.com` | Automatic |

---

## 🔧 App Settings in Streamlit Cloud

After deployment, you can:

1. **View Logs** - See real-time application logs
2. **Reboot App** - Restart if needed
3. **Delete App** - Remove deployment
4. **Manage Secrets** - Add environment variables (if needed)

---

## 📊 What Streamlit Cloud Does Automatically

✅ Reads `requirements.txt` and installs all packages
✅ Reads `runtime.txt` for Python version (3.11)
✅ Reads `packages.txt` for system dependencies
✅ Runs `streamlit run app.py`
✅ Provides HTTPS automatically
✅ Auto-redeploys when you push to GitHub

---

## 🎉 Benefits of Streamlit Cloud

- ✅ **100% FREE forever**
- ✅ **No credit card required**
- ✅ **Unlimited apps**
- ✅ **Auto-deploy from GitHub**
- ✅ **Built-in HTTPS**
- ✅ **Official Streamlit platform**
- ✅ **Community support**

---

## 🔄 Auto-Deploy on Git Push

Once deployed, every time you push to GitHub:
1. Streamlit Cloud detects the change
2. Automatically rebuilds your app
3. Deploys the new version
4. Zero downtime!

---

## 🆘 Troubleshooting

### App won't start?
- Check deployment logs in Streamlit Cloud
- Verify `requirements.txt` has all dependencies
- Check `app.py` for errors

### Custom domain not working?
- Wait for DNS propagation (up to 48 hours)
- Check DNS records are correct
- Use https://dnschecker.org to verify

### Need to add secrets?
- Go to App Settings → Secrets
- Add in TOML format:
```toml
[secrets]
api_key = "your-key-here"
```

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io
- Community Forum: https://discuss.streamlit.io
- GitHub Issues: https://github.com/streamlit/streamlit/issues

---

## 🚀 Deploy Now!

👉 **Go to:** https://share.streamlit.io

**Repository:** `chhany007/khsolar_com`
**Branch:** `main`
**File:** `app.py`

**Click Deploy and you're done!** 🎉
