"""
Telegram Deep Link Generator
Allows sending reports without manual registration
"""

import base64
import json
from urllib.parse import quote

def generate_report_deep_link(customer_name, report_id):
    """
    Generate a deep link that auto-sends report when user clicks START
    
    Args:
        customer_name: Customer's name
        report_id: Unique report identifier
        
    Returns:
        Deep link URL
    """
    # Encode report ID in start parameter (max 64 chars)
    start_param = f"report_{report_id}"
    deep_link = f"https://t.me/khsolar_bot?start={start_param}"
    
    return deep_link


def generate_share_message(customer_name, deep_link):
    """
    Generate shareable message for SMS/WhatsApp/Email
    
    Args:
        customer_name: Customer's name
        deep_link: Telegram bot deep link
        
    Returns:
        Formatted message
    """
    message = f"""
🌞 Hi {customer_name}!

Your solar system report is ready!

📱 Click here to view on Telegram:
{deep_link}

Just click "START" and your report will be sent immediately!

- KHSolar Team
    """.strip()
    
    return message


def generate_whatsapp_link(phone, customer_name, deep_link):
    """
    Generate WhatsApp link with pre-filled message
    
    Args:
        phone: Phone number (with country code, no +)
        customer_name: Customer's name
        deep_link: Telegram bot deep link
        
    Returns:
        WhatsApp URL
    """
    message = generate_share_message(customer_name, deep_link)
    whatsapp_url = f"https://wa.me/{phone}?text={quote(message)}"
    
    return whatsapp_url


def generate_sms_message(customer_name, deep_link):
    """
    Generate SMS message (keep it short)
    
    Args:
        customer_name: Customer's name
        deep_link: Telegram bot deep link
        
    Returns:
        Short SMS text
    """
    sms = f"Hi {customer_name}! Your solar report: {deep_link} (Click START to view)"
    return sms


# Example usage
if __name__ == "__main__":
    # Test
    customer = "John Doe"
    report_id = "12345"
    phone = "85512345678"  # Cambodia format without +
    
    deep_link = generate_report_deep_link(customer, report_id)
    print("Deep Link:", deep_link)
    print()
    
    share_msg = generate_share_message(customer, deep_link)
    print("Share Message:")
    print(share_msg)
    print()
    
    whatsapp = generate_whatsapp_link(phone, customer, deep_link)
    print("WhatsApp Link:", whatsapp)
    print()
    
    sms = generate_sms_message(customer, deep_link)
    print("SMS:", sms)
