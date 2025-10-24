"""
KHSolar - Ultimate Solar Planning & Business Software
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
import sqlite3
import re
from product_manager import ProductManager
from visualization import SolarVisualizer
from export_utils import ReportExporter
from calculations import SolarCalculator

# Page config
st.set_page_config(page_title="KHSolar - Solar Planning Software", page_icon="☀️", layout="wide")

# Custom CSS for Modern UI with Animations
st.markdown("""
<style>
    /* Smooth Page Transitions */
    .main {
        padding: 1rem 2rem;
        animation: fadeIn 0.4s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Smooth element transitions */
    .element-container {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Enhanced Metric Cards with Hover Effect */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: white !important;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
    }
    
    .stMetric label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Button Animations */
    .stButton button {
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* Form Animations */
    .stForm {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Loading Spinner Enhancement */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent !important;
    }
    
    /* Headers */
    h1 {
        color: #1e3a8a;
        font-size: 2.5rem;
        font-weight: 800;
        padding-bottom: 15px;
        border-bottom: 4px solid #3b82f6;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #1e40af;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #2563eb;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Primary Button */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8fafc;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Info/Warning/Success Boxes */
    .stAlert {
        border-radius: 10px;
        border-left-width: 4px;
        padding: 1rem 1.5rem;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }
    
    .css-1d391kg .stRadio>label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: #f8fafc;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #e0e7ff;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Checkbox */
    .stCheckbox {
        padding: 5px 0;
    }
    
    /* Custom Cards */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        transform: translateX(5px);
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(16,185,129,0.3);
    }
    
    /* Warning Box */
    .warning-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(245,158,11,0.3);
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
    }
    
    /* Fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
</style>
""", unsafe_allow_html=True)

# Device Database for Auto-Recognition
DEVICE_DATABASE = {
    # Cooling (inverter available for AC and refrigerators)
    "Refrigerator": {"power": 150, "hours": 24.0, "type": "cooling", "priority": True, "inverter": False},
    "Refrigerator (Inverter)": {"power": 150, "hours": 24.0, "type": "cooling", "priority": True, "inverter": True},
    "Freezer": {"power": 200, "hours": 24.0, "type": "cooling", "priority": True, "inverter": False},
    "Freezer (Inverter)": {"power": 200, "hours": 24.0, "type": "cooling", "priority": True, "inverter": True},
    "Air Conditioner 1HP": {"power": 1000, "hours": 8.0, "type": "cooling", "priority": False, "inverter": False},
    "Air Conditioner 1HP (Inverter)": {"power": 1000, "hours": 8.0, "type": "cooling", "priority": False, "inverter": True},
    "Air Conditioner 1.5HP": {"power": 1500, "hours": 8.0, "type": "cooling", "priority": False, "inverter": False},
    "Air Conditioner 1.5HP (Inverter)": {"power": 1500, "hours": 8.0, "type": "cooling", "priority": False, "inverter": True},
    "Air Conditioner 2HP": {"power": 2000, "hours": 8.0, "type": "cooling", "priority": False, "inverter": False},
    "Air Conditioner 2HP (Inverter)": {"power": 2000, "hours": 8.0, "type": "cooling", "priority": False, "inverter": True},
    "Ceiling Fan": {"power": 75, "hours": 10.0, "type": "cooling", "priority": False, "inverter": False},
    "Standing Fan": {"power": 60, "hours": 8.0, "type": "cooling", "priority": False, "inverter": False},
    "Table Fan": {"power": 50, "hours": 6.0, "type": "cooling", "priority": False, "inverter": False},
    
    # Lighting
    "LED Bulb 9W": {"power": 9, "hours": 5.0, "type": "lighting", "priority": True},
    "LED Bulb 12W": {"power": 12, "hours": 5.0, "type": "lighting", "priority": True},
    "LED Tube 18W": {"power": 18, "hours": 5.0, "type": "lighting", "priority": True},
    "CFL Bulb 20W": {"power": 20, "hours": 5.0, "type": "lighting", "priority": False},
    "LED Strip Lights": {"power": 30, "hours": 4.0, "type": "lighting", "priority": False},
    
    # Kitchen
    "Rice Cooker": {"power": 500, "hours": 1.0, "type": "kitchen", "priority": True},
    "Electric Stove": {"power": 2000, "hours": 1.5, "type": "kitchen", "priority": False},
    "Microwave": {"power": 1000, "hours": 0.3, "type": "kitchen", "priority": False},
    "Toaster": {"power": 800, "hours": 0.2, "type": "kitchen", "priority": False},
    "Electric Kettle": {"power": 1500, "hours": 0.3, "type": "kitchen", "priority": False},
    "Blender": {"power": 300, "hours": 0.2, "type": "kitchen", "priority": False},
    "Coffee Maker": {"power": 800, "hours": 0.5, "type": "kitchen", "priority": False},
    
    # Entertainment
    "TV LED 32 inch": {"power": 60, "hours": 4.0, "type": "entertainment", "priority": False},
    "TV LED 43 inch": {"power": 80, "hours": 4.0, "type": "entertainment", "priority": False},
    "TV LED 55 inch": {"power": 120, "hours": 4.0, "type": "entertainment", "priority": False},
    "Sound System": {"power": 100, "hours": 3.0, "type": "entertainment", "priority": False},
    "Gaming Console": {"power": 150, "hours": 3.0, "type": "entertainment", "priority": False},
    
    # Office/Computing
    "Desktop Computer": {"power": 300, "hours": 6.0, "type": "office", "priority": False},
    "Laptop": {"power": 65, "hours": 6.0, "type": "office", "priority": False},
    "Monitor": {"power": 40, "hours": 6.0, "type": "office", "priority": False},
    "Printer": {"power": 50, "hours": 0.5, "type": "office", "priority": False},
    "Router/Modem": {"power": 10, "hours": 24.0, "type": "office", "priority": True},
    
    # General Appliances (inverter available for washing machine)
    "Washing Machine": {"power": 500, "hours": 1.0, "type": "general", "priority": False, "inverter": False},
    "Washing Machine (Inverter)": {"power": 500, "hours": 1.0, "type": "general", "priority": False, "inverter": True},
    "Iron": {"power": 1000, "hours": 0.5, "type": "general", "priority": False, "inverter": False},
    "Vacuum Cleaner": {"power": 1000, "hours": 0.5, "type": "general", "priority": False, "inverter": False},
    "Water Pump": {"power": 300, "hours": 0.5, "type": "general", "priority": True, "inverter": False},
    "Water Heater": {"power": 2000, "hours": 1.0, "type": "heating", "priority": False, "inverter": False},
    "Water Heater (Inverter)": {"power": 2000, "hours": 1.0, "type": "heating", "priority": False, "inverter": True},
    "Hair Dryer": {"power": 1500, "hours": 0.2, "type": "general", "priority": False, "inverter": False},
}

# Khmer Translation Dictionary
TRANSLATIONS = {
    'en': {
        # Navigation
        'nav_title': '☀️ KHSolar',
        'nav_dashboard': '🏠 Dashboard',
        'nav_devices': '⚡ Devices',
        'nav_system': '🔧 System Config',
        'nav_products': '🛒 Products',
        'nav_simulation': '📊 Simulation',
        'nav_reports': '📈 Reports',
        
        # Dashboard
        'dash_title': '☀️ KHSolar - Solar Planning & Business Software',
        'dash_subtitle': 'Comprehensive Solar System Design for Khmer Households & Businesses',
        'customer_info': '👤 Customer Information',
        'customer_required': '👤 Customer Information Required',
        'customer_required_msg': 'Please add customer details to identify this project',
        'enter_customer_info': '📝 Enter Customer Information',
        'customer_name': 'Customer Name',
        'company_name': 'Company/Business Name',
        'phone_number': 'Phone Number',
        'telegram_username': 'Telegram Username',
        'email_address': 'Email Address',
        'address': 'Address',
        'save_customer_info': '💾 Save Customer Information',
        'edit_info': '✏️ Edit Info',
        'contact_details': '📞 Contact Details',
        'total_devices': '⚡ Total Devices',
        'daily_consumption': '🔋 Daily Consumption',
        'system_cost': '💰 System Cost',
        'self_sufficiency': '🎯 Self Sufficiency',
        
        # Devices
        'device_management': '⚡ Device Management',
        'device_subtitle': 'Manage your household and business electrical devices',
        'add_device': '➕ Add Device',
        'device_list': '📋 Device List',
        'quick_add': '🎯 Quick Add',
        'device_name': 'Device Name',
        'power_consumption': 'Power Consumption (W)',
        'daily_usage_hours': 'Daily Usage Hours',
        'device_category': 'Device Category',
        'priority_device': '⭐ Priority Device (Essential)',
        'inverter_tech': '⚡ Smart Inverter Technology',
        'quantity': 'Quantity',
        'add_devices': '➕ Add Device(s)',
        
        # System Config
        'system_config': '🔧 System Configuration',
        'system_subtitle': 'Configure your solar system or use auto-recommendations based on your devices',
        'auto_recommendations': '🤖 Auto-Calculated Recommendations',
        'based_on_devices': 'Based on {} devices with {:.2f} kWh/day load',
        'solar_panels': '☀️ Solar Panels',
        'battery': '🔋 Battery',
        'inverter': '⚡ Inverter',
        'recommended': '📊 Recommended',
        'auto_fill': '🤖 Auto-Fill Recommended Values',
        'solar_config': '☀️ Solar Panel Configuration',
        'battery_config': '🔋 Battery Configuration',
        'inverter_config': '⚡ Inverter Configuration',
        'panel_model': 'Panel Model',
        'power_per_panel': 'Power per Panel (W)',
        'total_capacity': 'Total Capacity',
        'total_cost': 'Total Cost',
        'battery_model': 'Battery Model',
        'capacity_kwh': 'Capacity (kWh)',
        'voltage': 'Voltage (V)',
        'inverter_model': 'Inverter Model',
        'power_rating': 'Power Rating (kW)',
        'save_config': '💾 Save {} Configuration',
        'optimal_sizing': '✅ Optimal sizing',
        
        # Simulation
        'simulation_title': '📊 24-Hour Simulation & Analysis',
        'simulation_subtitle': 'Analyze your solar system\'s performance over 24 hours',
        'customer_project': '👤 Customer Project',
        'run_simulation': '▶️ Run 24-Hour Simulation',
        'simulation_results': '📈 Simulation Results',
        'kpi': '⚡ Key Performance Indicators',
        'pv_generation': '☀️ PV Generation',
        'total_load': '🔌 Total Load',
        'grid_import': '🔗 Grid Import',
        'energy_flow': '📊 24-Hour Energy Flow',
        'system_insights': '💡 System Insights',
        'battery_performance': '🔋 Battery Performance',
        'solar_performance': '☀️ Solar Performance',
        'energy_economics': '💰 Energy Economics',
        
        # Reports
        'reports_title': '📈 Export Reports',
        'customer_report': '👤 Customer Report',
        'download_reports': '📥 Download Reports',
        'export_excel': '📊 Export to Excel',
        'export_csv': '📄 Export to CSV',
        'export_pdf': '📕 Export to PDF',
        
        # Common
        'save': 'Save',
        'cancel': 'Cancel',
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'company': 'Company',
        'phone': 'Phone',
        'telegram': 'Telegram',
        'email': 'Email',
        'cost': 'Cost',
        'status': 'Status',
        'not_configured': 'Not configured',
        'configured': 'Configured',
        'not_set': 'Not Set',
        'na': 'N/A',
        'contact_details': '📞 Contact Details',
        'active': 'Active',
        'add_devices_btn': 'Add devices',
        'pv_capacity': '☀️ PV Capacity',
        'battery_storage': '🔋 Battery Storage',
        'ready': 'Ready',
        'not_set_btn': 'Not set',
        'setup_progress': '📊 Setup Progress',
        'devices_added': 'Devices Added',
        'solar_panels_configured': 'Solar Panels Configured',
        'battery_configured': 'Battery Configured',
        'inverter_configured': 'Inverter Configured',
        'complete': 'Complete',
        'quick_start_guide': '🚀 Quick Start Guide',
        'step_add_devices': '⚡ Add Devices',
        'step_add_devices_desc': 'Input your electrical appliances',
        'step_configure_system': '🔧 Configure System',
        'step_configure_desc': 'Set up panels, battery & inverter',
        'step_browse_products': '🛒 Browse Products',
        'step_browse_desc': 'Explore equipment options',
        'step_run_simulation_btn': '📊 Run Simulation',
        'step_simulation_desc': 'Analyze 24-hour energy flow',
        'step_export_reports': '📈 Export Reports',
        'step_export_desc': 'Generate professional reports',
        'key_features': '✨ Key Features',
        'smart_scheduling': '📱 Smart device scheduling',
        'battery_optimization': '🔋 Battery optimization',
        'pv_array_design': '☀️ PV array design',
        'roi_analysis': '💰 ROI & payback analysis',
        'interactive_viz': '📊 Interactive visualizations',
        'khmer_focus': '🌍 Khmer household focus',
        'system_overview': '🎯 System Overview',
        'load_summary': '⚡ Load Summary',
        'daily': 'Daily',
        'monthly': 'Monthly',
        'devices': 'Devices',
        'solar_generation': '☀️ Solar Generation',
        'capacity': 'Capacity',
        'monthly_est': 'Monthly Est',
        'peak_hours': 'Peak Hours',
        'system_status': '📈 System Status',
        'coverage': 'Coverage',
        'battery': 'Battery',
        'excellent': 'Excellent',
        'good': 'Good',
        'needs_increase': 'Needs Increase',
        'configure_system_msg': 'Configure system',
        
        # Devices Page - Add Device
        'add_new_device': 'Add New Device',
        'tip_select_device': '💡 Tip: Select from common devices or enter custom device name',
        'select_device_custom': 'Select Device or Choose Custom',
        'custom_device': '-- Custom Device --',
        'choose_from_common': 'Choose from common devices or select Custom to enter your own',
        'example_placeholder': 'e.g., Refrigerator, Air Conditioner',
        'number_identical': 'Number of identical devices',
        'power_rating_watts': 'Power rating in Watts per device',
        'hours_per_day': 'How many hours per day this device runs',
        'category_help': 'Category helps with scheduling recommendations',
        'priority_help': 'Priority devices get backup power preference',
        'inverter_help': 'Inverter devices save 30-40% power through variable speed control',
        
        # Energy Impact
        'energy_impact': '📊 Energy Impact',
        'energy_impact_inverter': '⚡ Energy Impact (With Inverter)',
        'power_savings': 'Power Savings',
        'save_text': 'Save',
        'yearly_cost': 'Yearly Cost',
        
        # Device List
        'your_devices': '📋 Your Devices',
        'total_devices_label': 'Total Devices',
        'daily_consumption': 'Daily Consumption',
        'priority_devices': 'Priority Devices',
        'device': 'Device',
        'type': 'Type',
        'power_w': 'Power (W)',
        'effective_w': 'Effective (W)',
        'hours_day': 'Hours/Day',
        'daily_kwh': 'Daily (kWh)',
        'monthly_kwh': 'Monthly (kWh)',
        'priority': 'Priority',
        'total_inverter_savings': '⚡ Total Inverter Savings',
        'save_month': 'Save',
        'remove_device_title': '🗑️ Remove Device',
        'select_device_remove': 'Select device to remove:',
        'remove_device_btn': '🗑️ Remove Device',
        'removed': 'Removed',
        'no_devices_yet': '📭 No Devices Yet',
        'get_started_first': 'Get started by adding your first device in the',
        'add_device_tab': 'Add Device',
        'tab_above': 'tab above.',
        'or_use_quick': 'Or use the',
        'quick_add_tab': 'Quick Add',
        'to_add_typical': 'tab to add typical household devices!',
        
        # Quick Add
        'quick_add_home_presets': '🎯 Quick Add - Home Size Presets',
        'select_home_size': 'Select a home size to add a complete set of typical devices',
        'small_home': '🏠 Small Home',
        'medium_home': '🏡 Medium Home',
        'large_home': '🏘️ Large Home',
        'size': 'Size',
        'bedrooms': 'bedrooms',
        'people': 'People',
        'monthly_usage': 'Monthly',
        'add_small_setup': '➕ Add Small Home Setup',
        'add_medium_setup': '➕ Add Medium Home Setup',
        'add_large_setup': '➕ Add Large Home Setup',
        'added_small': '✅ Added Small Home setup (14 devices)',
        'added_medium': '✅ Added Medium Home setup (26 devices)',
        'added_large': '✅ Added Large Home setup (40 devices)',
        'individual_devices': '🔧 Individual Devices',
        'add_individual_one': 'Or add individual devices one at a time',
        'already_exists': '⚠️ {} already exists',
        'added_device': '✅ Added {}',
        
        # AI Recommendations
        'ai_recommendations': '🤖 AI Recommendations',
        'ai_subtitle': 'Get intelligent device suggestions based on your home profile',
        'analyze_devices': '🔍 Analyze Current Devices',
        'ai_analyzing': '🤖 AI is analyzing your devices...',
        'recommendation': 'Recommendation',
        'reason': 'Reason',
        'add_recommended': '➕ Add Recommended Device',
        'enter_device_name': 'Please enter a device name',
    },
    'kh': {
        # Navigation
        'nav_title': '☀️ KHSolar',
        'nav_dashboard': '🏠 ផ្ទាំងគ្រប់គ្រង',
        'nav_devices': '⚡ ឧបករណ៍',
        'nav_system': '🔧 ការកំណត់ប្រព័ន្ធ',
        'nav_products': '🛒 ផលិតផល',
        'nav_simulation': '📊 ការវិភាគ',
        'nav_reports': '📈 របាយការណ៍',
        
        # Dashboard
        'dash_title': '☀️ KHSolar - កម្មវិធីរចនាប្រព័ន្ធថាមពលពន្លឺព្រះអាទិត្យ និងគ្រប់គ្រងអាជីវកម្ម',
        'dash_subtitle': 'ការរចនាប្រព័ន្ធថាមពលពន្លឺព្រះអាទិត្យសម្រាប់គ្រួសារ និងអាជីវកម្មខ្មែរ',
        'customer_info': '👤 ព័ត៌មានអតិថិជន',
        'customer_required': '👤 ត្រូវការព័ត៌មានអតិថិជន',
        'customer_required_msg': 'សូមបញ្ចូលព័ត៌មានអតិថិជន ដើម្បីកំណត់គម្រោងនេះ',
        'enter_customer_info': '📝 បញ្ចូលព័ត៌មានអតិថិជន',
        'customer_name': 'ឈ្មោះអតិថិជន',
        'company_name': 'ឈ្មោះក្រុមហ៊ុន/អាជីវកម្ម',
        'phone_number': 'លេខទូរស័ព្ទ',
        'telegram_username': 'គណនី Telegram',
        'email_address': 'អ៊ីមែល',
        'address': 'អាសយដ្ឋាន',
        'save_customer_info': '💾 រក្សាទុកព័ត៌មានអតិថិជន',
        'edit_info': '✏️ កែសម្រួល',
        'contact_details': '📞 ព័ត៌មានទំនាក់ទំនង',
        'total_devices': '⚡ ឧបករណ៍សរុប',
        'daily_consumption': '🔋 ការប្រើប្រាស់ប្រចាំថ្ងៃ',
        'system_cost': '💰 តម្លៃប្រព័ន្ធ',
        'self_sufficiency': '🎯 ភាពឯករាជ្យ',
        
        # Devices
        'device_management': '⚡ ការគ្រប់គ្រងឧបករណ៍',
        'device_subtitle': 'គ្រប់គ្រងឧបករណ៍អគ្គិសនីក្នុងផ្ទះ និងអាជីវកម្មរបស់អ្នក',
        'add_device': '➕ បន្ថែមឧបករណ៍',
        'device_list': '📋 បញ្ជីឧបករណ៍',
        'quick_add': '🎯 បន្ថែមរហ័ស',
        'device_name': 'ឈ្មោះឧបករណ៍',
        'power_consumption': 'ការប្រើថាមពល (វ៉ាត់)',
        'daily_usage_hours': 'ម៉ោងប្រើប្រាស់ក្នុងមួយថ្ងៃ',
        'device_category': 'ប្រភេទឧបករណ៍',
        'priority_device': '⭐ ឧបករណ៍អាទិភាព (សំខាន់)',
        'inverter_tech': '⚡ បច្ចេកវិទ្យា Inverter ឆ្លាតវៃ',
        'quantity': 'បរិមាណ',
        'add_devices': '➕ បន្ថែមឧបករណ៍',
        
        # System Config
        'system_config': '🔧 ការកំណត់ប្រព័ន្ធ',
        'system_subtitle': 'កំណត់ប្រព័ន្ធថាមពលពន្លឺព្រះអាទិត្យ ឬប្រើការណែនាំស្វ័យប្រវត្តិតាមឧបករណ៍របស់អ្នក',
        'auto_recommendations': '🤖 ការណែនាំគណនាស្វ័យប្រវត្តិ',
        'based_on_devices': 'ផ្អែកលើឧបករណ៍ {} ជាមួយបន្ទុក {:.2f} kWh/ថ្ងៃ',
        'solar_panels': '☀️ បន្ទះពន្លឺព្រះអាទិត្យ',
        'battery': '🔋 ថ្ម',
        'inverter': '⚡ ឧបករណ៍បំលែង',
        'recommended': '📊 បានណែនាំ',
        'auto_fill': '🤖 បំពេញតម្លៃដែលបានណែនាំ',
        'solar_config': '☀️ ការកំណត់បន្ទះពន្លឺព្រះអាទិត្យ',
        'battery_config': '🔋 ការកំណត់ថ្ម',
        'inverter_config': '⚡ ការកំណត់ឧបករណ៍បំលែង',
        'panel_model': 'ម៉ូដែលបន្ទះ',
        'power_per_panel': 'ថាមពលក្នុងមួយបន្ទះ (វ៉ាត់)',
        'total_capacity': 'សមត្ថភាពសរុប',
        'total_cost': 'តម្លៃសរុប',
        'battery_model': 'ម៉ូដែលថ្ម',
        'capacity_kwh': 'សមត្ថភាព (kWh)',
        'voltage': 'វ៉ុលថាម (V)',
        'inverter_model': 'ម៉ូដែលឧបករណ៍បំលែង',
        'power_rating': 'អត្រាថាមពល (kW)',
        'save_config': '💾 រក្សាទុកការកំណត់{}',
        'optimal_sizing': '✅ ទំហំល្អបំផុត',
        
        # Simulation
        'simulation_title': '📊 ការវិភាគ និងការធ្វើត្រាប់តាម 24 ម៉ោង',
        'simulation_subtitle': 'វិភាគការអនុវត្តប្រព័ន្ធថាមពលពន្លឺព្រះអាទិត្យក្នុងរយៈពេល 24 ម៉ោង',
        'customer_project': '👤 គម្រោងអតិថិជន',
        'run_simulation': '▶️ ដំណើរការការធ្វើត្រាប់តាម 24 ម៉ោង',
        'simulation_results': '📈 លទ្ធផលការធ្វើត្រាប់តាម',
        'kpi': '⚡ សូចនាករសម្រេចការងារសំខាន់',
        'pv_generation': '☀️ ការផលិតថាមពលពន្លឺព្រះអាទិត្យ',
        'total_load': '🔌 បន្ទុកសរុប',
        'grid_import': '🔗 ការនាំចូលពីបណ្តាញ',
        'energy_flow': '📊 លំហូរថាមពល 24 ម៉ោង',
        'system_insights': '💡 ការយល់ដឹងអំពីប្រព័ន្ធ',
        'battery_performance': '🔋 ការអនុវត្តថ្ម',
        'solar_performance': '☀️ ការអនុវត្តថាមពលពន្លឺព្រះអាទិត្យ',
        'energy_economics': '💰 សេដ្ឋកិច្ចថាមពល',
        
        # Reports
        'reports_title': '📈 នាំចេញរបាយការណ៍',
        'customer_report': '👤 របាយការណ៍អតិថិជន',
        'download_reports': '📥 ទាញយករបាយការណ៍',
        'export_excel': '📊 នាំចេញទៅ Excel',
        'export_csv': '📄 នាំចេញទៅ CSV',
        'export_pdf': '📕 នាំចេញទៅ PDF',
        
        # Common
        'save': 'រក្សាទុក',
        'cancel': 'បោះបង់',
        'success': 'ជោគជ័យ',
        'error': 'កំហុស',
        'warning': 'ការព្រមាន',
        'company': 'ក្រុមហ៊ុន',
        'phone': 'ទូរស័ព្ទ',
        'telegram': 'Telegram',
        'email': 'អ៊ីមែល',
        'cost': 'តម្លៃ',
        'status': 'ស្ថានភាព',
        'not_configured': 'មិនទាន់កំណត់',
        'configured': 'បានកំណត់',
        'not_set': 'មិនទាន់កំណត់',
        'na': 'មិនមាន',
        'contact_details': '📞 ព័ត៌មានទំនាក់ទំនង',
        'active': 'សកម្ម',
        'add_devices_btn': 'បន្ថែមឧបករណ៍',
        'pv_capacity': '☀️ សមត្ថភាព PV',
        'battery_storage': '🔋 ឃ្លាំងថ្ម',
        'ready': 'ត្រៀមរួចរាល់',
        'not_set_btn': 'មិនទាន់កំណត់',
        'setup_progress': '📊 ដំណើរការរៀបចំ',
        'devices_added': 'បានបន្ថែមឧបករណ៍',
        'solar_panels_configured': 'បានកំណត់បន្ទះពន្លឺព្រះអាទិត្យ',
        'battery_configured': 'បានកំណត់ថ្ម',
        'inverter_configured': 'បានកំណត់ឧបករណ៍បំលែង',
        'complete': 'បានបញ្ចប់',
        'quick_start_guide': '🚀 មគ្គុទ្ទេសក៍ចាប់ផ្តើមរហ័ស',
        'step_add_devices': '⚡ បន្ថែមឧបករណ៍',
        'step_add_devices_desc': 'បញ្ចូលឧបករណ៍អគ្គិសនីរបស់អ្នក',
        'step_configure_system': '🔧 កំណត់ប្រព័ន្ធ',
        'step_configure_desc': 'រៀបចំបន្ទះ ថ្ម និងឧបករណ៍បំលែង',
        'step_browse_products': '🛒 រកមើលផលិតផល',
        'step_browse_desc': 'ស្វែងរកជម្រើសឧបករណ៍',
        'step_run_simulation_btn': '📊 ដំណើរការការធ្វើត្រាប់តាម',
        'step_simulation_desc': 'វិភាគលំហូរថាមពល 24 ម៉ោង',
        'step_export_reports': '📈 នាំចេញរបាយការណ៍',
        'step_export_desc': 'បង្កើតរបាយការណ៍វិជ្ជាជីវៈ',
        'key_features': '✨ មុខងារសំខាន់',
        'smart_scheduling': '📱 កាលវិភាគឧបករណ៍ឆ្លាតវៃ',
        'battery_optimization': '🔋 ការបង្កើនប្រសិទ្ធភាពថ្ម',
        'pv_array_design': '☀️ ការរចនាបន្ទះពន្លឺព្រះអាទិត្យ',
        'roi_analysis': '💰 ការវិភាគ ROI និងការសងត្រលប់',
        'interactive_viz': '📊 ការបង្ហាញអន្តរកម្ម',
        'khmer_focus': '🌍 ផ្តោតលើគ្រួសារខ្មែរ',
        'system_overview': '🎯 ទិដ្ឋភាពទូទៅប្រព័ន្ធ',
        'load_summary': '⚡ សង្ខេបបន្ទុក',
        'daily': 'ប្រចាំថ្ងៃ',
        'monthly': 'ប្រចាំខែ',
        'devices': 'ឧបករណ៍',
        'solar_generation': '☀️ ការផលិតថាមពលពន្លឺព្រះអាទិត្យ',
        'capacity': 'សមត្ថភាព',
        'monthly_est': 'ប៉ាន់ស្មានប្រចាំខែ',
        'peak_hours': 'ម៉ោងកំពូល',
        'system_status': '📈 ស្ថានភាពប្រព័ន្ធ',
        'coverage': 'ការគ្របដណ្តប់',
        'battery': 'ថ្ម',
        'excellent': 'ល្អឥតខ្ចោះ',
        'good': 'ល្អ',
        'needs_increase': 'ត្រូវការបង្កើន',
        'configure_system_msg': 'កំណត់ប្រព័ន្ធ',
        
        # Devices Page - Add Device
        'add_new_device': 'បន្ថែមឧបករណ៍ថ្មី',
        'tip_select_device': '💡 ព័ត៌មាន៖ ជ្រើសរើសពីឧបករណ៍ទូទៅ ឬបញ្ចូលឈ្មោះផ្ទាល់ខ្លួន',
        'select_device_custom': 'ជ្រើសរើសឧបករណ៍ ឬជ្រើសផ្ទាល់ខ្លួន',
        'custom_device': '-- ឧបករណ៍ផ្ទាល់ខ្លួន --',
        'choose_from_common': 'ជ្រើសរើសពីឧបករណ៍ទូទៅ ឬជ្រើសផ្ទាល់ខ្លួនដើម្បីបញ្ចូលផ្ទាល់',
        'example_placeholder': 'ឧ.៖ ទូរទឹកកក ម៉ាស៊ីនត្រជាក់',
        'number_identical': 'ចំនួនឧបករណ៍ដូចគ្នា',
        'power_rating_watts': 'កម្លាំងថាមពលជាវ៉ាត់ក្នុងមួយឧបករណ៍',
        'hours_per_day': 'ចំនួនម៉ោងដែលឧបករណ៍នេះដំណើរការក្នុងមួយថ្ងៃ',
        'category_help': 'ប្រភេទជួយក្នុងការណែនាំកាលវិភាគ',
        'priority_help': 'ឧបករណ៍អាទិភាពទទួលបានថាមពលបម្រុងជាមុន',
        'inverter_help': 'ឧបករណ៍ Inverter សន្សំថាមពល 30-40% តាមរយៈការគ្រប់គ្រងល្បឿនប្រែប្រួល',
        
        # Energy Impact
        'energy_impact': '📊 ផលប៉ះពាល់ថាមពល',
        'energy_impact_inverter': '⚡ ផលប៉ះពាល់ថាមពល (ជាមួយ Inverter)',
        'power_savings': 'ការសន្សំថាមពល',
        'save_text': 'សន្សំ',
        'yearly_cost': 'តម្លៃប្រចាំឆ្នាំ',
        
        # Device List
        'your_devices': '📋 ឧបករណ៍របស់អ្នក',
        'total_devices_label': 'ឧបករណ៍សរុប',
        'daily_consumption': 'ការប្រើប្រាស់ប្រចាំថ្ងៃ',
        'priority_devices': 'ឧបករណ៍អាទិភាព',
        'device': 'ឧបករណ៍',
        'type': 'ប្រភេទ',
        'power_w': 'ថាមពល (វ៉ាត់)',
        'effective_w': 'ប្រសិទ្ធភាព (វ៉ាត់)',
        'hours_day': 'ម៉ោង/ថ្ងៃ',
        'daily_kwh': 'ប្រចាំថ្ងៃ (kWh)',
        'monthly_kwh': 'ប្រចាំខែ (kWh)',
        'priority': 'អាទិភាព',
        'total_inverter_savings': '⚡ ការសន្សំ Inverter សរុប',
        'save_month': 'សន្សំ',
        'remove_device_title': '🗑️ លុបឧបករណ៍',
        'select_device_remove': 'ជ្រើសរើសឧបករណ៍ដើម្បីលុប៖',
        'remove_device_btn': '🗑️ លុបឧបករណ៍',
        'removed': 'បានលុប',
        'no_devices_yet': '📭 មិនទាន់មានឧបករណ៍',
        'get_started_first': 'ចាប់ផ្តើមដោយបន្ថែមឧបករណ៍ទីមួយរបស់អ្នកនៅក្នុង',
        'add_device_tab': 'បន្ថែមឧបករណ៍',
        'tab_above': 'ផ្ទាំងខាងលើ។',
        'or_use_quick': 'ឬប្រើ',
        'quick_add_tab': 'បន្ថែមរហ័ស',
        'to_add_typical': 'ផ្ទាំងដើម្បីបន្ថែមឧបករណ៍ក្នុងគ្រួសារធម្មតា!',
        
        # Quick Add
        'quick_add_home_presets': '🎯 បន្ថែមរហ័ស - ទំហំផ្ទះជាមុន',
        'select_home_size': 'ជ្រើសរើសទំហំផ្ទះដើម្បីបន្ថែមឧបករណ៍ធម្មតាពេញលេញ',
        'small_home': '🏠 ផ្ទះតូច',
        'medium_home': '🏡 ផ្ទះមធ្យម',
        'large_home': '🏘️ ផ្ទះធំ',
        'size': 'ទំហំ',
        'bedrooms': 'បន្ទប់គេង',
        'people': 'នាក់',
        'monthly_usage': 'ប្រចាំខែ',
        'add_small_setup': '➕ បន្ថែមការរៀបចំផ្ទះតូច',
        'add_medium_setup': '➕ បន្ថែមការរៀបចំផ្ទះមធ្យម',
        'add_large_setup': '➕ បន្ថែមការរៀបចំផ្ទះធំ',
        'added_small': '✅ បានបន្ថែមការរៀបចំផ្ទះតូច (14 ឧបករណ៍)',
        'added_medium': '✅ បានបន្ថែមការរៀបចំផ្ទះមធ្យម (26 ឧបករណ៍)',
        'added_large': '✅ បានបន្ថែមការរៀបចំផ្ទះធំ (40 ឧបករណ៍)',
        'individual_devices': '🔧 ឧបករណ៍ម្តងមួយ',
        'add_individual_one': 'ឬបន្ថែមឧបករណ៍ម្តងមួយៗ',
        'already_exists': '⚠️ {} មានរួចហើយ',
        'added_device': '✅ បានបន្ថែម {}',
        
        # AI Recommendations
        'ai_recommendations': '🤖 ការណែនាំដោយ AI',
        'ai_subtitle': 'ទទួលបានការណែនាំឧបករណ៍ឆ្លាតវៃផ្អែកលើប្រវត្តិរូបផ្ទះរបស់អ្នក',
        'analyze_devices': '🔍 វិភាគឧបករណ៍បច្ចុប្បន្ន',
        'ai_analyzing': '🤖 AI កំពុងវិភាគឧបករណ៍របស់អ្នក...',
        'recommendation': 'ការណែនាំ',
        'reason': 'មូលហេតុ',
        'add_recommended': '➕ បន្ថែមឧបករណ៍ដែលបានណែនាំ',
        'enter_device_name': 'សូមបញ្ចូលឈ្មោះឧបករណ៍',
    }
}

# Initialize VIP user database
def init_vip_database():
    """Initialize SQLite database for VIP users"""
    conn = sqlite3.connect('vip_users.db')
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

def check_vip_status(phone=None, telegram=None):
    """Check if user is VIP by phone or telegram"""
    try:
        conn = sqlite3.connect('vip_users.db')
        c = conn.cursor()
        
        if phone:
            c.execute('SELECT is_vip, expires_at FROM vip_users WHERE phone = ?', (phone,))
        elif telegram:
            telegram_clean = telegram.strip().lstrip('@')
            c.execute('SELECT is_vip, expires_at FROM vip_users WHERE telegram = ?', (telegram_clean,))
        else:
            return False
            
        result = c.fetchone()
        conn.close()
        
        if result and result[0] == 1:
            # Check if VIP hasn't expired
            if result[1] is None:  # No expiration
                return True
            expires = datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S')
            return datetime.now() < expires
        return False
    except:
        return False

def add_vip_user(phone, telegram='', name='', email='', expires_at=None):
    """Add or update VIP user"""
    try:
        conn = sqlite3.connect('vip_users.db')
        c = conn.cursor()
        telegram_clean = telegram.strip().lstrip('@') if telegram else ''
        
        c.execute('''INSERT OR REPLACE INTO vip_users 
                     (phone, telegram, name, email, is_vip, expires_at)
                     VALUES (?, ?, ?, ?, 1, ?)''',
                  (phone, telegram_clean, name, email, expires_at))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding VIP user: {e}")
        return False

# VIP Login Functions
def verify_vip_login(username, password):
    """Verify VIP login credentials"""
    import hashlib
    try:
        conn = sqlite3.connect('admin_users.db')
        c = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT id, username FROM admin_users WHERE username = ? AND password_hash = ?',
                  (username, password_hash))
        result = c.fetchone()
        conn.close()
        return result is not None
    except:
        return False

# Initialize session state
if 'devices' not in st.session_state:
    st.session_state.devices = []
if 'system_config' not in st.session_state:
    st.session_state.system_config = SystemConfiguration()
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'product_manager' not in st.session_state:
    st.session_state.product_manager = ProductManager()
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'is_vip' not in st.session_state:
    st.session_state.is_vip = False
if 'vip_logged_in' not in st.session_state:
    st.session_state.vip_logged_in = False
if 'vip_username' not in st.session_state:
    st.session_state.vip_username = ''
if 'show_vip_login' not in st.session_state:
    st.session_state.show_vip_login = False
if 'customer_info' not in st.session_state:
    st.session_state.customer_info = {
        'name': '',
        'company': '',
        'phone': '',
        'telegram': '',
        'email': '',
        'address': ''
    }
if 'language' not in st.session_state:
    st.session_state.language = 'en'  # Default to English

# Helper function to get translation
def t(key):
    """Get translation for current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# ==================== SIDEBAR - ONE PAGE DESIGN ====================
# Compact Sidebar Header with Logo
st.sidebar.markdown("""
<div style='
    text-align: center;
    padding: 1rem 0.5rem 0.75rem 0.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    margin-bottom: 1rem;
    box-shadow: 0 3px 10px rgba(102, 126, 234, 0.2);
'>
    <div style='font-size: 2.2rem; margin-bottom: 0.2rem;'>☀️</div>
    <div style='color: white; font-size: 1.2rem; font-weight: 800; letter-spacing: 0.5px;'>KHSolar</div>
    <div style='color: rgba(255,255,255,0.85); font-size: 0.65rem; font-weight: 500; margin-top: 0.1rem;'>Solar Designer</div>
</div>
""", unsafe_allow_html=True)

# VIP Login Button and Status
if not st.session_state.is_vip and not st.session_state.vip_logged_in:
    # Show VIP Login button
    if st.sidebar.button("👑 VIP Login", use_container_width=True, type="primary"):
        st.session_state.show_vip_login = True
        st.rerun()
elif st.session_state.vip_logged_in:
    # Show VIP status for logged in users
    st.sidebar.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 0.5rem; border-radius: 0.5rem; text-align: center; margin-bottom: 0.5rem;'>
        <div style='color: white; font-weight: 700; font-size: 0.9rem;'>👑 VIP ACCESS</div>
        <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem;'>{st.session_state.vip_username}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.vip_logged_in = False
        st.session_state.is_vip = False
        st.session_state.vip_username = ''
        st.success("✅ Logged out successfully")
        st.rerun()
elif st.session_state.is_vip:
    # Show VIP status for auto-detected users
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 0.5rem; border-radius: 0.5rem; text-align: center; margin-bottom: 0.5rem;'>
        <div style='color: white; font-weight: 700; font-size: 0.9rem;'>👑 VIP ACCESS</div>
        <div style='color: rgba(255,255,255,0.9); font-size: 0.7rem;'>All Features Unlocked</div>
    </div>
    """, unsafe_allow_html=True)

# Navigation Menu - VIP features unlocked for VIP users
if st.session_state.is_vip or st.session_state.vip_logged_in:
    # VIP users see all features without locks
    page = st.sidebar.radio("📍 Navigate", [
        t('nav_dashboard'),
        t('nav_devices'),
        t('nav_system'),
        t('nav_products'),
        t('nav_simulation'),
        t('nav_reports')
    ], label_visibility="visible")
else:
    # Non-VIP users see locked features
    page = st.sidebar.radio("📍 Navigate", [
        t('nav_dashboard'),
        t('nav_devices') + " 🔒",
        t('nav_system') + " 🔒",
        t('nav_products') + " 🔒",
        t('nav_simulation') + " 🔒",
        t('nav_reports') + " 🔒"
    ], label_visibility="visible")
    
    # Check if user trying to access VIP features
    if "🔒" in page:
        st.warning("🔒 **VIP Feature** - This feature is only available for VIP users. Contact admin: +855888836588 or @chhanycls")
        page = t('nav_dashboard')  # Redirect to dashboard

st.sidebar.markdown("<div style='margin: 0.75rem 0;'><hr style='margin: 0; border: none; border-top: 1px solid #e5e7eb;'></div>", unsafe_allow_html=True)

# Compact Flag-Based Language Switcher
current_lang = st.session_state.language
en_active = current_lang == 'en'
kh_active = current_lang == 'kh'

# Flag-only language selector - Ultra compact
st.sidebar.markdown("""
<div style='text-align: center; margin: 0.5rem 0 0.4rem 0;'>
    <div style='font-size: 0.65rem; color: #9ca3af; font-weight: 600;'>🌐 LANGUAGE</div>
</div>
""", unsafe_allow_html=True)

lang_col1, lang_col2 = st.sidebar.columns(2)
with lang_col1:
    if st.button("🇬🇧 Eng", use_container_width=True, key="lang_en_toggle", 
                 type="primary" if en_active else "secondary",
                 help="English"):
        st.session_state.language = 'en'
        st.rerun()
with lang_col2:
    if st.button("🇰🇭 ខ្មែរ", use_container_width=True, key="lang_kh_toggle", 
                 type="primary" if kh_active else "secondary",
                 help="Khmer Language"):
        st.session_state.language = 'kh'
        st.rerun()

# ==================== DASHBOARD ====================
if page == t('nav_dashboard'):
    # VIP Login Popup Modal
    if st.session_state.show_vip_login:
        st.markdown("""
        <div style='
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        '>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form in centered container
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container():
                st.markdown("""
                <div style='
                    background: white;
                    padding: 2rem;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                '>
                    <h2 style='text-align: center; color: #667eea; margin-bottom: 0.5rem;'>👑 VIP Login</h2>
                    <p style='text-align: center; color: #666; margin-bottom: 1.5rem;'>Enter your credentials to access VIP features</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("vip_login_form", clear_on_submit=True):
                    username = st.text_input("👤 Username", placeholder="Enter username")
                    password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        submit = st.form_submit_button("🔓 Login", type="primary", use_container_width=True)
                    with col_b:
                        cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
                    
                    if submit:
                        if username and password:
                            if verify_vip_login(username, password):
                                st.session_state.vip_logged_in = True
                                st.session_state.is_vip = True
                                st.session_state.vip_username = username
                                st.session_state.show_vip_login = False
                                st.success(f"✅ Welcome, {username}! VIP access granted.")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Invalid username or password")
                        else:
                            st.warning("⚠️ Please enter both username and password")
                    
                    if cancel:
                        st.session_state.show_vip_login = False
                        st.rerun()
                
                st.markdown("<div style='text-align: center; margin-top: 1rem; color: #666; font-size: 0.85rem;'>🔒 Secure VIP Access</div>", unsafe_allow_html=True)
    
    # Remove top hero section completely to save space
    
    # Enhanced Customer Information Section
    if st.session_state.customer_info['name'] or st.session_state.customer_info['company']:
        # Display existing customer info in enhanced card
        customer_display = st.session_state.customer_info['name'] or t('not_set')
        company_display = st.session_state.customer_info['company'] or t('na')
        phone_display = st.session_state.customer_info['phone'] or t('na')
        email_display = st.session_state.customer_info['email'] or t('na')
        telegram_display = st.session_state.customer_info.get('telegram', '') or t('na')
        address_display = st.session_state.customer_info.get('address', '') or t('na')
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
            padding: 1.2rem; 
            border-radius: 12px; 
            margin-bottom: 0.75rem;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.18);
        ">
            <div style="display: flex; align-items: center; gap: 1.5rem;">
                <div style="flex: 0 0 auto;">
                    <div style="
                        background: rgba(255,255,255,0.25); 
                        backdrop-filter: blur(10px);
                        width: 55px; 
                        height: 55px; 
                        border-radius: 50%; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        border: 2px solid rgba(255,255,255,0.4);
                    ">
                        <span style="font-size: 1.6rem;">👤</span>
                    </div>
                </div>
                <div style="flex: 1;">
                    <div style="display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 0.3rem;">
                        <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 700;">{customer_display}</h3>
                        <span style="
                            background: rgba(255,255,255,0.25); 
                            padding: 0.2rem 0.6rem; 
                            border-radius: 15px; 
                            font-size: 0.65rem; 
                            color: white;
                            font-weight: 600;
                        ">✅ ACTIVE</span>
                    </div>
                    <p style="color: rgba(255,255,255,0.95); margin: 0; font-size: 0.85rem; font-weight: 500;">🏢 {company_display}</p>
                    <p style="color: rgba(255,255,255,0.85); margin: 0.25rem 0 0 0; font-size: 0.8rem;">📍 {address_display}</p>
                </div>
                <div style="flex: 0 0 auto; display: flex; flex-direction: column; gap: 0.5rem; text-align: right;">
                    <div style="
                        background: rgba(255,255,255,0.2); 
                        backdrop-filter: blur(10px);
                        padding: 0.5rem 1rem; 
                        border-radius: 8px;
                        border: 1px solid rgba(255,255,255,0.3);
                    ">
                        <p style="color: white; margin: 0 0 0.2rem 0; font-size: 0.7rem; opacity: 0.9;">📞 Contact</p>
                        <p style="color: white; margin: 0; font-size: 0.85rem; font-weight: 600;">{phone_display}</p>
                        <p style="color: rgba(255,255,255,0.9); margin: 0.2rem 0 0 0; font-size: 0.7rem;">✉️ {email_display}</p>
                    </div>
                    <div style="
                        background: rgba(255,255,255,0.2); 
                        backdrop-filter: blur(10px);
                        padding: 0.5rem 1rem; 
                        border-radius: 8px;
                        border: 1px solid rgba(255,255,255,0.3);
                    ">
                        <p style="color: white; margin: 0 0 0.2rem 0; font-size: 0.7rem; opacity: 0.9;">💬 Telegram</p>
                        <p style="color: white; margin: 0; font-size: 0.85rem; font-weight: 600;">@{telegram_display}</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Functional Edit Button - Compact
        edit_col1, edit_col2, edit_col3 = st.columns([1, 2, 1])
        with edit_col2:
            if st.button("✏️ Edit Info", key="edit_customer_btn", use_container_width=True, type="secondary"):
                st.session_state.show_customer_form = True
                st.rerun()
    else:
        # Show form to add customer info
        st.markdown(f"""
        <div class="warning-box">
            <h3>{t('customer_required')}</h3>
            <p>{t('customer_required_msg')}</p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.show_customer_form = True
    
    # Customer info input form
    if st.session_state.get('show_customer_form', False) or not st.session_state.customer_info['name']:
        st.markdown(f"### {t('enter_customer_info')}")
        
        with st.form("customer_info_form"):
            form_col1, form_col2 = st.columns(2)
            
            with form_col1:
                name = st.text_input(
                    f"{t('customer_name')} *",
                    value=st.session_state.customer_info['name'],
                    placeholder="e.g., Sok Pisey"
                )
                company = st.text_input(
                    t('company_name'),
                    value=st.session_state.customer_info['company'],
                    placeholder="e.g., Pisey Electronics Shop"
                )
                phone = st.text_input(
                    f"{t('phone_number')} *",
                    value=st.session_state.customer_info['phone'],
                    placeholder="e.g., +855 12 345 678"
                )
            
            with form_col2:
                telegram = st.text_input(
                    t('telegram_username'),
                    value=st.session_state.customer_info['telegram'],
                    placeholder="@username or +855123456789",
                    help="Enter Telegram username or phone number"
                )
                email = st.text_input(
                    t('email_address'),
                    value=st.session_state.customer_info['email'],
                    placeholder="e.g., pisey@example.com"
                )
                address = st.text_input(
                    t('address'),
                    value=st.session_state.customer_info['address'],
                    placeholder="e.g., Phnom Penh, Cambodia"
                )
            
            submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
            with submit_col2:
                submitted = st.form_submit_button(t('save_customer_info'), type="primary", use_container_width=True)
            
            if submitted:
                if name and phone:
                    # Validate Telegram username/phone format if provided
                    telegram_valid = True
                    telegram_clean = telegram
                    
                    if telegram:
                        telegram_clean = telegram.strip().lstrip('@').lstrip('+')
                        
                        # Check if it's a phone number (digits only, possibly with +)
                        if telegram_clean.replace('+', '').isdigit():
                            # Valid phone number format
                            if len(telegram_clean) < 8 or len(telegram_clean) > 15:
                                st.error("⚠️ Phone number must be 8-15 digits")
                                telegram_valid = False
                        else:
                            # Check if username is valid (alphanumeric, underscore, 5-32 chars)
                            if not re.match(r'^[a-zA-Z0-9_]{5,32}$', telegram_clean):
                                st.error("⚠️ Telegram username must be 5-32 characters (letters, numbers, underscore only) or a valid phone number")
                                telegram_valid = False
                    
                    if telegram_valid:
                        # Check VIP status
                        is_vip = check_vip_status(phone=phone, telegram=telegram_clean)
                        st.session_state.is_vip = is_vip
                        
                        st.session_state.customer_info = {
                            'name': name,
                            'company': company,
                            'phone': phone,
                            'telegram': telegram_clean,
                            'email': email,
                            'address': address
                        }
                        st.session_state.show_customer_form = False
                        
                        success_msg = f"✅ Customer information saved for {name}"
                        if telegram_clean:
                            if telegram_clean.isdigit():
                                success_msg += f" | Telegram: +{telegram_clean}"
                            else:
                                success_msg += f" | Telegram: @{telegram_clean}"
                        
                        if is_vip:
                            success_msg += " | 👑 VIP ACCESS GRANTED"
                        
                        st.success(success_msg)
                        st.rerun()
                else:
                    st.error("⚠️ Please enter at least Customer Name and Phone Number")
    
    # =============== SYSTEM SIZING ===============
    if st.session_state.customer_info['name']:
        with st.container():
            with st.form("quick_sizing_form"):
                st.markdown("### 📊 System Configuration")
                
                # Row 1: kWh Usage, Status, and System Type
                input_row1_col1, input_row1_col2, input_row1_col3 = st.columns(3)
                with input_row1_col1:
                    monthly_kwh = st.number_input(
                        "⚡ Monthly kWh Usage *",
                        min_value=50,
                        max_value=10000,
                        value=300,
                        step=50,
                        help="Enter your average monthly electricity consumption in kWh (Required)"
                    )
                
                with input_row1_col2:
                    usage_status = st.selectbox(
                        "📊 Usage Status",
                        ["Average", "Low Usage", "High Usage", "Peak Season"],
                        help="Select your typical usage pattern"
                    )
                
                with input_row1_col3:
                    system_type = st.selectbox(
                        "🔧 System Type *",
                        ["Hybrid (Grid + Battery)", "On-Grid (No Battery)", "Off-Grid (Full Battery)"],
                        help="Choose your preferred system configuration"
                    )
                
                # Row 3: Brand Selection (Optional - Auto-recommend if empty)
                st.markdown("---")
                st.markdown("##### 🏷️ Component Selection (Optional - Leave empty for auto-recommend)")
                
                # Get available brands from product manager
                pm = st.session_state.product_manager
                
                # Get PV panel brands
                pv_products = [p for p in pm.products.values() if p.category == 'pv_panel']
                pv_brands = sorted(list(set([p.name for p in pv_products])))
                pv_brands.insert(0, "Auto-Recommend (Best Value)")
                
                # Get battery brands
                battery_products = [p for p in pm.products.values() if p.category == 'battery']
                battery_brands = sorted(list(set([p.name for p in battery_products])))
                battery_brands.insert(0, "Auto-Recommend (Best Value)")
                
                # Get inverter brands
                inverter_products = [p for p in pm.products.values() if p.category == 'inverter']
                inverter_brands = sorted(list(set([p.name for p in inverter_products])))
                inverter_brands.insert(0, "Auto-Recommend (Best Value)")
                
                brand_col1, brand_col2, brand_col3 = st.columns(3)
                
                with brand_col1:
                    selected_pv = st.selectbox(
                        "☀️ Solar Panel Brand",
                        pv_brands,
                        help="Select specific panel or leave as auto-recommend"
                    )
                
                with brand_col2:
                    selected_battery = st.selectbox(
                        "🔋 Battery Brand",
                        battery_brands,
                        help="Select specific battery or leave as auto-recommend"
                    )
                
                with brand_col3:
                    selected_inverter = st.selectbox(
                        "⚡ Inverter Brand",
                        inverter_brands,
                        help="Select specific inverter or leave as auto-recommend"
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
                with submit_col2:
                    calculate_system = st.form_submit_button("⚡ Calculate System", type="primary", use_container_width=True)
                
                if calculate_system:
                    # Calculate system requirements
                    daily_kwh = monthly_kwh / 30
                    sunlight_hours = st.session_state.system_config.sunlight_hours
                    
                    # Calculate PV requirement (with 15% safety margin and system losses)
                    pv_kw_needed = (daily_kwh / sunlight_hours) * 1.25
                    
                    # Calculate battery based on system type
                    if "Off-Grid" in system_type:
                        battery_kwh_needed = daily_kwh * 2  # 2 days autonomy
                    elif "Hybrid" in system_type:
                        battery_kwh_needed = daily_kwh * 0.7  # Night coverage
                    else:
                        battery_kwh_needed = 0  # No battery for on-grid
                    
                    # Improved inverter calculation based on actual load patterns
                    # Peak load = sum of all simultaneous loads (typically 60-70% of total daily load compressed into peak hours)
                    # For residential: peak typically occurs 6-8 hours with 3-4x average load
                    average_hourly_load = daily_kwh / 24
                    peak_load_kw = average_hourly_load * 3.5  # Peak is 3.5x average (more accurate)
                    inverter_kw_needed = peak_load_kw * 1.3  # 30% safety margin for surge protection
                    
                    # Get recommended products
                    pm = st.session_state.product_manager
                    
                    # ===== SOLAR PANEL SELECTION =====
                    if selected_pv == "Auto-Recommend (Best Value)":
                        # Auto-recommend mode: find best value panel
                        rec_panel = pm.get_recommended_panel(min_wattage=500)
                        if not rec_panel:
                            rec_panel = pm.get_recommended_panel(min_wattage=300)
                        
                        panel_wattage = rec_panel.specifications.get('power', 550) if rec_panel else 550
                        panel_cost = rec_panel.cost if rec_panel else 66.0
                        panel_name = rec_panel.name if rec_panel else "Lvtopsun 550W"
                    else:
                        # User selected specific panel
                        selected_panel_product = pm.products.get(selected_pv)
                        if selected_panel_product:
                            panel_wattage = selected_panel_product.specifications.get('power', 550)
                            panel_cost = selected_panel_product.cost
                            panel_name = selected_panel_product.name
                        else:
                            # Fallback if product not found
                            panel_wattage = 550
                            panel_cost = 66.0
                            panel_name = selected_pv
                    
                    num_panels = max(1, int((pv_kw_needed * 1000) / panel_wattage))
                    
                    # ===== BATTERY SELECTION =====
                    if battery_kwh_needed > 0:
                        if selected_battery == "Auto-Recommend (Best Value)":
                            # Auto-recommend mode
                            rec_battery = pm.get_recommended_battery(min_capacity_kwh=5.0)
                            if rec_battery:
                                battery_unit_capacity = rec_battery.specifications.get('capacity', 5.12)
                                battery_cost_per_unit = rec_battery.cost
                                battery_name = rec_battery.name
                                battery_voltage = rec_battery.specifications.get('voltage', 51.2)
                            else:
                                battery_unit_capacity = 5.12
                                battery_cost_per_unit = 1440.0
                                battery_name = "DEYE 100AH 51.2v (5.12KWH)"
                                battery_voltage = 51.2
                        else:
                            # User selected specific battery
                            selected_battery_product = pm.products.get(selected_battery)
                            if selected_battery_product:
                                battery_unit_capacity = selected_battery_product.specifications.get('capacity', 5.12)
                                battery_cost_per_unit = selected_battery_product.cost
                                battery_name = selected_battery_product.name
                                battery_voltage = selected_battery_product.specifications.get('voltage', 51.2)
                            else:
                                # Fallback
                                battery_unit_capacity = 5.12
                                battery_cost_per_unit = 1440.0
                                battery_name = selected_battery
                                battery_voltage = 51.2
                        
                        num_batteries = max(1, int(battery_kwh_needed / battery_unit_capacity))
                    else:
                        num_batteries = 0
                        battery_name = "Not Required (On-Grid System)"
                        battery_cost_per_unit = 0
                        battery_unit_capacity = 0
                        battery_voltage = 0
                    
                    # ===== INVERTER SELECTION =====
                    inv_type = "Hybrid" if "Hybrid" in system_type else "On-Grid" if "On-Grid" in system_type else "Off-Grid"
                    
                    if selected_inverter == "Auto-Recommend (Best Value)":
                        # Auto-recommend mode
                        rec_inverter = pm.get_recommended_inverter(min_power_kw=inverter_kw_needed, inverter_type=inv_type)
                        if rec_inverter:
                            inverter_power = rec_inverter.specifications.get('power', 5.0)
                            inverter_cost = rec_inverter.cost
                            inverter_name = rec_inverter.name
                        else:
                            inverter_power = max(5.0, inverter_kw_needed)
                            inverter_cost = inverter_power * 180
                            inverter_name = f"Deye {inv_type} {inverter_power:.0f}kw"
                    else:
                        # User selected specific inverter
                        selected_inverter_product = pm.products.get(selected_inverter)
                        if selected_inverter_product:
                            inverter_power = selected_inverter_product.specifications.get('power', 5.0)
                            inverter_cost = selected_inverter_product.cost
                            inverter_name = selected_inverter_product.name
                        else:
                            # Fallback
                            inverter_power = max(5.0, inverter_kw_needed)
                            inverter_cost = inverter_power * 180
                            inverter_name = selected_inverter
                    
                    # Calculate installation area (approx 2 m² per 550W panel)
                    area_per_panel = 2.0 if panel_wattage >= 500 else 1.7
                    total_area = num_panels * area_per_panel
                    
                    # Calculate costs
                    pv_cost = num_panels * panel_cost
                    battery_cost = num_batteries * battery_cost_per_unit
                    inverter_total_cost = inverter_cost
                    labor_cost = 250.0 if inverter_power <= 5 else 500.0
                    
                    # Support materials based on inverter size
                    if inverter_power <= 5.0:
                        support_cost = 450.0
                    elif inverter_power >= 10.0:
                        support_cost = 600.0
                    else:
                        support_cost = 450.0 + ((inverter_power - 5.0) / 5.0) * (600.0 - 450.0)
                    
                    equipment_cost = pv_cost + battery_cost + inverter_total_cost
                    total_wholesale = equipment_cost + labor_cost + support_cost
                    total_customer = total_wholesale * 1.3  # 30% markup
                    
                    # Store results in session state
                    st.session_state.quick_sizing_results = {
                        'monthly_kwh': monthly_kwh,
                        'daily_kwh': daily_kwh,
                        'usage_status': usage_status,
                        'system_type': system_type,
                        'selected_pv': selected_pv,
                        'selected_battery': selected_battery,
                        'selected_inverter': selected_inverter,
                        'pv_kw': pv_kw_needed,
                        'num_panels': num_panels,
                        'panel_name': panel_name,
                        'panel_wattage': panel_wattage,
                        'panel_cost': panel_cost,
                        'battery_kwh': battery_kwh_needed,
                        'num_batteries': num_batteries,
                        'battery_name': battery_name,
                        'battery_unit_capacity': battery_unit_capacity,
                        'battery_voltage': battery_voltage,
                        'battery_cost_per_unit': battery_cost_per_unit,
                        'inverter_kw': inverter_power,
                        'inverter_name': inverter_name,
                        'inverter_cost': inverter_total_cost,
                        'area_needed': total_area,
                        'equipment_cost': equipment_cost,
                        'labor_cost': labor_cost,
                        'support_cost': support_cost,
                        'total_wholesale': total_wholesale,
                        'total_customer': total_customer
                    }
                    
                    # AUTO-APPLY: Automatically configure the system
                    from models import SolarPanel, Battery, Inverter, Device
                    
                    # Apply Solar Panels
                    st.session_state.system_config.solar_panels = SolarPanel(
                        name=panel_name,
                        power_watts=panel_wattage,
                        efficiency=0.21,
                        cost_per_panel=panel_cost,
                        quantity=num_panels
                    )
                    
                    # Apply Battery (if needed)
                    if num_batteries > 0:
                        st.session_state.system_config.battery = Battery(
                            name=battery_name,
                            capacity_kwh=battery_unit_capacity,
                            voltage=battery_voltage,
                            depth_of_discharge=0.8,
                            efficiency=0.95,
                            cost=battery_cost_per_unit,
                            quantity=num_batteries
                        )
                    else:
                        st.session_state.system_config.battery = None
                    
                    # Apply Inverter
                    st.session_state.system_config.inverter = Inverter(
                        name=inverter_name,
                        power_kw=inverter_power,
                        efficiency=0.97,
                        cost=inverter_total_cost
                    )
                    
                    # AUTO-CREATE DEVICES: Generate sample devices based on daily consumption
                    # Clear existing devices and create new ones based on usage pattern
                    st.session_state.devices = []
                    
                    # Generate devices based on daily kWh (distribute across common appliances)
                    if daily_kwh > 0:
                        # Common device distribution ratios for typical usage
                        if usage_status == "Low Usage":
                            device_templates = [
                                ("Lights (LED)", 0.05, 6, 0.25),  # 50W, 6 hours
                                ("Refrigerator", 0.15, 24, 0.15),  # 150W, 24 hours
                                ("TV", 0.10, 4, 0.20),  # 100W, 4 hours
                                ("Fan", 0.075, 8, 0.20)  # 75W, 8 hours
                            ]
                        elif usage_status == "High Usage" or usage_status == "Peak Season":
                            device_templates = [
                                ("Air Conditioner", 1.5, 8, 0.35),  # 1500W, 8 hours
                                ("Refrigerator", 0.20, 24, 0.15),  # 200W, 24 hours
                                ("Water Pump", 0.75, 2, 0.10),  # 750W, 2 hours
                                ("Lights (LED)", 0.10, 8, 0.15),  # 100W, 8 hours
                                ("TV", 0.15, 5, 0.10),  # 150W, 5 hours
                                ("Washing Machine", 0.50, 2, 0.08),  # 500W, 2 hours
                                ("Microwave", 1.0, 0.5, 0.05)  # 1000W, 30 min
                            ]
                        else:  # Average
                            device_templates = [
                                ("Lights (LED)", 0.08, 7, 0.20),  # 80W, 7 hours
                                ("Refrigerator", 0.18, 24, 0.20),  # 180W, 24 hours
                                ("TV", 0.12, 5, 0.15),  # 120W, 5 hours
                                ("Fan", 0.10, 10, 0.15),  # 100W, 10 hours
                                ("Computer", 0.15, 6, 0.12),  # 150W, 6 hours
                                ("Washing Machine", 0.45, 1.5, 0.10),  # 450W, 1.5 hours
                                ("Rice Cooker", 0.70, 1, 0.08)  # 700W, 1 hour
                            ]
                        
                        # Calculate total energy from templates and scale to match input
                        total_template_ratio = sum(ratio for _, _, _, ratio in device_templates)
                        
                        # Calculate total energy from template devices
                        template_total_kwh = sum(power * hours for _, power, hours, _ in device_templates)
                        
                        # Scale factor to match actual daily_kwh input
                        scale_factor = daily_kwh / template_total_kwh if template_total_kwh > 0 else 1
                        
                        # Create devices with scaled hours to match input daily_kwh exactly
                        for device_name, power_kw, hours, ratio in device_templates:
                            # Scale hours to match total daily consumption
                            scaled_hours = hours * scale_factor
                            device = Device(
                                device_name,
                                power_kw,
                                scaled_hours,
                                1  # quantity
                            )
                            st.session_state.devices.append(device)
                    
                    st.rerun()
        
        # Display results if available
        if 'quick_sizing_results' in st.session_state and st.session_state.quick_sizing_results:
            results = st.session_state.quick_sizing_results
            
            st.markdown("---")
            
            # Configuration Summary
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                border: 2px solid #6366f1;
            ">
                <h3 style="margin: 0 0 1rem 0; color: #4338ca; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.8rem;">📋</span> Configuration Summary
                </h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div style="background: rgba(255,255,255,0.6); padding: 1rem; border-radius: 10px;">
                        <p style="margin: 0; color: #6b7280; font-size: 0.85rem; font-weight: 600;">MONTHLY USAGE</p>
                        <p style="margin: 0.3rem 0 0 0; color: #1f2937; font-size: 1.3rem; font-weight: 700;">{results['monthly_kwh']} kWh</p>
                        <p style="margin: 0.3rem 0 0 0; color: #6b7280; font-size: 0.8rem;">{results['usage_status']}</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.6); padding: 1rem; border-radius: 10px;">
                        <p style="margin: 0; color: #6b7280; font-size: 0.85rem; font-weight: 600;">SYSTEM TYPE</p>
                        <p style="margin: 0.3rem 0 0 0; color: #1f2937; font-size: 1rem; font-weight: 700;">{results['system_type']}</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.6); padding: 1rem; border-radius: 10px;">
                        <p style="margin: 0; color: #6b7280; font-size: 0.85rem; font-weight: 600;">SELECTION MODE</p>
                        <p style="margin: 0.3rem 0 0 0; color: #1f2937; font-size: 0.85rem; font-weight: 600;">
                            {'🤖 Auto-Recommended' if results['selected_pv'] == "Auto-Recommend (Best Value)" and results['selected_battery'] == "Auto-Recommend (Best Value)" and results['selected_inverter'] == "Auto-Recommend (Best Value)" else '👤 User-Selected Components'}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎯 Recommended System Configuration")
            
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                st.markdown(f"""
                <div class="success-box" style="padding: 1.5rem;">
                    <h4>☀️ Solar Panels</h4>
                    <p><b>Model:</b> {results['panel_name']}</p>
                    <p><b>Quantity:</b> {results['num_panels']} panels × {results['panel_wattage']}W</p>
                    <p><b>Total Capacity:</b> {(results['num_panels'] * results['panel_wattage'] / 1000):.2f} kW</p>
                    <p><b>Installation Area:</b> ~{results['area_needed']:.1f} m²</p>
                    <hr>
                    <p><b>Cost:</b> ${results['num_panels'] * results['panel_cost']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col2:
                st.markdown(f"""
                <div class="success-box" style="padding: 1.5rem;">
                    <h4>🔋 Battery Storage</h4>
                    <p><b>Model:</b> {results['battery_name']}</p>
                    {'<p><b>Quantity:</b> ' + str(results['num_batteries']) + ' units</p>' if results['num_batteries'] > 0 else '<p><b>Quantity:</b> Not Required</p>'}
                    {'<p><b>Unit Capacity:</b> ' + f"{results['battery_unit_capacity']:.2f}" + ' kWh</p>' if results['num_batteries'] > 0 else ''}
                    {'<p><b>Total Capacity:</b> ' + f"{results['battery_kwh']:.2f}" + ' kWh</p>' if results['num_batteries'] > 0 else '<p><b>Type:</b> On-Grid (No Battery)</p>'}
                    {'<p><b>Backup Time:</b> ~' + f"{(results['battery_kwh'] / results['daily_kwh'] * 24):.1f}" + ' hours</p>' if results['num_batteries'] > 0 else ''}
                    <hr>
                    <p><b>Cost:</b> ${results['num_batteries'] * results['battery_cost_per_unit']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col3:
                st.markdown(f"""
                <div class="success-box" style="padding: 1.5rem;">
                    <h4>⚡ Inverter</h4>
                    <p><b>Model:</b> {results['inverter_name']}</p>
                    <p><b>Power Rating:</b> {results['inverter_kw']:.1f} kW</p>
                    <p><b>Type:</b> {results['system_type']}</p>
                    <p><b>Max Output:</b> {results['inverter_kw'] * 0.9:.1f} kW</p>
                    <hr>
                    <p><b>Cost:</b> ${results['inverter_cost']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Modern Section Header
            st.markdown("""<div style='text-align: center; padding: 2rem 0 1rem 0;'>
                <h2 style='font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;'>
                    💰 Investment & Savings
                </h2>
                <p style='color: #6b7280; font-size: 1rem; margin: 0.5rem 0 0 0;'>Complete system breakdown & financial analysis</p>
            </div>""", unsafe_allow_html=True)
            
            cost_col1, cost_col2 = st.columns([1.2, 1])
            
            with cost_col1:
                # Component Pricing Cards
                st.markdown("""<div style='background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <h3 style='margin: 0 0 1rem 0; color: #111827; font-size: 1.2rem; font-weight: 700;'>📋 System Components</h3>
                </div>""", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                
                # Individual component cards
                components = [
                    {"icon": "☀️", "name": f"Solar Panels ({results['num_panels']}x {results['panel_wattage']}W)", 
                     "price": results['num_panels'] * results['panel_cost'] * 1.3, "color": "#f59e0b"},
                    {"icon": "🔋", "name": f"Battery Storage ({results['num_batteries']} units)" if results['num_batteries'] > 0 else "Battery (Not Required)",
                     "price": results['num_batteries'] * results['battery_cost_per_unit'] * 1.3 if results['num_batteries'] > 0 else 0, "color": "#10b981"},
                    {"icon": "⚡", "name": f"Inverter ({results['inverter_kw']:.1f}kW)",
                     "price": results['inverter_cost'] * 1.3, "color": "#3b82f6"},
                    {"icon": "🔧", "name": "Installation & Labor",
                     "price": results['labor_cost'] * 1.3, "color": "#8b5cf6"},
                    {"icon": "📦", "name": "Mounting & Cables",
                     "price": results['support_cost'] * 1.3, "color": "#6b7280"}
                ]
                
                for comp in components:
                    st.markdown(f"""
                    <div style='background: white; padding: 1rem; margin-bottom: 0.5rem; border-radius: 10px; 
                                border-left: 4px solid {comp['color']}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                                display: flex; justify-content: space-between; align-items: center;'>
                        <div style='display: flex; align-items: center; gap: 0.75rem;'>
                            <span style='font-size: 1.5rem;'>{comp['icon']}</span>
                            <span style='color: #374151; font-weight: 500;'>{comp['name']}</span>
                        </div>
                        <div style='color: {comp['color']}; font-weight: 700; font-size: 1.1rem;'>${comp['price']:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Telegram Send Button - Send from YOUR personal account
                if st.session_state.customer_info.get('telegram'):
                    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                    telegram_contact = st.session_state.customer_info['telegram']
                    
                    try:
                        from datetime import datetime
                        
                        # Language selector - compact
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); padding: 1rem; 
                                    border-radius: 10px; text-align: center; margin-bottom: 0.75rem;'>
                            <span style='font-size: 1.3rem; margin-right: 0.5rem;'>🌐</span>
                            <span style='color: white; font-weight: 600; font-size: 0.9rem;'>Report Language</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        report_lang = st.radio(
                            "Choose:",
                            options=["🇺🇸🇰🇭 Bilingual", "🇺🇸 English", "🇰🇭 Khmer"],
                            index=0,
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                        
                        # Map selection
                        lang_map = {
                            "🇺🇸🇰🇭 Bilingual": "bilingual",
                            "🇺🇸 English": "english",
                            "🇰🇭 Khmer": "khmer"
                        }
                        selected_language = lang_map[report_lang]
                        
                        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                        
                        # Send button
                        if st.button("📤 Send Report to My Telegram", type="primary", use_container_width=True):
                            # Prepare report data
                            report_data = {
                                'customer_name': st.session_state.customer_info['name'],
                                'phone': st.session_state.customer_info['phone'],
                                'address': st.session_state.customer_info.get('address', 'Cambodia'),
                                'monthly_kwh': results['monthly_kwh'],
                                'daily_kwh': results['daily_kwh'],
                                'system_type': results['system_type'],
                                'num_panels': results['num_panels'],
                                'panel_wattage': results['panel_wattage'],
                                'pv_kw': results['pv_kw'],
                                'pv_generation': results['monthly_kwh'],
                                'battery_kwh': results['battery_kwh'],
                                'num_batteries': results['num_batteries'],
                                'inverter_kw': results['inverter_kw'],
                                'total_price': results['total_customer'],
                                'monthly_savings': results['monthly_kwh'] * 0.20,
                                'annual_savings': results['monthly_kwh'] * 0.20 * 12,
                                'payback_years': results['total_customer'] / (results['monthly_kwh'] * 0.20 * 12) if results['monthly_kwh'] > 0 else 0,
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M')
                            }
                            
                            # Try personal sender first (better experience)
                            try:
                                from telegram_personal_sender import send_report_from_personal
                                
                                with st.spinner(f'📤 Sending from your Telegram to {telegram_contact}...'):
                                    success, message = send_report_from_personal(telegram_contact, report_data, selected_language)
                                
                                if success:
                                    st.success(f"✅ Sent from YOUR account to {telegram_contact}!")
                                    st.balloons()
                                    st.info("📞 Contact: 0888836588 | @chhanycls")
                                else:
                                    st.error(f"❌ {message}")
                                    st.info("💡 Make sure you've setup personal sender (see SETUP_PERSONAL_TELEGRAM.md)")
                                    
                            except ImportError:
                                # Fallback to bot method if personal sender not available
                                st.warning("📝 Personal sender not setup. Using bot method...")
                                try:
                                    from telegram_bot import TelegramReportSender
                                    sender = TelegramReportSender()
                                    
                                    with st.spinner(f'📤 Sending via bot to @{telegram_contact}...'):
                                        success, message = sender.send_report(telegram_contact, report_data, selected_language)
                                    
                                    if success:
                                        st.success(f"✅ Sent to @{telegram_contact}!")
                                        st.balloons()
                                        st.info("📞 Contact: 0888836588 | @chhanycls")
                                    else:
                                        st.error(f"❌ {message}")
                                        st.warning("💡 Ask customer to send /start to @khsolar_bot first")
                                except:
                                    st.error("❌ Neither personal sender nor bot available. Check setup.")
                                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            with cost_col2:
                monthly_savings = results['monthly_kwh'] * 0.20  # Assume $0.20/kWh grid rate
                payback_years = results['total_customer'] / (monthly_savings * 12) if monthly_savings > 0 else 0
                annual_savings = monthly_savings * 12
                
                # Total Investment Card - Redesigned
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%, #14b8a6 200%); 
                            padding: 2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(15, 118, 110, 0.4);
                            position: relative; overflow: hidden;'>
                    <div style='position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; 
                                background: rgba(255,255,255,0.1); border-radius: 50%;'></div>
                    <div style='position: relative; z-index: 1;'>
                        <div style='text-align: center; margin-bottom: 1rem;'>
                            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>💎</div>
                            <p style='margin: 0; font-size: 0.95rem; color: rgba(255,255,255,0.9); font-weight: 600; letter-spacing: 2px;'>TOTAL INVESTMENT</p>
                        </div>
                        <h1 style='margin: 1rem 0; color: white; font-size: 3.8rem; font-weight: 900; text-align: center; 
                                   text-shadow: 2px 2px 12px rgba(0,0,0,0.3); letter-spacing: -2px;'>
                            ${results['total_customer']:,.2f}
                        </h1>
                        <p style='margin: 0; font-size: 0.9rem; color: rgba(255,255,255,0.85); text-align: center; font-weight: 500;'>
                            ✨ Complete turnkey solar solution
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Financial Metrics in Cards
                st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-radius: 10px;'>
                            <div style='font-size: 1.8rem; margin-bottom: 0.3rem;'>💵</div>
                            <div style='font-size: 0.75rem; color: #1e40af; font-weight: 600; margin-bottom: 0.3rem;'>MONTHLY SAVINGS</div>
                            <div style='font-size: 1.5rem; color: #1e3a8a; font-weight: 800;'>${monthly_savings:.2f}</div>
                        </div>
                        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-radius: 10px;'>
                            <div style='font-size: 1.8rem; margin-bottom: 0.3rem;'>📅</div>
                            <div style='font-size: 0.75rem; color: #065f46; font-weight: 600; margin-bottom: 0.3rem;'>ANNUAL SAVINGS</div>
                            <div style='font-size: 1.5rem; color: #064e3b; font-weight: 800;'>${annual_savings:.2f}</div>
                        </div>
                    </div>
                </div>
                
                <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;'>
                    <div style='font-size: 2rem; margin-bottom: 0.3rem;'>⏱️</div>
                    <div style='font-size: 0.8rem; color: #92400e; font-weight: 600; margin-bottom: 0.5rem;'>PAYBACK PERIOD</div>
                    <div style='font-size: 2.2rem; color: #78350f; font-weight: 800;'>{payback_years:.1f} <span style='font-size: 1.2rem;'>years</span></div>
                    <div style='font-size: 0.75rem; color: #92400e; margin-top: 0.5rem;'>🚀 Start saving from day one!</div>
                </div>
                """, unsafe_allow_html=True)
                
            
            # Auto-applied success message
            st.markdown("<br>", unsafe_allow_html=True)
            st.success("✅ Configuration automatically applied to your system! Sample devices created based on usage pattern. Scroll down to see System Overview.")
        
        st.markdown("---")
    
    # Modern Metric Cards
    device_count = len(st.session_state.devices)
    total_load = sum(d.daily_energy_kwh for d in st.session_state.devices)
    monthly_load = total_load * 30
    pv_cap = st.session_state.system_config.solar_panels.total_power_kw if st.session_state.system_config.solar_panels else 0
    bat_cap = st.session_state.system_config.battery.capacity_kwh if st.session_state.system_config.battery else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚡</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">DEVICES</div>
            <div style="color: white; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.3rem;">{device_count}</div>
            <div style="
                background: rgba(255,255,255,0.2);
                padding: 0.3rem 0.8rem;
                border-radius: 12px;
                color: white;
                font-size: 0.75rem;
                display: inline-block;
                font-weight: 600;
            ">{'✅ ACTIVE' if device_count > 0 else '➕ Add devices'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔋</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">DAILY CONSUMPTION</div>
            <div style="color: white; font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">{total_load:.2f} kWh</div>
            <div style="
                background: rgba(255,255,255,0.2);
                padding: 0.3rem 0.8rem;
                border-radius: 12px;
                color: white;
                font-size: 0.75rem;
                display: inline-block;
                font-weight: 600;
            ">{monthly_load:.0f} kWh/month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pv_status = '✅ CONFIGURED' if pv_cap > 0 else '⚙️ Not set'
        pv_color = '#10b981' if pv_cap > 0 else '#6b7280'
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">☀️</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">PV CAPACITY</div>
            <div style="color: white; font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">{pv_cap:.2f} kW</div>
            <div style="
                background: rgba(255,255,255,0.2);
                padding: 0.3rem 0.8rem;
                border-radius: 12px;
                color: white;
                font-size: 0.75rem;
                display: inline-block;
                font-weight: 600;
            ">{pv_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        bat_status = '✅ READY' if bat_cap > 0 else '⚙️ Not set'
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔌</div>
            <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">BATTERY STORAGE</div>
            <div style="color: white; font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">{bat_cap:.1f} kWh</div>
            <div style="
                background: rgba(255,255,255,0.2);
                padding: 0.3rem 0.8rem;
                border-radius: 12px;
                color: white;
                font-size: 0.75rem;
                display: inline-block;
                font-weight: 600;
            ">{bat_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced System Status Cards with Detailed Information
    if device_count > 0 or pv_cap > 0:
        st.markdown("---")
        st.markdown(f"""
        <div style='text-align: center; margin: 1.5rem 0 1rem 0;'>
            <h2 style='margin: 0; color: #1f2937;'>🎯 {t('system_overview')}</h2>
            <p style='color: #6b7280; font-size: 0.9rem; margin-top: 0.5rem;'>Complete system specifications and pricing breakdown</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Row 1: Load Summary and Solar Panel Details
        overview_col1, overview_col2, overview_col3 = st.columns(3)
        
        with overview_col1:
            st.markdown(f"""
            <div class="custom-card" style='
                background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                border-left: 4px solid #6b7280;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            '>
                <h4 style='color: #374151; margin-bottom: 0.8rem;'>⚡ {t('load_summary')}</h4>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📅 {t('daily')}:</b> <span style='color: #1f2937; font-weight: 600;'>{total_load:.2f} kWh</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📆 {t('monthly')}:</b> <span style='color: #1f2937; font-weight: 600;'>{monthly_load:.0f} kWh</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🔌 {t('devices')}:</b> <span style='color: #1f2937; font-weight: 600;'>{device_count}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col2:
            # Calculate solar panel details
            pv_monthly = pv_cap * st.session_state.system_config.sunlight_hours * 30 if pv_cap > 0 else 0
            panel_count = st.session_state.system_config.solar_panels.quantity if st.session_state.system_config.solar_panels else 0
            panel_wattage = st.session_state.system_config.solar_panels.power_watts if st.session_state.system_config.solar_panels else 0
            # Calculate area needed (approx 2 m² per 550W panel, adjust based on wattage)
            area_per_panel = 2.0 if panel_wattage >= 500 else 1.7
            total_area = panel_count * area_per_panel
            
            st.markdown(f"""
            <div class="custom-card" style='
                background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                border-left: 4px solid #f59e0b;
                box-shadow: 0 4px 6px rgba(245, 158, 11, 0.2);
            '>
                <h4 style='color: #92400e; margin-bottom: 0.8rem;'>☀️ Solar Panels</h4>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>⚡ Total Capacity:</b> <span style='color: #92400e; font-weight: 600;'>{pv_cap:.2f} kW</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📦 Panels:</b> <span style='color: #92400e; font-weight: 600;'>{panel_count} × {panel_wattage}W</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📊 Monthly Gen:</b> <span style='color: #92400e; font-weight: 600;'>{pv_monthly:.0f} kWh</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📐 Area Needed:</b> <span style='color: #92400e; font-weight: 600;'>~{total_area:.1f} m²</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col3:
            # Battery details
            battery_count = st.session_state.system_config.battery.quantity if st.session_state.system_config.battery else 0
            battery_voltage = st.session_state.system_config.battery.voltage if st.session_state.system_config.battery else 0
            # Calculate Ah from kWh and voltage: Ah = (kWh * 1000) / voltage
            battery_capacity_ah = (st.session_state.system_config.battery.capacity_kwh * 1000 / battery_voltage) if (st.session_state.system_config.battery and battery_voltage > 0) else 0
            # Extract battery type from name (Lithium, Gel, etc.)
            battery_name = st.session_state.system_config.battery.name if st.session_state.system_config.battery else ""
            battery_type = "Lithium" if "lithium" in battery_name.lower() else "Gel" if "gel" in battery_name.lower() else "Lead-Acid" if "lead" in battery_name.lower() else "Battery"
            
            st.markdown(f"""
            <div class="custom-card" style='
                background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
                border-left: 4px solid #3b82f6;
                box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
            '>
                <h4 style='color: #1e40af; margin-bottom: 0.8rem;'>🔋 Battery Storage</h4>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>⚡ Total Capacity:</b> <span style='color: #1e40af; font-weight: 600;'>{bat_cap:.1f} kWh</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🔋 Batteries:</b> <span style='color: #1e40af; font-weight: 600;'>{battery_count} × {battery_voltage}V {battery_capacity_ah}Ah</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🏷️ Type:</b> <span style='color: #1e40af; font-weight: 600;'>{battery_type}</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>⏱️ Backup:</b> <span style='color: #1e40af; font-weight: 600;'>~{(bat_cap * 0.8 / total_load * 24) if total_load > 0 else 0:.1f} hours</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Row 2: Inverter, System Status, and Pricing
        st.markdown("<br>", unsafe_allow_html=True)
        overview_col4, overview_col5, overview_col6 = st.columns(3)
        
        with overview_col4:
            # Inverter details
            inverter_power = st.session_state.system_config.inverter.power_kw if st.session_state.system_config.inverter else 0
            # Extract inverter type from name (Hybrid, On-Grid, Off-Grid)
            inverter_name = st.session_state.system_config.inverter.name if st.session_state.system_config.inverter else ""
            inverter_type = "Hybrid" if "hybrid" in inverter_name.lower() else "On-Grid" if "ongrid" in inverter_name.lower() or "on-grid" in inverter_name.lower() else "Off-Grid" if "off" in inverter_name.lower() else "Inverter"
            inverter_voltage = st.session_state.system_config.inverter.input_voltage if st.session_state.system_config.inverter else 48
            # Determine phases from name (3P = 3-phase, 1P or default = single phase)
            inverter_phases = "3-Phase" if "3p" in inverter_name.lower() else "Single Phase"
            
            st.markdown(f"""
            <div class="custom-card" style='
                background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
                border-left: 4px solid #6366f1;
                box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
            '>
                <h4 style='color: #4338ca; margin-bottom: 0.8rem;'>⚡ Inverter</h4>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🔌 Power Rating:</b> <span style='color: #4338ca; font-weight: 600;'>{inverter_power:.1f} kW</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🏷️ Type:</b> <span style='color: #4338ca; font-weight: 600;'>{inverter_type}</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>⚡ Voltage:</b> <span style='color: #4338ca; font-weight: 600;'>{inverter_voltage}V</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🔄 Phases:</b> <span style='color: #4338ca; font-weight: 600;'>{inverter_phases}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col5:
            # System status and coverage
            if pv_cap > 0 and total_load > 0:
                coverage = (pv_monthly / monthly_load * 100) if monthly_load > 0 else 0
                coverage_status = t('excellent') if coverage >= 100 else t('good') if coverage >= 80 else t('needs_increase')
                coverage_color = "#10b981" if coverage >= 100 else "#f59e0b" if coverage >= 80 else "#ef4444"
            else:
                coverage = 0
                coverage_status = t('configure_system_msg')
                coverage_color = "#6b7280"
            
            st.markdown(f"""
            <div class="custom-card" style='
                background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
                border-left: 4px solid #10b981;
                box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);
            '>
                <h4 style='color: #065f46; margin-bottom: 0.8rem;'>✅ {t('system_status')}</h4>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📊 {t('coverage')}:</b> <span style="color: {coverage_color}; font-weight: 700; font-size: 1.1rem;">{coverage:.0f}%</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🎯 {t('status')}:</b> <span style='color: #065f46; font-weight: 600;'>{coverage_status}</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>☀️ Peak Hours:</b> <span style='color: #065f46; font-weight: 600;'>{st.session_state.system_config.sunlight_hours:.1f} hrs/day</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📍 Location:</b> <span style='color: #065f46; font-weight: 600;'>{st.session_state.system_config.location}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col6:
            # Calculate total pricing (with 30% markup for customer)
            equipment_cost = 0.0
            if st.session_state.system_config.solar_panels:
                equipment_cost += st.session_state.system_config.solar_panels.cost_per_panel * st.session_state.system_config.solar_panels.quantity
            if st.session_state.system_config.battery:
                equipment_cost += st.session_state.system_config.battery.total_cost
            if st.session_state.system_config.inverter:
                equipment_cost += st.session_state.system_config.inverter.cost
            
            labor_cost = st.session_state.system_config.labor_cost
            support_cost = st.session_state.system_config.support_material_cost
            total_wholesale = equipment_cost + labor_cost + support_cost
            total_customer = total_wholesale * 1.30  # 30% markup
            
            st.markdown(f"""
            <div class="custom-card" style='
                background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
                border-left: 4px solid #ec4899;
                box-shadow: 0 4px 6px rgba(236, 72, 153, 0.2);
            '>
                <h4 style='color: #9f1239; margin-bottom: 0.8rem;'>💰 System Pricing</h4>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>📦 Equipment:</b> <span style='color: #9f1239; font-weight: 600;'>${equipment_cost:,.2f}</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>🔧 Installation:</b> <span style='color: #9f1239; font-weight: 600;'>${(labor_cost + support_cost):,.2f}</span></p>
                <p style='margin: 0.4rem 0; font-size: 0.9rem;'><b>💵 Wholesale:</b> <span style='color: #9f1239; font-weight: 600;'>${total_wholesale:,.2f}</span></p>
                <p style='margin: 0.6rem 0 0.2rem 0; padding-top: 0.5rem; border-top: 2px solid #ec4899; font-size: 0.95rem;'><b>🏷️ Customer Price (+30%):</b></p>
                <p style='margin: 0; font-size: 1.3rem;'><span style="color: #be185d; font-weight: 700;">${total_customer:,.2f}</span></p>
            </div>
            """, unsafe_allow_html=True)

# ==================== DEVICES ====================
elif page == t('nav_devices'):
    st.title(t('device_management'))
    st.markdown(f"#### {t('device_subtitle')}")
    
    tab1, tab2, tab3, tab4 = st.tabs([t('add_device'), t('device_list'), t('quick_add'), '🧮 Quick Calculator'])
    
    with tab1:
        st.markdown(f"### {t('add_new_device')}")
        st.markdown(f"**{t('tip_select_device')}**")
        
        with st.form("device_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Device selection with auto-recognition
                device_options = [t('custom_device')] + sorted(list(DEVICE_DATABASE.keys()))
                selected_device = st.selectbox(
                    t('select_device_custom'),
                    device_options,
                    help=t('choose_from_common')
                )
                
                # Auto-fill values if device is selected from database
                if selected_device != t('custom_device'):
                    device_info = DEVICE_DATABASE[selected_device]
                    default_name = selected_device
                    default_power = int(device_info["power"])
                    default_hours = 4.0  # Will be updated from device_info
                    # Ensure hours is always float
                    try:
                        default_hours = float(device_info["hours"])
                    except (ValueError, TypeError):
                        default_hours = 4.0
                    default_type = device_info["type"]
                    default_priority = device_info["priority"]
                    default_inverter = device_info.get("inverter", False)
                else:
                    default_name = ""
                    default_power = 100
                    default_hours = 4.0
                    default_type = "general"
                    default_priority = False
                    default_inverter = False
                
                name = st.text_input(
                    f"{t('device_name')} *",
                    value=default_name,
                    placeholder=t('example_placeholder')
                )
                
                quantity = st.number_input(
                    t('quantity'),
                    min_value=1,
                    value=1,
                    step=1,
                    help=t('number_identical')
                )
                
                power = st.number_input(
                    f"{t('power_consumption')} *",
                    min_value=1,
                    value=default_power,
                    step=10,
                    help=t('power_rating_watts')
                )
                
                # Absolutely ensure hours value is float type
                hours_value = float(default_hours) if default_hours is not None else 4.0
                hours = st.number_input(
                    f"{t('daily_usage_hours')} *",
                    min_value=0.0,
                    max_value=24.0,
                    value=hours_value,
                    step=0.5,
                    format="%.1f",
                    help=t('hours_per_day')
                )
            
            with col2:
                device_type = st.selectbox(
                    t('device_category'),
                    ["general", "cooling", "heating", "lighting", "kitchen", "entertainment", "office"],
                    index=["general", "cooling", "heating", "lighting", "kitchen", "entertainment", "office"].index(default_type),
                    help=t('category_help')
                )
                
                is_priority = st.checkbox(
                    t('priority_device'),
                    value=default_priority,
                    help=t('priority_help')
                )
                
                # Inverter technology checkbox
                has_inverter = st.checkbox(
                    t('inverter_tech'),
                    value=default_inverter,
                    help=t('inverter_help')
                )
                
                # Calculate inverter savings
                inverter_savings_percent = 0
                if has_inverter:
                    if device_type == "cooling":
                        inverter_savings_percent = 40
                    elif device_type == "heating":
                        inverter_savings_percent = 35
                    else:
                        inverter_savings_percent = 30
                
                effective_power = power * (1 - inverter_savings_percent / 100) if has_inverter else power
                
                # Calculate and display energy
                daily_energy = (effective_power * hours / 1000) * quantity
                daily_without_inverter = (power * hours / 1000) * quantity
                daily_savings = daily_without_inverter - daily_energy if has_inverter else 0
                monthly_energy = daily_energy * 30
                monthly_savings = daily_savings * 30
                yearly_cost = monthly_energy * 12 * 0.20  # Assume $0.20/kWh
                yearly_savings_cost = monthly_savings * 12 * 0.20
                
                if has_inverter:
                    st.markdown(f"""
                    <div class="success-box" style="padding: 1rem;">
                        <h4>{t('energy_impact_inverter')}</h4>
                        <p><b>{t('quantity')}:</b> {quantity}x</p>
                        <p><b>{t('power_savings')}:</b> {inverter_savings_percent}%</p>
                        <p><b>{t('daily')}:</b> {daily_energy:.2f} kWh <span style="color: #10b981;">({t('save_text')} {daily_savings:.2f} kWh)</span></p>
                        <p><b>{t('monthly')}:</b> {monthly_energy:.2f} kWh <span style="color: #10b981;">({t('save_text')} {monthly_savings:.2f} kWh)</span></p>
                        <p><b>{t('yearly_cost')}:</b> ${yearly_cost:.2f} <span style="color: #10b981;">({t('save_text')} ${yearly_savings_cost:.2f})</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="info-box" style="padding: 1rem;">
                        <h4>{t('energy_impact')}</h4>
                        <p><b>{t('quantity')}:</b> {quantity}x</p>
                        <p><b>{t('daily')}:</b> {daily_energy:.2f} kWh</p>
                        <p><b>{t('monthly')}:</b> {monthly_energy:.2f} kWh</p>
                        <p><b>{t('yearly_cost')}:</b> ${yearly_cost:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            submitted = st.form_submit_button(t('add_devices'), type="primary", use_container_width=True)
            
            if submitted:
                if name and name.strip():
                    # Add devices based on quantity
                    for i in range(quantity):
                        device_name = name.strip() if quantity == 1 else f"{name.strip()} #{i+1}"
                        new_device = Device(device_name, power, hours, is_priority, [], device_type, has_inverter)
                        st.session_state.devices.append(new_device)
                    
                    inverter_text = " with Inverter Technology" if has_inverter else ""
                    savings_text = f" (Saves {daily_savings:.2f} kWh/day)" if has_inverter else ""
                    success_msg = f"✅ Successfully added **{quantity}x {name}**{inverter_text} - {daily_energy:.2f} kWh/day{savings_text}"
                    st.success(success_msg)
                    st.rerun()
                else:
                    st.error(f"⚠️ {t('enter_device_name')}")
    
    with tab2:
        if st.session_state.devices:
            st.markdown(f"### {t('your_devices')}")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            total_devices = len(st.session_state.devices)
            total_daily = sum(d.daily_energy_kwh for d in st.session_state.devices)
            priority_count = sum(1 for d in st.session_state.devices if d.is_priority)
            
            with col1:
                st.metric(t('total_devices_label'), total_devices)
            with col2:
                st.metric(t('daily_consumption'), f"{total_daily:.2f} kWh")
            with col3:
                st.metric(t('priority_devices'), priority_count)
            
            st.markdown("---")
            
            # Enhanced device table with inverter info
            device_data = []
            total_saved = 0
            for idx, d in enumerate(st.session_state.devices):
                inverter_icon = "⚡" if d.has_inverter else ""
                savings_pct = f"(-{d.inverter_savings_percent}%)" if d.has_inverter else ""
                total_saved += d.power_saved_kwh
                
                device_data.append({
                    "#": idx + 1,
                    t('device'): d.name,
                    t('type'): d.device_type.title(),
                    t('power_w'): f"{d.power_watts:.0f} {inverter_icon}",
                    t('effective_w'): f"{d.effective_power_watts:.0f} {savings_pct}" if d.has_inverter else f"{d.power_watts:.0f}",
                    t('hours_day'): d.daily_hours,
                    t('daily_kwh'): round(d.daily_energy_kwh, 2),
                    t('monthly_kwh'): round(d.daily_energy_kwh * 30, 1),
                    t('priority'): "⭐" if d.is_priority else "○"
                })
            
            df = pd.DataFrame(device_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Show total inverter savings if any
            if total_saved > 0:
                st.markdown(f"""
                <div class="success-box" style="padding: 0.8rem; margin-top: 1rem;">
                    <p style="margin: 0;"><b>{t('total_inverter_savings')}:</b> {total_saved:.2f} kWh/{t('daily').lower()} ({total_saved * 30:.2f} kWh/{t('monthly').lower()}) - {t('save_month')} ${total_saved * 30 * 0.20:.2f}/{t('monthly').lower()}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Device management
            st.markdown("---")
            st.markdown(f"#### {t('remove_device_title')}")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                idx = st.selectbox(
                    t('select_device_remove'),
                    range(len(st.session_state.devices)),
                    format_func=lambda x: f"{st.session_state.devices[x].name} ({st.session_state.devices[x].daily_energy_kwh:.2f} kWh/{t('daily').lower()})"
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(t('remove_device_btn'), type="secondary", use_container_width=True):
                    removed = st.session_state.devices.pop(idx)
                    st.success(f"{t('removed')} {removed.name}")
                    st.rerun()
        else:
            st.markdown(f"""
            <div class="warning-box">
                <h3>{t('no_devices_yet')}</h3>
                <p>{t('get_started_first')} <b>{t('add_device_tab')}</b> {t('tab_above')}</p>
                <p>{t('or_use_quick')} <b>{t('quick_add_tab')}</b> {t('to_add_typical')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown(f"### {t('quick_add_home_presets')}")
        st.markdown(t('select_home_size'))
        
        # Home size presets
        preset_col1, preset_col2, preset_col3 = st.columns(3)
        
        # Small Home Preset
        with preset_col1:
            st.markdown(f"""
            <div class="custom-card">
                <h4>{t('small_home')}</h4>
                <p><b>{t('size')}:</b> 1-2 {t('bedrooms')}</p>
                <p><b>{t('people')}:</b> 1-3</p>
                <p><b>{t('monthly_usage')}:</b> ~250-350 kWh</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(t('add_small_setup'), key="small_home", use_container_width=True):
                small_home_devices = [
                    ("Refrigerator", 150, 24, True, "cooling"),
                    ("Air Conditioner 1HP", 1000, 6, False, "cooling"),
                    ("Ceiling Fan #1", 75, 8, False, "cooling"),
                    ("Ceiling Fan #2", 75, 8, False, "cooling"),
                    ("LED Bulb 9W #1", 9, 5, True, "lighting"),
                    ("LED Bulb 9W #2", 9, 5, True, "lighting"),
                    ("LED Bulb 9W #3", 9, 5, True, "lighting"),
                    ("LED Bulb 9W #4", 9, 4, True, "lighting"),
                    ("Rice Cooker", 500, 1, True, "kitchen"),
                    ("TV LED 32 inch", 60, 4, False, "entertainment"),
                    ("Washing Machine", 500, 0.5, False, "general"),
                    ("Water Pump", 300, 0.5, True, "general"),
                    ("Router/Modem", 10, 24, True, "office"),
                    ("Iron", 1000, 0.3, False, "general"),
                ]
                for name, power, hours, priority, dtype in small_home_devices:
                    st.session_state.devices.append(Device(name, power, hours, priority, [], dtype))
                st.success(t('added_small'))
                st.rerun()
        
        # Medium Home Preset
        with preset_col2:
            st.markdown(f"""
            <div class="custom-card">
                <h4>{t('medium_home')}</h4>
                <p><b>{t('size')}:</b> 3-4 {t('bedrooms')}</p>
                <p><b>{t('people')}:</b> 4-6</p>
                <p><b>{t('monthly_usage')}:</b> ~400-600 kWh</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(t('add_medium_setup'), key="medium_home", use_container_width=True):
                medium_home_devices = [
                    ("Refrigerator", 150, 24, True, "cooling"),
                    ("Freezer", 200, 24, True, "cooling"),
                    ("Air Conditioner 1.5HP #1", 1500, 8, False, "cooling"),
                    ("Air Conditioner 1.5HP #2", 1500, 6, False, "cooling"),
                    ("Ceiling Fan #1", 75, 10, False, "cooling"),
                    ("Ceiling Fan #2", 75, 10, False, "cooling"),
                    ("Ceiling Fan #3", 75, 8, False, "cooling"),
                    ("LED Bulb 12W #1", 12, 6, True, "lighting"),
                    ("LED Bulb 12W #2", 12, 6, True, "lighting"),
                    ("LED Bulb 12W #3", 12, 6, True, "lighting"),
                    ("LED Bulb 9W #1", 9, 5, True, "lighting"),
                    ("LED Bulb 9W #2", 9, 5, True, "lighting"),
                    ("LED Tube 18W #1", 18, 5, True, "lighting"),
                    ("LED Tube 18W #2", 18, 5, True, "lighting"),
                    ("Rice Cooker", 500, 1.5, True, "kitchen"),
                    ("Microwave", 1000, 0.5, False, "kitchen"),
                    ("Electric Kettle", 1500, 0.5, False, "kitchen"),
                    ("TV LED 43 inch", 80, 5, False, "entertainment"),
                    ("TV LED 32 inch", 60, 3, False, "entertainment"),
                    ("Sound System", 100, 3, False, "entertainment"),
                    ("Washing Machine", 500, 1, False, "general"),
                    ("Water Pump", 300, 0.8, True, "general"),
                    ("Iron", 1000, 0.5, False, "general"),
                    ("Router/Modem", 10, 24, True, "office"),
                    ("Laptop #1", 65, 6, False, "office"),
                    ("Laptop #2", 65, 4, False, "office"),
                ]
                for name, power, hours, priority, dtype in medium_home_devices:
                    st.session_state.devices.append(Device(name, power, hours, priority, [], dtype))
                st.success(t('added_medium'))
                st.rerun()
        
        # Large Home Preset
        with preset_col3:
            st.markdown(f"""
            <div class="custom-card">
                <h4>{t('large_home')}</h4>
                <p><b>{t('size')}:</b> 5+ {t('bedrooms')}</p>
                <p><b>{t('people')}:</b> 6-10</p>
                <p><b>{t('monthly_usage')}:</b> ~700-1000 kWh</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(t('add_large_setup'), key="large_home", use_container_width=True):
                large_home_devices = [
                    ("Refrigerator #1", 150, 24, True, "cooling"),
                    ("Refrigerator #2", 150, 24, True, "cooling"),
                    ("Freezer", 200, 24, True, "cooling"),
                    ("Air Conditioner 2HP #1", 2000, 10, False, "cooling"),
                    ("Air Conditioner 1.5HP #1", 1500, 8, False, "cooling"),
                    ("Air Conditioner 1.5HP #2", 1500, 8, False, "cooling"),
                    ("Air Conditioner 1HP #1", 1000, 6, False, "cooling"),
                    ("Ceiling Fan #1", 75, 12, False, "cooling"),
                    ("Ceiling Fan #2", 75, 12, False, "cooling"),
                    ("Ceiling Fan #3", 75, 10, False, "cooling"),
                    ("Ceiling Fan #4", 75, 10, False, "cooling"),
                    ("Standing Fan #1", 60, 8, False, "cooling"),
                    ("LED Bulb 12W #1", 12, 7, True, "lighting"),
                    ("LED Bulb 12W #2", 12, 7, True, "lighting"),
                    ("LED Bulb 12W #3", 12, 7, True, "lighting"),
                    ("LED Bulb 12W #4", 12, 6, True, "lighting"),
                    ("LED Tube 18W #1", 18, 6, True, "lighting"),
                    ("LED Tube 18W #2", 18, 6, True, "lighting"),
                    ("LED Tube 18W #3", 18, 5, True, "lighting"),
                    ("LED Strip Lights", 30, 5, False, "lighting"),
                    ("Rice Cooker", 500, 2, True, "kitchen"),
                    ("Microwave", 1000, 0.8, False, "kitchen"),
                    ("Electric Kettle", 1500, 0.8, False, "kitchen"),
                    ("Toaster", 800, 0.3, False, "kitchen"),
                    ("Blender", 300, 0.3, False, "kitchen"),
                    ("Water Heater", 2000, 1.5, False, "heating"),
                    ("TV LED 55 inch", 120, 6, False, "entertainment"),
                    ("TV LED 43 inch", 80, 4, False, "entertainment"),
                    ("Sound System", 100, 4, False, "entertainment"),
                    ("Gaming Console", 150, 3, False, "entertainment"),
                    ("Washing Machine", 500, 1.5, False, "general"),
                    ("Water Pump", 300, 1, True, "general"),
                    ("Iron", 1000, 0.8, False, "general"),
                    ("Vacuum Cleaner", 1000, 0.5, False, "general"),
                    ("Router/Modem", 10, 24, True, "office"),
                    ("Desktop Computer", 300, 8, False, "office"),
                    ("Laptop #1", 65, 6, False, "office"),
                    ("Laptop #2", 65, 6, False, "office"),
                    ("Monitor", 40, 8, False, "office"),
                    ("Printer", 50, 0.5, False, "office"),
                ]
                for name, power, hours, priority, dtype in large_home_devices:
                    st.session_state.devices.append(Device(name, power, hours, priority, [], dtype))
                st.success(t('added_large'))
                st.rerun()
    
    with tab4:
        st.markdown("### 🧮 Quick System Calculator")
        st.markdown("Get instant system recommendations based on your usage or desired inverter size")
        
        calc_tab1, calc_tab2 = st.tabs(["📊 From Monthly Usage", "⚡ From Inverter Size"])
        
        with calc_tab1:
            st.markdown("#### Calculate System from Monthly kWh Usage")
            st.markdown("Enter your monthly electricity usage to get AI-powered system recommendations")
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                monthly_kwh = st.number_input(
                    "Monthly Usage (kWh)",
                    min_value=50.0,
                    max_value=5000.0,
                    value=400.0,
                    step=50.0,
                    help="Enter your average monthly electricity consumption in kWh"
                )
                
                usage_pattern = st.selectbox(
                    "Usage Pattern",
                    ["Balanced (Day & Night)", "Mostly Daytime", "Mostly Evening/Night"],
                    help="When do you use most electricity?"
                )
                
                grid_available = st.checkbox("Grid Connection Available", value=True)
                
                if st.button("🔍 Calculate System", type="primary", use_container_width=True):
                    # Calculate daily load
                    daily_kwh = monthly_kwh / 30
                    
                    # Calculate system requirements
                    sunlight_hours = 5.5  # Cambodia average
                    system_efficiency = 0.85
                    
                    # PV sizing
                    pv_kw = daily_kwh / (sunlight_hours * system_efficiency)
                    
                    # Battery sizing based on usage pattern
                    if usage_pattern == "Mostly Daytime":
                        battery_kwh = daily_kwh * 0.3  # 30% backup
                        battery_note = "Smaller battery since most usage is during solar generation"
                    elif usage_pattern == "Mostly Evening/Night":
                        battery_kwh = daily_kwh * 0.7  # 70% backup
                        battery_note = "Larger battery for evening/night usage"
                    else:
                        battery_kwh = daily_kwh * 0.5  # 50% backup
                        battery_note = "Balanced battery for day and night usage"
                    
                    # Improved inverter sizing
                    # Residential peak load typically occurs over 4-6 hours
                    # Using 5 hours as optimal balance
                    estimated_peak_kw = daily_kwh / 5  # Peak concentrated in 5 hours
                    inverter_kw = estimated_peak_kw * 1.3  # 30% safety margin
                    
                    # Panel calculations
                    panel_wattage = 450  # Standard panel
                    num_panels = int(pv_kw * 1000 / panel_wattage) + 1
                    
                    st.session_state.calc_results = {
                        'monthly_kwh': monthly_kwh,
                        'daily_kwh': daily_kwh,
                        'pv_kw': pv_kw,
                        'battery_kwh': battery_kwh,
                        'inverter_kw': inverter_kw,
                        'num_panels': num_panels,
                        'panel_wattage': panel_wattage,
                        'battery_note': battery_note,
                        'usage_pattern': usage_pattern
                    }
            
            with col2:
                if 'calc_results' in st.session_state:
                    results = st.session_state.calc_results
                    
                    st.markdown(f"""
                    <div class="success-box" style="padding: 1.5rem;">
                        <h3 style="margin-top: 0;">🎯 Recommended System Configuration</h3>
                        <hr>
                        <h4>📊 Your Usage</h4>
                        <p><b>Monthly:</b> {results['monthly_kwh']:.0f} kWh</p>
                        <p><b>Daily Average:</b> {results['daily_kwh']:.2f} kWh</p>
                        <p><b>Pattern:</b> {results['usage_pattern']}</p>
                        
                        <hr>
                        <h4>☀️ Solar Panels</h4>
                        <p><b>Total Capacity:</b> {results['pv_kw']:.2f} kW</p>
                        <p><b>Recommended:</b> {results['num_panels']}x {results['panel_wattage']}W panels</p>
                        <p><small>Actual capacity: {results['num_panels'] * results['panel_wattage'] / 1000:.2f} kW</small></p>
                        
                        <hr>
                        <h4>🔋 Battery Storage</h4>
                        <p><b>Capacity:</b> {results['battery_kwh']:.2f} kWh</p>
                        <p><small>{results['battery_note']}</small></p>
                        
                        <hr>
                        <h4>⚡ Inverter</h4>
                        <p><b>Power Rating:</b> {results['inverter_kw']:.2f} kW</p>
                        <p><small>Sized for peak loads with 25% safety margin</small></p>
                        
                        <hr>
                        <h4>💰 Estimated Costs</h4>
                        <p><b>Equipment:</b> ${(results['num_panels'] * 180 + results['battery_kwh'] * 300 + results['inverter_kw'] * 200):,.0f}</p>
                        <p><b>Labor:</b> ${250 if results['inverter_kw'] <= 5 else 500}</p>
                        <p><b>Materials:</b> ${450 + (results['inverter_kw'] - 5) * 30 if results['inverter_kw'] > 5 else 450}</p>
                        <p><b>Total Est.:</b> ${(results['num_panels'] * 180 + results['battery_kwh'] * 300 + results['inverter_kw'] * 200 + (250 if results['inverter_kw'] <= 5 else 500) + (450 + (results['inverter_kw'] - 5) * 30 if results['inverter_kw'] > 5 else 450)):,.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("✅ Apply to System Config", use_container_width=True):
                        # Create system configuration
                        st.session_state.system_config.solar_panels = SolarPanel(
                            name=f"Solar Panel {results['panel_wattage']}W",
                            power_watts=results['panel_wattage'],
                            efficiency=0.21,
                            cost_per_panel=180.0,
                            quantity=results['num_panels']
                        )
                        st.session_state.system_config.battery = Battery(
                            name=f"Battery {results['battery_kwh']:.1f}kWh",
                            capacity_kwh=results['battery_kwh'],
                            voltage=48.0,
                            depth_of_discharge=0.8,
                            efficiency=0.95,
                            cost=results['battery_kwh'] * 300,
                            quantity=1
                        )
                        st.session_state.system_config.inverter = Inverter(
                            name=f"Hybrid Inverter {results['inverter_kw']:.1f}kW",
                            power_kw=results['inverter_kw'],
                            efficiency=0.97,
                            cost=results['inverter_kw'] * 180
                        )
                        
                        # Auto-generate typical devices based on calculated load
                        # Clear existing devices first
                        st.session_state.devices.clear()
                        
                        # Calculate device distribution based on usage pattern
                        daily_kwh = results['daily_kwh']
                        
                        # Generate typical household devices that sum to the daily load
                        # Base devices (always present)
                        typical_devices = [
                            ("Refrigerator", 150, 24, True, "cooling", False),
                            ("LED Bulb 12W #1", 12, 6, True, "lighting", False),
                            ("LED Bulb 12W #2", 12, 6, True, "lighting", False),
                            ("LED Bulb 12W #3", 12, 5, True, "lighting", False),
                            ("Router/Modem", 10, 24, True, "office", False),
                            ("Rice Cooker", 500, 1, True, "kitchen", False),
                            ("Water Pump", 300, 0.5, True, "general", False),
                        ]
                        
                        # Add cooling devices based on load size
                        if daily_kwh > 10:
                            typical_devices.append(("Air Conditioner 1.5HP", 1500, 6, False, "cooling", True))
                            typical_devices.append(("Ceiling Fan #1", 75, 8, False, "cooling", False))
                            typical_devices.append(("Ceiling Fan #2", 75, 8, False, "cooling", False))
                        
                        if daily_kwh > 15:
                            typical_devices.append(("TV LED 43 inch", 80, 4, False, "entertainment", False))
                            typical_devices.append(("Washing Machine", 500, 1, False, "general", False))
                        
                        if daily_kwh > 20:
                            typical_devices.append(("Air Conditioner 1HP", 1000, 5, False, "cooling", True))
                            typical_devices.append(("Microwave", 1000, 0.5, False, "kitchen", False))
                            typical_devices.append(("Laptop", 65, 6, False, "office", False))
                        
                        if daily_kwh > 30:
                            typical_devices.append(("Freezer", 200, 24, True, "cooling", False))
                            typical_devices.append(("Water Heater", 2000, 1.5, False, "heating", False))
                        
                        # Add devices to session state
                        for name, power, hours, priority, dtype, has_inverter in typical_devices:
                            st.session_state.devices.append(Device(name, power, hours, priority, [], dtype, has_inverter))
                        
                        st.success(f"✅ System configuration applied with {len(typical_devices)} typical devices! Ready for simulation.")
                        st.balloons()
                else:
                    st.info("👈 Enter your monthly usage and click Calculate to see recommendations")
        
        with calc_tab2:
            st.markdown("#### Calculate System from Inverter Size")
            st.markdown("Start with your desired inverter size and get complete system recommendations")
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                inverter_size = st.number_input(
                    "Inverter Size (kW)",
                    min_value=1.0,
                    max_value=50.0,
                    value=5.0,
                    step=0.5,
                    help="Enter your desired inverter capacity in kW"
                )
                
                target_autonomy = st.slider(
                    "Backup Hours (Autonomy)",
                    min_value=2,
                    max_value=24,
                    value=6,
                    step=1,
                    help="How many hours of backup do you need?"
                )
                
                pv_ratio = st.slider(
                    "PV to Inverter Ratio",
                    min_value=0.8,
                    max_value=2.0,
                    value=1.2,
                    step=0.1,
                    help="PV array size relative to inverter. Higher = more generation"
                )
                
                if st.button("🔍 Calculate System", type="primary", use_container_width=True, key="calc_inv"):
                    # Calculate based on inverter
                    pv_kw = inverter_size * pv_ratio
                    
                    # Battery sizing
                    # Assume inverter runs at 70% capacity during peak
                    peak_load_kw = inverter_size * 0.7
                    battery_kwh = (peak_load_kw * target_autonomy) / 0.8  # 80% DoD
                    
                    # Daily energy estimate
                    sunlight_hours = 5.5
                    system_efficiency = 0.85
                    daily_kwh = pv_kw * sunlight_hours * system_efficiency
                    monthly_kwh = daily_kwh * 30
                    
                    # Panel calculations
                    panel_wattage = 450
                    num_panels = int(pv_kw * 1000 / panel_wattage) + 1
                    
                    st.session_state.calc_inv_results = {
                        'inverter_kw': inverter_size,
                        'pv_kw': pv_kw,
                        'battery_kwh': battery_kwh,
                        'daily_kwh': daily_kwh,
                        'monthly_kwh': monthly_kwh,
                        'num_panels': num_panels,
                        'panel_wattage': panel_wattage,
                        'target_autonomy': target_autonomy,
                        'pv_ratio': pv_ratio
                    }
            
            with col2:
                if 'calc_inv_results' in st.session_state:
                    results = st.session_state.calc_inv_results
                    
                    st.markdown(f"""
                    <div class="success-box" style="padding: 1.5rem;">
                        <h3 style="margin-top: 0;">🎯 Recommended System Configuration</h3>
                        <hr>
                        <h4>⚡ Inverter (Starting Point)</h4>
                        <p><b>Power Rating:</b> {results['inverter_kw']:.2f} kW</p>
                        <p><b>Peak Output:</b> {results['inverter_kw'] * 0.9:.2f} kW (continuous)</p>
                        
                        <hr>
                        <h4>☀️ Solar Panels</h4>
                        <p><b>Total Capacity:</b> {results['pv_kw']:.2f} kW</p>
                        <p><b>Recommended:</b> {results['num_panels']}x {results['panel_wattage']}W panels</p>
                        <p><b>PV/Inv Ratio:</b> {results['pv_ratio']:.1f}x</p>
                        <p><small>Higher ratio = more daytime generation</small></p>
                        
                        <hr>
                        <h4>🔋 Battery Storage</h4>
                        <p><b>Capacity:</b> {results['battery_kwh']:.2f} kWh</p>
                        <p><b>Backup Time:</b> {results['target_autonomy']} hours at 70% load</p>
                        <p><small>Provides backup during grid outages</small></p>
                        
                        <hr>
                        <h4>📊 Expected Generation</h4>
                        <p><b>Daily:</b> {results['daily_kwh']:.2f} kWh</p>
                        <p><b>Monthly:</b> {results['monthly_kwh']:.0f} kWh</p>
                        <p><b>Annual:</b> {results['daily_kwh'] * 365:.0f} kWh</p>
                        
                        <hr>
                        <h4>💰 Estimated Costs</h4>
                        <p><small>Based on actual products from catalog</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("✅ Apply to System Config", use_container_width=True, key="apply_inv"):
                        # Get actual products from catalog
                        pm = st.session_state.product_manager
                        recommended_panel = pm.get_recommended_panel(min_wattage=results['panel_wattage'])
                        recommended_battery = pm.get_recommended_battery(min_capacity_kwh=results['battery_kwh'])
                        recommended_inverter = pm.get_recommended_inverter(min_power_kw=results['inverter_kw'], inverter_type="Hybrid")
                        
                        # Use recommended products or fallback to generic with estimated prices
                        panel_name = recommended_panel.name if recommended_panel else f"Solar Panel {results['panel_wattage']}W"
                        panel_cost = recommended_panel.cost if recommended_panel else (results['panel_wattage'] * 0.15)
                        
                        battery_name = recommended_battery.name if recommended_battery else f"Battery {results['battery_kwh']:.1f}kWh"
                        battery_cost = recommended_battery.cost if recommended_battery else (results['battery_kwh'] * 250)
                        battery_voltage = recommended_battery.specifications.get('voltage', 48.0) if recommended_battery else 48.0
                        
                        inverter_name = recommended_inverter.name if recommended_inverter else f"Hybrid Inverter {results['inverter_kw']:.1f}kW"
                        inverter_cost = recommended_inverter.cost if recommended_inverter else (results['inverter_kw'] * 180)
                        
                        # Create system configuration
                        st.session_state.system_config.solar_panels = SolarPanel(
                            name=panel_name,
                            power_watts=results['panel_wattage'],
                            efficiency=0.21,
                            cost_per_panel=panel_cost,
                            quantity=results['num_panels']
                        )
                        st.session_state.system_config.battery = Battery(
                            name=battery_name,
                            capacity_kwh=results['battery_kwh'],
                            voltage=battery_voltage,
                            depth_of_discharge=0.8,
                            efficiency=0.95,
                            cost=battery_cost,
                            quantity=1
                        )
                        st.session_state.system_config.inverter = Inverter(
                            name=inverter_name,
                            power_kw=results['inverter_kw'],
                            efficiency=0.97,
                            cost=inverter_cost
                        )
                        
                        # Auto-generate typical devices based on calculated load
                        # Clear existing devices first
                        st.session_state.devices.clear()
                        
                        # Calculate device distribution based on expected generation
                        daily_kwh = results['daily_kwh']
                        
                        # Generate typical household devices that sum to the daily load
                        # Base devices (always present)
                        typical_devices = [
                            ("Refrigerator", 150, 24, True, "cooling", False),
                            ("LED Bulb 12W #1", 12, 6, True, "lighting", False),
                            ("LED Bulb 12W #2", 12, 6, True, "lighting", False),
                            ("LED Bulb 12W #3", 12, 5, True, "lighting", False),
                            ("Router/Modem", 10, 24, True, "office", False),
                            ("Rice Cooker", 500, 1, True, "kitchen", False),
                            ("Water Pump", 300, 0.5, True, "general", False),
                        ]
                        
                        # Add cooling devices based on load size
                        if daily_kwh > 10:
                            typical_devices.append(("Air Conditioner 1.5HP", 1500, 6, False, "cooling", True))
                            typical_devices.append(("Ceiling Fan #1", 75, 8, False, "cooling", False))
                            typical_devices.append(("Ceiling Fan #2", 75, 8, False, "cooling", False))
                        
                        if daily_kwh > 15:
                            typical_devices.append(("TV LED 43 inch", 80, 4, False, "entertainment", False))
                            typical_devices.append(("Washing Machine", 500, 1, False, "general", False))
                        
                        if daily_kwh > 20:
                            typical_devices.append(("Air Conditioner 1HP", 1000, 5, False, "cooling", True))
                            typical_devices.append(("Microwave", 1000, 0.5, False, "kitchen", False))
                            typical_devices.append(("Laptop", 65, 6, False, "office", False))
                        
                        if daily_kwh > 30:
                            typical_devices.append(("Freezer", 200, 24, True, "cooling", False))
                            typical_devices.append(("Water Heater", 2000, 1.5, False, "heating", False))
                        
                        # Add devices to session state
                        for name, power, hours, priority, dtype, has_inverter in typical_devices:
                            st.session_state.devices.append(Device(name, power, hours, priority, [], dtype, has_inverter))
                        
                        st.success(f"✅ System configuration applied with {len(typical_devices)} typical devices! Ready for simulation.")
                        st.balloons()
                else:
                    st.info("👈 Enter your inverter size and click Calculate to see recommendations")
        
        st.markdown("---")
        st.markdown(f"### {t('individual_devices')}")
        st.markdown(t('add_individual_one'))
        
        # Individual device quick add
        individual_devices = [
            ("Refrigerator", 150, 24, True, "cooling"),
            ("Air Conditioner 1.5HP", 1500, 8, False, "cooling"),
            ("Ceiling Fan", 75, 10, False, "cooling"),
            ("LED Bulb 12W", 12, 5, True, "lighting"),
            ("Rice Cooker", 500, 1, True, "kitchen"),
            ("TV LED 43 inch", 80, 4, False, "entertainment"),
            ("Washing Machine", 500, 1, False, "general"),
            ("Water Pump", 300, 0.5, True, "general"),
            ("Laptop", 65, 6, False, "office"),
            ("Router/Modem", 10, 24, True, "office"),
        ]
        
        cols = st.columns(2)
        for idx, (name, power, hours, priority, dtype) in enumerate(individual_devices):
            with cols[idx % 2]:
                daily_kwh = (power * hours) / 1000
                if st.button(
                    f"➕ {name}\n{power}W, {hours}h/day ({daily_kwh:.2f} kWh)",
                    key=f"quick_individual_{idx}",
                    use_container_width=True
                ):
                    # Check if device already exists
                    existing = any(d.name == name for d in st.session_state.devices)
                    if not existing:
                        st.session_state.devices.append(Device(name, power, hours, priority, [], dtype))
                        st.success(t('added_device').format(name))
                        st.rerun()
                    else:
                        st.warning(t('already_exists').format(name))
        
        # AI Recommendations Section
        st.markdown("---")
        st.markdown(f"### {t('ai_recommendations')}")
        st.markdown(t('ai_subtitle'))
        
        if st.button(t('analyze_devices'), use_container_width=True, type="primary"):
            with st.spinner(t('ai_analyzing')):
                import time
                time.sleep(1)  # Simulate AI processing
                
                # AI recommendation logic based on current devices
                current_device_types = [d.device_type for d in st.session_state.devices]
                current_device_names = [d.name.lower() for d in st.session_state.devices]
                
                recommendations = []
                
                # Check for missing essential devices
                if not any('refrigerator' in name or 'fridge' in name for name in current_device_names):
                    recommendations.append({
                        'name': 'Refrigerator',
                        'power': 150,
                        'hours': 24,
                        'priority': True,
                        'type': 'cooling',
                        'reason': 'Essential for food preservation, runs 24/7'
                    })
                
                if not any('router' in name or 'modem' in name or 'wifi' in name for name in current_device_names):
                    recommendations.append({
                        'name': 'Router/Modem',
                        'power': 10,
                        'hours': 24,
                        'priority': True,
                        'type': 'office',
                        'reason': 'Essential for internet connectivity'
                    })
                
                # Check for efficiency upgrades
                if any('air conditioner' in name or 'ac' in name for name in current_device_names):
                    if not any(d.has_inverter and 'air conditioner' in d.name.lower() for d in st.session_state.devices):
                        recommendations.append({
                            'name': 'Inverter Air Conditioner 1.5HP',
                            'power': 1500,
                            'hours': 8,
                            'priority': False,
                            'type': 'cooling',
                            'reason': 'Upgrade to inverter AC saves 40% energy',
                            'inverter': True
                        })
                
                # Suggest lighting upgrades
                if not any('led' in name for name in current_device_names):
                    recommendations.append({
                        'name': 'LED Bulb 12W',
                        'power': 12,
                        'hours': 5,
                        'priority': True,
                        'type': 'lighting',
                        'reason': 'Energy-efficient lighting, uses 80% less power than incandescent'
                    })
                
                # Suggest fan for cooling efficiency
                cooling_devices = [d for d in st.session_state.devices if d.device_type == 'cooling']
                fan_count = sum(1 for d in st.session_state.devices if 'fan' in d.name.lower())
                if len(cooling_devices) > 2 and fan_count < 2:
                    recommendations.append({
                        'name': 'Ceiling Fan',
                        'power': 75,
                        'hours': 10,
                        'priority': False,
                        'type': 'cooling',
                        'reason': 'Reduces AC load by circulating air, saves energy'
                    })
                
                # Suggest water heating for modern homes
                if len(st.session_state.devices) > 15 and not any('water heater' in name or 'heater' in name for name in current_device_names):
                    recommendations.append({
                        'name': 'Water Heater',
                        'power': 2000,
                        'hours': 1.5,
                        'priority': False,
                        'type': 'heating',
                        'reason': 'Convenient for daily hot water needs'
                    })
                
                # Suggest backup power devices
                if not any('water pump' in name or 'pump' in name for name in current_device_names):
                    recommendations.append({
                        'name': 'Water Pump',
                        'power': 300,
                        'hours': 0.5,
                        'priority': True,
                        'type': 'general',
                        'reason': 'Essential for water supply, priority during power outage'
                    })
                
                if recommendations:
                    st.success(f"🤖 Found {len(recommendations)} recommendations based on your current setup!")
                    
                    for idx, rec in enumerate(recommendations):
                        with st.expander(f"💡 {rec['name']} - {rec['power']}W"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"""
                                **{t('recommendation')}:** {rec['name']}  
                                **{t('power_w')}:** {rec['power']}W  
                                **{t('hours_day')}:** {rec['hours']}h/{t('daily').lower()}  
                                **{t('type')}:** {rec['type'].title()}  
                                **{t('priority')}:** {'⭐ Yes' if rec['priority'] else '○ No'}  
                                {'**Inverter:** ⚡ Yes' if rec.get('inverter') else ''}  
                                
                                **{t('reason')}:** {rec['reason']}
                                """)
                                
                                daily_energy = (rec['power'] * rec['hours']) / 1000
                                monthly_cost = daily_energy * 30 * 0.20
                                st.info(f"📊 {t('energy_impact')}: {daily_energy:.2f} kWh/{t('daily').lower()} (${monthly_cost:.2f}/{t('monthly').lower()})")
                            
                            with col2:
                                if st.button(t('add_recommended'), key=f"ai_rec_{idx}", use_container_width=True):
                                    has_inverter = rec.get('inverter', False)
                                    new_device = Device(
                                        rec['name'],
                                        rec['power'],
                                        rec['hours'],
                                        rec['priority'],
                                        [],
                                        rec['type'],
                                        has_inverter
                                    )
                                    st.session_state.devices.append(new_device)
                                    st.success(t('added_device').format(rec['name']))
                                    st.rerun()
                else:
                    st.info("✅ Your device setup looks comprehensive! No additional recommendations at this time.")

# ==================== SYSTEM CONFIG ====================
elif page == t('nav_system'):
    st.title(t('system_config'))
    st.markdown(f"#### {t('system_subtitle')}")
    
    # Calculate recommendations based on devices
    if st.session_state.devices:
        total_daily_load = sum(d.daily_energy_kwh for d in st.session_state.devices)
        peak_power = sum(d.effective_power_watts for d in st.session_state.devices) / 1000
        
        # Calculate night load (assuming 50% during night hours 18:00-06:00)
        night_load = total_daily_load * 0.5
        
        # Recommendations
        sunlight_hours = st.session_state.system_config.sunlight_hours
        system_efficiency = 0.85
        
        recommended_pv_kw = total_daily_load / (sunlight_hours * system_efficiency)
        recommended_battery_kwh = night_load / 0.8  # 80% DoD
        recommended_inverter_kw = peak_power * 1.3  # 30% safety margin for better reliability
        
        # Show recommendations banner
        st.markdown(f"""
        <div class="info-box">
            <h4>{t('auto_recommendations')}</h4>
            <p><b>{t('based_on_devices').format(len(st.session_state.devices), total_daily_load)}</b></p>
            <p>{t('solar_panels')}: {recommended_pv_kw:.2f} kW | {t('battery')}: {recommended_battery_kwh:.2f} kWh | {t('inverter')}: {recommended_inverter_kw:.2f} kW</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
    else:
        st.warning("⚠️ Add devices first to get auto-calculated recommendations")
        recommended_pv_kw = 5.0
        recommended_battery_kwh = 5.0
        recommended_inverter_kw = 5.0
    
    tab1, tab2, tab3 = st.tabs([t('solar_panels'), t('battery'), t('inverter')])
    
    with tab1:
        st.markdown(f"### {t('solar_config')}")
        
        # Auto-calculate section
        if st.session_state.devices:
            # Get recommended panel from product catalog
            pm = st.session_state.product_manager
            recommended_panel = pm.get_recommended_panel(min_wattage=400)
            rec_panel_wattage = recommended_panel.specifications.get('power', 550) if recommended_panel else 550
            
            col_auto1, col_auto2 = st.columns(2)
            with col_auto1:
                st.markdown(f"""
                <div class="success-box" style="padding: 1rem;">
                    <h4>{t('recommended')}</h4>
                    <p><b>{t('total_capacity')}:</b> {recommended_pv_kw:.2f} kW</p>
                    <p><b>Example:</b> {int(recommended_pv_kw * 1000 / rec_panel_wattage)} x {rec_panel_wattage}W panels</p>
                    <p><b>Recommended:</b> {recommended_panel.name if recommended_panel else 'Check Products page'}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_auto2:
                if st.button(t('auto_fill'), key="auto_solar", use_container_width=True):
                    if recommended_panel:
                        st.session_state.auto_solar_quantity = int(recommended_pv_kw * 1000 / rec_panel_wattage)
                        st.session_state.auto_panel_name = recommended_panel.name
                        st.session_state.auto_panel_power = rec_panel_wattage
                        st.session_state.auto_panel_cost = recommended_panel.cost
                    st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            # Get default values from recommended product or session state
            pm = st.session_state.product_manager
            default_panel = pm.get_recommended_panel(min_wattage=400)
            
            default_name = st.session_state.get('auto_panel_name', default_panel.name if default_panel else "Lvtopsun 550W")
            default_power = st.session_state.get('auto_panel_power', default_panel.specifications.get('power', 550) if default_panel else 550)
            default_cost = st.session_state.get('auto_panel_cost', default_panel.cost if default_panel else 66.0)
            
            panel_name = st.text_input(t('panel_model'), default_name)
            panel_power = st.number_input(t('power_per_panel'), 100, value=int(default_power), step=50)
            
            # Use auto-calculated quantity if available
            default_qty = st.session_state.get('auto_solar_quantity', 10)
            quantity = st.number_input(t('quantity'), 1, value=default_qty)
            cost = st.number_input(f"{t('cost')}/Panel ($)", 0.0, value=float(default_cost))
        
        with col2:
            total_pv_kw = (panel_power * quantity / 1000)
            st.metric(t('total_capacity'), f"{total_pv_kw:.2f} kW")
            st.metric(t('total_cost'), f"${cost * quantity:,.2f}")
            
            # Show comparison with recommendation
            if st.session_state.devices:
                difference = total_pv_kw - recommended_pv_kw
                if abs(difference) < 0.5:
                    st.success(t('optimal_sizing'))
                elif difference > 0:
                    st.info(f"ℹ️ {difference:.1f} kW above recommended (good for growth)")
                else:
                    st.warning(f"⚠️ {abs(difference):.1f} kW below recommended")
        
        if st.button(t('save_config').format(' Solar'), type="primary"):
            st.session_state.system_config.solar_panels = SolarPanel(name=panel_name, power_watts=panel_power, efficiency=0.21, cost_per_panel=cost, quantity=quantity)
            st.success("✅ Solar panels configured successfully!")
            st.rerun()
    
    with tab2:
        st.markdown(f"### {t('battery_config')}")
        
        # Auto-calculate section
        if st.session_state.devices:
            col_auto1, col_auto2 = st.columns(2)
            with col_auto1:
                st.markdown(f"""
                <div class="success-box" style="padding: 1rem;">
                    <h4>{t('recommended')}</h4>
                    <p><b>{t('capacity_kwh')}:</b> {recommended_battery_kwh:.2f} kWh</p>
                    <p><b>Purpose:</b> Cover night load + safety margin</p>
                </div>
                """, unsafe_allow_html=True)
            with col_auto2:
                if st.button(t('auto_fill'), key="auto_battery", use_container_width=True):
                    st.session_state.auto_battery_capacity = recommended_battery_kwh
                    st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            # Get default values from recommended battery
            pm = st.session_state.product_manager
            default_capacity = st.session_state.get('auto_battery_capacity', 5.0)
            default_battery = pm.get_recommended_battery(min_capacity_kwh=default_capacity)
            
            default_bat_name = st.session_state.get('auto_battery_name', default_battery.name if default_battery else "DEYE 100AH 51.2v (5.12KWH)")
            default_bat_capacity = default_battery.specifications.get('capacity', 5.12) if default_battery else 5.12
            default_bat_voltage = default_battery.specifications.get('voltage', 51.2) if default_battery else 51.2
            default_bat_cost = default_battery.cost if default_battery else 1440.0
            
            bat_name = st.text_input(t('battery_model'), default_bat_name)
            
            # Use auto-calculated capacity if available
            capacity = st.number_input(t('capacity_kwh'), 1.0, value=float(default_bat_capacity), step=0.5, help="Capacity per battery unit")
            
            bat_quantity = st.number_input(
                "🔢 Quantity (Units)",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="Number of battery units to install (connected in parallel for more capacity)"
            )
            
            voltage = st.number_input(t('voltage'), 12, value=int(default_bat_voltage), step=12)
            bat_cost = st.number_input(f"{t('cost')}/Unit ($)", 0.0, value=float(default_bat_cost), help="Cost per battery unit")
        
        with col2:
            total_capacity = capacity * bat_quantity
            total_usable = total_capacity * 0.8
            total_bat_cost = bat_cost * bat_quantity
            
            st.metric(t('total_capacity'), f"{total_capacity:.1f} kWh", help=f"{bat_quantity}x {capacity}kWh batteries")
            st.metric("Usable Energy (80% DoD)", f"{total_usable:.1f} kWh")
            st.metric(t('total_cost'), f"${total_bat_cost:,.2f}", help=f"{bat_quantity} units × ${bat_cost:,.2f}")
            
            # Show comparison with recommendation
            if st.session_state.devices:
                difference = total_capacity - recommended_battery_kwh
                if abs(difference) < 1.0:
                    st.success(t('optimal_sizing'))
                elif difference > 0:
                    st.info(f"ℹ️ {difference:.1f} kWh above recommended (extra backup)")
                else:
                    st.warning(f"⚠️ {abs(difference):.1f} kWh below recommended")
            
            # Show battery configuration info
            if bat_quantity > 1:
                st.markdown(f"""
                <div class="info-box" style="padding: 0.8rem; margin-top: 1rem;">
                    <p style="margin: 0;"><b>⚡ Configuration:</b> {bat_quantity} batteries in parallel</p>
                    <p style="margin: 0;"><small>Each: {capacity}kWh @ {voltage}V | Total: {total_capacity:.1f}kWh</small></p>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button(t('save_config').format(' Battery'), type="primary"):
            st.session_state.system_config.battery = Battery(name=bat_name, capacity_kwh=capacity, voltage=voltage, depth_of_discharge=0.8, efficiency=0.95, cost=bat_cost, quantity=bat_quantity)
            st.success(f"✅ Battery configured successfully! ({bat_quantity}x {capacity}kWh = {total_capacity:.1f}kWh total)")
            st.rerun()
    
    with tab3:
        st.markdown(f"### {t('inverter_config')}")
        
        # Auto-calculate section
        if st.session_state.devices:
            col_auto1, col_auto2 = st.columns(2)
            with col_auto1:
                st.markdown(f"""
                <div class="success-box" style="padding: 1rem;">
                    <h4>{t('recommended')}</h4>
                    <p><b>{t('power_rating')}:</b> {recommended_inverter_kw:.2f} kW</p>
                    <p><b>Peak Load:</b> {peak_power:.2f} kW + 25% margin</p>
                </div>
                """, unsafe_allow_html=True)
            with col_auto2:
                if st.button(t('auto_fill'), key="auto_inverter", use_container_width=True):
                    st.session_state.auto_inverter_power = recommended_inverter_kw
                    st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            # Get default values from recommended inverter
            pm = st.session_state.product_manager
            default_power = st.session_state.get('auto_inverter_power', 5.0)
            default_inverter = pm.get_recommended_inverter(min_power_kw=default_power, inverter_type="Hybrid")
            
            default_inv_name = st.session_state.get('auto_inverter_name', default_inverter.name if default_inverter else "Deye Hybrid 5kw EU 1P")
            default_inv_power = default_inverter.specifications.get('power', 5.0) if default_inverter else 5.0
            default_inv_cost = default_inverter.cost if default_inverter else 888.0
            
            inv_name = st.text_input(t('inverter_model'), default_inv_name)
            
            # Use auto-calculated power if available
            inv_power = st.number_input(t('power_rating'), 1.0, value=float(default_inv_power), step=0.5)
            inv_cost = st.number_input(f"{t('inverter')} {t('cost')} ($)", 0.0, value=float(default_inv_cost))
        
        with col2:
            st.metric(t('power_rating'), f"{inv_power} kW")
            st.metric("Max Output", f"{inv_power * 0.9:.1f} kW (continuous)")
            st.metric(t('total_cost'), f"${inv_cost:,.2f}")
            
            # Show comparison with recommendation
            if st.session_state.devices:
                difference = inv_power - recommended_inverter_kw
                if abs(difference) < 0.5:
                    st.success(t('optimal_sizing'))
                elif difference > 0:
                    st.info(f"ℹ️ {difference:.1f} kW above recommended (good headroom)")
                else:
                    st.warning(f"⚠️ {abs(difference):.1f} kW below recommended")
        
        if st.button(t('save_config').format(' Inverter'), type="primary"):
            st.session_state.system_config.inverter = Inverter(name=inv_name, power_kw=inv_power, efficiency=0.97, cost=inv_cost)
            st.success("✅ Inverter configured successfully!")
            st.rerun()
    
    # Cost Breakdown Section
    st.markdown("---")
    st.markdown("### 💰 Complete Cost Breakdown")
    
    # Calculate all costs
    equipment_cost = 0.0
    if st.session_state.system_config.solar_panels:
        equipment_cost += st.session_state.system_config.solar_panels.cost_per_panel * st.session_state.system_config.solar_panels.quantity
    if st.session_state.system_config.battery:
        equipment_cost += st.session_state.system_config.battery.total_cost
    if st.session_state.system_config.inverter:
        equipment_cost += st.session_state.system_config.inverter.cost
    
    labor_cost = st.session_state.system_config.labor_cost
    support_cost = st.session_state.system_config.support_material_cost
    total_cost = st.session_state.system_config.total_system_cost
    
    # Display cost breakdown
    cost_col1, cost_col2 = st.columns([2, 1])
    
    with cost_col1:
        # Cost breakdown table
        cost_breakdown_data = []
        
        if st.session_state.system_config.solar_panels:
            panels = st.session_state.system_config.solar_panels
            cost_breakdown_data.append({
                'Item': f'Solar Panels ({panels.quantity}x {panels.name})',
                'Cost': f'${panels.cost_per_panel * panels.quantity:,.2f}'
            })
        
        if st.session_state.system_config.battery:
            battery = st.session_state.system_config.battery
            if battery.quantity > 1:
                cost_breakdown_data.append({
                    'Item': f'Battery ({battery.quantity}x {battery.name})',
                    'Cost': f'${battery.total_cost:,.2f}'
                })
            else:
                cost_breakdown_data.append({
                    'Item': f'Battery ({battery.name})',
                    'Cost': f'${battery.total_cost:,.2f}'
                })
        
        if st.session_state.system_config.inverter:
            inverter = st.session_state.system_config.inverter
            cost_breakdown_data.append({
                'Item': f'Inverter ({inverter.name})',
                'Cost': f'${inverter.cost:,.2f}'
            })
        
        # Add labor cost
        if labor_cost > 0:
            inverter_size = st.session_state.system_config.inverter.power_kw if st.session_state.system_config.inverter else 0
            labor_note = f"({'≤5kW' if inverter_size <= 5 else '>5kW'})"
            cost_breakdown_data.append({
                'Item': f'Labor Cost {labor_note}',
                'Cost': f'${labor_cost:,.2f}'
            })
        
        # Add support materials
        if support_cost > 0:
            cost_breakdown_data.append({
                'Item': 'Support Materials',
                'Cost': f'${support_cost:,.2f}'
            })
        
        if cost_breakdown_data:
            df_cost = pd.DataFrame(cost_breakdown_data)
            st.dataframe(df_cost, use_container_width=True, hide_index=True)
        else:
            st.info("Configure system components to see cost breakdown")
    
    with cost_col2:
        # Summary cards
        st.markdown(f"""
        <div class="custom-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px;">
            <h3 style="margin: 0; color: white;">Total System Cost</h3>
            <h2 style="margin: 10px 0; color: white;">${total_cost:,.2f}</h2>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="margin: 5px 0; font-size: 0.9rem;"><b>Equipment:</b> ${equipment_cost:,.2f}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><b>Labor:</b> ${labor_cost:,.2f}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><b>Materials:</b> ${support_cost:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show cost per kW if PV is configured
        if st.session_state.system_config.solar_panels:
            pv_capacity = st.session_state.system_config.solar_panels.total_power_kw
            if pv_capacity > 0:
                cost_per_kw = total_cost / pv_capacity
                st.metric("Cost per kW", f"${cost_per_kw:,.2f}/kW")

# ==================== PRODUCTS ====================
elif page == "🛒 Products":
    st.title("🛒 Product Catalog")
    st.markdown("#### Browse all products from your wholesale price list")
    
    pm = st.session_state.product_manager
    
    # Get all unique categories
    all_categories = sorted(set(p.category for p in pm.products.values()))
    category_options = ["All"] + all_categories
    
    col1, col2 = st.columns([2, 1])
    with col1:
        category = st.selectbox("Filter by Category", category_options)
    with col2:
        st.metric("Total Products", len(pm.products))
    
    # Filter products
    products = list(pm.products.values()) if category == "All" else pm.get_products_by_category(category)
    
    # Display category summary
    if category == "All":
        st.markdown("### 📊 Category Summary")
        summary_cols = st.columns(4)
        for idx, cat in enumerate(all_categories[:4]):
            with summary_cols[idx]:
                cat_products = pm.get_products_by_category(cat)
                st.metric(f"{cat.replace('_', ' ').title()}", len(cat_products))
    
    st.markdown(f"### Showing {len(products)} Products")
    
    # Display products in a more organized way
    for p in products:
        with st.expander(f"💰 {p.name} - ${p.cost:,.2f} (Wholesale)"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Category:** {p.category.replace('_', ' ').title()}")
                st.markdown(f"**Supplier:** {p.supplier}")
                st.markdown(f"**Warranty:** {p.warranty_years} years")
                if p.notes:
                    st.info(f"ℹ️ {p.notes}")
            with col2:
                st.markdown("**Specifications:**")
                for key, value in p.specifications.items():
                    st.write(f"• {key.replace('_', ' ').title()}: {value}")
                
                # Show customer price with 30% markup
                customer_price = p.cost * 1.3
                st.success(f"💵 Customer Price: ${customer_price:,.2f} (+30%)")
    
    # Show note about pricing
    st.markdown("---")
    st.info("💡 **Pricing Note:** Wholesale prices are shown. Customer reports include a 30% markup for retail pricing.")

# ==================== SIMULATION ====================
elif page == t('nav_simulation'):
    st.title(t('simulation_title'))
    st.markdown(f"#### {t('simulation_subtitle')}")
    
    # Check customer info first
    if not st.session_state.customer_info['name'] or not st.session_state.customer_info['phone']:
        st.markdown("""
        <div class="warning-box">
            <h3>👤 Customer Information Required</h3>
            <p>Please add customer information in the <b>🏠 Dashboard</b> page before running simulation.</p>
            <p>This helps identify each customer's unique requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ Go to Dashboard", type="primary", use_container_width=True):
                st.switch_page("app.py")
        st.stop()
    
    # Display customer info at top
    st.markdown(f"### {t('customer_project')}")
    customer_col1, customer_col2 = st.columns(2)
    with customer_col1:
        st.markdown(f"""
        <div class="custom-card" style="padding: 1rem;">
            <p style="margin: 0;"><b>Customer:</b> {st.session_state.customer_info['name']}</p>
            <p style="margin: 0;"><b>Company:</b> {st.session_state.customer_info['company'] or 'N/A'}</p>
        </div>
        """, unsafe_allow_html=True)
    with customer_col2:
        st.markdown(f"""
        <div class="custom-card" style="padding: 1rem;">
            <p style="margin: 0;"><b>Phone:</b> {st.session_state.customer_info['phone']}</p>
            <p style="margin: 0;"><b>Telegram:</b> {st.session_state.customer_info['telegram'] or 'N/A'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Prerequisites Checklist
    st.markdown("### ✅ Prerequisites Check")
    
    # Calculate prerequisites status
    has_devices = len(st.session_state.devices) > 0
    has_panels = st.session_state.system_config.solar_panels is not None
    has_battery = st.session_state.system_config.battery is not None
    has_inverter = st.session_state.system_config.inverter is not None
    
    total_load = sum(d.daily_energy_kwh for d in st.session_state.devices) if has_devices else 0
    pv_cap = st.session_state.system_config.solar_panels.total_power_kw if has_panels else 0
    bat_cap = st.session_state.system_config.battery.total_capacity_kwh if has_battery else 0
    inv_cap = st.session_state.system_config.inverter.power_kw if has_inverter else 0
    
    # Check if system is properly sized
    pv_adequate = pv_cap >= (total_load / 4) if has_devices and has_panels else False
    battery_adequate = bat_cap >= (total_load * 0.5) if has_devices and has_battery else False
    inverter_adequate = inv_cap >= (pv_cap * 0.8) if has_panels and has_inverter else False
    
    all_required = has_devices and has_panels and has_battery and has_inverter
    all_optimal = all_required and pv_adequate and battery_adequate and inverter_adequate
    
    # Display checklist in a nice card
    checklist_col1, checklist_col2 = st.columns([2, 1])
    
    with checklist_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white;">
            <h4 style="margin: 0 0 1rem 0;">🎯 System Readiness</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Required items
        st.markdown("**Required Components:**")
        req_col1, req_col2, req_col3, req_col4 = st.columns(4)
        
        with req_col1:
            if has_devices:
                st.markdown(f"✅ **Devices**<br>{len(st.session_state.devices)} configured", unsafe_allow_html=True)
            else:
                st.markdown("❌ **Devices**<br>None added", unsafe_allow_html=True)
        
        with req_col2:
            if has_panels:
                st.markdown(f"✅ **Solar**<br>{pv_cap:.1f} kW", unsafe_allow_html=True)
            else:
                st.markdown("❌ **Solar**<br>Not set", unsafe_allow_html=True)
        
        with req_col3:
            if has_battery:
                st.markdown(f"✅ **Battery**<br>{bat_cap:.1f} kWh", unsafe_allow_html=True)
            else:
                st.markdown("❌ **Battery**<br>Not set", unsafe_allow_html=True)
        
        with req_col4:
            if has_inverter:
                st.markdown(f"✅ **Inverter**<br>{inv_cap:.1f} kW", unsafe_allow_html=True)
            else:
                st.markdown("❌ **Inverter**<br>Not set", unsafe_allow_html=True)
        
        # System sizing check
        if all_required:
            st.markdown("---")
            st.markdown("**System Sizing Analysis:**")
            size_col1, size_col2, size_col3 = st.columns(3)
            
            with size_col1:
                if pv_adequate:
                    st.markdown("✅ **PV Sizing**<br>Adequate for load", unsafe_allow_html=True)
                else:
                    shortfall = (total_load / 4) - pv_cap
                    st.markdown(f"⚠️ **PV Sizing**<br>Add {shortfall:.1f} kW", unsafe_allow_html=True)
            
            with size_col2:
                if battery_adequate:
                    st.markdown("✅ **Battery Size**<br>Good capacity", unsafe_allow_html=True)
                else:
                    needed = (total_load * 0.5) - bat_cap
                    st.markdown(f"⚠️ **Battery Size**<br>Add {needed:.1f} kWh", unsafe_allow_html=True)
            
            with size_col3:
                if inverter_adequate:
                    st.markdown("✅ **Inverter Size**<br>Properly sized", unsafe_allow_html=True)
                else:
                    needed = (pv_cap * 0.8) - inv_cap
                    st.markdown(f"⚠️ **Inverter Size**<br>Add {needed:.1f} kW", unsafe_allow_html=True)
    
    with checklist_col2:
        # Overall status
        if all_optimal:
            st.markdown("""
            <div style="background: #10b981; padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">✅</h2>
                <h4 style="margin: 0.5rem 0;">Ready to Simulate</h4>
                <p style="margin: 0; font-size: 0.9rem;">All systems optimal</p>
            </div>
            """, unsafe_allow_html=True)
        elif all_required:
            st.markdown("""
            <div style="background: #f59e0b; padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">⚠️</h2>
                <h4 style="margin: 0.5rem 0;">Can Simulate</h4>
                <p style="margin: 0; font-size: 0.9rem;">Some sizing issues</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #ef4444; padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">❌</h2>
                <h4 style="margin: 0.5rem 0;">Cannot Simulate</h4>
                <p style="margin: 0; font-size: 0.9rem;">Missing components</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick action buttons
        st.markdown("<br>", unsafe_allow_html=True)
        if not has_devices:
            if st.button("➕ Add Devices", use_container_width=True, type="secondary"):
                st.switch_page("app.py")
        if not has_panels or not has_battery or not has_inverter:
            if st.button("🔧 Configure System", use_container_width=True, type="secondary"):
                st.switch_page("app.py")
    
    # Stop if required components missing
    if not all_required:
        st.stop()
    
    # Detailed System Configuration Display
    st.markdown("### 📋 System Configuration Summary")
    
    config_col1, config_col2 = st.columns([2, 1])
    
    with config_col1:
        # Component details
        st.markdown("🔹 **Solar Panels:**")
        if st.session_state.system_config.solar_panels:
            panels = st.session_state.system_config.solar_panels
            st.write(f"  • {panels.quantity}x {panels.name} ({panels.power_watts}W each)")
            st.write(f"  • Total Capacity: {panels.total_power_kw:.2f} kW")
            st.write(f"  • Cost: ${panels.cost_per_panel * panels.quantity:,.2f}")
        
        st.markdown("🔹 **Battery Storage:**")
        if st.session_state.system_config.battery:
            battery = st.session_state.system_config.battery
            if battery.quantity > 1:
                st.write(f"  • {battery.quantity}x {battery.name} ({battery.capacity_kwh}kWh each)")
                st.write(f"  • Total Capacity: {battery.total_capacity_kwh:.2f} kWh")
                st.write(f"  • Usable: {battery.usable_capacity_kwh:.2f} kWh (80% DoD)")
                st.write(f"  • Cost: ${battery.total_cost:,.2f} ({battery.quantity} units)")
            else:
                st.write(f"  • {battery.name} ({battery.capacity_kwh}kWh)")
                st.write(f"  • Usable: {battery.usable_capacity_kwh:.2f} kWh (80% DoD)")
                st.write(f"  • Cost: ${battery.cost:,.2f}")
        
        st.markdown("🔹 **Inverter:**")
        if st.session_state.system_config.inverter:
            inverter = st.session_state.system_config.inverter
            st.write(f"  • {inverter.name} ({inverter.power_kw}kW)")
            st.write(f"  • Efficiency: {inverter.efficiency * 100:.0f}%")
            st.write(f"  • Cost: ${inverter.cost:,.2f}")
    
    with config_col2:
        # Cost summary
        equipment_cost = 0.0
        if st.session_state.system_config.solar_panels:
            equipment_cost += st.session_state.system_config.solar_panels.cost_per_panel * st.session_state.system_config.solar_panels.quantity
        if st.session_state.system_config.battery:
            equipment_cost += st.session_state.system_config.battery.total_cost
        if st.session_state.system_config.inverter:
            equipment_cost += st.session_state.system_config.inverter.cost
        
        labor_cost = st.session_state.system_config.labor_cost
        support_cost = st.session_state.system_config.support_material_cost
        total_cost = st.session_state.system_config.total_system_cost
        
        st.markdown("💰 **Cost Summary (Wholesale):**")
        st.write(f"  • Equipment: ${equipment_cost:,.2f}")
        st.write(f"  • Labor: ${labor_cost:,.2f}")
        st.write(f"  • Materials: ${support_cost:,.2f}")
        st.markdown(f"**Total: ${total_cost:,.2f}**")
        st.caption("ℹ️ Customer price (+30%): ${:,.2f}".format(total_cost * 1.3))
    
    st.markdown("---")
    
    # Quick metrics
    st.markdown("### 📊 Quick Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⚡ Devices", len(st.session_state.devices))
    with col2:
        pv_cap = st.session_state.system_config.solar_panels.total_power_kw
        st.metric("☀️ PV Capacity", f"{pv_cap:.2f} kW")
    with col3:
        if st.session_state.system_config.battery:
            bat_cap = st.session_state.system_config.battery.total_capacity_kwh
            bat_qty = st.session_state.system_config.battery.quantity
            if bat_qty > 1:
                st.metric("🔋 Battery", f"{bat_cap:.1f} kWh", delta=f"{bat_qty} units")
            else:
                st.metric("🔋 Battery", f"{bat_cap:.1f} kWh")
        else:
            bat_cap = 5.0
            st.metric("🔋 Battery", f"{bat_cap:.1f} kWh")
    with col4:
        total_load = sum(d.daily_energy_kwh for d in st.session_state.devices)
        st.metric("🔌 Daily Load", f"{total_load:.2f} kWh")
    
    st.markdown("---")
    
    # Run simulation button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Run 24-Hour Simulation", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("⚙️ Initializing calculator...")
            progress_bar.progress(20)
            
            calc = SolarCalculator(st.session_state.system_config)
            
            status_text.text("☀️ Calculating PV generation...")
            progress_bar.progress(40)
            
            status_text.text("🔋 Simulating battery flow...")
            progress_bar.progress(60)
            
            results = calc.simulate_24_hours(pv_cap, bat_cap, st.session_state.devices)
            
            status_text.text("📊 Processing results...")
            progress_bar.progress(80)
            
            st.session_state.simulation_results = results
            
            progress_bar.progress(100)
            status_text.text("✅ Simulation complete!")
            
            st.success("🎉 Simulation completed successfully!")
            st.rerun()
    
    if st.session_state.simulation_results:
        st.markdown("---")
        st.markdown("### 📈 Simulation Results")
        
        viz = SolarVisualizer()
        results = st.session_state.simulation_results
        calc = SolarCalculator(st.session_state.system_config)
        
        # Calculate metrics
        total_pv = sum(r.pv_generation_kw for r in results)
        total_load = sum(r.load_kw for r in results)
        total_grid = sum(r.grid_import_kw for r in results)
        total_grid_export = sum(r.grid_export_kw for r in results)
        self_suff = ((total_load - total_grid) / total_load * 100) if total_load > 0 else 0
        
        # Create tabs for organized results
        results_tab1, results_tab2, results_tab3, results_tab4, results_tab5 = st.tabs([
            "📊 Overview & KPIs",
            "📈 Energy Flow",
            "💡 System Insights",
            "💰 Financial Analysis",
            "🎯 Recommendations"
        ])
        
        # ===== TAB 1: Overview & KPIs =====
        with results_tab1:
            st.markdown(f"#### {t('kpi')}")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label=t('pv_generation'),
                    value=f"{total_pv:.2f} kWh",
                    delta=f"{total_pv * 30:.0f} kWh/month"
                )
            with col2:
                st.metric(
                    label=t('total_load'),
                    value=f"{total_load:.2f} kWh",
                    delta=f"{total_load * 30:.0f} kWh/month"
                )
            with col3:
                grid_status = "Low" if total_grid < total_load * 0.2 else "Moderate"
                st.metric(
                    t('grid_import'),
                    f"{total_grid:.2f} kWh",
                    delta=grid_status,
                    delta_color="inverse"
                )
            with col4:
                suff_status = "Excellent" if self_suff >= 80 else "Good" if self_suff >= 50 else "Low"
                st.metric(
                    "🎯 Self-Sufficiency",
                    f"{self_suff:.1f}%",
                    delta=suff_status
                )
        
        # ===== TAB 2: Energy Flow =====
        with results_tab2:
            st.markdown("#### 📊 24-Hour Energy Flow")
            fig = viz.create_24h_energy_flow_chart(results)
            st.plotly_chart(fig, use_container_width=True)
        
        # ===== TAB 3: System Insights =====
        with results_tab3:
            st.markdown("#### 💡 System Insights")
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                avg_battery_soc = sum(r.battery_soc for r in results) / len(results)
                min_battery_soc = min(r.battery_soc for r in results)
                
                st.markdown(f"""
                <div class="custom-card">
                    <h4>🔋 Battery Performance</h4>
                    <p><b>Average SoC:</b> {avg_battery_soc:.1f}%</p>
                    <p><b>Minimum SoC:</b> {min_battery_soc:.1f}%</p>
                    <p><b>Status:</b> {"Excellent" if min_battery_soc > 30 else "Needs attention"}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with insight_col2:
                peak_pv = max(r.pv_generation_kw for r in results)
                peak_hour = next(r.hour for r in results if r.pv_generation_kw == peak_pv)
                
                st.markdown(f"""
                <div class="custom-card">
                    <h4>☀️ Solar Performance</h4>
                    <p><b>Peak Generation:</b> {peak_pv:.2f} kW</p>
                    <p><b>Peak Hour:</b> {peak_hour}:00</p>
                    <p><b>Daily Total:</b> {total_pv:.2f} kWh</p>
                </div>
                """, unsafe_allow_html=True)
            
            with insight_col3:
                energy_wasted = sum(r.energy_surplus_kw for r in results)
                grid_export_value = total_grid_export * 0.15
                
                st.markdown(f"""
                <div class="custom-card">
                    <h4>💰 Energy Economics</h4>
                    <p><b>Grid Export:</b> {total_grid_export:.2f} kWh</p>
                    <p><b>Export Value:</b> ${grid_export_value:.2f}</p>
                    <p><b>Wasted Energy:</b> {energy_wasted:.2f} kWh</p>
                </div>
                """, unsafe_allow_html=True)
        
        # ===== TAB 4: Financial Analysis =====
        with results_tab4:
            st.markdown("#### 💰 Financial Analysis & ROI Breakdown")
            
            # Add Pricing Mode Toggle
            pricing_col1, pricing_col2 = st.columns([3, 1])
        with pricing_col1:
            st.markdown("### 💰 Pricing Mode")
        with pricing_col2:
            customer_pricing = st.checkbox(
                "🏷️ Customer Pricing (+30%)",
                value=True,
                help="Enable to show financial analysis with customer pricing (30% markup). Disable for wholesale pricing."
            )
        
        # Apply markup if customer pricing is selected
        markup_multiplier = 1.30 if customer_pricing else 1.0
        
        if customer_pricing:
            st.info("ℹ️ **Customer Pricing Mode**: All costs include 30% markup for retail customers")
        else:
            st.warning("⚠️ **Wholesale Pricing Mode**: Showing wholesale costs (internal use only)")
        
        st.markdown("---")
        
        calc = SolarCalculator(st.session_state.system_config)
        wholesale_cost = st.session_state.system_config.total_system_cost
        system_cost = wholesale_cost * markup_multiplier
        annual_energy = total_pv * 365
        
        # Use fixed electricity rate for Cambodia
        electricity_rate = 0.1875  # $0.1875 per kWh
        
        financial = calc.calculate_financial_analysis(
            system_cost, annual_energy,
            electricity_rate
        )
        
        # Initial Investment Summary
        st.markdown("#### 📈 Initial Investment")
        inv_col1, inv_col2, inv_col3, inv_col4 = st.columns(4)
        with inv_col1:
            if customer_pricing:
                st.metric("System Cost (Customer)", f"${system_cost:,.2f}", delta=f"+30% from ${wholesale_cost:,.2f}")
            else:
                st.metric("System Cost (Wholesale)", f"${system_cost:,.2f}")
        with inv_col2:
            annual_generation = annual_energy
            st.metric("Annual Generation", f"{annual_generation:,.0f} kWh")
        with inv_col3:
            annual_savings = annual_generation * electricity_rate
            st.metric("Annual Savings", f"${annual_savings:,.2f}")
        with inv_col4:
            payback = system_cost / annual_savings if annual_savings > 0 else 0
            st.metric("Payback Period", f"{payback:.1f} years")
        
        pricing_mode = "Customer (+30%)" if customer_pricing else "Wholesale"
        st.caption(f"⚡ Electricity Rate: ${electricity_rate}/kWh | 📅 Analysis based on {annual_generation:,.0f} kWh/year | 🏷️ {pricing_mode} pricing")
        
        st.markdown("---")
        
        # ROI Timeline Breakdown
        st.markdown("#### 📅 ROI Timeline Breakdown")
        
        timeline_data = []
        
        # Year 3 - After initial warranty
        years_3 = 3
        total_savings_3y = annual_savings * years_3
        maintenance_3y = system_cost * 0.02 * years_3  # 2% per year maintenance
        net_savings_3y = total_savings_3y - maintenance_3y
        net_profit_3y = net_savings_3y - system_cost
        roi_3y = (net_profit_3y / system_cost) * 100
        
        timeline_data.append({
            "Period": "🔹 Year 3",
            "Milestone": "Inverter Warranty Ends",
            "Total Savings": f"${total_savings_3y:,.2f}",
            "Maintenance": f"${maintenance_3y:,.2f}",
            "Net Profit": f"${net_profit_3y:,.2f}",
            "ROI": f"{roi_3y:.1f}%",
            "Status": "❌ Not Paid Off" if net_profit_3y < 0 else "✅ Profitable"
        })
        
        # Year 5 - Mid-term review
        years_5 = 5
        total_savings_5y = annual_savings * years_5
        maintenance_5y = system_cost * 0.02 * years_5
        net_savings_5y = total_savings_5y - maintenance_5y
        net_profit_5y = net_savings_5y - system_cost
        roi_5y = (net_profit_5y / system_cost) * 100
        
        timeline_data.append({
            "Period": "🔹 Year 5",
            "Milestone": "Extended Warranty Period",
            "Total Savings": f"${total_savings_5y:,.2f}",
            "Maintenance": f"${maintenance_5y:,.2f}",
            "Net Profit": f"${net_profit_5y:,.2f}",
            "ROI": f"{roi_5y:.1f}%",
            "Status": "❌ Not Paid Off" if net_profit_5y < 0 else "✅ Profitable"
        })
        
        # Year 10 - Mid-life
        years_10 = 10
        total_savings_10y = annual_savings * years_10
        maintenance_10y = system_cost * 0.02 * years_10
        # Possible inverter replacement at year 10
        inverter_replacement = (st.session_state.system_config.inverter.cost * markup_multiplier) if st.session_state.system_config.inverter else 0
        net_savings_10y = total_savings_10y - maintenance_10y - inverter_replacement
        net_profit_10y = net_savings_10y - system_cost
        roi_10y = (net_profit_10y / system_cost) * 100
        
        timeline_data.append({
            "Period": "🔹 Year 10",
            "Milestone": "Inverter Replacement (~$800)",
            "Total Savings": f"${total_savings_10y:,.2f}",
            "Maintenance": f"${maintenance_10y + inverter_replacement:,.2f}",
            "Net Profit": f"${net_profit_10y:,.2f}",
            "ROI": f"{roi_10y:.1f}%",
            "Status": "❌ Not Paid Off" if net_profit_10y < 0 else "✅ Profitable"
        })
        
        # Year 15 - Battery lifespan
        years_15 = 15
        total_savings_15y = annual_savings * years_15
        maintenance_15y = system_cost * 0.02 * years_15
        # Add inverter replacement cost
        total_replacements = inverter_replacement
        net_savings_15y = total_savings_15y - maintenance_15y - total_replacements
        net_profit_15y = net_savings_15y - system_cost
        roi_15y = (net_profit_15y / system_cost) * 100
        
        timeline_data.append({
            "Period": "🔹 Year 15",
            "Milestone": "Battery Lifespan End",
            "Total Savings": f"${total_savings_15y:,.2f}",
            "Maintenance": f"${maintenance_15y + total_replacements:,.2f}",
            "Net Profit": f"${net_profit_15y:,.2f}",
            "ROI": f"{roi_15y:.1f}%",
            "Status": "❌ Not Paid Off" if net_profit_15y < 0 else "✅ Profitable"
        })
        
        # Year 25 - Panel lifespan
        years_25 = 25
        total_savings_25y = annual_savings * years_25 * 0.9  # 10% degradation
        maintenance_25y = system_cost * 0.02 * years_25
        # Battery replacement at year 15
        battery_replacement = (st.session_state.system_config.battery.total_cost * markup_multiplier) if st.session_state.system_config.battery else 0
        total_replacements_25y = inverter_replacement + battery_replacement
        net_savings_25y = total_savings_25y - maintenance_25y - total_replacements_25y
        net_profit_25y = net_savings_25y - system_cost
        roi_25y = (net_profit_25y / system_cost) * 100
        
        timeline_data.append({
            "Period": "🔹 Year 25",
            "Milestone": "Full System Lifespan",
            "Total Savings": f"${total_savings_25y:,.2f}",
            "Maintenance": f"${maintenance_25y + total_replacements_25y:,.2f}",
            "Net Profit": f"${net_profit_25y:,.2f}",
            "ROI": f"{roi_25y:.1f}%",
            "Status": "✅ Fully Profitable"
        })
        
        # Display as table
        import pandas as pd
        timeline_df = pd.DataFrame(timeline_data)
        st.dataframe(timeline_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Key Financial Highlights
        st.markdown("#### 🎯 Key Financial Highlights")
        highlight_col1, highlight_col2, highlight_col3 = st.columns(3)
        
        with highlight_col1:
            st.markdown(f"""
            <div class="success-box" style="padding: 1rem;">
                <h4>💵 Break-Even Point</h4>
                <p><b>Estimated:</b> Year {payback:.1f}</p>
                <p><b>After payback:</b> Pure profit!</p>
            </div>
            """, unsafe_allow_html=True)
        
        with highlight_col2:
            st.markdown(f"""
            <div class="info-box" style="padding: 1rem;">
                <h4>🔋 Battery Impact</h4>
                <p><b>Lifespan:</b> 15 years</p>
                <p><b>Replacement Cost:</b> ${battery_replacement:,.2f}</p>
                <p><b>At Year 15:</b> Consider upgrade</p>
            </div>
            """, unsafe_allow_html=True)
        
        with highlight_col3:
            st.markdown(f"""
            <div class="custom-card" style="padding: 1rem;">
                <h4>🌱 Environmental Impact</h4>
                <p><b>CO₂ Reduction:</b> {financial.co2_reduction_kg_per_year * 15:,.0f} kg</p>
                <p><b>Over 15 years</b></p>
            </div>
            """, unsafe_allow_html=True)
        
        # ===== TAB 5: Recommendations =====
        with results_tab5:
            st.markdown("#### 💡 AI Recommendations")
            st.markdown("Based on your simulation results and system configuration:")
            st.markdown("---")
            recommendations = calc.get_device_recommendations(
                st.session_state.devices, pv_cap, bat_cap
            )
            for idx, rec in enumerate(recommendations, 1):
                st.info(f"**{idx}.** {rec}")

# ==================== REPORTS ====================
elif page == t('nav_reports'):
    st.title(t('reports_title'))
    
    if not st.session_state.simulation_results:
        st.warning("⚠️ Run a simulation first")
        st.stop()
    
    # Display customer info
    if st.session_state.customer_info['name']:
        st.markdown(f"### {t('customer_report')}")
        report_col1, report_col2 = st.columns(2)
        with report_col1:
            st.markdown(f"""
            <div class="custom-card" style="padding: 1rem;">
                <p style="margin: 0;"><b>Customer:</b> {st.session_state.customer_info['name']}</p>
                <p style="margin: 0;"><b>Company:</b> {st.session_state.customer_info['company'] or 'N/A'}</p>
                <p style="margin: 0;"><b>Address:</b> {st.session_state.customer_info['address'] or 'N/A'}</p>
            </div>
            """, unsafe_allow_html=True)
        with report_col2:
            st.markdown(f"""
            <div class="custom-card" style="padding: 1rem;">
                <p style="margin: 0;"><b>Phone:</b> {st.session_state.customer_info['phone']}</p>
                <p style="margin: 0;"><b>Telegram:</b> {st.session_state.customer_info['telegram'] or 'N/A'}</p>
                <p style="margin: 0;"><b>Email:</b> {st.session_state.customer_info['email'] or 'N/A'}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
    
    exporter = ReportExporter()
    results = st.session_state.simulation_results
    devices = st.session_state.devices
    
    # Add Customer Pricing Toggle
    st.markdown("### 💰 Pricing Mode")
    customer_markup_mode = st.checkbox(
        "🏷️ Customer Report (Add 30% Markup)",
        value=True,
        help="Enable this to add 30% markup to all wholesale prices for customer reports. Wholesale prices are used for internal analysis."
    )
    
    markup_multiplier = 1.30 if customer_markup_mode else 1.0
    
    if customer_markup_mode:
        st.info("ℹ️ **Customer Pricing Mode Active**: All prices shown include 30% markup for retail customers")
    else:
        st.warning("⚠️ **Wholesale Pricing Mode**: Showing wholesale prices (for internal use only)")
    
    st.markdown("---")
    
    # Financial data with markup applied
    calc = SolarCalculator(st.session_state.system_config)
    total_pv = sum(r.pv_generation_kw for r in results)
    annual_energy = total_pv * 365
    system_cost = st.session_state.system_config.total_system_cost * markup_multiplier
    financial = calc.calculate_financial_analysis(system_cost, annual_energy, 0.20)
    
    st.markdown(f"### {t('download_reports')}")
    
    # Quick Export All Button
    quick_export_col1, quick_export_col2, quick_export_col3 = st.columns([1, 2, 1])
    with quick_export_col2:
        if st.button("⚡ Quick Export All (PDF + Word + Excel)", type="primary", use_container_width=True, help="Export all report formats at once"):
            with st.spinner("Generating all reports..."):
                # Prepare data
                equipment_cost = 0.0
                if st.session_state.system_config.solar_panels:
                    equipment_cost += (st.session_state.system_config.solar_panels.cost_per_panel * st.session_state.system_config.solar_panels.quantity) * markup_multiplier
                if st.session_state.system_config.battery:
                    equipment_cost += st.session_state.system_config.battery.total_cost * markup_multiplier
                if st.session_state.system_config.inverter:
                    equipment_cost += st.session_state.system_config.inverter.cost * markup_multiplier
                
                system_config = {
                    "customer_name": st.session_state.customer_info['name'],
                    "customer_company": st.session_state.customer_info['company'],
                    "customer_phone": st.session_state.customer_info['phone'],
                    "customer_telegram": st.session_state.customer_info['telegram'],
                    "customer_email": st.session_state.customer_info['email'],
                    "customer_address": st.session_state.customer_info['address'],
                    "location": st.session_state.system_config.location,
                    "pv_capacity": st.session_state.system_config.solar_panels.total_power_kw if st.session_state.system_config.solar_panels else 0,
                    "battery_capacity": st.session_state.system_config.battery.total_capacity_kwh if st.session_state.system_config.battery else 0,
                    "inverter_power": st.session_state.system_config.inverter.power_kw if st.session_state.system_config.inverter else 0,
                    "labor_cost": st.session_state.system_config.labor_cost * markup_multiplier,
                    "support_material_cost": st.session_state.system_config.support_material_cost * markup_multiplier,
                    "equipment_cost": equipment_cost
                }
                
                # Export all formats
                exporter.generate_pdf_report(results, devices, financial, system_config, "solar_report.pdf")
                exporter.generate_word_report(results, devices, financial, system_config, "solar_report.docx")
                exporter.export_to_excel(results, devices, financial, "solar_report.xlsx")
                
                st.success("✅ All reports exported successfully!")
                st.balloons()
    
    st.markdown("---")
    st.markdown("#### Or export individually:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(t('export_excel'), type="primary", use_container_width=True):
            exporter.export_to_excel(results, devices, financial, "solar_report.xlsx")
            st.success("✅ Exported to solar_report.xlsx")
    
    with col2:
        if st.button(t('export_csv'), use_container_width=True):
            exporter.export_to_csv(results, "solar_simulation.csv")
            st.success("✅ Exported to solar_simulation.csv")
    
    with col3:
        if st.button(t('export_pdf'), use_container_width=True):
            # Calculate equipment cost with markup
            equipment_cost = 0.0
            if st.session_state.system_config.solar_panels:
                equipment_cost += (st.session_state.system_config.solar_panels.cost_per_panel * st.session_state.system_config.solar_panels.quantity) * markup_multiplier
            if st.session_state.system_config.battery:
                equipment_cost += st.session_state.system_config.battery.total_cost * markup_multiplier
            if st.session_state.system_config.inverter:
                equipment_cost += st.session_state.system_config.inverter.cost * markup_multiplier
            
            system_config = {
                "customer_name": st.session_state.customer_info['name'],
                "customer_company": st.session_state.customer_info['company'],
                "customer_phone": st.session_state.customer_info['phone'],
                "customer_telegram": st.session_state.customer_info['telegram'],
                "customer_email": st.session_state.customer_info['email'],
                "customer_address": st.session_state.customer_info['address'],
                "location": st.session_state.system_config.location,
                "pv_capacity": st.session_state.system_config.solar_panels.total_power_kw if st.session_state.system_config.solar_panels else 0,
                "battery_capacity": st.session_state.system_config.battery.capacity_kwh if st.session_state.system_config.battery else 0,
                "inverter_power": st.session_state.system_config.inverter.power_kw if st.session_state.system_config.inverter else 0,
                "labor_cost": st.session_state.system_config.labor_cost * markup_multiplier,
                "support_material_cost": st.session_state.system_config.support_material_cost * markup_multiplier,
                "equipment_cost": equipment_cost
            }
            exporter.generate_pdf_report(results, devices, financial, system_config, "solar_report.pdf")
            st.success("✅ Exported to solar_report.pdf")
    
    with col4:
        if st.button("📄 Export Word", use_container_width=True):
            # Calculate equipment cost with markup
            equipment_cost = 0.0
            if st.session_state.system_config.solar_panels:
                equipment_cost += (st.session_state.system_config.solar_panels.cost_per_panel * st.session_state.system_config.solar_panels.quantity) * markup_multiplier
            if st.session_state.system_config.battery:
                equipment_cost += st.session_state.system_config.battery.total_cost * markup_multiplier
            if st.session_state.system_config.inverter:
                equipment_cost += st.session_state.system_config.inverter.cost * markup_multiplier
            
            system_config = {
                "customer_name": st.session_state.customer_info['name'],
                "customer_company": st.session_state.customer_info['company'],
                "customer_phone": st.session_state.customer_info['phone'],
                "customer_telegram": st.session_state.customer_info['telegram'],
                "customer_email": st.session_state.customer_info['email'],
                "customer_address": st.session_state.customer_info['address'],
                "location": st.session_state.system_config.location,
                "pv_capacity": st.session_state.system_config.solar_panels.total_power_kw if st.session_state.system_config.solar_panels else 0,
                "battery_capacity": st.session_state.system_config.battery.capacity_kwh if st.session_state.system_config.battery else 0,
                "inverter_power": st.session_state.system_config.inverter.power_kw if st.session_state.system_config.inverter else 0,
                "labor_cost": st.session_state.system_config.labor_cost * markup_multiplier,
                "support_material_cost": st.session_state.system_config.support_material_cost * markup_multiplier,
                "equipment_cost": equipment_cost
            }
            exporter.generate_word_report(results, devices, financial, system_config, "solar_report.docx")
            st.success("✅ Exported to solar_report.docx")
    
    # Summary table
    st.markdown("---")
    st.subheader("Daily Summary Table")
    viz = SolarVisualizer()
    summary_df = viz.create_monthly_summary_table(results)
    st.dataframe(summary_df, use_container_width=True)

# Footer - Ultra Compact
st.sidebar.markdown("<div style='margin: 0.75rem 0;'><hr style='margin: 0; border: none; border-top: 1px solid #e5e7eb;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='text-align: center; padding: 0.3rem 0; color: #9ca3af; font-size: 0.65rem; line-height: 1.4;'>
    <div>📞 <b>0888836588</b></div>
    <div>💬 @chhanycls</div>
    <div style='margin-top: 0.3rem; opacity: 0.6;'>v2.0 © 2025</div>
</div>
""", unsafe_allow_html=True)
