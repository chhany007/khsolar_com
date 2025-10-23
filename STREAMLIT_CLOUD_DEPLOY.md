# 🚀 Deploy KHSolar to Streamlit Cloud

## ✅ Prerequisites Complete
- ✓ Streamlit Cloud account registered
- ✓ requirements.txt updated
- ✓ Application ready

---

## 📋 **STEP-BY-STEP DEPLOYMENT**

### **Step 1: Prepare Your Repository**

#### **1.1 Create GitHub Repository**
```bash
# Navigate to project folder
cd "c:\Users\Jason\OneDrive\Desktop\sola project\2nd update software"

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "KHSolar v2.0 - Production Ready"

# Add remote (replace with YOUR GitHub repo)
git remote add origin https://github.com/YOUR_USERNAME/khsolar.git

# Push to GitHub
git push -u origin main
```

#### **1.2 Important Files to Include**
```
✓ app.py (main application)
✓ requirements.txt (dependencies)
✓ models.py
✓ calculations.py
✓ product_manager.py
✓ visualization.py
✓ export_utils.py
✓ telegram_personal_sender.py
✓ telegram_report_templates.py
✓ product_prices.txt
```

#### **1.3 Files to EXCLUDE (already in .gitignore)**
```
✗ .env (contains secrets)
✗ khsolar_session.session (Telegram session)
✗ __pycache__/
✗ *.db files
```

---

### **Step 2: Deploy on Streamlit Cloud**

#### **2.1 Login to Streamlit Cloud**
1. Go to: https://share.streamlit.io
2. Click **"Sign in"**
3. Use your GitHub account

#### **2.2 Create New App**
1. Click **"New app"**
2. Choose your repository: `YOUR_USERNAME/khsolar`
3. Select branch: `main`
4. Main file path: `app.py`
5. Click **"Deploy"**

---

### **Step 3: Configure Secrets**

⚠️ **IMPORTANT:** You need to add Telegram credentials as secrets

#### **3.1 Add Secrets in Streamlit Cloud**
1. In your deployed app, click **Settings** (gear icon)
2. Click **"Secrets"**
3. Paste this configuration:

```toml
# Telegram API Configuration
[telegram]
api_id = "23473875"
api_hash = "0a487bc6b3460217fe1fb7f8b91e5cfb"
phone = "+8550888836588"
bot_token = "8258016332:AAFdR7b4y-BPzM-CdIpIMLnF2-8SFESQz1g"
```

4. Click **"Save"**

#### **3.2 Update Code to Use Secrets**

The app needs to read from `st.secrets` instead of `.env` file.

**Current code reads from .env:**
```python
from dotenv import load_dotenv
load_dotenv()
api_id = os.getenv('TELEGRAM_API_ID')
```

**Needs to check for Streamlit Cloud:**
```python
import streamlit as st
import os
from dotenv import load_dotenv

# Check if running on Streamlit Cloud
if hasattr(st, 'secrets'):
    # Running on Streamlit Cloud - use secrets
    api_id = st.secrets["telegram"]["api_id"]
    api_hash = st.secrets["telegram"]["api_hash"]
    phone = st.secrets["telegram"]["phone"]
    bot_token = st.secrets["telegram"]["bot_token"]
else:
    # Running locally - use .env file
    load_dotenv()
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
```

---

### **Step 4: Handle Telegram Session**

⚠️ **PROBLEM:** The `khsolar_session.session` file cannot be uploaded to GitHub (security)

#### **Solutions:**

**Option A: Disable Telegram on Cloud (Recommended for Now)**
```python
# In app.py, add a check
import os

# Check if session file exists
TELEGRAM_ENABLED = os.path.exists('khsolar_session.session')

if TELEGRAM_ENABLED:
    # Show Telegram send button
else:
    st.info("💬 Telegram sending not available on cloud. Use local version for reports.")
```

**Option B: Re-authorize on Cloud (Advanced)**
- Upload session file manually via Streamlit Cloud file manager
- Not recommended for security reasons

**Option C: Use Telegram Bot Instead (Future Enhancement)**
- Create a bot-based sending system
- No session file needed
- More secure for cloud deployment

---

### **Step 5: Test Deployment**

#### **5.1 Access Your App**
Your app will be available at:
```
https://YOUR_USERNAME-khsolar-app-xxxxxx.streamlit.app
```

#### **5.2 Test Features**
```
□ Dashboard loads
□ Customer form works
□ Calculator functions
□ Language switching
□ VIP features locked
□ No errors in logs
```

