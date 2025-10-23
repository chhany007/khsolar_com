from telegram_bot import TelegramReportSender

# Register user
username = "chhanycls"
chat_id = 1734533584
name = "Chhany"

sender = TelegramReportSender()
result = sender.register_user(username, chat_id, name)

if result:
    print(f"✅ SUCCESS! @{username} is now registered!")
    print(f"   Chat ID: {chat_id}")
    print(f"   Name: {name}")
    print()
    print("You can now:")
    print("1. Use the KHSolar app to send reports")
    print("2. Run test_send_report.py to test")
else:
    print("❌ Registration failed")
