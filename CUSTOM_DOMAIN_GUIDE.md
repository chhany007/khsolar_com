# 🌐 Custom Domain Setup Guide for KHSolar

This guide shows you how to add a custom domain (like `khsolar.com` or `solar.yourdomain.com`) to your deployed app.

---

## 🎯 Overview

After deploying to a hosting platform, you can connect your own domain name instead of using the default URL.

**Default URLs:**
- Hugging Face: `https://huggingface.co/spaces/username/khsolar`
- Railway: `https://khsolar-production.up.railway.app`
- Render: `https://khsolar.onrender.com`

**With Custom Domain:**
- Your domain: `https://khsolar.com` or `https://app.khsolar.com`

---

## 📋 Prerequisites

1. **Own a domain name** (buy from):
   - Namecheap (~$10/year) - https://www.namecheap.com
   - GoDaddy (~$12/year) - https://www.godaddy.com
   - Cloudflare (~$10/year) - https://www.cloudflare.com
   - Google Domains (~$12/year) - https://domains.google

2. **App deployed** on one of these platforms:
   - Hugging Face Spaces
   - Railway
   - Render

---

## 🚀 Option 1: Hugging Face Spaces Custom Domain

### Step 1: Deploy Your App
1. Create Space on Hugging Face
2. Connect GitHub repo
3. Wait for deployment

### Step 2: Get Your Space URL
```
https://huggingface.co/spaces/YOUR_USERNAME/khsolar
```

### Step 3: Add Custom Domain

**In Hugging Face:**
1. Go to your Space
2. Click "Settings"
3. Scroll to "Custom Domain"
4. Enter your domain: `khsolar.com` or `app.khsolar.com`
5. Click "Add Domain"
6. You'll get DNS records to add

### Step 4: Configure DNS

**In your domain registrar (Namecheap, GoDaddy, etc.):**

**For root domain (khsolar.com):**
```
Type: A
Name: @
Value: [IP provided by Hugging Face]
TTL: 3600
```

**For subdomain (app.khsolar.com):**
```
Type: CNAME
Name: app
Value: [CNAME provided by Hugging Face]
TTL: 3600
```

### Step 5: Wait for DNS Propagation
- Usually takes 5-60 minutes
- Can take up to 48 hours
- Check status: https://dnschecker.org

### Step 6: Enable SSL (Automatic)
- Hugging Face automatically provides SSL certificate
- Your site will be https://

---

## 🚂 Option 2: Railway Custom Domain

### Step 1: Deploy to Railway
1. Connect GitHub repo
2. Deploy app
3. Get default URL

### Step 2: Add Custom Domain

**In Railway Dashboard:**
1. Go to your project
2. Click "Settings"
3. Go to "Domains" section
4. Click "Add Domain"
5. Enter: `khsolar.com` or `app.khsolar.com`

### Step 3: Get DNS Records

Railway will show you:
```
Type: CNAME
Name: app (or @)
Value: [your-app].up.railway.app
```

### Step 4: Configure DNS

**In your domain registrar:**

**For subdomain (app.khsolar.com):**
```
Type: CNAME
Name: app
Value: [shown by Railway]
TTL: 3600
```

**For root domain (khsolar.com):**
```
Type: CNAME (if supported)
Name: @
Value: [shown by Railway]

OR

Type: A
Name: @
Value: [IP from Railway]
```

### Step 5: Verify Domain
- Railway will auto-verify
- SSL certificate issued automatically
- Usually takes 5-10 minutes

---

## 🎨 Option 3: Render Custom Domain

### Step 1: Deploy to Render
1. Create Web Service
2. Connect GitHub
3. Deploy app

### Step 2: Add Custom Domain

**In Render Dashboard:**
1. Go to your service
2. Click "Settings"
3. Scroll to "Custom Domains"
4. Click "Add Custom Domain"
5. Enter your domain

### Step 3: Configure DNS

**Render will provide:**
```
Type: CNAME
Name: [your choice]
Value: [your-app].onrender.com
```

**In your domain registrar:**

**For subdomain:**
```
Type: CNAME
Name: app
Value: [shown by Render]
TTL: 3600
```

**For root domain:**
```
Type: A
Name: @
Value: [IP from Render]
TTL: 3600
```

### Step 4: Verify & Enable SSL
- Render auto-verifies domain
- Free SSL certificate issued
- Takes 5-15 minutes

---

## 📊 DNS Configuration Examples

### Example 1: Using Namecheap

1. **Login to Namecheap**
2. **Go to Domain List**
3. **Click "Manage" on your domain**
4. **Advanced DNS tab**
5. **Add New Record:**

```
Type: CNAME Record
Host: app
Value: your-app.up.railway.app
TTL: Automatic
```

6. **Save Changes**

### Example 2: Using Cloudflare

1. **Login to Cloudflare**
2. **Select your domain**
3. **DNS tab**
4. **Add Record:**

