"""
VIP User Management System for KHSolar
Admin tool to add/remove VIP users
"""

import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'vip_users.db'

def init_database():
    """Initialize VIP users database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vip_users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  phone TEXT UNIQUE,
                  telegram TEXT,
                  name TEXT,
                  email TEXT,
                  is_vip INTEGER DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  expires_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_vip_user(phone, telegram='', name='', email='', days=None):
    """
    Add a VIP user
    
    Args:
        phone: Phone number (required)
        telegram: Telegram username or phone
        name: Customer name
        email: Email address
        days: Number of days for VIP access (None = lifetime)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Clean telegram input
        telegram_clean = telegram.strip().lstrip('@').lstrip('+') if telegram else ''
        
        # Calculate expiration date
        expires_at = None
        if days:
            expires_at = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('''INSERT OR REPLACE INTO vip_users 
                     (phone, telegram, name, email, is_vip, expires_at)
                     VALUES (?, ?, ?, ?, 1, ?)''',
                  (phone, telegram_clean, name, email, expires_at))
        conn.commit()
        conn.close()
        
        print(f"✅ VIP user added successfully!")
        print(f"   Phone: {phone}")
        if telegram_clean:
            print(f"   Telegram: {telegram_clean}")
        if name:
            print(f"   Name: {name}")
        if days:
            print(f"   Expires: {expires_at}")
        else:
            print(f"   Expires: Never (Lifetime)")
        
        return True
    except Exception as e:
        print(f"❌ Error adding VIP user: {e}")
        return False

def remove_vip_user(phone):
    """Remove VIP status from a user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE vip_users SET is_vip = 0 WHERE phone = ?', (phone,))
        conn.commit()
        conn.close()
        print(f"✅ VIP status removed for {phone}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def delete_user(phone):
    """Completely delete a user from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM vip_users WHERE phone = ?', (phone,))
        conn.commit()
        conn.close()
        print(f"✅ User {phone} deleted from database")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def list_vip_users():
    """List all VIP users"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT phone, telegram, name, email, is_vip, created_at, expires_at 
                     FROM vip_users ORDER BY created_at DESC''')
        users = c.fetchall()
        conn.close()
        
        if not users:
            print("📋 No users in database")
            return
        
        print("\n" + "="*80)
        print("📋 VIP USERS DATABASE")
        print("="*80)
        
        for i, (phone, telegram, name, email, is_vip, created, expires) in enumerate(users, 1):
            status = "👑 VIP" if is_vip else "❌ Expired"
            
            print(f"\n{i}. {status}")
            print(f"   Phone: {phone}")
            if telegram:
                print(f"   Telegram: @{telegram}")
            if name:
                print(f"   Name: {name}")
            if email:
                print(f"   Email: {email}")
            print(f"   Created: {created}")
            
            if expires:
                expires_dt = datetime.strptime(expires, '%Y-%m-%d %H:%M:%S')
                if datetime.now() > expires_dt:
                    print(f"   Expires: {expires} (EXPIRED)")
                else:
                    days_left = (expires_dt - datetime.now()).days
                    print(f"   Expires: {expires} ({days_left} days left)")
            else:
                print(f"   Expires: Never (Lifetime)")
        
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def extend_vip(phone, days):
    """Extend VIP access for a user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get current expiration
        c.execute('SELECT expires_at FROM vip_users WHERE phone = ?', (phone,))
        result = c.fetchone()
        
        if not result:
            print(f"❌ User {phone} not found")
            return False
        
        current_expires = result[0]
        
        if current_expires:
            # Extend from current expiration
            current_dt = datetime.strptime(current_expires, '%Y-%m-%d %H:%M:%S')
            new_expires = (current_dt + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            # Set new expiration from now
            new_expires = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('UPDATE vip_users SET expires_at = ?, is_vip = 1 WHERE phone = ?', 
                  (new_expires, phone))
        conn.commit()
        conn.close()
        
        print(f"✅ VIP extended for {phone}")
        print(f"   New expiration: {new_expires}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Interactive VIP management menu"""
    init_database()
    
    while True:
        print("\n" + "="*50)
        print("👑 KHSolar VIP Management System")
        print("="*50)
        print("\n1. Add VIP User")
        print("2. Remove VIP Status")
        print("3. Delete User")
        print("4. List All Users")
        print("5. Extend VIP Access")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            print("\n--- Add VIP User ---")
            phone = input("Phone number (required): ").strip()
            telegram = input("Telegram username/phone (optional): ").strip()
            name = input("Customer name (optional): ").strip()
            email = input("Email (optional): ").strip()
            days_input = input("VIP duration in days (leave empty for lifetime): ").strip()
            
            days = int(days_input) if days_input else None
            
            if phone:
                add_vip_user(phone, telegram, name, email, days)
            else:
                print("❌ Phone number is required")
        
        elif choice == '2':
            phone = input("\nPhone number to remove VIP: ").strip()
            if phone:
                remove_vip_user(phone)
        
        elif choice == '3':
            phone = input("\nPhone number to delete: ").strip()
            confirm = input(f"Are you sure you want to delete {phone}? (yes/no): ").strip().lower()
            if confirm == 'yes' and phone:
                delete_user(phone)
        
        elif choice == '4':
            list_vip_users()
        
        elif choice == '5':
            phone = input("\nPhone number: ").strip()
            days_input = input("Days to extend: ").strip()
            if phone and days_input:
                try:
                    days = int(days_input)
                    extend_vip(phone, days)
                except ValueError:
                    print("❌ Invalid number of days")
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
