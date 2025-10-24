# 👑 VIP Admin Panel Guide

## 🎯 Overview

Web-based admin panel to manage VIP users with secure login system.

---

## 🔐 Master Admin Credentials

```
Username: chhany
Password: chhany@#$088
```

**⚠️ IMPORTANT:** Change the password after first login!

---

## 🚀 Quick Start

### **1. Launch Admin Panel:**

```bash
cd "c:\Users\Jason\OneDrive\Desktop\sola project\2nd update software"
streamlit run vip_admin_panel.py
```

### **2. Login:**
- Open browser (should auto-open)
- Enter username: `chhany`
- Enter password: `chhany@#$088`
- Click "🔓 Login"

### **3. Manage VIPs:**
- View all VIP users
- Add new VIP users
- Extend VIP access
- Deactivate/Delete users
- Create new admin users (master only)

---

## 📋 Features

### **Dashboard:**
- 📊 Total Users count
- 👑 Active VIPs count
- ❌ Expired/Inactive count
- 👥 Admin Users count

### **VIP Users Tab:**
- View all VIP users
- See expiration dates
- Extend VIP access
- Deactivate VIP status
- Delete users completely

### **Add VIP Tab:**
- Add new VIP users
- Set lifetime or time-limited access
- Enter phone, telegram, name, email

### **Admin Management Tab (Master Only):**
- Create new admin users
- View all admin users
- Delete admin users (cannot delete master)
- Set admin roles

---

## 🎨 User Interface

### **Login Screen:**
```
┌─────────────────────────────┐
│  👑 KHSolar VIP Admin Panel │
│  Manage VIP Users & Access  │
└─────────────────────────────┘

        🔐 Admin Login
    ┌─────────────────────┐
    │ Username: [____]    │
    │ Password: [____]    │
    │   [🔓 Login]        │
    └─────────────────────┘
```

### **Dashboard:**
```
┌──────────────────────────────────────┐
│   👑 VIP Admin Dashboard             │
│   Welcome, chhany (Master Admin)     │
└──────────────────────────────────────┘

┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│   15   │ │   12   │ │   3    │ │   2    │
│ Total  │ │ Active │ │Expired │ │ Admins │
└────────┘ └────────┘ └────────┘ └────────┘

[👥 VIP Users] [➕ Add VIP] [⚙️ Admin Management]
```

---

## 📝 How to Use

### **Add VIP User:**

1. Click "➕ Add VIP" tab
2. Fill in details:
   - Phone: `855888836588` (required)
   - Telegram: `@chhanycls` or `855888836588`
   - Name: `Customer Name`
   - Email: `customer@example.com`
3. Choose VIP type:
   - **Lifetime:** Never expires
   - **Time-Limited:** Set days (e.g., 365 for 1 year)
4. Click "➕ Add VIP User"
5. Done! ✅

### **Extend VIP Access:**

1. Go to "👥 VIP Users" tab
2. Find the user
3. Click to expand their details
4. Enter days to extend (e.g., 30)
5. Click "➕ Extend"
6. Done! ✅

### **Deactivate VIP:**

1. Go to "👥 VIP Users" tab
2. Find the user
3. Click "🔒 Deactivate"
4. Confirm
5. User loses VIP access immediately

### **Delete User:**

1. Go to "👥 VIP Users" tab
2. Find the user
3. Click "🗑️ Delete"
4. User removed from database completely

### **Create New Admin (Master Only):**

1. Go to "⚙️ Admin Management" tab
2. Enter new admin details:
   - Username: `admin2`
   - Password: `SecurePassword123`
   - Check "Make Master Admin" if needed
3. Click "➕ Add Admin"
4. New admin can now login!

---

## 🔐 Security Features

### **Password Hashing:**
- All passwords stored as SHA-256 hashes
- Cannot be reversed or read

### **Session Management:**
- Secure login sessions
- Auto-logout on browser close
- Manual logout button

### **Role-Based Access:**
- **Master Admin:** Full access to everything
- **Regular Admin:** Can manage VIPs only

### **Database Security:**
- `admin_users.db` - Admin credentials
- `vip_users.db` - VIP user data
- Both in `.gitignore` (not uploaded to GitHub)

---

## 👥 User Roles

### **Master Admin (chhany):**
- ✅ Manage VIP users
- ✅ Add/extend/deactivate VIPs
- ✅ Create new admin users
- ✅ Delete admin users
- ✅ View all statistics

### **Regular Admin:**
- ✅ Manage VIP users
- ✅ Add/extend/deactivate VIPs
- ✅ View statistics
- ❌ Cannot manage admin users

---

## 📊 VIP User Information

