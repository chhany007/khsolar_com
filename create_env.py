"""
Create .env file with your credentials
"""

env_content = """# Telegram Personal Sender Configuration
TELEGRAM_API_ID=23473875
TELEGRAM_API_HASH=0a487bc6b3460217fe1fb7f8b91e5cfb
TELEGRAM_PHONE=+855888836588

# Bot Token (fallback)
TELEGRAM_BOT_TOKEN=8258016332:AAFdR7b4y-BPzM-CdIpIMLnF2-8SFESQz1g
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ .env file created!")
print("📁 Location: .env")
print("\n✅ You can now send reports!")