#### **5.3 Known Limitations on Cloud**
```
⚠️ Telegram reports may not work (session file issue)
✓ All other features work normally
✓ Calculator works
✓ Forms work
✓ Customer management works
```

---

## 🔧 **CODE UPDATES NEEDED**

### **Update 1: telegram_personal_sender.py**

Add Streamlit Cloud support:

```python
import streamlit as st
import os
from telethon import TelegramClient
from dotenv import load_dotenv

def get_telegram_config():
    """Get Telegram config from either secrets or .env"""
    try:
        # Try Streamlit Cloud secrets first
        if hasattr(st, 'secrets') and 'telegram' in st.secrets:
            return {
                'api_id': int(st.secrets["telegram"]["api_id"]),
                'api_hash': st.secrets["telegram"]["api_hash"],
                'phone': st.secrets["telegram"]["phone"],
                'bot_token': st.secrets["telegram"]["bot_token"]
            }
    except:
        pass
    
    # Fall back to .env file (local)
    load_dotenv()
    return {
        'api_id': int(os.getenv('TELEGRAM_API_ID')),
        'api_hash': os.getenv('TELEGRAM_API_HASH'),
        'phone': os.getenv('TELEGRAM_PHONE'),
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN')
    }

# Usage
config = get_telegram_config()
client = TelegramClient('khsolar_session', config['api_id'], config['api_hash'])
```

### **Update 2: app.py**

Add cloud detection and conditional Telegram:

```python
# At the top of app.py
import os

# Detect if running on Streamlit Cloud
IS_CLOUD = not os.path.exists('khsolar_session.session')

# In the Telegram section
if st.session_state.customer_info.get('telegram'):
    if not IS_CLOUD:
        # Show Telegram send button (local only)
        st.markdown("### 💬 Send Report via Telegram")
        # ... rest of telegram code
    else:
        st.info("""
        💬 **Telegram Reports**
        
        Telegram sending is only available when running locally.
        
        To send reports:
        1. Download and run the app locally
        2. Use: `streamlit run app.py`
        3. Reports will send from your Telegram account
        
        📞 Contact: 0888836588 | 💬 @chhanycls
        """)
```

---

## 📝 **QUICK DEPLOYMENT CHECKLIST**

### **Before Pushing to GitHub:**
```bash
□ Updated requirements.txt ✅
□ Removed sensitive files from git ✅
□ Tested locally ✅
□ Committed all changes
```

### **On Streamlit Cloud:**
```bash
□ Created new app
□ Selected correct repo
□ Set main file to app.py
□ Added secrets (Telegram config)
□ Deployed successfully
```

### **After Deployment:**
```bash
□ Tested dashboard
□ Tested calculator
□ Tested forms
□ Checked language switching
□ Verified VIP locks work
□ Noted Telegram limitations
```

---

## ⚠️ **IMPORTANT NOTES**

### **Telegram Functionality:**
```
LOCAL VERSION:
✅ Full Telegram integration
✅ Send reports from your account
✅ All language options
✅ Direct sending

CLOUD VERSION:
⚠️ Telegram limited (no session file)
✅ All other features work
✅ Calculator fully functional
✅ Customer management works
```

### **Recommendation:**
```
Deploy to cloud for:
- Public access
- Customer demos
- System calculations
- Cost estimates

Keep local version for:
- Telegram reports
- Full functionality
- Business operations
```

---

## 🚀 **DEPLOYMENT COMMANDS**

### **Push to GitHub:**
```bash
cd "c:\Users\Jason\OneDrive\Desktop\sola project\2nd update software"
git init
git add .
git commit -m "KHSolar v2.0 - Cloud Deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/khsolar.git
git push -u origin main
```

### **Update After Changes:**
```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud will auto-redeploy! 🎉

---

## 🎯 **YOUR DEPLOYMENT URL**

After deployment, your app will be at:
```
https://YOUR_USERNAME-khsolar-app-xxxxxx.streamlit.app
```

Share this link with customers! 🚀

---

## 📞 **SUPPORT**

If you need help:
```
📞 Phone: 0888836588
💬 Telegram: @chhanycls
📧 Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
```

---

## ✅ **NEXT STEPS**

1. **Create GitHub repo** (if not exists)
2. **Push code** to GitHub
3. **Login** to https://share.streamlit.io
4. **Deploy app** from your repo
5. **Add secrets** in Streamlit Cloud settings
6. **Test** your deployed app
7. **Share** the URL!

---

🎉 **You're ready to deploy to Streamlit Cloud!**

**Note:** For full Telegram functionality, keep the local version running alongside the cloud version.
