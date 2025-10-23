"""
Telegram Bot Server for KHSolar
Handles user registrations and commands
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram_bot import TelegramReportSender, init_database

# Load environment variables
load_dotenv()

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8258016332:AAFdR7b4y-BPzM-CdIpIMLnF2-8SFESQz1g')

# Initialize database
init_database()
sender = TelegramReportSender()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Register user and optionally send report"""
    user = update.effective_user
    username = user.username
    chat_id = update.effective_chat.id
    first_name = user.first_name or ""
    
    # Check if there's a deep link parameter (report_xxx)
    deep_link_param = context.args[0] if context.args else None
    
    if not username:
        await update.message.reply_text(
            "⚠️ <b>Username Required</b>\n\n"
            "Please set a Telegram username in your Settings first:\n"
            "Settings → Edit Profile → Username\n\n"
            "Then send /start again.",
            parse_mode='HTML'
        )
        return
    
    # Register user in database
    success = sender.register_user(username, chat_id, first_name)
    
    if success:
        # Check if this is a deep link with report ID
        if deep_link_param and deep_link_param.startswith('report_'):
            report_id = deep_link_param.replace('report_', '')
            await update.message.reply_text(
                f"🌞 <b>Welcome to KHSolar!</b>\n\n"
                f"✅ Account connected: <b>@{username}</b>\n\n"
                f"📊 <b>Fetching your solar report...</b>",
                parse_mode='HTML'
            )
            
            # TODO: Fetch and send report by report_id
            # For now, show success message
            await update.message.reply_text(
                f"📄 <b>Your Solar Report</b>\n\n"
                f"Report ID: {report_id}\n\n"
                f"<i>The report will be sent by your consultant shortly.</i>\n"
                f"<i>This is an auto-send link - you don't need to do anything else!</i>",
                parse_mode='HTML'
            )
            print(f"✅ New user with deep link: @{username} (Report: {report_id})")
        else:
            # Regular registration without report
            await update.message.reply_text(
                f"🌞 <b>Welcome to KHSolar!</b>\n\n"
                f"✅ Your account is now connected, <b>@{username}</b>!\n\n"
                f"📊 You will receive your solar system reports here.\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<b>Next Steps:</b>\n"
                f"1. Tell your solar consultant your Telegram username: @{username}\n"
                f"2. They will design your solar system\n"
                f"3. Receive detailed reports here instantly\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 <b>Commands:</b>\n"
                f"/start - Register/Connect account\n"
                f"/status - Check registration status\n"
                f"/help - Get help\n\n"
                f"<i>Chat ID: {chat_id}</i>",
                parse_mode='HTML'
            )
            print(f"✅ New user registered: @{username} (Chat ID: {chat_id})")
    else:
        await update.message.reply_text(
            "❌ Registration failed. Please try again or contact support.",
            parse_mode='HTML'
        )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - Show registration status"""
    user = update.effective_user
    username = user.username
    chat_id = update.effective_chat.id
    
    if not username:
        await update.message.reply_text(
            "⚠️ You don't have a Telegram username set.",
            parse_mode='HTML'
        )
        return
    
    # Check if user is registered
    stored_chat_id = sender._get_chat_id(username)
    
    if stored_chat_id:
        await update.message.reply_text(
            f"✅ <b>Account Status: Active</b>\n\n"
            f"Username: @{username}\n"
            f"Chat ID: {chat_id}\n"
            f"Status: Ready to receive reports\n\n"
            f"Your solar consultant can now send reports to this account.",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            f"⚠️ <b>Not Registered</b>\n\n"
            f"Please send /start to register your account.",
            parse_mode='HTML'
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "🌞 <b>KHSolar Bot Help</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<b>Available Commands:</b>\n\n"
        "/start - Register your Telegram account to receive solar reports\n"
        "/status - Check your registration status\n"
        "/help - Show this help message\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<b>What This Bot Does:</b>\n\n"
        "📊 Sends you detailed solar system reports\n"
        "💰 Shows pricing and savings information\n"
        "⚡ Provides system specifications\n"
        "🔋 Details about solar panels, batteries, and inverters\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<b>How to Get Started:</b>\n\n"
        "1. Send /start to register\n"
        "2. Give your Telegram username to your solar consultant\n"
        "3. Receive instant reports when your system is designed\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📞 Need help? Contact your KHSolar consultant.",
        parse_mode='HTML'
    )


async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /users command - Admin only, list registered users"""
    # You can add admin check here
    users = sender.get_registered_users()
    
    if not users:
        await update.message.reply_text("No users registered yet.")
        return
    
    user_list = f"📱 <b>Registered Users ({len(users)}):</b>\n\n"
    for username, name, registered in users:
        user_list += f"• @{username}"
        if name:
            user_list += f" - {name}"
        user_list += f"\n  <i>Registered: {registered}</i>\n\n"
    
    await update.message.reply_text(user_list, parse_mode='HTML')


def main():
    """Start the bot server"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🌞 KHSolar Telegram Bot Server")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ Bot Token: {BOT_TOKEN[:15]}...")
    print(f"✅ Database initialized")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("users", list_users))
    
    print("🤖 Bot is running!")
    print("📱 Users can now send /start to register")
    print("💡 Press Ctrl+C to stop\n")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Start bot polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
