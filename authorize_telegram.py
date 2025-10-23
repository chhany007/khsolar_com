"""
One-time authorization for Telegram
Run this ONCE to login, then use the app normally
"""

from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Your credentials
API_ID = 23473875
API_HASH = '0a487bc6b3460217fe1fb7f8b91e5cfb'
PHONE = '+8550888836588'

print("=" * 60)
print("📱 TELEGRAM ONE-TIME AUTHORIZATION")
print("=" * 60)
print()
print("⚠️ You'll receive a code on your Telegram app")
print("⚠️ Check your phone and enter the code below")
print()

try:
    client = TelegramClient('khsolar_session', API_ID, API_HASH)
    client.connect()
    
    if client.is_user_authorized():
        print("✅ Already authorized! You're good to go!")
        print("\n🎉 You can now use the app:")
        print("   1. Run: streamlit run app.py")
        print("   2. Calculate system")
        print("   3. Click 'Send Report to My Telegram'")
    else:
        print(f"📱 Sending code to {PHONE}...")
        client.send_code_request(PHONE)
        
        code = input('\n🔢 Enter the code from Telegram: ')
        
        try:
            client.sign_in(PHONE, code)
            print("\n✅ Authorized successfully!")
        except SessionPasswordNeededError:
            password = input('\n🔐 Two-factor auth enabled. Enter password: ')
            client.sign_in(password=password)
            print("\n✅ Authorized successfully!")
        
        # Send test message
        print("\n📤 Sending test message to yourself...")
        client.send_message('me', '✅ KHSolar Telegram sender is ready!\n\nYou can now send reports from the app.')
        print("✅ Test message sent! Check 'Saved Messages' in Telegram")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Authorization complete!")
        print("=" * 60)
        print("\n✅ Next steps:")
        print("   1. Run your app: streamlit run app.py")
        print("   2. Enter customer Telegram (username or phone)")
        print("   3. Calculate system")
        print("   4. Click 'Send Report to My Telegram'")
        print("   5. Report sent instantly from YOUR account! 🚀")
        print()
        print("💡 You only need to run this script ONCE")
        print("   After this, everything works automatically!")
    
    client.disconnect()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Make sure:")
    print("   - Phone number is correct: +855888836588")
    print("   - You have internet connection")
    print("   - Telegram app is installed on your phone")

print("\n" + "=" * 60)
input("Press Enter to exit...")