```
Type: CNAME
Name: app
Target: your-app.onrender.com
Proxy status: Proxied (orange cloud)
TTL: Auto
```

5. **Save**

### Example 3: Using GoDaddy

1. **Login to GoDaddy**
2. **My Products → Domains**
3. **Click DNS**
4. **Add Record:**

```
Type: CNAME
Name: app
Value: your-space.hf.space
TTL: 1 Hour
```

5. **Save**

---

## 🔒 SSL Certificate (HTTPS)

All platforms provide **FREE SSL certificates** automatically:

- ✅ **Hugging Face:** Auto SSL via Let's Encrypt
- ✅ **Railway:** Auto SSL included
- ✅ **Render:** Auto SSL included

**No configuration needed!** Just add domain and SSL is automatic.

---

## 🎯 Recommended Domain Structure

### For Business:
```
Main site: khsolar.com (marketing website)
App: app.khsolar.com (your Streamlit app)
API: api.khsolar.com (if you add API later)
```

### For Personal:
```
App: khsolar.com (direct to app)
```

### For Testing:
```
Staging: staging.khsolar.com
Production: app.khsolar.com
```

---

## 💰 Domain Costs

| Registrar | .com Price | Features |
|-----------|-----------|----------|
| **Namecheap** | $9-13/year | Free privacy, easy DNS |
| **Cloudflare** | $10/year | Best DNS, free CDN |
| **GoDaddy** | $12-20/year | Popular, support |
| **Google Domains** | $12/year | Simple, reliable |

**Recommendation:** Namecheap or Cloudflare for best value

---

## 🔧 Troubleshooting

### Domain Not Working

**Problem:** Domain shows "Not Found" or doesn't load

**Solutions:**
1. **Check DNS propagation:** https://dnschecker.org
2. **Verify DNS records** are correct
3. **Wait 24-48 hours** for full propagation
4. **Clear browser cache:** Ctrl+Shift+Delete
5. **Try incognito mode**

### SSL Certificate Error

**Problem:** "Not Secure" warning

**Solutions:**
1. **Wait for SSL to provision** (5-30 minutes)
2. **Check domain is verified** in platform dashboard
3. **Force HTTPS** in platform settings
4. **Contact platform support** if issue persists

### Wrong Content Showing

**Problem:** Domain shows old content or different site

**Solutions:**
1. **Clear DNS cache:**
   ```powershell
   ipconfig /flushdns
   ```
2. **Check CNAME target** is correct
3. **Verify domain** in platform dashboard
4. **Wait for propagation**

---

## 📝 Step-by-Step Checklist

### Before You Start:
- [ ] App deployed and working
- [ ] Domain purchased
- [ ] Access to domain DNS settings

### Setup Process:
- [ ] Login to hosting platform
- [ ] Add custom domain in settings
- [ ] Copy DNS records provided
- [ ] Login to domain registrar
- [ ] Add DNS records
- [ ] Save changes
- [ ] Wait for propagation (5-60 min)
- [ ] Verify domain works
- [ ] Check SSL certificate (https://)
- [ ] Test on different devices

---

## 🌟 Free Domain Alternatives

If you don't want to buy a domain yet:

### 1. **Freenom** (Free .tk, .ml, .ga domains)
- Website: https://www.freenom.com
- Free for 12 months
- Can renew for free
- Good for testing

### 2. **Use Subdomain**
If you own `yourdomain.com`:
- Create: `solar.yourdomain.com`
- Free to add
- Professional looking

### 3. **Use Platform Default**
- Hugging Face: `username-khsolar.hf.space`
- Railway: `khsolar-production.up.railway.app`
- Render: `khsolar.onrender.com`

---

## 🎬 Video Tutorials

- **Namecheap DNS Setup:** https://www.youtube.com/watch?v=vQHJNvqPqe8
- **Cloudflare DNS:** https://www.youtube.com/watch?v=XQKkb84EjNQ
- **Custom Domain on Railway:** https://www.youtube.com/watch?v=xXB8lhCXkqw

---

## 📞 Support

**Need Help?**

- **Hugging Face:** https://huggingface.co/docs/hub/spaces-domains
- **Railway:** https://docs.railway.app/deploy/custom-domains
- **Render:** https://render.com/docs/custom-domains

---

## ✅ Quick Summary

1. **Buy domain** (~$10/year)
2. **Deploy app** to hosting platform
3. **Add custom domain** in platform settings
4. **Configure DNS** at domain registrar
5. **Wait 5-60 minutes** for propagation
6. **SSL auto-enabled** - site is https://
7. **Done!** Share your custom URL

---

**Example Final Setup:**

```
Domain: khsolar.com
Hosting: Hugging Face Spaces
URL: https://khsolar.com
SSL: ✅ Automatic
Cost: $10/year domain + $0 hosting = $10/year total
```

**Professional, affordable, and easy!** 🚀