Each VIP user has:
- **Phone:** Unique identifier (required)
- **Telegram:** Username or phone (optional)
- **Name:** Customer name (optional)
- **Email:** Email address (optional)
- **Status:** Active/Inactive
- **Created:** Registration date
- **Expires:** Expiration date (or "Never")

---

## 🎯 Common Tasks

### **Task 1: Add Lifetime VIP**
```
1. Click "➕ Add VIP"
2. Phone: 855888836588
3. Telegram: chhanycls
4. Name: Chhany
5. VIP Type: Lifetime
6. Click "Add VIP User"
```

### **Task 2: Add 30-Day Trial VIP**
```
1. Click "➕ Add VIP"
2. Phone: 855123456789
3. Name: Trial Customer
4. VIP Type: Time-Limited
5. Days: 30
6. Click "Add VIP User"
```

### **Task 3: Extend Expiring VIP**
```
1. Go to "👥 VIP Users"
2. Find user with expiring access
3. Enter days: 90
4. Click "➕ Extend"
```

### **Task 4: Create New Admin**
```
1. Go to "⚙️ Admin Management"
2. Username: sales_admin
3. Password: Sales@2025
4. Don't check "Make Master Admin"
5. Click "➕ Add Admin"
```

---

## 🔄 Integration with Main App

The admin panel shares the same `vip_users.db` database with the main KHSolar app.

**Flow:**
1. Admin adds VIP user in admin panel
2. User opens KHSolar app
3. User enters their phone/telegram
4. System checks `vip_users.db`
5. If VIP found → All features unlocked! 👑

---

## 📱 Access Methods

### **Local Development:**
```bash
streamlit run vip_admin_panel.py
# Opens at: http://localhost:8501
```

### **Network Access:**
```bash
streamlit run vip_admin_panel.py --server.address 0.0.0.0
# Access from other devices: http://YOUR_IP:8501
```

### **Production (Streamlit Cloud):**
1. Deploy `vip_admin_panel.py` separately
2. Use different subdomain (e.g., `admin.khsolar.app`)
3. Restrict access with authentication

---

## ⚠️ Important Notes

### **Security:**
- ⚠️ Change master password after first login
- ⚠️ Don't share admin credentials
- ⚠️ Use strong passwords for new admins
- ⚠️ Keep databases backed up

### **Database:**
- `admin_users.db` - Admin credentials
- `vip_users.db` - VIP user data
- Both auto-created on first run
- Already in `.gitignore`

### **Backup:**
```bash
# Backup databases
copy vip_users.db vip_users_backup.db
copy admin_users.db admin_users_backup.db
```

---

## 🐛 Troubleshooting

### **Cannot Login:**
1. Check username/password spelling
2. Try master admin: `chhany` / `chhany@#$088`
3. Delete `admin_users.db` to reset (recreates master)

### **VIP Not Working in Main App:**
1. Check phone/telegram matches exactly
2. Verify VIP status is Active (not expired)
3. Check `vip_users.db` exists in same folder
4. Restart main app

### **Admin Panel Won't Start:**
1. Check Streamlit is installed: `pip install streamlit`
2. Check you're in correct folder
3. Run: `streamlit run vip_admin_panel.py`

---

## 📈 Statistics & Reporting

The dashboard shows:
- **Total Users:** All users in database
- **Active VIPs:** Users with active VIP status
- **Expired:** Users with expired VIP
- **Admin Users:** Number of admin accounts

---

## 🎓 Best Practices

1. **Regular Review:**
   - Check expiring VIPs weekly
   - Extend or notify customers

2. **User Management:**
   - Keep customer info updated
   - Use descriptive names
   - Add email for notifications

3. **Admin Management:**
   - Create separate admin for each staff
   - Use strong passwords
   - Delete inactive admins

4. **Backup:**
   - Backup databases weekly
   - Keep backups secure
   - Test restore process

---

## 📞 Support

**For Admin Panel Issues:**
- Developer: Chhany
- Phone: +855 888 836 588
- Telegram: @chhanycls

---

## 🔄 Updates

**Version 1.0 - October 24, 2025**
- Initial release
- Master admin system
- VIP management
- Admin user management
- Web-based interface

---

## ✅ Quick Reference

### **Login:**
```
URL: http://localhost:8501
Username: chhany
Password: chhany@#$088
```

### **Add VIP:**
```
Tab: ➕ Add VIP
Required: Phone number
Optional: Telegram, Name, Email
Type: Lifetime or Time-Limited
```

### **Extend VIP:**
```
Tab: 👥 VIP Users
Action: Expand user → Enter days → Extend
```

### **Create Admin:**
```
Tab: ⚙️ Admin Management
Required: Username, Password
Optional: Make Master Admin
```

---

**Last Updated:** October 24, 2025
**Version:** 1.0
**Status:** ✅ Production Ready
