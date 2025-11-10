# 🚂 Railway Deployment Guide for KHSolar

## ✅ Your App is Ready for Railway!

All configuration files are already in place:
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Start command
- ✅ `runtime.txt` - Python version
- ✅ `railway.json` - Railway configuration

---

## 🚀 Deploy to Railway (5 Minutes)

### **Step 1: Go to Railway**
1. Open: https://railway.app
2. Click **"Start a New Project"** or **"Login"**
3. Sign in with **GitHub**

### **Step 2: Deploy from GitHub**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose repository: **`chhany007/khsolar_com`**
4. Railway will automatically detect it's a Streamlit app
5. Click **"Deploy Now"**

### **Step 3: Wait for Deployment**
- Railway will:
  - ✅ Install Python 3.11
  - ✅ Install all dependencies from `requirements.txt`
  - ✅ Start your Streamlit app
  - ⏱️ Takes 2-3 minutes

### **Step 4: Get Your App URL**
- Once deployed, you'll see:
  - **Deployment URL**: `https://khsolar-production.up.railway.app`
  - Click to test your app!

---

## 🌐 Add Custom Domain (solarkh.com)

### **Step 1: In Railway Dashboard**
1. Click on your deployed project
2. Go to **"Settings"** tab
3. Scroll to **"Domains"** section
4. Click **"+ Custom Domain"**
5. Enter: `solarkh.com`
6. Also add: `www.solarkh.com`
7. Railway will show you DNS records to add

### **Step 2: Update Namecheap DNS**

Railway will give you records like this:

**Option A: CNAME (Recommended)**
```
Type: CNAME
Host: www
Value: khsolar-production.up.railway.app
TTL: Automatic
```

**Option B: A Record**
```
Type: A
Host: @
Value: [IP provided by Railway]
TTL: Automatic
```

### **Step 3: Configure in Namecheap**

1. Login to Namecheap
2. Go to **Domain List** → **Manage** (solarkh.com)
3. Click **"Advanced DNS"** tab
4. Delete existing records for `@` and `www`
5. Add Railway's DNS records:

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME | www | `khsolar-production.up.railway.app` | Automatic |
| CNAME | @ | `khsolar-production.up.railway.app` | Automatic |

*Note: If Namecheap doesn't allow CNAME for @, use:*
| Type | Host | Value | TTL |
|------|------|-------|-----|
| A Record | @ | [Railway IP] | Automatic |
| CNAME | www | `khsolar-production.up.railway.app` | Automatic |

### **Step 4: Wait for DNS Propagation**
- Takes 1-4 hours (sometimes up to 48 hours)
- Check status: https://dnschecker.org

---

## 💰 Railway Free Tier

- ✅ **$5 free credit per month**
- ✅ **Enough for your app** (estimated $3-4/month usage)
- ✅ **No credit card required initially**
- ✅ **Custom domain included**
- ✅ **Automatic deployments from GitHub**

### Usage Estimate:
- Your Streamlit app: ~$3-4/month
- Free credit: $5/month
- **Result: FREE!** ✅

---

## 🔄 Auto-Deploy from GitHub

Once set up, every time you push to GitHub:
1. Railway automatically detects changes
2. Rebuilds and redeploys your app
3. Your site updates automatically!

No manual deployment needed! 🎉

---

## 📊 Monitor Your App

In Railway dashboard you can see:
- ✅ Deployment logs
- ✅ Resource usage
- ✅ Build status
- ✅ Custom domain status
- ✅ Environment variables

---

## 🆘 Troubleshooting

### If deployment fails:
1. Check **"Deployments"** tab for error logs
2. Common issues:
   - Missing dependencies → Check `requirements.txt`
   - Port issues → Already configured in `Procfile`
   - Python version → Already set in `runtime.txt`

### If custom domain doesn't work:
1. Verify DNS records in Namecheap
2. Wait for DNS propagation (use dnschecker.org)
3. Check Railway domain settings
4. Ensure SSL certificate is generated (automatic)

---

## ✅ Final Checklist

- [ ] Railway account created
- [ ] Project deployed from GitHub
- [ ] App is running (test Railway URL)
- [ ] Custom domain added in Railway
- [ ] DNS records updated in Namecheap
- [ ] Wait for DNS propagation
- [ ] Test: https://solarkh.com

---

## 🎯 Next Steps After Deployment

1. **Test your app**: Visit Railway URL
2. **Add custom domain**: Follow steps above
3. **Update DNS**: In Namecheap
4. **Wait**: 1-4 hours for DNS
5. **Enjoy**: Your app at solarkh.com! 🎉

---

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- DNS Checker: https://dnschecker.org
- Your GitHub Repo: https://github.com/chhany007/khsolar_com

---

**Need help? The Railway community is very responsive on their Discord!**
