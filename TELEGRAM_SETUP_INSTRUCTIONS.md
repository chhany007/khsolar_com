# 📱 Telegram Bot Setup Instructions

## ✅ Your Bot is Ready to Use!

**🤖 Bot Username:** `@khsolar_bot`  
**🔗 Direct Link:** https://t.me/khsolar_bot  
**🔑 Bot Token:** `8258016332:AAFdR7b4y-BPzM-CdIpIMLnF2-8SFESQz1g`

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
cd "c:\Users\Jason\OneDrive\Desktop\sola project\2nd update software"
pip install -r requirements_telegram.txt
```

Or install individually:
```bash
pip install python-telegram-bot==20.7
pip install python-dotenv==1.0.0
```

### Step 2: Start the Bot Server

```bash
python bot_server.py
```

You should see:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌞 KHSolar Telegram Bot Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Bot Token: 8258016332:AAFd...
✅ Database initialized
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Bot is running!
📱 Users can now send /start to register
💡 Press Ctrl+C to stop
```

**Keep this terminal window open!** The bot server must be running to receive user registrations.

### Step 3: Connect to Your Bot on Telegram

**Option 1 - Direct Link (Easiest):**
1. Click this link: https://t.me/khsolar_bot
2. Telegram opens automatically
3. Click "START" button

**Option 2 - Search:**
1. Open Telegram on your phone or computer
2. Search for: `@khsolar_bot`
3. Click on your bot
4. Send `/start`

You should receive:
```
🌞 Welcome to KHSolar!

✅ Your account is now connected, @yourusername!

📊 You will receive your solar system reports here.
```

### Step 4: Test in KHSolar App

1. Start the Streamlit app (if not running):
   ```bash
   streamlit run app.py
   ```

2. Go to Dashboard
3. Add customer info with your Telegram username
4. Design a system (enter kWh, calculate)
5. Click "📤 Send Report to Telegram"
6. Check Telegram for the report!

---

## 📋 Files Created

✅ **`.env`** - Bot token (secure storage)
✅ **`telegram_bot.py`** - Report sender
✅ **`bot_server.py`** - User registration handler
✅ **`requirements_telegram.txt`** - Dependencies
✅ **`telegram_users.db`** - User database (auto-created)

---

## 🔧 Bot Commands

Users can send these commands to your bot:

| Command | Description |
|---------|-------------|
| `/start` | Register Telegram account to receive reports |
| `/status` | Check registration status |
| `/help` | Show help message |
| `/users` | List registered users (admin) |

---

## 👥 How Customers Use It

### Customer Side:
1. Customer gives you their Telegram username: `@john_doe`
2. Customer opens Telegram
3. Customer searches for your bot
4. Customer sends `/start` to bot
5. Customer receives confirmation message

### Your Side:
1. Enter customer's Telegram username in KHSolar app: `@john_doe`
2. Design their solar system
3. Click "📤 Send Report to Telegram"
4. Customer instantly receives detailed report on Telegram!

---

## 📊 What Gets Sent in Reports

The Telegram report includes:

✅ **Customer Information**
- Name, Phone, Location

✅ **System Overview**
- Monthly/Daily consumption
- System type

✅ **Solar Panels**
- Quantity, wattage, total capacity
- Expected generation

✅ **Battery Storage**
- Total and usable capacity
- Backup hours
- Number of units

✅ **Inverter**
- Power rating
- Type, efficiency

✅ **Investment Details**
- Total system price
- Monthly/Annual savings
- Payback period
- ROI calculation

✅ **System Benefits**
- Electricity bill reduction %
- Environmental impact
- Energy independence

---

## 🐛 Troubleshooting

### Problem: "User hasn't started conversation with bot yet"

**Solution:**
1. User must send `/start` to your bot first
2. Bot server must be running
3. Username must match exactly (case-sensitive)

### Problem: "python-telegram-bot not installed"

**Solution:**
```bash
pip install python-telegram-bot==20.7
```

### Problem: "Telegram bot module not found"

**Solution:**
- Make sure `telegram_bot.py` is in the same folder as `app.py`
- Restart Streamlit app

### Problem: Bot doesn't respond

**Solution:**
1. Check bot server is running (`python bot_server.py`)
2. Check bot token in `.env` file is correct
3. Check internet connection

