# 👑 KHSolar VIP System Guide

## 🎯 Overview

The VIP system allows premium users to access all features of KHSolar without restrictions.

---

## ✨ Features

### **For VIP Users:**
- ✅ Access to all locked features
- ✅ Device Management
- ✅ System Configuration
- ✅ Product Catalog
- ✅ 24-Hour Simulation
- ✅ Professional Reports
- ✅ Priority support

### **For Regular Users:**
- ✅ Dashboard (Basic Calculator)
- 🔒 Advanced features locked

---

## 📝 Telegram Input Improvements

### **Accepts Both:**

1. **Username Format:**
   ```
   @sokpisey
   sokpisey
   john_doe123
   ```

2. **Phone Number Format:**
   ```
   +855123456789
   855123456789
   0123456789
   ```

### **Validation:**
- Username: 5-32 characters (letters, numbers, underscore)
- Phone: 8-15 digits
- Auto-detects format
- Removes @ and + symbols automatically

---

## 🔧 VIP Management (Admin Only)

### **1. Add VIP User**

```bash
python vip_manager.py
```

Then select option 1 and enter:
- Phone number (required)
- Telegram username/phone (optional)
- Customer name (optional)
- Email (optional)
- Duration in days (leave empty for lifetime)

**Example:**
```
Phone: 855888836588
Telegram: chhanycls
Name: Chhany
Email: chhany@khsolar.com
Days: 365 (or leave empty for lifetime)
```

### **2. Quick Add via Python:**

```python
from vip_manager import add_vip_user

# Lifetime VIP
add_vip_user(
    phone="855888836588",
    telegram="chhanycls",
    name="Chhany",
    email="chhany@khsolar.com"
)

# 30-day VIP
add_vip_user(
    phone="855123456789",
    telegram="customer1",
    name="Customer Name",
    days=30
)
```

### **3. List All VIP Users:**

```bash
python vip_manager.py
# Select option 4
```

### **4. Remove VIP Status:**

```bash
python vip_manager.py
# Select option 2
# Enter phone number
```

### **5. Extend VIP Access:**

```bash
python vip_manager.py
# Select option 5
# Enter phone and days to extend
```

---

## 🎨 User Experience

### **When User Enters Info:**

1. User enters phone and telegram
2. System checks VIP database
3. If VIP found:
   - ✅ Shows "👑 VIP ACCESS GRANTED"
   - Unlocks all features
   - Shows VIP badge in sidebar

### **VIP Badge Display:**

```
┌─────────────────────┐
│   👑 VIP ACCESS     │
│ All Features Unlocked│
└─────────────────────┘
```

### **Non-VIP User:**

```
🔒 VIP Feature
This feature is only available for VIP users.
Contact admin: +855888836588 or @chhanycls
```

---

## 📊 Database Structure

**Table: `vip_users`**

| Column      | Type      | Description                    |
|-------------|-----------|--------------------------------|
| id          | INTEGER   | Primary key                    |
| phone       | TEXT      | Phone number (unique)          |
| telegram    | TEXT      | Telegram username/phone        |
| name        | TEXT      | Customer name                  |
| email       | TEXT      | Email address                  |
| is_vip      | INTEGER   | 1 = VIP, 0 = Not VIP          |
| created_at  | TIMESTAMP | Registration date              |
| expires_at  | TIMESTAMP | Expiration (NULL = lifetime)   |

---

## 🔐 Security

- Database stored locally: `vip_users.db`
- Phone numbers are unique identifiers
- Telegram can be username or phone
- Expiration dates automatically checked
- Expired VIPs lose access automatically

---

## 🚀 Quick Start for Admin

### **Add Your First VIP User:**

```bash
# 1. Open terminal in project folder
cd "c:\Users\Jason\OneDrive\Desktop\sola project\2nd update software"

# 2. Run VIP manager
python vip_manager.py

# 3. Select option 1 (Add VIP User)

# 4. Enter details:
Phone: 855888836588
Telegram: chhanycls
Name: Admin
Email: admin@khsolar.com
Days: [leave empty for lifetime]

# 5. Done! ✅
```

### **Test VIP Access:**

1. Open KHSolar app
2. Enter customer info with VIP phone/telegram
3. Should see "👑 VIP ACCESS GRANTED"
4. All features unlocked!

---

## 📱 Contact for VIP Access

**For customers wanting VIP:**
- Phone: +855 888 836 588
- Telegram: @chhanycls
- Email: chhany@khsolar.com

---

## 🎯 Use Cases

### **1. Lifetime VIP (Business Partners):**
```python
add_vip_user("855888836588", "partner1", "Partner Company", days=None)
```

### **2. Trial VIP (30 days):**
```python
add_vip_user("855123456789", "trial_user", "Trial Customer", days=30)
```

### **3. Annual VIP:**
```python
add_vip_user("855987654321", "annual_user", "Annual Customer", days=365)
```

### **4. Extend Existing VIP:**
```python
from vip_manager import extend_vip
extend_vip("855123456789", days=90)  # Add 90 more days
```

---

## ✅ Testing

### **Test VIP System:**

1. **Add test VIP:**
   ```bash
   python vip_manager.py
   # Add phone: 855999999999
   ```

2. **Test in app:**
   - Enter customer info with phone: 855999999999
   - Should see VIP badge
   - All features unlocked

3. **Remove VIP:**
   ```bash
   python vip_manager.py
   # Remove VIP status
   ```

4. **Test again:**
   - Features should be locked again

---

## 🔄 Auto-Expiration

VIP access automatically expires based on `expires_at` date:
- System checks on every login
- Expired users automatically lose VIP status
- No manual intervention needed

---

## 📈 Future Enhancements

- [ ] Email notifications before expiration
- [ ] Payment integration
- [ ] VIP tiers (Bronze, Silver, Gold)
- [ ] Usage analytics for VIP users
- [ ] Referral system

---

## 🆘 Troubleshooting

### **VIP not working:**
1. Check database: `python vip_manager.py` → option 4
2. Verify phone/telegram matches exactly
3. Check expiration date
4. Restart app

### **Can't add VIP:**
1. Make sure phone is unique
2. Check database file exists: `vip_users.db`
3. Run `python vip_manager.py` to initialize

### **Features still locked:**
1. Verify VIP badge shows in sidebar
2. Check `st.session_state.is_vip` is True
3. Refresh the page
4. Re-enter customer info

---

## 📞 Support

For technical support:
- Developer: Chhany
- Phone: +855 888 836 588
- Telegram: @chhanycls

---

**Last Updated:** October 24, 2025
**Version:** 2.0
