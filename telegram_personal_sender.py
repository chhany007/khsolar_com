"""
Send Telegram reports from YOUR personal account (no bot needed)
Uses Telethon - Telegram Client API
"""

import asyncio
import os
from dotenv import load_dotenv

# Fix for Streamlit threading - allow nested event loops
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Try to get config from Streamlit Cloud secrets first, then fall back to .env
def get_telegram_config():
    """Get Telegram config from Streamlit secrets or .env file"""
    try:
        # Try Streamlit Cloud secrets
        import streamlit as st
        if hasattr(st, 'secrets') and 'telegram' in st.secrets:
            return {
                'api_id': str(st.secrets["telegram"]["api_id"]),
                'api_hash': st.secrets["telegram"]["api_hash"],
                'phone': st.secrets["telegram"]["phone"]
            }
    except:
        pass
    
    # Fall back to .env file (local development)
    load_dotenv()
    return {
        'api_id': os.getenv('TELEGRAM_API_ID', '23473875'),
        'api_hash': os.getenv('TELEGRAM_API_HASH', '0a487bc6b3460217fe1fb7f8b91e5cfb'),
        'phone': os.getenv('TELEGRAM_PHONE', '+8550888836588')
    }

# Get configuration
config = get_telegram_config()
API_ID = config['api_id']
API_HASH = config['api_hash']
PHONE = config['phone']

class PersonalTelegramSender:
    """Send messages from your personal Telegram account"""
    
    def __init__(self):
        self.client = TelegramClient('khsolar_session', API_ID, API_HASH)
        self.connected = False
    
    def connect(self):
        """Connect and login to Telegram"""
        try:
            # Connect with timeout
            self.client.connect()
            
            if not self.client.is_user_authorized():
                # Not authorized - need manual setup
                raise Exception("Not authorized. Please run: python setup_telegram_now.py")
            
            self.connected = True
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def send_report(self, username_or_phone, report_text, language='bilingual'):
        """
        Send report to a Telegram user
        
        Args:
            username_or_phone: Username (without @) or phone number (+855...)
            report_text: Pre-formatted report text
            language: 'bilingual', 'english', or 'khmer'
        
        Returns:
            (success: bool, message: str)
        """
        if not self.connected:
            if not self.connect():
                return False, "Failed to connect to Telegram"
        
        try:
            from telegram_report_templates import (
                format_report_english, 
                format_report_khmer, 
                format_report_bilingual
            )
            
            # Format report based on language
            if language == 'english':
                message = format_report_english(report_text)
            elif language == 'khmer':
                message = format_report_khmer(report_text)
            else:
                message = format_report_bilingual(report_text)
            
            # Send message
            # If username, add @ prefix
            if not username_or_phone.startswith('+'):
                recipient = f"@{username_or_phone}" if not username_or_phone.startswith('@') else username_or_phone
            else:
                recipient = username_or_phone
            
            self.client.send_message(recipient, message, parse_mode='html')
            
            return True, f"✅ Report sent to {recipient}!"
            
        except Exception as e:
            return False, f"❌ Failed to send: {str(e)}"
    
    def disconnect(self):
        """Disconnect from Telegram"""
        if self.client:
            self.client.disconnect()
            self.connected = False


# Thread-safe synchronous wrapper for Streamlit compatibility
def send_report_from_personal(username_or_phone, report_data, language='bilingual'):
    """
    Simple function to send report from your personal Telegram
    
    Args:
        username_or_phone: Recipient's username or phone
        report_data: Dictionary with report information
        language: 'bilingual', 'english', or 'khmer'
    
    Returns:
        (success: bool, message: str)
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        sender = PersonalTelegramSender()
        if not sender.connect():
            return False, "Could not connect to Telegram"
        
        success, message = sender.send_report(username_or_phone, report_data, language)
        sender.disconnect()
        
        return success, message
        
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        loop.close()


if __name__ == "__main__":
    # Test script
    print("=" * 50)
    print("📱 Personal Telegram Sender Test")
    print("=" * 50)
    print()
    
    # Test data
    test_report = {
        'customer_name': 'Test Customer',
        'phone': '+855 12 345 678',
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
        'monthly_savings': 120.00,
        'annual_savings': 1440.00,
        'payback_years': 3.9,
        'date': '2025-10-23 23:40'
    }
    
    recipient = input("Enter username or phone number (e.g., @username or +855...): ")
    
    print()
    print("Choose language:")
    print("1. Bilingual (EN + KH)")
    print("2. English")
    print("3. Khmer")
    choice = input("Enter 1, 2, or 3: ").strip() or "1"
    
    lang_map = {"1": "bilingual", "2": "english", "3": "khmer"}
    language = lang_map.get(choice, "bilingual")
    
    print()
    print(f"📤 Sending {language} report to {recipient}...")
    
    success, message = send_report_from_personal(recipient, test_report, language)
    print(message)
    
    if success:
        print()
        print("✅ Success! Check the conversation in your Telegram!")
