"""
Telegram Bot Integration for KHSolar
Sends system reports to customers via Telegram
"""

import os
import sqlite3
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from telegram import Bot
    from telegram.error import TelegramError
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ python-telegram-bot not installed. Run: pip install python-telegram-bot==20.7")

# Bot configuration
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8258016332:AAFdR7b4y-BPzM-CdIpIMLnF2-8SFESQz1g')
DB_PATH = Path(__file__).parent / 'telegram_users.db'


def init_database():
    """Initialize SQLite database for user mappings"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  chat_id INTEGER,
                  customer_name TEXT,
                  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


class TelegramReportSender:
    """Handle sending reports to Telegram users"""
    
    def __init__(self, bot_token=BOT_TOKEN):
        if not TELEGRAM_AVAILABLE:
            raise ImportError("python-telegram-bot library not installed")
        
        self.bot = Bot(token=bot_token)
        init_database()
    
    async def send_report_async(self, username, report_data, language='bilingual'):
        """
        Send system report to Telegram user
        
        Args:
            username: Telegram username (without @)
            report_data: Dictionary with system configuration
            language: 'english', 'khmer', or 'bilingual' (default)
            
        Returns:
            (success: bool, message: str)
        """
        try:
            # Get user's chat_id from database
            chat_id = self._get_chat_id(username)
            
            if not chat_id:
                return False, f"User @{username} hasn't started conversation with bot yet. Ask them to send /start to your bot."
            
            # Format the report message using templates
            from telegram_report_templates import format_report_english, format_report_khmer, format_report_bilingual
            
            if language == 'english':
                message = format_report_english(report_data)
            elif language == 'khmer':
                message = format_report_khmer(report_data)
            else:  # bilingual (default)
                message = format_report_bilingual(report_data)
            
            # Send message
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML'
            )
            
            return True, f"✅ Report sent successfully to @{username}"
            
        except TelegramError as e:
            return False, f"Telegram error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def _format_report(self, data):
        """Format system data into readable Telegram message"""
        
        # Calculate backup hours
        backup_hours = 0
        if data.get('battery_kwh', 0) > 0 and data.get('daily_kwh', 0) > 0:
            backup_hours = (data['battery_kwh'] * 0.8) / (data['daily_kwh'] / 24)
        
        msg = f"""
🌞 <b>KHSolar System Report</b>

━━━━━━━━━━━━━━━━━━━━
👤 <b>Customer Information</b>
━━━━━━━━━━━━━━━━━━━━

<b>Name:</b> {data.get('customer_name', 'N/A')}
<b>Phone:</b> {data.get('phone', 'N/A')}
<b>Location:</b> {data.get('address', 'Cambodia')}

━━━━━━━━━━━━━━━━━━━━
⚡ <b>System Overview</b>
━━━━━━━━━━━━━━━━━━━━

<b>Monthly Consumption:</b> {data.get('monthly_kwh', 0):.0f} kWh
<b>Daily Average:</b> {data.get('daily_kwh', 0):.1f} kWh
<b>System Type:</b> {data.get('system_type', 'N/A')}

━━━━━━━━━━━━━━━━━━━━
☀️ <b>Solar Panels</b>
━━━━━━━━━━━━━━━━━━━━

<b>Quantity:</b> {data.get('num_panels', 0)} panels
<b>Power per Panel:</b> {data.get('panel_wattage', 0)}W
<b>Total Capacity:</b> {data.get('pv_kw', 0):.2f} kW
<b>Monthly Generation:</b> ~{data.get('pv_generation', 0):.0f} kWh

━━━━━━━━━━━━━━━━━━━━
🔋 <b>Battery Storage</b>
━━━━━━━━━━━━━━━━━━━━

<b>Total Capacity:</b> {data.get('battery_kwh', 0):.2f} kWh
<b>Usable Capacity:</b> {data.get('battery_kwh', 0) * 0.8:.2f} kWh (80% DoD)
<b>Backup Time:</b> ~{backup_hours:.1f} hours
<b>Units:</b> {data.get('num_batteries', 0)}

━━━━━━━━━━━━━━━━━━━━
⚡ <b>Inverter</b>
━━━━━━━━━━━━━━━━━━━━

<b>Power Rating:</b> {data.get('inverter_kw', 0):.1f} kW
<b>Type:</b> {data.get('system_type', 'N/A')}
<b>Efficiency:</b> 97%

━━━━━━━━━━━━━━━━━━━━
💰 <b>Investment Details</b>
━━━━━━━━━━━━━━━━━━━━

<b>💎 TOTAL SYSTEM PRICE</b>
<b>${data.get('total_price', 0):,.2f}</b>

<b>Monthly Savings:</b> ${data.get('monthly_savings', 0):,.2f}
<b>Annual Savings:</b> ${data.get('annual_savings', 0):,.2f}
<b>Payback Period:</b> {data.get('payback_years', 0):.1f} years

━━━━━━━━━━━━━━━━━━━━
📊 <b>System Benefits</b>
━━━━━━━━━━━━━━━━━━━━

✅ Reduce electricity bills by ~{(data.get('annual_savings', 0) / (data.get('monthly_kwh', 1) * 12 * 0.20)) * 100:.0f}%
✅ Clean, renewable energy
✅ Energy independence
✅ Increase property value
✅ 25+ year solar panel lifespan

━━━━━━━━━━━━━━━━━━━━

<i>Generated by KHSolar System Designer</i>
<i>Report Date: {data.get('date', 'N/A')}</i>

📞 Contact us for installation or questions!
"""
        return msg
    
    def _get_chat_id(self, username):
        """Get chat_id for a username from database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT chat_id FROM users WHERE username = ?', (username,))
            result = c.fetchone()
            conn.close()
            return result[0] if result else None
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
    def send_report(self, username, report_data, language='bilingual'):
        """Synchronous wrapper for send_report_async"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.send_report_async(username, report_data, language))
            loop.close()
            return result
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def register_user(self, username, chat_id, customer_name=""):
        """Register a new user (called by bot server)"""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO users (username, chat_id, customer_name) 
                        VALUES (?, ?, ?)''', (username, chat_id, customer_name))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def get_registered_users(self):
        """Get list of all registered users"""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT username, customer_name, registered_at FROM users ORDER BY registered_at DESC')
            users = c.fetchall()
            conn.close()
            return users
        except Exception:
            return []


def is_telegram_available():
    """Check if Telegram integration is available"""
    return TELEGRAM_AVAILABLE


if __name__ == "__main__":
    # Test the bot connection
    print("Testing Telegram Bot Connection...")
    
    if not TELEGRAM_AVAILABLE:
        print("❌ python-telegram-bot not installed")
        print("Run: pip install python-telegram-bot==20.7")
    else:
        try:
            sender = TelegramReportSender()
            print(f"✅ Bot initialized successfully!")
            print(f"Token: {BOT_TOKEN[:10]}...")
            print(f"Database: {DB_PATH}")
            
            # Show registered users
            users = sender.get_registered_users()
            if users:
                print(f"\n📱 Registered Users: {len(users)}")
                for username, name, registered in users:
                    print(f"  @{username} - {name} - {registered}")
            else:
                print("\n⚠️ No users registered yet")
                print("Users must send /start to your bot first")
                
        except Exception as e:
            print(f"❌ Error: {e}")
