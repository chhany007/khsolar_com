"""
VIP Admin Panel - Web Interface for Managing VIP Users
Master Admin: chhany / chhany@#$088
"""

import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import hashlib

# Page config
st.set_page_config(
    page_title="KHSolar VIP Admin Panel",
    page_icon="👑",
    layout="wide"
)

# Database paths
VIP_DB = 'vip_users.db'
ADMIN_DB = 'admin_users.db'

# Initialize admin database
def init_admin_database():
    """Initialize admin users database"""
    conn = sqlite3.connect(ADMIN_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admin_users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password_hash TEXT,
                  is_master INTEGER DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  last_login TIMESTAMP)''')
    
    # Create master admin if doesn't exist
    master_password = hashlib.sha256("chhany@#$088".encode()).hexdigest()
    c.execute('''INSERT OR IGNORE INTO admin_users (username, password_hash, is_master)
                 VALUES (?, ?, 1)''', ('chhany', master_password))
    
    conn.commit()
    conn.close()

init_admin_database()

def verify_admin(username, password):
    """Verify admin credentials"""
    try:
        conn = sqlite3.connect(ADMIN_DB)
        c = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT id, is_master FROM admin_users WHERE username = ? AND password_hash = ?',
                  (username, password_hash))
        result = c.fetchone()
        
        if result:
            # Update last login
            c.execute('UPDATE admin_users SET last_login = ? WHERE id = ?',
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), result[0]))
            conn.commit()
        
        conn.close()
        return result
    except:
        return None

def add_admin_user(username, password, is_master=0):
    """Add new admin user (master only)"""
    try:
        conn = sqlite3.connect(ADMIN_DB)
        c = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        c.execute('''INSERT INTO admin_users (username, password_hash, is_master)
                     VALUES (?, ?, ?)''', (username, password_hash, is_master))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def list_admin_users():
    """List all admin users"""
    try:
        conn = sqlite3.connect(ADMIN_DB)
        c = conn.cursor()
        c.execute('SELECT username, is_master, created_at, last_login FROM admin_users ORDER BY created_at DESC')
        users = c.fetchall()
        conn.close()
        return users
    except:
        return []

def delete_admin_user(username):
    """Delete admin user (cannot delete master)"""
    try:
        conn = sqlite3.connect(ADMIN_DB)
        c = conn.cursor()
        c.execute('DELETE FROM admin_users WHERE username = ? AND is_master = 0', (username,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# VIP Management Functions
def init_vip_database():
    """Initialize VIP users database"""
    conn = sqlite3.connect(VIP_DB)
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

init_vip_database()

def add_vip_user(phone, telegram='', name='', email='', days=None):
    """Add VIP user"""
    try:
        conn = sqlite3.connect(VIP_DB)
        c = conn.cursor()
        telegram_clean = telegram.strip().lstrip('@').lstrip('+') if telegram else ''
        
        expires_at = None
        if days:
            expires_at = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('''INSERT OR REPLACE INTO vip_users 
                     (phone, telegram, name, email, is_vip, expires_at)
                     VALUES (?, ?, ?, ?, 1, ?)''',
                  (phone, telegram_clean, name, email, expires_at))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def list_vip_users():
    """List all VIP users"""
    try:
        conn = sqlite3.connect(VIP_DB)
        c = conn.cursor()
        c.execute('''SELECT phone, telegram, name, email, is_vip, created_at, expires_at 
                     FROM vip_users ORDER BY created_at DESC''')
        users = c.fetchall()
        conn.close()
        return users
    except:
        return []

def remove_vip_status(phone):
    """Remove VIP status"""
    try:
        conn = sqlite3.connect(VIP_DB)
        c = conn.cursor()
        c.execute('UPDATE vip_users SET is_vip = 0 WHERE phone = ?', (phone,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def delete_vip_user(phone):
    """Delete VIP user completely"""
    try:
        conn = sqlite3.connect(VIP_DB)
        c = conn.cursor()
        c.execute('DELETE FROM vip_users WHERE phone = ?', (phone,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def extend_vip(phone, days):
    """Extend VIP access"""
    try:
        conn = sqlite3.connect(VIP_DB)
        c = conn.cursor()
        c.execute('SELECT expires_at FROM vip_users WHERE phone = ?', (phone,))
        result = c.fetchone()
        
        if not result:
            return False
        
        current_expires = result[0]
        if current_expires:
            current_dt = datetime.strptime(current_expires, '%Y-%m-%d %H:%M:%S')
            new_expires = (current_dt + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            new_expires = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('UPDATE vip_users SET expires_at = ?, is_vip = 1 WHERE phone = ?',
                  (new_expires, phone))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_master' not in st.session_state:
    st.session_state.is_master = False

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Login Page
if not st.session_state.logged_in:
    st.markdown("""
    <div class='main-header'>
        <h1>👑 KHSolar VIP Admin Panel</h1>
        <p>Manage VIP Users & Access Control</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Admin Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
            
            if submit:
                if username and password:
                    result = verify_admin(username, password)
                    if result:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.is_master = bool(result[1])
                        st.success(f"✅ Welcome, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        st.markdown("---")
        st.caption("🔒 Secure Admin Access Only")
        st.caption("Master Admin: chhany")

else:
    # Admin Dashboard
    st.markdown(f"""
    <div class='main-header'>
        <h1>👑 VIP Admin Dashboard</h1>
        <p>Welcome, {st.session_state.username} {'(Master Admin)' if st.session_state.is_master else '(Admin)'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_master = False
            st.rerun()
    
    # Statistics
    vip_users = list_vip_users()
    active_vips = sum(1 for u in vip_users if u[4] == 1)  # is_vip column
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{len(vip_users)}</div>
            <div class='stat-label'>Total Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{active_vips}</div>
            <div class='stat-label'>Active VIPs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        expired = len(vip_users) - active_vips
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{expired}</div>
            <div class='stat-label'>Expired/Inactive</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        admin_users = list_admin_users()
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{len(admin_users)}</div>
            <div class='stat-label'>Admin Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["👥 VIP Users", "➕ Add VIP", "⚙️ Admin Management" if st.session_state.is_master else "👤 My Account"])
    
    # Tab 1: VIP Users List
    with tab1:
        st.markdown("### 👥 VIP Users Database")
        
        if vip_users:
            for phone, telegram, name, email, is_vip, created, expires in vip_users:
                with st.expander(f"{'👑' if is_vip else '❌'} {name or 'No Name'} - {phone}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Phone:** {phone}")
                        st.write(f"**Telegram:** {telegram or 'Not provided'}")
                        st.write(f"**Name:** {name or 'Not provided'}")
                        st.write(f"**Email:** {email or 'Not provided'}")
                    
                    with col2:
                        st.write(f"**Status:** {'✅ Active VIP' if is_vip else '❌ Inactive'}")
                        st.write(f"**Created:** {created}")
                        
                        if expires:
                            expires_dt = datetime.strptime(expires, '%Y-%m-%d %H:%M:%S')
                            if datetime.now() > expires_dt:
                                st.write(f"**Expires:** {expires} (EXPIRED)")
                            else:
                                days_left = (expires_dt - datetime.now()).days
                                st.write(f"**Expires:** {expires} ({days_left} days left)")
                        else:
                            st.write(f"**Expires:** Never (Lifetime)")
                    
                    # Actions
                    st.markdown("---")
                    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                    
                    with action_col1:
                        extend_days = st.number_input(f"Days to extend", min_value=1, max_value=3650, value=30, key=f"extend_{phone}")
                    
                    with action_col2:
                        if st.button("➕ Extend", key=f"btn_extend_{phone}"):
                            if extend_vip(phone, extend_days):
                                st.success(f"✅ Extended {extend_days} days")
                                st.rerun()
                    
                    with action_col3:
                        if is_vip and st.button("🔒 Deactivate", key=f"btn_deactivate_{phone}"):
                            if remove_vip_status(phone):
                                st.success("✅ VIP deactivated")
                                st.rerun()
                    
                    with action_col4:
                        if st.button("🗑️ Delete", key=f"btn_delete_{phone}"):
                            if delete_vip_user(phone):
                                st.success("✅ User deleted")
                                st.rerun()
        else:
            st.info("📋 No VIP users in database yet")
    
    # Tab 2: Add VIP
    with tab2:
        st.markdown("### ➕ Add New VIP User")
        
        with st.form("add_vip_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                phone = st.text_input("Phone Number *", placeholder="855888836588")
                telegram = st.text_input("Telegram", placeholder="@username or phone")
                name = st.text_input("Customer Name", placeholder="John Doe")
            
            with col2:
                email = st.text_input("Email", placeholder="customer@example.com")
                vip_type = st.radio("VIP Type", ["Lifetime", "Time-Limited"])
                
                if vip_type == "Time-Limited":
                    days = st.number_input("Days", min_value=1, max_value=3650, value=365)
                else:
                    days = None
            
            submit = st.form_submit_button("➕ Add VIP User", type="primary", use_container_width=True)
            
            if submit:
                if phone:
                    if add_vip_user(phone, telegram, name, email, days):
                        st.success(f"✅ VIP user added successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to add user")
                else:
                    st.warning("⚠️ Phone number is required")
    
    # Tab 3: Admin Management (Master only)
    with tab3:
        if st.session_state.is_master:
            st.markdown("### ⚙️ Admin User Management")
            
            # Add new admin
            st.markdown("#### ➕ Add New Admin")
            with st.form("add_admin_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    new_username = st.text_input("Username", placeholder="admin_user")
                
                with col2:
                    new_password = st.text_input("Password", type="password", placeholder="Strong password")
                
                with col3:
                    make_master = st.checkbox("Make Master Admin")
                
                if st.form_submit_button("➕ Add Admin", type="primary"):
                    if new_username and new_password:
                        if add_admin_user(new_username, new_password, 1 if make_master else 0):
                            st.success(f"✅ Admin '{new_username}' added successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add admin (username may already exist)")
                    else:
                        st.warning("⚠️ Please enter username and password")
            
            st.markdown("---")
            
            # List admins
            st.markdown("#### 👥 Admin Users")
            admin_users = list_admin_users()
            
            for username, is_master, created, last_login in admin_users:
                with st.expander(f"{'👑' if is_master else '👤'} {username}"):
                    st.write(f"**Username:** {username}")
                    st.write(f"**Role:** {'Master Admin' if is_master else 'Admin'}")
                    st.write(f"**Created:** {created}")
                    st.write(f"**Last Login:** {last_login or 'Never'}")
                    
                    if not is_master:
                        if st.button(f"🗑️ Delete {username}", key=f"del_admin_{username}"):
                            if delete_admin_user(username):
                                st.success(f"✅ Admin '{username}' deleted")
                                st.rerun()
        else:
            st.markdown("### 👤 My Account")
            st.info(f"**Username:** {st.session_state.username}")
            st.info(f"**Role:** Admin")
            st.warning("⚠️ Only Master Admin can manage admin users")
