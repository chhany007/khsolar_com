# 🌐 Setup Guide for solarkh.com

Your custom domain setup instructions for **solarkh.com** from Namecheap.

---

## 🎯 Your Domain Configuration

**Domain:** `solarkh.com`  
**Registrar:** Namecheap  
**Hosting:** Hugging Face Spaces (FREE)  
**Final URLs:**
- Main app: `https://solarkh.com`
- Or subdomain: `https://app.solarkh.com`

---

## 🚀 Step-by-Step Setup

### Step 1: Deploy to Hugging Face Spaces

1. **Go to:** https://huggingface.co
2. **Sign up/Login** (free account)
3. **Create New Space:**
   - Click "New" → "Space"
   - Name: `khsolar` (or `solarkh`)
   - SDK: **Streamlit**
   - Visibility: Public
   - Click "Create Space"

4. **Connect GitHub:**
   - In Space settings
   - Click "Connect to GitHub"
   - Select repository: `chhany007/khsolar`
   - Branch: `main`
   - Auto-deploy enabled!

5. **Wait for deployment** (2-3 minutes)
   - Your app will be live at:
   - `https://huggingface.co/spaces/YOUR_USERNAME/khsolar`

---

### Step 2: Add Custom Domain in Hugging Face

1. **Go to your Space**
2. **Click "Settings"** (top right)
3. **Scroll to "Custom Domain" section**
4. **Click "Add Domain"**
5. **Enter your domain:**
   - Option A: `solarkh.com` (root domain)
   - Option B: `app.solarkh.com` (subdomain)
   - **Recommended:** Use root `solarkh.com`