### Problem: Can't find bot in Telegram

**Solution:**
1. Check bot username with @BotFather
2. Make sure bot is not disabled
3. Search by exact username (including @)

---

## 🔒 Security Notes

### ✅ Token Security:
- Token is stored in `.env` file
- `.env` should be in `.gitignore`
- Never commit `.env` to version control

### ✅ Add to `.gitignore`:
```
.env
telegram_users.db
```

### ✅ Database Security:
- SQLite database stores username → chat_id mappings
- Located at: `telegram_users.db`
- Backup regularly

---

## 🚀 Running in Production

### Option 1: Keep Terminal Open
Simple but requires computer to stay on:
```bash
python bot_server.py
```

### Option 2: Run in Background (Windows)

Create `start_bot.bat`:
```batch
@echo off
cd "c:\Users\Jason\OneDrive\Desktop\sola project\2nd update software"
python bot_server.py
```

Create shortcut in Startup folder:
1. Press `Win + R`
2. Type: `shell:startup`
3. Create shortcut to `start_bot.bat`

### Option 3: Use PM2 (Recommended)

Install PM2:
```bash
npm install -g pm2
```

Start bot:
```bash
pm2 start bot_server.py --name khsolar-bot --interpreter python
pm2 save
pm2 startup
```

Check status:
```bash
pm2 status
pm2 logs khsolar-bot
```

### Option 4: Windows Service

Use NSSM (Non-Sucking Service Manager):
1. Download NSSM: https://nssm.cc/download
2. Install as service:
   ```bash
   nssm install KHSolarBot python "c:\path\to\bot_server.py"
   ```

---

## 📊 Monitoring

### Check Registered Users:

```bash
python telegram_bot.py
```

Output:
```
Testing Telegram Bot Connection...
✅ Bot initialized successfully!
Token: 8258016332...
Database: telegram_users.db

📱 Registered Users: 3
  @john_doe - John - 2025-10-23 10:30:00
  @jane_smith - Jane - 2025-10-23 11:45:00
  @bob_wilson - Bob - 2025-10-23 14:20:00
```

### Check Database Directly:

```bash
sqlite3 telegram_users.db
```

```sql
SELECT * FROM users;
```

---

## 🧪 Testing Checklist

### ✅ Installation Test:
```bash
pip list | findstr telegram
```
Should show: `python-telegram-bot 20.7`

### ✅ Bot Connection Test:
```bash
python telegram_bot.py
```
Should show: `✅ Bot initialized successfully!`

### ✅ Server Test:
```bash
python bot_server.py
```
Should show: `🤖 Bot is running!`

### ✅ User Registration Test:
1. Send `/start` to bot on Telegram
2. Should receive welcome message
3. Check registered users: `python telegram_bot.py`

### ✅ Report Sending Test:
1. Open KHSolar app
2. Enter customer with Telegram username
3. Calculate system
4. Click "Send Report to Telegram"
5. Check Telegram for report

---

## 📱 Bot Information

**Your Bot Details:**
- **Token:** `8258016332:AAFdR7b4y-BPzM-CdIpIMLnF2-8SFESQz1g`
- **Bot Username:** (Set with @BotFather)
- **Commands:** `/start`, `/status`, `/help`, `/users`

**Bot Features:**
- ✅ User registration
- ✅ Report sending
- ✅ HTML formatting
- ✅ Status checking
- ✅ Help system
- ✅ User management

---

## 🎉 You're All Set!

Your Telegram integration is fully configured and ready to use!

**Next Steps:**
1. Install dependencies: `pip install -r requirements_telegram.txt`
2. Start bot server: `python bot_server.py`
3. Register yourself: Send `/start` to your bot
4. Test in KHSolar app: Send a report
5. Share bot with customers!

---

## 📞 Support

If you need help:
1. Check troubleshooting section above
2. Review `TELEGRAM_BOT_SETUP.md` for detailed info
3. Test connection: `python telegram_bot.py`
4. Check logs in bot server terminal

---

**Bot Status:** ✅ Configured and Ready
**Integration:** ✅ Complete
**Testing Required:** ✅ Yes (5 minutes)

Happy reporting! 🌞📊
