"""
Quick test to verify Telegram personal sender works
"""

print("🧪 Testing Telegram Personal Sender...")
print("=" * 50)

try:
    from telegram_personal_sender import send_report_from_personal
    print("✅ Module imported successfully")
    
    # Test data
    test_report = {
        'customer_name': 'Test Customer',
        'phone': '+855 88 888 365',
        'address': 'Phnom Penh',
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
        'monthly_savings': 60.00,
        'annual_savings': 720.00,
        'payback_years': 7.8,
        'date': '2025-10-23 23:56'
    }
    
    print("\n📤 Sending test report to yourself (Saved Messages)...")
    print("⚠️ This will send a message to YOUR Telegram\n")
    
    # Send to yourself
    success, message = send_report_from_personal('me', test_report, 'bilingual')
    
    if success:
        print("\n✅ SUCCESS!")
        print("📱 Check your Telegram 'Saved Messages'")
        print("You should see the test report!")
        print("\n🎉 Everything is working!")
        print("\n✅ You can now use it in the app:")
        print("   1. Run: streamlit run app.py")
        print("   2. Calculate a system")
        print("   3. Click 'Send Report to My Telegram'")
    else:
        print(f"\n❌ Failed: {message}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure .env file exists with your credentials")
        print("   2. Run: python setup_telegram_now.py")
        print("   3. Complete the login process")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Setup needed:")
    print("   Run: python setup_telegram_now.py")

print("\n" + "=" * 50)
input("\nPress Enter to exit...")
