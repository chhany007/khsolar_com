"""
Quick test script for Telegram bot integration
Run this to verify everything is set up correctly
"""

import os
import sys
from pathlib import Path

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🧪 KHSolar Telegram Integration Test")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

# Test 1: Check .env file
print("📄 Test 1: Checking .env file...")
env_file = Path(".env")
if env_file.exists():
    print("   ✅ .env file found")
    with open(env_file, 'r') as f:
        content = f.read()
        if 'TELEGRAM_BOT_TOKEN' in content:
            print("   ✅ TELEGRAM_BOT_TOKEN present")
        else:
            print("   ❌ TELEGRAM_BOT_TOKEN not found in .env")
else:
    print("   ❌ .env file not found")

# Test 2: Check python-dotenv
print("\n📦 Test 2: Checking python-dotenv...")
try:
    import dotenv
    print("   ✅ python-dotenv installed")
except ImportError:
    print("   ❌ python-dotenv not installed")
    print("   Run: pip install python-dotenv")

# Test 3: Check python-telegram-bot
print("\n📦 Test 3: Checking python-telegram-bot...")
try:
    import telegram
    print(f"   ✅ python-telegram-bot installed (version {telegram.__version__})")
except ImportError:
    print("   ❌ python-telegram-bot not installed")
    print("   Run: pip install python-telegram-bot==20.7")
    sys.exit(1)

# Test 4: Check telegram_bot.py
print("\n📄 Test 4: Checking telegram_bot.py...")
if Path("telegram_bot.py").exists():
    print("   ✅ telegram_bot.py found")
    try:
        from telegram_bot import TelegramReportSender, is_telegram_available
        print("   ✅ telegram_bot.py imports successfully")
        
        if is_telegram_available():
            print("   ✅ Telegram integration available")
        else:
            print("   ❌ Telegram integration not available")
    except Exception as e:
        print(f"   ❌ Error importing: {e}")
else:
    print("   ❌ telegram_bot.py not found")

# Test 5: Check bot_server.py
print("\n📄 Test 5: Checking bot_server.py...")
if Path("bot_server.py").exists():
    print("   ✅ bot_server.py found")
else:
    print("   ❌ bot_server.py not found")

# Test 6: Test bot connection
print("\n🤖 Test 6: Testing bot connection...")
try:
    from telegram_bot import TelegramReportSender
    from dotenv import load_dotenv
    
    load_dotenv()
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if token:
        print(f"   ✅ Bot token loaded: {token[:15]}...")
        
        try:
            sender = TelegramReportSender()
            print("   ✅ Bot initialized successfully")
            
            # Check database
            if Path("telegram_users.db").exists():
                print("   ✅ Database exists")
                users = sender.get_registered_users()
                print(f"   📱 Registered users: {len(users)}")
                if users:
                    for username, name, registered in users:
                        print(f"      • @{username} - {name}")
                else:
                    print("   ℹ️  No users registered yet")
                    print("   💡 Users must send /start to your bot")
            else:
                print("   ℹ️  Database will be created on first use")
                
        except Exception as e:
            print(f"   ⚠️  Bot initialization error: {e}")
            print("   💡 This is normal if bot server hasn't been started yet")
    else:
        print("   ❌ Bot token not found in environment")
        
except Exception as e:
    print(f"   ❌ Test failed: {e}")

# Test 7: Check .gitignore
print("\n🔒 Test 7: Checking .gitignore...")
gitignore = Path(".gitignore")
if gitignore.exists():
    with open(gitignore, 'r') as f:
        content = f.read()
        if '.env' in content:
            print("   ✅ .env is in .gitignore")
        else:
            print("   ⚠️  .env not in .gitignore (add it!)")
        if 'telegram_users.db' in content:
            print("   ✅ telegram_users.db is in .gitignore")
        else:
            print("   ⚠️  telegram_users.db not in .gitignore (add it!)")
else:
    print("   ⚠️  .gitignore not found")

# Summary
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📊 Test Summary")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

print("✅ If all tests passed, you're ready to:")
print("   1. Start bot server: python bot_server.py")
print("   2. Register on Telegram: Send /start to your bot")
print("   3. Test in KHSolar app: Send a report")
print("\n❌ If tests failed, check:")
print("   1. Install dependencies: pip install -r requirements_telegram.txt")
print("   2. Check .env file has correct token")
print("   3. Make sure all files are present")
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