6. **Click "Add"**
7. **Copy the DNS records** shown (you'll need these next)

---

### Step 3: Configure DNS in Namecheap

1. **Login to Namecheap:** https://www.namecheap.com
2. **Go to Domain List**
3. **Find `solarkh.com`** and click "Manage"
4. **Click "Advanced DNS" tab**

#### For Root Domain (solarkh.com):

**Add these records:**

```
Type: A Record
Host: @
Value: [IP address from Hugging Face]
TTL: Automatic (or 3600)
```

**OR if Hugging Face provides CNAME:**

```
Type: CNAME Record
Host: @
Value: [CNAME from Hugging Face]
TTL: Automatic
```

**Also add www redirect:**

```
Type: CNAME Record
Host: www
Value: solarkh.com
TTL: Automatic
```

#### For Subdomain (app.solarkh.com):

**If you prefer subdomain:**

```
Type: CNAME Record
Host: app
Value: [CNAME from Hugging Face]
TTL: Automatic
```

5. **Click "Save All Changes"**

---

### Step 4: Wait for DNS Propagation

**Time:** Usually 5-60 minutes, max 48 hours

**Check propagation status:**
- Go to: https://dnschecker.org
- Enter: `solarkh.com`
- Wait until it shows green checkmarks globally

**While waiting:**
- ☕ Take a break
- 📱 Check on mobile data (different DNS)
- 🔄 Clear browser cache: `Ctrl + Shift + Delete`

---

### Step 5: Verify & Test

1. **Open browser** (incognito mode recommended)
2. **Go to:** `https://solarkh.com`
3. **Check SSL:** Should show 🔒 (automatic from Hugging Face)
4. **Test app:** Make sure everything works
5. **Test on mobile:** Check responsive design

---

## 📋 Quick DNS Configuration Reference

### Namecheap DNS Settings for solarkh.com

**Recommended Setup (Root Domain):**

| Type | Host | Value | TTL |
|------|------|-------|-----|
| A | @ | [HF IP] | Auto |
| CNAME | www | solarkh.com | Auto |

**Alternative Setup (Subdomain):**

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME | app | [HF CNAME] | Auto |

---

## 🔒 SSL Certificate (HTTPS)

**Good news:** SSL is 100% automatic and FREE!

- ✅ Hugging Face provides SSL via Let's Encrypt
- ✅ No configuration needed
- ✅ Auto-renews forever
- ✅ Your site will be `https://solarkh.com`

**If you see "Not Secure" warning:**
- Wait 5-15 minutes for SSL to provision
- Clear browser cache
- Try incognito mode
- Force refresh: `Ctrl + Shift + R`

---

## 🎨 Branding Suggestions

Now that you have `solarkh.com`, consider:

### Professional Email:
- `info@solarkh.com`
- `support@solarkh.com`
- `sales@solarkh.com`

**Setup via:**
- Namecheap Email (~$10/year)
- Google Workspace (~$6/month)
- Zoho Mail (FREE for 5 users)

### Social Media:
- Facebook: `facebook.com/solarkh`
- Telegram: `@solarkh`
- Instagram: `@solarkh`

### Business Cards:
```
☀️ SolarKH
Solar Planning & Design

🌐 solarkh.com
📞 +855 888 836 588
📧 info@solarkh.com
💬 @chhanycls
```

---

## 🔧 Troubleshooting

### Issue 1: Domain not working after 1 hour

**Solution:**
1. Check DNS records in Namecheap
2. Verify values match Hugging Face exactly
3. Check propagation: https://dnschecker.org
4. Clear DNS cache:
   ```powershell
   ipconfig /flushdns
   ```
5. Try different browser/device

### Issue 2: Shows "This site can't be reached"

**Solution:**
1. Wait longer (up to 48 hours)
2. Check DNS records are saved
3. Verify domain is not expired
4. Contact Namecheap support

### Issue 3: SSL certificate error

**Solution:**
1. Wait 15-30 minutes for SSL provisioning
2. Check domain is verified in Hugging Face
3. Force HTTPS in Hugging Face settings
4. Clear browser cache completely

### Issue 4: Shows old content or wrong site

**Solution:**
1. Clear browser cache: `Ctrl + Shift + Delete`
2. Flush DNS cache: `ipconfig /flushdns`
3. Try incognito mode
4. Check CNAME target is correct

---

## 📞 Support Contacts

### Namecheap Support:
- **Live Chat:** https://www.namecheap.com/support/live-chat/
- **Phone:** Available 24/7
- **Email:** support@namecheap.com

### Hugging Face Support:
- **Docs:** https://huggingface.co/docs/hub/spaces-domains
- **Forum:** https://discuss.huggingface.co
- **Discord:** https://hf.co/join/discord

---

## ✅ Setup Checklist

### Before Starting:
- [x] Domain purchased: `solarkh.com`
- [x] App code pushed to GitHub
- [ ] Hugging Face account created
- [ ] Space deployed

### During Setup:
- [ ] Space created on Hugging Face
- [ ] GitHub repository connected
- [ ] App deployed successfully
- [ ] Custom domain added in HF settings
- [ ] DNS records copied
- [ ] DNS configured in Namecheap
- [ ] Changes saved

### After Setup:
- [ ] Wait for DNS propagation (5-60 min)
- [ ] Check domain works: `solarkh.com`
- [ ] Verify SSL (https://)
- [ ] Test all features
- [ ] Test on mobile
- [ ] Share with customers!

---

## 🎯 Expected Timeline

| Step | Time |
|------|------|
| Deploy to Hugging Face | 2-3 minutes |
| Add custom domain | 1 minute |
| Configure DNS in Namecheap | 2 minutes |
| DNS propagation | 5-60 minutes |
| SSL certificate | Automatic |
| **Total** | **10-65 minutes** |

---

## 🌟 Final Result

After setup, your customers will access:

```
🌐 https://solarkh.com
```

**Features:**
- ✅ Professional domain
- ✅ Secure (HTTPS)
- ✅ Fast loading
- ✅ Always online
- ✅ Free hosting
- ✅ Auto-updates from GitHub

**Cost:**
- Domain: $10/year (already paid)
- Hosting: $0/year (Hugging Face)
- SSL: $0/year (included)
- **Total: $10/year**

---

## 📱 Share Your App

Once live, share with customers:

**Direct link:**
```
https://solarkh.com
```

**QR Code:**
Generate at: https://www.qr-code-generator.com
- Enter: `https://solarkh.com`
- Download QR code
- Print on business cards

**Social media post:**
```
🎉 Introducing SolarKH!

Professional solar system planning and design tool for Cambodia.

✅ Calculate system size
✅ Estimate costs
✅ Generate reports
✅ VIP features available

Visit: https://solarkh.com

#Solar #Cambodia #RenewableEnergy #SolarKH
```

---

## 🚀 Next Steps After Domain is Live

1. **Test thoroughly**
   - All features working
   - Mobile responsive
   - Fast loading

2. **Marketing**
   - Update business cards
   - Share on social media
   - Add to email signature

3. **SEO** (Optional)
   - Add Google Analytics
   - Submit to Google Search Console
   - Add meta descriptions

4. **Professional Email** (Optional)
   - Setup: info@solarkh.com
   - Use for customer communication

5. **Monitor**
   - Check uptime
   - Monitor performance
   - Gather user feedback

---

**Your domain `solarkh.com` is ready to go live!** 🎉

Just follow the steps above and your professional solar planning app will be accessible at:

# 🌐 https://solarkh.com

**Professional. Secure. Free hosting. Perfect!** ☀️
