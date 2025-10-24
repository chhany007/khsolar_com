"""
Quick test script for VIP system
"""

from vip_manager import add_vip_user, list_vip_users, init_database
import re

def test_telegram_validation():
    """Test telegram input validation"""
    print("\n" + "="*50)
    print("🧪 Testing Telegram Validation")
    print("="*50)
    
    test_cases = [
        ("@chhanycls", True, "Username with @"),
        ("chhanycls", True, "Username without @"),
        ("john_doe_123", True, "Username with underscore and numbers"),
        ("+855888836588", True, "Phone with +"),
        ("855888836588", True, "Phone without +"),
        ("0888836588", True, "Phone starting with 0"),
        ("abc", False, "Too short username"),
        ("a"*33, False, "Too long username"),
        ("user@name", False, "Invalid character @"),
        ("12345", False, "Too short phone"),
    ]
    
    for input_val, should_pass, description in test_cases:
        # Clean input
        cleaned = input_val.strip().lstrip('@').lstrip('+')
        
        # Check if phone or username
        is_phone = cleaned.replace('+', '').isdigit()
        
        if is_phone:
            valid = 8 <= len(cleaned) <= 15
        else:
            valid = bool(re.match(r'^[a-zA-Z0-9_]{5,32}$', cleaned))
        
        status = "✅" if valid == should_pass else "❌"
        result = "PASS" if valid == should_pass else "FAIL"
        
        print(f"{status} {result}: {description}")
        print(f"   Input: '{input_val}' → Cleaned: '{cleaned}' → Valid: {valid}")

def test_vip_system():
    """Test VIP system functionality"""
    print("\n" + "="*50)
    print("🧪 Testing VIP System")
    print("="*50)
    
    # Initialize database
    print("\n1. Initializing database...")
    init_database()
    print("   ✅ Database initialized")
    
    # Add test VIP users
    print("\n2. Adding test VIP users...")
    
    # Test user 1: Username
    result1 = add_vip_user(
        phone="855999999991",
        telegram="testuser1",
        name="Test User 1",
        email="test1@example.com"
    )
    
    # Test user 2: Phone
    result2 = add_vip_user(
        phone="855999999992",
        telegram="855999999992",
        name="Test User 2",
        email="test2@example.com",
        days=30
    )
    
    # Test user 3: Lifetime VIP
    result3 = add_vip_user(
        phone="855888836588",
        telegram="chhanycls",
        name="Chhany (Admin)",
        email="chhany@khsolar.com"
    )
    
    if result1 and result2 and result3:
        print("\n   ✅ All test users added successfully")
    else:
        print("\n   ❌ Some users failed to add")
    
    # List all users
    print("\n3. Listing all VIP users...")
    list_vip_users()
    
    print("\n" + "="*50)
    print("✅ VIP System Test Complete!")
    print("="*50)
    print("\n💡 Next Steps:")
    print("   1. Open KHSolar app")
    print("   2. Enter customer info with phone: 855888836588")
    print("   3. Should see '👑 VIP ACCESS GRANTED'")
    print("   4. All features should be unlocked")
    print("\n   To manage VIP users, run: python vip_manager.py")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 KHSolar VIP System Test Suite")
    print("="*60)
    
    # Test telegram validation
    test_telegram_validation()
    
    # Test VIP system
    test_vip_system()
    
    print("\n" + "="*60)
    print("✅ All Tests Complete!")
    print("="*60)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
