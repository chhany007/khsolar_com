"""
Quick setup script for your Telegram credentials
Run this to create .env file and test connection
"""

import os
import asyncio

# Fix for asyncio in Windows
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

# Your credentials
API_ID = "23473875"
API_HASH = "0a487bc6b3460217fe1fb7f8b91e5cfb"
PHONE = "+855888836588"
BOT_TOKEN = "8258016332:AAFdR7b4y-BPzM-CdIpIMLnF2-8SFESQz1g"

def create_env_file():
    """Create .env file with your credentials"""
    env_content = f"""# Telegram Personal Sender Configuration
TELEGRAM_API_ID={API_ID}
TELEGRAM_API_HASH={API_HASH}
TELEGRAM_PHONE={PHONE}

# Bot Token (fallback)
TELEGRAM_BOT_TOKEN={BOT_TOKEN}
"""
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print(f"📁 Location: {env_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_connection():
    """Test Telegram connection"""
    print("\n" + "="*50)
    print("📱 Testing Telegram Connection")
    print("="*50)
    
    try:
        from telethon.sync import TelegramClient
        
        print("\n✅ Telethon library found!")
        print("\n🔐 Connecting to Telegram...")
        print("⚠️ You'll receive a code on your Telegram app")
        print("⚠️ Enter it when prompted (check your phone!)\n")
        
        client = TelegramClient('khsolar_session', API_ID, API_HASH)
        client.connect()
        
        if not client.is_user_authorized():
            print(f"📱 Sending code to {PHONE}...")
            client.send_code_request(PHONE)
            
            code = input('\n🔢 Enter the code you received on Telegram: ')
            
            try:
                client.sign_in(PHONE, code)
                print("✅ Logged in successfully!")
            except Exception as e:
                if "PASSWORD" in str(e).upper():
                    password = input('\n🔐 Two-factor auth enabled. Enter your password: ')
                    client.sign_in(password=password)
                    print("✅ Logged in successfully!")
                else:
                    raise e
        else:
            print("✅ Already logged in!")
        
        # Test sending a message to yourself
        print("\n📤 Sending test message to yourself...")
        me = client.get_me()
        print(f"👤 Your name: {me.first_name} {me.last_name or ''}")
        print(f"📱 Phone: {me.phone}")
        print(f"🆔 Username: @{me.username or 'none'}")
        
        client.send_message('me', '🎉 KHSolar Telegram sender is ready!\n\n✅ You can now send reports from the app!')
        print("\n✅ Test message sent to yourself!")
        print("📱 Check your Telegram 'Saved Messages' - you should see it!")
        
        client.disconnect()
        
        print("\n" + "="*50)
        print("🎉 SUCCESS! Everything is working!")
        print("="*50)
        print("\n✅ Next steps:")
        print("   1. Run your Streamlit app: streamlit run app.py")
        print("   2. Calculate a system")
        print("   3. Click 'Send Report to My Telegram'")
        print("   4. Reports will send from YOUR account!")
        print("\n📱 Remember: Messages appear from YOUR profile, not a bot!")
        
        return True
        
    except ImportError:
        print("\n❌ Telethon library not installed!")
        print("📦 Install it with: pip install telethon")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("🚀 KHSolar Telegram Setup")
    print("="*50)
    print()
    
    # Step 1: Create .env file
    print("Step 1: Creating .env file...")
    if not create_env_file():
        print("\n⚠️ Could not create .env file automatically")
        print("\n📝 Manual steps:")
        print("   1. Create a file named '.env' in this folder")
        print("   2. Copy content from 'telegram_config.txt'")
        print("   3. Run this script again")
        input("\nPress Enter to exit...")
        exit(1)
    
    print("\n✅ .env file created!")
    
    # Step 2: Test connection
    print("\nStep 2: Testing Telegram connection...")
    input("Press Enter to continue (you'll need to enter a code from Telegram)...")
    
    if test_connection():
        print("\n🎉 All done! You're ready to send reports!")
    else:
        print("\n⚠️ Setup incomplete. Please check the errors above.")
    
    input("\nPress Enter to exit...")
