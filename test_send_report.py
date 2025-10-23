"""
Quick test script to send a report directly
"""

from telegram_bot import TelegramReportSender
from datetime import datetime

# Your Telegram username (without @)
TEST_USERNAME = "chhanycls"  # Your registered username

# Test report data
test_report = {
    'customer_name': 'Test Customer',
    'phone': '+855 12 345 678',
    'address': 'Phnom Penh, Cambodia',
    'monthly_kwh': 300,
    'daily_kwh': 10,
    'system_type': 'Hybrid',
    'num_panels': 8,
    'panel_wattage': 550,
    'pv_kw': 4.4,
    'pv_generation': 300,
    'battery_kwh': 5.12,
    'num_batteries': 1,
    'inverter_kw': 5.0,
    'total_price': 5626.40,
    'monthly_savings': 120.00,
    'annual_savings': 1440.00,
    'payback_years': 3.9,
    'date': datetime.now().strftime('%Y-%m-%d %H:%M')
}

print("=" * 50)
print("📱 TELEGRAM REPORT SEND TEST")
print("=" * 50)
print()

# Try to send
sender = TelegramReportSender()

print(f"Checking if @{TEST_USERNAME} is registered...")
chat_id = sender._get_chat_id(TEST_USERNAME)

if chat_id:
    print(f"✅ Found! Chat ID: {chat_id}")
    print()
    
    # Ask which language to test
    print("Choose language to test:")
    print("1. English + Khmer (Bilingual)")
    print("2. English Only")
    print("3. Khmer Only")
    print()
    
    choice = input("Enter 1, 2, or 3 (default=1): ").strip() or "1"
    
    lang_options = {
        "1": ("bilingual", "English + Khmer"),
        "2": ("english", "English"),
        "3": ("khmer", "Khmer")
    }
    
    language, lang_name = lang_options.get(choice, ("bilingual", "English + Khmer"))
    
    print()
    print(f"📤 Sending {lang_name} report...")
    success, message = sender.send_report(TEST_USERNAME, test_report, language)
    
    if success:
        print(f"✅ SUCCESS: {message}")
        print()
        print("📱 Check your Telegram!")
        print()
        print("Contact Info included:")
        print("  📞 Phone: 088888365")
        print("  💬 Telegram: @chhanycls")
    else:
        print(f"❌ FAILED: {message}")
else:
    print(f"❌ @{TEST_USERNAME} is NOT registered")
    print()
    print("📋 To register:")
    print("1. Open Telegram")
    print("2. Search for: @khsolar_bot")
    print("3. Send: /start")
    print()
    print("⚠️ BUT WAIT - the bot server has an error!")
    print("You need to:")
    print("1. Manually add yourself to database, OR")
    print("2. Fix bot server version issue")
    print()
    print("Let me show you the manual method...")
    print()
    
    # Manual registration option
    print("=" * 50)
    print("MANUAL REGISTRATION")
    print("=" * 50)
    print()
    print("1. Get your Telegram Chat ID:")
    print("   - Open https://t.me/userinfobot")
    print("   - Send any message")
    print("   - It will show your ID (numbers)")
    print()
    print("2. Once you have your chat_id, run:")
    print(f"   python -c \"from telegram_bot import TelegramReportSender; s = TelegramReportSender(); s.register_user('{TEST_USERNAME}', YOUR_CHAT_ID, 'Test User')\"")
    print()
    print("3. Then run this script again")
    
print()
print("=" * 50)
