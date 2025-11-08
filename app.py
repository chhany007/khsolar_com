"""
KHSolar - Ultimate Solar Planning & Business Software
"""
import streamlit as st

# Page config - MUST be first Streamlit command
st.set_page_config(page_title="KHSolar - Solar Planning Software", page_icon="☀️", layout="wide")

import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
import sqlite3
import re
import base64
from product_manager import ProductManager
from visualization import SolarVisualizer
from export_utils import ReportExporter
from calculations import SolarCalculator
from models import (
    SystemConfiguration, 
    Device, 
    SimulationResult, 
    SolarPanel, 
    Battery, 
    Inverter, 
    Product, 
    FinancialAnalysis
)

# Load logo once at startup
@st.cache_data
def load_logo():
    """Load and encode logo image"""
    logo_path = Path("logo/logo.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

LOGO_BASE64 = load_logo()

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
        'nav_devices': '📱 Device Management',
        'nav_system': '⚙️ System Configuration',
        'nav_products': '📦 Product Catalog',
        'individual_products': '🛍️ Individual Products',
        'complete_system_sets': '📦 Complete System Sets',
        'filter_category': 'Filter by Category',
        'all_products': '🌐 All Products',
        'solar_panels': '☀️ Solar Panels',
        'inverters': '⚡ Inverters',
        'batteries': '🔋 Batteries',
        'water_pumps': '💧 Water Pumps',
        'accessories': '🔧 Accessories & Materials',
        'total_products': 'Total Products',
        'search': '🔍 Search',
        'showing_products': 'Showing {count} Products',
        'wholesale': 'Wholesale',
        'retail': 'Retail',
        'product_details': '📋 Product Details',
        'category': 'Category',
        'supplier': 'Supplier',
        'warranty': 'Warranty',
        'years': 'years',
        'specifications': '⚙️ Specifications',
        'pricing': '💰 Pricing',
        'pricing_note': '💡 **Pricing Note:** Wholesale prices are base costs. Retail prices include 30% markup for customer quotes.',
        'ready_install_packages': '📦 Ready-to-Install System Packages',
        'complete_solar_desc': 'Complete solar system sets with all components, materials, and installation',
        'system_performance': '📊 System Performance',
        'daily_generation': 'Daily Generation',
        'backup_time': 'Backup Time',
        'recommended_load': 'Recommended Load',
        'component_specs': '🔧 Component Specifications',
        'model': 'Model',
        'total_power': 'Total Power',
        'power_panel': 'Power/Panel',
        'efficiency': 'Efficiency',
        'size': 'Size',
        'weight': 'Weight',
        'area_needed': 'Area Needed',
        'power': 'Power',
        'type': 'Type',
        'max_pv_input': 'Max PV Input',
        'mppt_trackers': 'MPPT Trackers',
        'max_charge': 'Max Charge',
        'battery_voltage': 'Battery Voltage',
        'phases': 'Phases',
        'battery_storage': '🔋 Battery Storage',
        'capacity_unit': 'Capacity/Unit',
        'voltage': 'Voltage',
        'cycle_life': 'Cycle Life',
        'usable_energy': 'Usable Energy',
        'complete_pricing': '💰 Complete System Pricing',
        'detailed_breakdown': '📊 Detailed Cost Breakdown',
        'main_equipment': 'Main Equipment',
        'equipment_subtotal': 'Equipment Subtotal',
        'mounting_materials': 'Mounting & Materials',
        'rails': 'Rails',
        'clamps': 'Clamps (Mid + End)',
        'connectors_feet': 'Connectors & L-Feet',
        'pv_cables': 'PV Cables',
        'materials_subtotal': 'Materials Subtotal',
        'installation': 'Installation',
        'labor': 'Labor',
        'complexity_factor': 'Complexity Factor',
        'labor_subtotal': 'Labor Subtotal',
        'final_pricing': '💵 Final Pricing',
        'wholesale_price': '💼 Wholesale Price',
        'retail_price': '🏷️ Retail Price',
        'price_per_kw': 'Price per kW',
        'whats_included': '📋 What\'s Included',
        'all_sets_include': '✅ **All system sets include:** Complete equipment, materials, installation labor, and 1-year service warranty',
        'nav_simulation': '🔄 24-Hour Simulation',
        'nav_reports': '📊 Reports & Export',
        'nav_technician': '🔧 Technician Calculator',
        
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
        'total_devices': '📱 Total Devices',
        'daily_consumption': '🔋 Daily Consumption',
        'system_cost': '💰 System Cost',
        'self_sufficiency': '🎯 Self Sufficiency',
        
        # Devices
        'device_management': '📱 Device Management',
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
        'system_config': '⚙️ System Configuration',
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
        
        # Technician Calculator
        'tech_calc': '🔧 Technician Calculator',
        'tech_subtitle': 'Professional tools for electrical calculations and wire sizing',
        'ohms_law': '⚡ Ohm\'s Law Calculator',
        'wire_sizing': '📏 Wire Sizing Calculator',
        'voltage_drop': '📉 Voltage Drop Calculator',
        'power_calc': '💡 Power Calculator',
        'battery_calc': '🔋 Battery Calculator',
        'solar_calc': '☀️ Solar Array Calculator',
        'calculate': '🧮 Calculate',
        'result': '📊 Result',
        'voltage_v': 'Voltage (V)',
        'current_a': 'Current (A)',
        'power_w': 'Power (W)',
        'resistance_ohm': 'Resistance (Ω)',
        'wire_length': 'Wire Length (m)',
        'wire_gauge': 'Wire Gauge (AWG)',
        'max_current': 'Maximum Current (A)',
        'voltage_drop_percent': 'Voltage Drop (%)',
        'recommended_wire': 'Recommended Wire Size',
        'battery_capacity': 'Battery Capacity (Ah)',
        'discharge_time': 'Discharge Time (hours)',
        'dod': 'Depth of Discharge (%)',
        'panel_voltage': 'Panel Voltage (V)',
        'panel_current': 'Panel Current (A)',
        'num_panels': 'Number of Panels',
        'series_parallel': 'Series/Parallel Configuration',
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
        'step_configure_system': '⚙️ Configure System',
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
        'nav_devices': '📱 គ្រប់គ្រងឧបករណ៍',
        'nav_system': '⚙️ ការកំណត់រចនាសម្ព័ន្ធ',
        'nav_products': '📦 កាតាឡុកផលិតផល',
        'individual_products': '🛍️ ផលិតផលបុគ្គល',
        'complete_system_sets': '📦 សំណុំប្រព័ន្ធពេញលេញ',
        'filter_category': 'ច្រោះតាមប្រភេទ',
        'all_products': '🌐 ផលិតផលទាំងអស់',
        'solar_panels': '☀️ បន្ទះសូឡា',
        'inverters': '⚡ អ៊ីនវឺរទ័រ',
        'batteries': '🔋 ថ្ម',
        'water_pumps': '💧 ម៉ាស៊ីនបូមទឹក',
        'accessories': '🔧 គ្រឿងបន្លាស់ និងសម្ភារៈ',
        'total_products': 'ផលិតផលសរុប',
        'search': '🔍 ស្វែងរក',
        'showing_products': 'បង្ហាញផលិតផល {count}',
        'wholesale': 'តម្លៃលក់ដុំ',
        'retail': 'តម្លៃលក់រាយ',
        'product_details': '📋 ព័ត៌មានលម្អិត',
        'category': 'ប្រភេទ',
        'supplier': 'អ្នកផ្គត់ផ្គង់',
        'warranty': 'ការធានា',
        'years': 'ឆ្នាំ',
        'specifications': '⚙️ លក្ខណៈបច្ចេកទេស',
        'pricing': '💰 តម្លៃ',
        'pricing_note': '💡 **ចំណាំតម្លៃ:** តម្លៃលក់ដុំគឺជាតម្លៃមូលដ្ឋាន។ តម្លៃលក់រាយរួមបញ្ចូល 30% សម្រាប់សម្រង់អតិថិជន។',
        'ready_install_packages': '📦 កញ្ចប់ប្រព័ន្ធរួចរាល់ដំឡើង',
        'complete_solar_desc': 'សំណុំប្រព័ន្ធសូឡាពេញលេញជាមួយគ្រឿងបរិក្ខារ សម្ភារៈ និងការដំឡើង',
        'system_performance': '📊 ការអនុវត្តប្រព័ន្ធ',
        'daily_generation': 'ការផលិតប្រចាំថ្ងៃ',
        'backup_time': 'ពេលវេលាបម្រុងទុក',
        'recommended_load': 'ការប្រើប្រាស់ណែនាំ',
        'component_specs': '🔧 លក្ខណៈបច្ចេកទេសគ្រឿង',
        'model': 'ម៉ូដែល',
        'total_power': 'ថាមពលសរុប',
        'power_panel': 'ថាមពល/បន្ទះ',
        'efficiency': 'ប្រសិទ្ធភាព',
        'size': 'ទំហំ',
        'weight': 'ទម្ងន់',
        'area_needed': 'ទំហំតម្រូវការ',
        'power': 'ថាមពល',
        'type': 'ប្រភេទ',
        'max_pv_input': 'PV បញ្ចូលអតិបរមា',
        'mppt_trackers': 'MPPT Trackers',
        'max_charge': 'សាកអតិបរមា',
        'battery_voltage': 'វ៉ុលថ្ម',
        'phases': 'ដំណាក់កាល',
        'battery_storage': '🔋 ការផ្ទុកថ្ម',
        'capacity_unit': 'ចំណុះ/ឯកតា',
        'voltage': 'វ៉ុល',
        'cycle_life': 'អាយុកាលវដ្ត',
        'usable_energy': 'ថាមពលប្រើបាន',
        'complete_pricing': '💰 តម្លៃប្រព័ន្ធពេញលេញ',
        'detailed_breakdown': '📊 ការបែងចែកលម្អិត',
        'main_equipment': 'គ្រឿងបរិក្ខារសំខាន់',
        'equipment_subtotal': 'សរុបគ្រឿងបរិក្ខារ',
        'mounting_materials': 'សម្ភារៈដំឡើង',
        'rails': 'ផ្លូវរថភ្លើង',
        'clamps': 'តង្កៀប (កណ្តាល + ចុង)',
        'connectors_feet': 'ឧបករណ៍ភ្ជាប់ & L-Feet',
        'pv_cables': 'ខ្សែ PV',
        'materials_subtotal': 'សរុបសម្ភារៈ',
        'installation': 'ការដំឡើង',
        'labor': 'ការងារ',
        'complexity_factor': 'កត្តាស្មុគស្មាញ',
        'labor_subtotal': 'សរុបការងារ',
        'final_pricing': '💵 តម្លៃចុងក្រោយ',
        'wholesale_price': '💼 តម្លៃលក់ដុំ',
        'retail_price': '🏷️ តម្លៃលក់រាយ',
        'price_per_kw': 'តម្លៃក្នុងមួយ kW',
        'whats_included': '📋 អ្វីដែលរួមបញ្ចូល',
        'all_sets_include': '✅ **សំណុំទាំងអស់រួមបញ្ចូល:** គ្រឿងបរិក្ខារពេញលេញ សម្ភារៈ ការងារដំឡើង និងការធានា 1 ឆ្នាំ',
        'nav_simulation': '🔄 ការក្លែងធ្វើ 24 ម៉ោង',
        'nav_reports': '📊 របាយការណ៍ និងនាំចេញ',
        'nav_technician': '🔧 ម៉ាស៊ីនគណនាបច្ចេកទេស',
        
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
# Compact Sidebar Header with Logo (No Background)
if LOGO_BASE64:
    logo_html = f'<img src="data:image/png;base64,{LOGO_BASE64}" style="max-width: 120px; width: 100%; height: auto;">'
else:
    logo_html = '<div style="font-size: 1.8rem;"></div>'

st.sidebar.markdown(f"""
<div style='text-align: center; padding: 0.3rem 0; margin-bottom: 0.3rem;'>
    {logo_html}
    <div style='color: #667eea; font-size: 1rem; font-weight: 800; margin-top: 0.2rem;'>KHSolar</div>
</div>
""", unsafe_allow_html=True)

# VIP Status Display (Compact)
if st.session_state.vip_logged_in:
    st.sidebar.markdown(f"<div style='text-align: center; padding: 0.3rem; background: #f0fdf4; border-radius: 5px; margin-bottom: 0.5rem;'><span style='color: #15803d; font-weight: 600; font-size: 0.85rem;'>👑 {st.session_state.vip_username}</span></div>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout", use_container_width=True, key="logout_btn"):
        st.session_state.vip_logged_in = False
        st.session_state.is_vip = False
        st.session_state.vip_username = ''
        st.rerun()
elif st.session_state.is_vip:
    st.sidebar.markdown("<div style='text-align: center; padding: 0.3rem; background: #f0fdf4; border-radius: 5px; margin-bottom: 0.5rem;'><span style='color: #15803d; font-weight: 600; font-size: 0.85rem;'>👑 VIP</span></div>", unsafe_allow_html=True)
else:
    if st.sidebar.button("👑 VIP Login", use_container_width=True, type="primary", key="vip_login_btn"):
        st.session_state.show_vip_login = True
        st.rerun()

# Navigation Menu - Compact
if st.session_state.is_vip or st.session_state.vip_logged_in:
    page = st.sidebar.radio("📍 Navigate", [
        t('nav_dashboard'),
        t('nav_devices'),
        t('nav_system'),
        t('nav_products'),
        t('nav_simulation'),
        t('nav_reports'),
        t('nav_technician')
    ], label_visibility="collapsed")
else:
    page = st.sidebar.radio("📍 Navigate", [
        t('nav_dashboard'),
        t('nav_devices') + " 🔒",
        t('nav_system') + " 🔒",
        t('nav_products') + " 🔒",
        t('nav_simulation') + " 🔒",
        t('nav_reports') + " 🔒",
        t('nav_technician') + " 🔒"
    ], label_visibility="collapsed")
    
    # Check if user trying to access locked features - Show message
    if "🔒" in page:
        st.warning("🔒 **This feature is only available for VIP users.**")
        st.info("📞 Contact admin: **+855888836588** or **@chhanycls**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👑 Login as VIP", use_container_width=True, type="primary"):
                st.session_state.show_vip_login = True
                st.rerun()
        with col2:
            if st.button("← Back to Dashboard", use_container_width=True):
                st.rerun()
        
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

# VIP Login Popup Modal (Global - works on any page)
if st.session_state.show_vip_login:
    # Enhanced modal overlay with premium design
    st.markdown("""
    <style>
    /* Modal Overlay with blur effect */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(8px);
        z-index: 9998;
        animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Premium Modal Content */
    .vip-modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 0;
        border-radius: 20px;
        box-shadow: 0 25px 80px rgba(102, 126, 234, 0.4), 0 0 0 1px rgba(102, 126, 234, 0.1);
        z-index: 9999;
        max-width: 480px;
        width: 92%;
        animation: modalSlide 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        overflow: hidden;
    }
    
    /* Modal Header with gradient */
    .vip-modal-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .vip-modal-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    .vip-modal-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .vip-modal-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 0.95rem;
        margin-top: 0.5rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Modal Body */
    .vip-modal-body {
        padding: 2rem;
    }
    
    /* Close button */
    .modal-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
        z-index: 2;
    }
    
    .modal-close:hover {
        background: rgba(255,255,255,0.3);
        transform: rotate(90deg);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes modalSlide {
        from { 
            opacity: 0;
            transform: translate(-50%, -55%) scale(0.9);
        }
        to { 
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
    
    @keyframes shimmer {
        0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
        50% { transform: translate(-50%, -50%) rotate(180deg); }
    }
    
    /* Feature badges */
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.25rem;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin: 1rem 0;
    }
    
    .benefit-item {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: all 0.3s;
    }
    
    .benefit-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    .benefit-icon {
        font-size: 1.5rem;
        margin-bottom: 0.25rem;
    }
    
    .benefit-text {
        font-size: 0.8rem;
        color: #495057;
        font-weight: 600;
    }
    </style>
    <div class="modal-overlay"></div>
    <div class="vip-modal">
        <div class="vip-modal-header">
            <div class="vip-modal-title">👑 VIP Access</div>
            <div class="vip-modal-subtitle">Unlock Premium Solar Planning Features</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Modal body content
    st.markdown('<div class="vip-modal-body">', unsafe_allow_html=True)
    
    # VIP Benefits showcase
    st.markdown("""
    <div class="benefits-grid">
        <div class="benefit-item">
            <div class="benefit-icon">⚡</div>
            <div class="benefit-text">Advanced Simulation</div>
        </div>
        <div class="benefit-item">
            <div class="benefit-icon">📊</div>
            <div class="benefit-text">Detailed Reports</div>
        </div>
        <div class="benefit-item">
            <div class="benefit-icon">🛠️</div>
            <div class="benefit-text">Technician Tools</div>
        </div>
        <div class="benefit-item">
            <div class="benefit-icon">💾</div>
            <div class="benefit-text">Export Options</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login form
    username = st.text_input(
        "👤 Username", 
        placeholder="Enter your username", 
        key="vip_user_popup",
        help="Enter your VIP username"
    )
    password = st.text_input(
        "🔒 Password", 
        type="password", 
        placeholder="Enter your password", 
        key="vip_pass_popup",
        help="Enter your VIP password"
    )
    
    # Demo credentials (collapsible)
    with st.expander("🎯 Need Test Credentials?", expanded=False):
        st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;'>
            <strong>Demo Account:</strong><br>
            Username: <code>demo</code><br>
            Password: <code>demo123</code>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action buttons
    col_a, col_b = st.columns([2, 1])
    with col_a:
        if st.button("🔓 Login to VIP", type="primary", use_container_width=True):
            if username and password:
                if verify_vip_login(username, password):
                    st.session_state.vip_logged_in = True
                    st.session_state.is_vip = True
                    st.session_state.vip_username = username
                    st.session_state.show_vip_login = False
                    st.success(f"✅ Welcome back, {username}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
            else:
                st.warning("⚠️ Please enter both username and password")
    with col_b:
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_vip_login = False
            st.rerun()
    
    # Contact info
    st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #e9ecef;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 0.5rem; background: #f8f9fa; border-radius: 8px;'>
        <div style='font-size: 0.85rem; color: #6c757d; margin-bottom: 0.5rem;'>
            <strong>Need VIP Access?</strong>
        </div>
        <div style='font-size: 0.9rem;'>
            📞 <strong>+855 888 836 588</strong> | 
            💬 <strong>@chhanycls</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if page == t('nav_dashboard'):
    
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
elif page == t('nav_products'):
    st.title("📦 Product Catalog & System Sets")
    st.markdown("#### Complete product pricing with specifications and ready-to-install system packages")
    
    pm = st.session_state.product_manager
    
    # Initialize session state for pricing control
    if 'price_markup' not in st.session_state:
        st.session_state.price_markup = 30.0
    if 'hide_wholesale' not in st.session_state:
        st.session_state.hide_wholesale = False
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    if 'show_admin_panel' not in st.session_state:
        st.session_state.show_admin_panel = False
    
    # ========== PRICING CONTROL PANEL (PASSWORD PROTECTED) ==========
    # Admin panel toggle button (clean, no header)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn1:
        if st.button("🔐 Admin Pricing Control" if not st.session_state.show_admin_panel else "✖️ Close Admin Panel", 
                     use_container_width=True, 
                     type="primary" if not st.session_state.show_admin_panel else "secondary"):
            st.session_state.show_admin_panel = not st.session_state.show_admin_panel
            if not st.session_state.show_admin_panel:
                st.session_state.admin_authenticated = False
    
    # Show admin panel if toggled
    if st.session_state.show_admin_panel:
        if not st.session_state.admin_authenticated:
            # Password authentication using popup dialog
            @st.dialog("🔒 Admin Authentication")
            def password_dialog():
                st.markdown("**Enter admin password to access pricing controls**")
                admin_password = st.text_input("🔑 Password", type="password", key="admin_pwd_popup")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔓 Unlock", use_container_width=True, type="primary"):
                        if admin_password == "admin123":
                            st.session_state.admin_authenticated = True
                            st.success("✅ Access granted!")
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password")
                with col2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state.show_admin_panel = False
                        st.rerun()
            
            password_dialog()
        else:
            # Admin controls (authenticated)
            st.markdown("""
            <div style='background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); 
                        padding: 1rem; border-radius: 8px; margin: 1rem 0;
                        border-left: 4px solid #10b981;'>
                <p style='margin: 0; color: #065f46; font-weight: 600;'>
                    ✅ Admin Access Granted - Pricing Controls Active
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Simple and clean control layout
            ctrl_col1, ctrl_col2 = st.columns(2)
            
            with ctrl_col1:
                st.markdown("#### 💰 Markup Control")
                markup_percentage = st.slider(
                    "Retail Markup (%)",
                    min_value=0,
                    max_value=100,
                    value=int(st.session_state.price_markup),
                    step=5,
                    help="Adjust retail price markup percentage"
                )
                st.session_state.price_markup = float(markup_percentage)
                
                # Show example
                example_cost = 1000.00
                example_retail = example_cost * (1 + markup_percentage / 100)
                st.info(f"**Example:** ${example_cost:,.0f} → ${example_retail:,.0f} (+{markup_percentage}%)")
            
            with ctrl_col2:
                st.markdown("#### 🔒 Display Settings")
                hide_wholesale = st.toggle(
                    "Hide Wholesale Prices from Customers",
                    value=st.session_state.hide_wholesale,
                    help="When enabled, customers only see retail prices"
                )
                st.session_state.hide_wholesale = hide_wholesale
                
                # Show status
                if hide_wholesale:
                    st.warning("🚫 **Wholesale prices are HIDDEN**")
                else:
                    st.success("✅ **Wholesale prices are VISIBLE**")
            
            # Quick stats
            st.markdown("---")
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Current Markup", f"{markup_percentage}%", delta=f"{markup_percentage-30}%" if markup_percentage != 30 else "Default")
            with stat_col2:
                st.metric("Wholesale Display", "Hidden" if hide_wholesale else "Visible")
            with stat_col3:
                if st.button("🔄 Reset to Default", use_container_width=True):
                    st.session_state.price_markup = 30.0
                    st.session_state.hide_wholesale = False
                    st.success("✅ Reset to default settings!")
                    st.rerun()
    
    # Main tabs for Products, System Sets, and Water Pump Sets
    main_tab1, main_tab2, main_tab3 = st.tabs([t('individual_products'), t('complete_system_sets'), "💧 Water Pump Sets"])
    
    # ========== TAB 1: INDIVIDUAL PRODUCTS ==========
    with main_tab1:
        # Category filter with icons
        category_map = {
            "All": t('all_products'),
            "solar_panel": t('solar_panels'),
            "inverter": t('inverters'),
            "battery": t('batteries'),
            "water_pump": t('water_pumps'),
            "accessories": t('accessories')
        }
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            category = st.selectbox(t('filter_category'), 
                                   list(category_map.keys()),
                                   format_func=lambda x: category_map[x])
        with col2:
            st.metric(t('total_products'), len(pm.products))
        with col3:
            search = st.text_input(t('search'), placeholder="Product name...")
        
        # Filter products
        if category == "All":
            products = list(pm.products.values())
        else:
            products = pm.get_products_by_category(category)
        
        # Apply search filter
        if search:
            products = [p for p in products if search.lower() in p.name.lower()]
        
        st.markdown(f"### {t('showing_products').format(count=len(products))}")
        
        # Product image mapping (real product images)
        product_images = {
            # Deye Inverters
            "Deye Hybrid 5kw EU 1P": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye Hybrid 8kw EU 1P": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 16kw EP 1P": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 10kw eu 1P Low Voltage": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 10kw eu 3P Low Voltage": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 12kw eu 3P Low Voltage": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 20kw eu 3P Low Voltage": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 20kw eu 3P High Voltage": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 30kw eu 3p": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 40kw eu 3p": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            "Deye 50kw eu 3p": "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg",
            
            # Solar Panels
            "Lvtopsun 340W": "https://m.media-amazon.com/images/I/61qL8ZxGvEL._AC_SL1500_.jpg",
            "Lvtopsun 550W": "https://m.media-amazon.com/images/I/61qL8ZxGvEL._AC_SL1500_.jpg",
            "Lvtopsun 620W": "https://m.media-amazon.com/images/I/61qL8ZxGvEL._AC_SL1500_.jpg",
            "LONGi Panel 360w": "https://m.media-amazon.com/images/I/71KqVH8XJNL._AC_SL1500_.jpg",
            "LONGi Panel 585w": "https://m.media-amazon.com/images/I/71KqVH8XJNL._AC_SL1500_.jpg",
            
            # Batteries
            "DEYE 100AH 51.2v (5.12KWH)": "https://m.media-amazon.com/images/I/61J8vZ9HPNL._AC_SL1500_.jpg",
            "DEYE Battery Controller": "https://m.media-amazon.com/images/I/61J8vZ9HPNL._AC_SL1500_.jpg",
            "LVtopsun-51.2V100AH Lithium": "https://m.media-amazon.com/images/I/61J8vZ9HPNL._AC_SL1500_.jpg",
            "LVtopsun-51.2V200AH Lithium": "https://m.media-amazon.com/images/I/61J8vZ9HPNL._AC_SL1500_.jpg",
            "LVtopsun-51.2V300AH Lithium": "https://m.media-amazon.com/images/I/61J8vZ9HPNL._AC_SL1500_.jpg",
            "LVtopsun-51.2V100AH Lithium HV": "https://m.media-amazon.com/images/I/61J8vZ9HPNL._AC_SL1500_.jpg",
            "LV 100AH 12V GEL": "https://m.media-amazon.com/images/I/71qYMXqVBOL._AC_SL1500_.jpg",
            "LV 150AH 12V GEL BATTERY": "https://m.media-amazon.com/images/I/71qYMXqVBOL._AC_SL1500_.jpg",
            "LV 200AH 12V GEL BATTERY": "https://m.media-amazon.com/images/I/71qYMXqVBOL._AC_SL1500_.jpg",
            "LV 250AH 12V GEL BATTERY": "https://m.media-amazon.com/images/I/71qYMXqVBOL._AC_SL1500_.jpg",
            
            # Sungrow Inverters
            "Sungrow SG33CX-P2": "https://m.media-amazon.com/images/I/61-8zXqXqBL._AC_SL1500_.jpg",
            "Sungrow SG40CX-P2": "https://m.media-amazon.com/images/I/61-8zXqXqBL._AC_SL1500_.jpg",
            "Sungrow SG50CX-P2": "https://m.media-amazon.com/images/I/61-8zXqXqBL._AC_SL1500_.jpg",
            "Sungrow SG125CX-P2": "https://m.media-amazon.com/images/I/61-8zXqXqBL._AC_SL1500_.jpg",
            "Sungrow SG150CX": "https://m.media-amazon.com/images/I/61-8zXqXqBL._AC_SL1500_.jpg",
            "Sungrow 250KW": "https://m.media-amazon.com/images/I/61-8zXqXqBL._AC_SL1500_.jpg",
            
            # Solis Inverters
            "Solis Ongrid Inverter 5kw": "https://m.media-amazon.com/images/I/61kZxH8XJNL._AC_SL1500_.jpg",
            "Solis Ongrid Inverter 10kw": "https://m.media-amazon.com/images/I/61kZxH8XJNL._AC_SL1500_.jpg",
            "Solis Ongrid Inverter 20kw": "https://m.media-amazon.com/images/I/61kZxH8XJNL._AC_SL1500_.jpg",
            "Solis Ongrid Inverter 40kw": "https://m.media-amazon.com/images/I/61kZxH8XJNL._AC_SL1500_.jpg",
            
            # Water Pumps
            "3DPC5.2-50-48-600W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "4DPC9-45-110-750W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "3DPC6-84-110-1100W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "4DPC9-85-110-1500W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "4DSC19-60-300-2200W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "4DSC19-98-380/550-3000W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "4DSC19-135-380/550-4000W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "DCPM21-14-72-750W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "DCPM50-17-110-1500W": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            "DCPM60-20-300-2200W-A/D": "https://m.media-amazon.com/images/I/61xqL8ZxGvEL._AC_SL1500_.jpg",
            
            # Accessories
            "Rail 4.8m": "https://m.media-amazon.com/images/I/71KqVH8XJNL._AC_SL1000_.jpg",
            "Mid clamp": "https://m.media-amazon.com/images/I/61KqVH8XJNL._AC_SL1000_.jpg",
            "End Clamp": "https://m.media-amazon.com/images/I/61KqVH8XJNL._AC_SL1000_.jpg",
            "LV 4mm PV CABLE 100M": "https://m.media-amazon.com/images/I/71xqL8ZxGvEL._AC_SL1000_.jpg",
            "LV 6mm PV CABLE 100M": "https://m.media-amazon.com/images/I/71xqL8ZxGvEL._AC_SL1000_.jpg",
        }
        
        # Display products in enhanced cards
        for p in products:
            # Determine category icon
            cat_icon = "☀️" if "panel" in p.category.lower() else \
                      "⚡" if "inverter" in p.category.lower() else \
                      "🔋" if "battery" in p.category.lower() else \
                      "💧" if "pump" in p.category.lower() else "🔧"
            
            customer_price = p.cost * 1.3
            
            # Apply markup from control panel
            customer_price = p.cost * (1 + st.session_state.price_markup / 100)
            
            # Create expander title based on wholesale visibility
            if st.session_state.hide_wholesale:
                expander_title = f"{cat_icon} {p.name} | {t('retail')}: ${customer_price:,.2f}"
            else:
                expander_title = f"{cat_icon} {p.name} | {t('wholesale')}: ${p.cost:,.2f} | {t('retail')}: ${customer_price:,.2f}"
            
            with st.expander(expander_title):
                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                
                with col1:
                    # Display product image using HTML img tag for better compatibility
                    product_img = product_images.get(p.name, "https://via.placeholder.com/300x300.png?text=No+Image")
                    st.markdown(f"""
                    <div style='text-align: center;'>
                        <img src='{product_img}' style='max-width: 250px; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);' onerror="this.src='https://via.placeholder.com/300x300.png?text=No+Image'">
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #6366f1;'>
                        <h4 style='margin: 0 0 0.5rem 0; color: #4338ca;'>{t('product_details')}</h4>
                        <p style='margin: 0.3rem 0;'><b>{t('category')}:</b> {cat_icon} {p.category.replace('_', ' ').title()}</p>
                        <p style='margin: 0.3rem 0;'><b>{t('supplier')}:</b> {p.supplier}</p>
                        <p style='margin: 0.3rem 0;'><b>{t('warranty')}:</b> {p.warranty_years} {t('years')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if p.notes:
                        st.info(f"ℹ️ {p.notes}")
                
                with col3:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;'>
                        <h4 style='margin: 0 0 0.5rem 0; color: #1e3a8a;'>{t('specifications')}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if p.specifications:
                        for key, value in p.specifications.items():
                            st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
                    else:
                        st.write("• Standard specifications")
                    
                    # Add area calculation for solar panels
                    if "panel" in p.category.lower():
                        st.markdown("---")
                        st.info(f"📐 **Area per panel:** ~2.6 m²")
                
                with col4:
                    # Show pricing based on visibility settings
                    if st.session_state.hide_wholesale:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); 
                                    padding: 1rem; border-radius: 8px; border-left: 4px solid #ec4899; text-align: center;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #9f1239;'>{t('pricing')}</h4>
                            <p style='margin: 0.3rem 0; font-size: 0.9rem;'><b>Price:</b></p>
                            <p style='margin: 0; font-size: 1.6rem; color: #be185d; font-weight: 700;'>${customer_price:,.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); 
                                    padding: 1rem; border-radius: 8px; border-left: 4px solid #ec4899; text-align: center;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #9f1239;'>{t('pricing')}</h4>
                            <p style='margin: 0.3rem 0; font-size: 0.9rem;'><b>{t('wholesale')}:</b></p>
                            <p style='margin: 0; font-size: 1.2rem; color: #9f1239; font-weight: 600;'>${p.cost:,.2f}</p>
                            <hr style='margin: 0.5rem 0; border: 1px solid #ec4899;'>
                            <p style='margin: 0.3rem 0; font-size: 0.9rem;'><b>{t('retail')} (+{st.session_state.price_markup:.0f}%):</b></p>
                            <p style='margin: 0; font-size: 1.4rem; color: #be185d; font-weight: 700;'>${customer_price:,.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info(t('pricing_note'))
    
    # ========== TAB 2: COMPLETE SYSTEM SETS ==========
    with main_tab2:
        st.markdown("### 📦 Ready-to-Install System Packages")
        st.markdown("Complete solar system sets with all components, materials, and installation")
        
        # Define system sets with detailed specifications based on inverter capacity
        # Calculation logic: PV = Inverter × 1.1-1.2, Battery = Inverter × 2 (for backup)
        system_sets = [
            {
                "name": "5kW Hybrid Solar System",
                "inverter": "Deye Hybrid 5kw EU 1P",
                "inverter_power": 5.0,
                "inverter_specs": {
                    "max_pv_input": "6.5kW",
                    "mppt_trackers": "2",
                    "max_charge_current": "135A",
                    "battery_voltage": "48V",
                    "efficiency": "97.6%",
                    "phases": "Single Phase"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 10, "total_kw": 5.5},
                "panel_specs": {
                    "power": "550W",
                    "efficiency": "21.2%",
                    "voltage_vmp": "41.8V",
                    "current_imp": "13.16A",
                    "dimensions": "2278×1134×35mm",
                    "weight": "27.5kg"
                },
                "battery": {"name": "DEYE 100AH 51.2v (5.12KWH)", "quantity": 1, "total_kwh": 5.12},
                "battery_specs": {
                    "capacity": "100Ah / 5.12kWh",
                    "voltage": "51.2V",
                    "type": "LiFePO4",
                    "cycle_life": "6000+ cycles",
                    "dod": "90%",
                    "dimensions": "483×420×177mm"
                },
                "description": "Perfect for small homes and offices (Daily consumption: 15-20 kWh)",
                "daily_generation": "22-27.5 kWh",
                "backup_time": "8-12 hours",
                "recommended_load": "15-20 kWh/day",
                "icon": "🏠",
                "image_url": "https://www.deyeinverter.com/upload/image/20210901/5kw-hybrid-inverter.jpg"
            },
            {
                "name": "8kW Hybrid Solar System",
                "inverter": "Deye Hybrid 8kw EU 1P",
                "inverter_power": 8.0,
                "inverter_specs": {
                    "max_pv_input": "10.4kW",
                    "mppt_trackers": "2",
                    "max_charge_current": "190A",
                    "battery_voltage": "48V",
                    "efficiency": "97.6%",
                    "phases": "Single Phase"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 16, "total_kw": 8.8},
                "panel_specs": {
                    "power": "550W",
                    "efficiency": "21.2%",
                    "voltage_vmp": "41.8V",
                    "current_imp": "13.16A",
                    "dimensions": "2278×1134×35mm",
                    "weight": "27.5kg"
                },
                "battery": {"name": "DEYE 100AH 51.2v (5.12KWH)", "quantity": 1, "total_kwh": 5.12},
                "battery_specs": {
                    "capacity": "100Ah / 5.12kWh",
                    "voltage": "51.2V",
                    "type": "LiFePO4",
                    "cycle_life": "6000+ cycles",
                    "dod": "90%",
                    "dimensions": "483×420×177mm"
                },
                "description": "Ideal for medium-sized homes (Daily consumption: 25-32 kWh)",
                "daily_generation": "35-44 kWh",
                "backup_time": "10-14 hours",
                "recommended_load": "25-32 kWh/day",
                "icon": "🏡",
                "image_url": "https://www.deyeinverter.com/upload/image/20210901/8kw-hybrid-inverter.jpg"
            },
            {
                "name": "10kW Hybrid Solar System",
                "inverter": "Deye 10kw eu 1P Low Voltage",
                "inverter_power": 10.0,
                "inverter_specs": {
                    "max_pv_input": "13kW",
                    "mppt_trackers": "2",
                    "max_charge_current": "210A",
                    "battery_voltage": "48V",
                    "efficiency": "97.6%",
                    "phases": "Single Phase"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 20, "total_kw": 11.0},
                "panel_specs": {
                    "power": "550W",
                    "efficiency": "21.2%",
                    "voltage_vmp": "41.8V",
                    "current_imp": "13.16A",
                    "dimensions": "2278×1134×35mm",
                    "weight": "27.5kg"
                },
                "battery": {"name": "DEYE 100AH 51.2v (5.12KWH)", "quantity": 1, "total_kwh": 5.12},
                "battery_specs": {
                    "capacity": "100Ah / 5.12kWh",
                    "voltage": "51.2V",
                    "type": "LiFePO4",
                    "cycle_life": "6000+ cycles",
                    "dod": "90%",
                    "dimensions": "483×420×177mm"
                },
                "description": "Great for large homes and small businesses (Daily consumption: 30-40 kWh)",
                "daily_generation": "44-55 kWh",
                "backup_time": "12-16 hours",
                "recommended_load": "30-40 kWh/day",
                "icon": "🏢",
                "image_url": "https://www.deyeinverter.com/upload/image/20210901/10kw-hybrid-inverter.jpg"
            },
            {
                "name": "20kW Commercial Solar System",
                "inverter": "Deye 20kw eu 3P Low Voltage",
                "inverter_power": 20.0,
                "inverter_specs": {
                    "max_pv_input": "26kW",
                    "mppt_trackers": "2",
                    "max_charge_current": "210A",
                    "battery_voltage": "48V",
                    "efficiency": "97.8%",
                    "phases": "Three Phase"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 40, "total_kw": 22.0},
                "panel_specs": {
                    "power": "550W",
                    "efficiency": "21.2%",
                    "voltage_vmp": "41.8V",
                    "current_imp": "13.16A",
                    "dimensions": "2278×1134×35mm",
                    "weight": "27.5kg"
                },
                "battery": {"name": "DEYE 100AH 51.2v (5.12KWH)", "quantity": 1, "total_kwh": 5.12},
                "battery_specs": {
                    "capacity": "100Ah / 5.12kWh",
                    "voltage": "51.2V",
                    "type": "LiFePO4",
                    "cycle_life": "6000+ cycles",
                    "dod": "90%",
                    "dimensions": "483×420×177mm"
                },
                "description": "Perfect for commercial buildings (Daily consumption: 60-80 kWh)",
                "daily_generation": "88-110 kWh",
                "backup_time": "10-14 hours",
                "recommended_load": "60-80 kWh/day",
                "icon": "🏭",
                "image_url": "https://www.deyeinverter.com/upload/image/20210901/20kw-hybrid-inverter.jpg"
            },
            {
                "name": "30kW Industrial Solar System",
                "inverter": "Deye 30kw eu 3p",
                "inverter_power": 30.0,
                "inverter_specs": {
                    "max_pv_input": "39kW",
                    "mppt_trackers": "2",
                    "max_charge_current": "210A",
                    "battery_voltage": "48V",
                    "efficiency": "97.8%",
                    "phases": "Three Phase"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 60, "total_kw": 33.0},
                "panel_specs": {
                    "power": "550W",
                    "efficiency": "21.2%",
                    "voltage_vmp": "41.8V",
                    "current_imp": "13.16A",
                    "dimensions": "2278×1134×35mm",
                    "weight": "27.5kg"
                },
                "battery": {"name": "DEYE 100AH 51.2v (5.12KWH)", "quantity": 1, "total_kwh": 5.12},
                "battery_specs": {
                    "capacity": "100Ah / 5.12kWh",
                    "voltage": "51.2V",
                    "type": "LiFePO4",
                    "cycle_life": "6000+ cycles",
                    "dod": "90%",
                    "dimensions": "483×420×177mm"
                },
                "description": "Industrial-grade power solution (Daily consumption: 90-120 kWh)",
                "daily_generation": "132-165 kWh",
                "backup_time": "12-16 hours",
                "recommended_load": "90-120 kWh/day",
                "icon": "🏗️",
                "image_url": "https://www.deyeinverter.com/upload/image/20210901/30kw-hybrid-inverter.jpg"
            }
        ]
        
        # Display each system set
        for sys_set in system_sets:
            with st.expander(f"{sys_set['icon']} {sys_set['name']} - {sys_set['inverter_power']}kW"):
                # Display system image
                img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
                with img_col2:
                    inverter_img = product_images.get(sys_set['inverter'], "https://m.media-amazon.com/images/I/61VH9YqVZlL._AC_SL1500_.jpg")
                    st.image(inverter_img, caption=f"{sys_set['inverter']} - Main System Component", width=400)
                
                st.markdown(f"**{sys_set['description']}**")
                st.markdown("---")
                
                # Performance Summary Card
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                            padding: 1.2rem; border-radius: 10px; border-left: 4px solid #10b981; margin-bottom: 1rem;'>
                    <h3 style='margin: 0 0 0.8rem 0; color: #065f46;'>📊 System Performance</h3>
                    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
                        <div style='text-align: center;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #065f46;'><b>Daily Generation</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #047857; font-weight: 700;'>{sys_set['daily_generation']}</p>
                        </div>
                        <div style='text-align: center; border-left: 2px solid #10b981; border-right: 2px solid #10b981;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #065f46;'><b>Backup Time</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #047857; font-weight: 700;'>{sys_set['backup_time']}</p>
                        </div>
                        <div style='text-align: center;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #065f46;'><b>Recommended Load</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #047857; font-weight: 700;'>{sys_set['recommended_load']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed Component Specifications
                st.markdown("### 🔧 Component Specifications")
                
                spec_col1, spec_col2, spec_col3 = st.columns(3)
                
                with spec_col1:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #92400e;'>☀️ Solar Panels</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Model:</b> {sys_set['solar_panels']['name']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Quantity:</b> {sys_set['solar_panels']['quantity']} panels</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Total Power:</b> {sys_set['solar_panels']['total_kw']} kW</p>
                        <hr style='margin: 0.5rem 0; border: 1px solid #f59e0b;'>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Power/Panel:</b> {sys_set['panel_specs']['power']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Efficiency:</b> {sys_set['panel_specs']['efficiency']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Vmp:</b> {sys_set['panel_specs']['voltage_vmp']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Imp:</b> {sys_set['panel_specs']['current_imp']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Size:</b> {sys_set['panel_specs']['dimensions']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Weight:</b> {sys_set['panel_specs']['weight']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Area Needed:</b> ~{sys_set['solar_panels']['quantity'] * 2.6:.1f} m²</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with spec_col2:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #6366f1;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #4338ca;'>⚡ Inverter</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Model:</b> {sys_set['inverter']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Power:</b> {sys_set['inverter_power']} kW</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Type:</b> Hybrid (Grid-Tied + Off-Grid)</p>
                        <hr style='margin: 0.5rem 0; border: 1px solid #6366f1;'>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Max PV Input:</b> {sys_set['inverter_specs']['max_pv_input']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>MPPT Trackers:</b> {sys_set['inverter_specs']['mppt_trackers']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Max Charge:</b> {sys_set['inverter_specs']['max_charge_current']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Battery Voltage:</b> {sys_set['inverter_specs']['battery_voltage']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Efficiency:</b> {sys_set['inverter_specs']['efficiency']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Phases:</b> {sys_set['inverter_specs']['phases']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with spec_col3:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #1e40af;'>🔋 Battery Storage</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Model:</b> {sys_set['battery']['name']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Quantity:</b> {sys_set['battery']['quantity']} units</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Total:</b> {sys_set['battery']['total_kwh']:.2f} kWh</p>
                        <hr style='margin: 0.5rem 0; border: 1px solid #3b82f6;'>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Capacity/Unit:</b> {sys_set['battery_specs']['capacity']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Voltage:</b> {sys_set['battery_specs']['voltage']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Type:</b> {sys_set['battery_specs']['type']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Cycle Life:</b> {sys_set['battery_specs']['cycle_life']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>DoD:</b> {sys_set['battery_specs']['dod']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Size:</b> {sys_set['battery_specs']['dimensions']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.8rem;'><b>Usable Energy:</b> {sys_set['battery']['total_kwh'] * 0.9:.2f} kWh</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Calculate pricing
                # Get product prices - search by exact name match
                inverter_price = 0
                for prod_name, prod in pm.products.items():
                    if prod_name == sys_set['inverter']:
                        inverter_price = prod.cost
                        break
                
                # Fallback prices based on inverter model
                if inverter_price == 0:
                    inverter_prices = {
                        "Deye Hybrid 5kw EU 1P": 888.00,
                        "Deye Hybrid 8kw EU 1P": 1320.00,
                        "Deye 10kw eu 1P Low Voltage": 1800.00,
                        "Deye 20kw eu 3P Low Voltage": 3096.00,
                        "Deye 30kw eu 3p": 4080.00
                    }
                    inverter_price = inverter_prices.get(sys_set['inverter'], 888.00)
                
                panel_product = pm.products.get(sys_set['solar_panels']['name'])
                panel_price = panel_product.cost if panel_product else 66
                
                battery_product = pm.products.get(sys_set['battery']['name'])
                battery_price = battery_product.cost if battery_product else 1440
                
                # Improved calculation for materials and labor based on system size
                panel_qty = sys_set['solar_panels']['quantity']
                
                # Calculate mounting materials (more accurate) + 20% markup
                rails_needed = panel_qty * 0.5  # 2 panels per 4.8m rail
                base_materials_cost = (
                    (rails_needed * 19.20) +  # Rails
                    (panel_qty * 2 * 0.60) +  # Mid clamps (2 per panel)
                    (panel_qty * 0.60) +  # End clamps
                    ((rails_needed - 1) * 0.84) +  # Rail connectors
                    (panel_qty * 4 * 1.32) +  # L feet (4 per panel)
                    (panel_qty * 6 * 64.80 / 100)  # PV cables (6m per panel average)
                )
                materials_cost = base_materials_cost * 1.20  # Add 20% markup
                
                # Labor cost calculation based on system complexity + 20% markup
                # Base: $80/kW + complexity factor
                base_labor = sys_set['inverter_power'] * 80
                complexity_factor = 1.0 + (0.05 * (panel_qty // 10))  # 5% more per 10 panels
                labor_cost = (base_labor * complexity_factor) * 1.20  # Add 20% markup
                
                equipment_total = (inverter_price + 
                                 (panel_price * panel_qty) + 
                                 (battery_price * sys_set['battery']['quantity']))
                
                wholesale_total = equipment_total + materials_cost + labor_cost
                retail_total = wholesale_total * (1 + st.session_state.price_markup / 100)
                
                # Pricing breakdown
                if st.session_state.hide_wholesale:
                    st.markdown("### 💰 System Pricing")
                else:
                    st.markdown("### 💰 Complete System Pricing")
                
                price_col1, price_col2 = st.columns(2)
                
                with price_col1:
                    # Only show breakdown if wholesale is visible
                    if not st.session_state.hide_wholesale:
                        # Calculate individual material costs for display (with 20% markup)
                        rails_cost = (rails_needed * 19.20) * 1.20
                        clamps_cost = ((panel_qty * 2 * 0.60) + (panel_qty * 0.60)) * 1.20
                        connectors_cost = ((rails_needed - 1) * 0.84) * 1.20
                        lfeet_cost = (panel_qty * 4 * 1.32) * 1.20
                        cables_cost = (panel_qty * 6 * 64.80 / 100) * 1.20
                        
                        st.markdown("#### 📊 Detailed Cost Breakdown")
                        
                        # Main Equipment
                        st.markdown("**Main Equipment**")
                        st.write(f"⚡ Inverter (1x): ${inverter_price:,.2f}")
                        st.write(f"☀️ Solar Panels ({panel_qty}x): ${panel_price * panel_qty:,.2f}")
                        st.write(f"🔋 Battery ({sys_set['battery']['quantity']}x): ${battery_price * sys_set['battery']['quantity']:,.2f}")
                        st.markdown(f"**Equipment Subtotal: ${equipment_total:,.2f}**")
                        
                        st.markdown("---")
                        
                        # Mounting & Materials (with 20% markup)
                        st.markdown("**Mounting & Materials (+20%)**")
                        st.write(f"Rails ({rails_needed:.0f}x 4.8m): ${rails_cost:,.2f}")
                        st.write(f"Clamps (Mid + End): ${clamps_cost:,.2f}")
                        st.write(f"Connectors & L-Feet: ${connectors_cost + lfeet_cost:,.2f}")
                        st.write(f"PV Cables (~{panel_qty * 6}m): ${cables_cost:,.2f}")
                        st.markdown(f"**Materials Subtotal: ${materials_cost:,.2f}**")
                        
                        st.markdown("---")
                        
                        # Installation (with 20% markup)
                        st.markdown("**Installation (+20%)**")
                        base_labor_raw = base_labor / 1.20
                        st.write(f"👷 Base Labor ({sys_set['inverter_power']}kW × $80): ${base_labor_raw:,.2f}")
                        st.write(f"Complexity (+{(complexity_factor-1)*100:.0f}%): ${base_labor_raw * (complexity_factor - 1):,.2f}")
                        st.write(f"Markup (+20%): ${(base_labor * complexity_factor) * 0.20:,.2f}")
                        st.markdown(f"**Labor Subtotal: ${labor_cost:,.2f}**")
                    else:
                        # Show simplified info when wholesale is hidden
                        st.markdown("#### 📦 System Includes")
                        st.write(f"⚡ {sys_set['inverter']} Inverter")
                        st.write(f"☀️ {panel_qty}x {sys_set['solar_panels']['name']}")
                        st.write(f"🔋 {sys_set['battery']['quantity']}x {sys_set['battery']['name']}")
                        st.write(f"🔧 Complete mounting & materials")
                        st.write(f"👷 Professional installation")
                        st.write(f"📐 Area needed: ~{panel_qty * 2.6:.1f} m²")
                
                with price_col2:
                    # Apply pricing control settings
                    if st.session_state.hide_wholesale:
                        # Show only retail price
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); 
                                    padding: 1.2rem; border-radius: 10px; border-left: 4px solid #ec4899; text-align: center;'>
                            <h4 style='margin: 0 0 0.8rem 0; color: #9f1239;'>💵 System Price</h4>
                            <p style='margin: 0; font-size: 2.2rem; color: #be185d; font-weight: 700;'>${retail_total:,.2f}</p>
                            <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #9f1239;'>
                                <b>Price per kW:</b> ${retail_total / sys_set['inverter_power']:,.2f}/kW
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Show both wholesale and retail
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); 
                                    padding: 1.2rem; border-radius: 10px; border-left: 4px solid #ec4899;'>
                            <h4 style='margin: 0 0 0.8rem 0; color: #9f1239;'>💵 Final Pricing</h4>
                            <div style='margin: 1rem 0;'>
                                <p style='margin: 0.3rem 0; font-size: 0.95rem;'><b>💼 Wholesale Price:</b></p>
                                <p style='margin: 0; font-size: 1.5rem; color: #9f1239; font-weight: 600;'>${wholesale_total:,.2f}</p>
                            </div>
                            <hr style='margin: 1rem 0; border: 2px solid #ec4899;'>
                            <div style='margin: 1rem 0;'>
                                <p style='margin: 0.3rem 0; font-size: 0.95rem;'><b>🏷️ Retail Price (+{st.session_state.price_markup:.0f}%):</b></p>
                                <p style='margin: 0; font-size: 1.8rem; color: #be185d; font-weight: 700;'>${retail_total:,.2f}</p>
                            </div>
                            <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #9f1239;'>
                                <b>Price per kW:</b> ${retail_total / sys_set['inverter_power']:,.2f}/kW
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Installation notes
                st.markdown("---")
                st.info(f"""
                **📋 What's Included:**
                • {sys_set['solar_panels']['quantity']}x {sys_set['solar_panels']['name']} solar panels
                • 1x {sys_set['inverter']} hybrid inverter
                • {sys_set['battery']['quantity']}x {sys_set['battery']['name']} battery units
                • Complete mounting system (rails, clamps, connectors)
                • PV cables and electrical accessories
                • Professional installation and commissioning
                • System testing and warranty activation
                """)
        
        st.markdown("---")
        st.success("✅ **All system sets include:** Complete equipment, materials, installation labor, and 1-year service warranty")
    
    # ========== TAB 3: WATER PUMP SETS ==========
    with main_tab3:
        st.markdown("### 💧 Solar Water Pump System Sets")
        st.markdown("Complete solar-powered water pumping systems with panels, controller, and installation")
        
        # Water pump system configurations - ALL MODELS
        pump_sets = [
            {
                "name": "600W Solar Water Pump System (3DPC)",
                "hp": 0.8,
                "pump_model": "3DPC5.2-50-48-600W",
                "pump_power": 600,
                "pump_specs": {
                    "power": "600W (0.8 HP)",
                    "voltage": "48V DC",
                    "max_flow": "5.2 m³/h",
                    "max_head": "50m",
                    "outlet": "1.5 inch"
                },
                "solar_panels": {"name": "Lvtopsun 340W", "quantity": 2, "total_kw": 0.68},
                "controller": "MPPT Solar Pump Controller 48V",
                "description": "Perfect for small farms and home gardens",
                "applications": "Irrigation, livestock watering, domestic use",
                "daily_water": "20-30 m³/day",
                "icon": "🏡"
            },
            {
                "name": "750W Solar Water Pump System (4DPC)",
                "hp": 1,
                "pump_model": "4DPC9-45-110-750W",
                "pump_power": 750,
                "pump_specs": {
                    "power": "750W (1 HP)",
                    "voltage": "110V DC",
                    "max_flow": "9 m³/h",
                    "max_head": "45m",
                    "outlet": "2 inch"
                },
                "solar_panels": {"name": "Lvtopsun 340W", "quantity": 3, "total_kw": 1.02},
                "controller": "MPPT Solar Pump Controller 110V",
                "description": "Ideal for small to medium farms",
                "applications": "Farm irrigation, garden watering",
                "daily_water": "35-45 m³/day",
                "icon": "🌱"
            },
            {
                "name": "750W Solar Water Pump System (DCPM)",
                "hp": 1,
                "pump_model": "DCPM21-14-72-750W",
                "pump_power": 750,
                "pump_specs": {
                    "power": "750W (1 HP)",
                    "voltage": "72V DC",
                    "max_flow": "21 m³/h",
                    "max_head": "14m",
                    "outlet": "2 inch"
                },
                "solar_panels": {"name": "Lvtopsun 340W", "quantity": 3, "total_kw": 1.02},
                "controller": "MPPT Solar Pump Controller 72V",
                "description": "High flow for shallow wells",
                "applications": "Surface water pumping, pond filling",
                "daily_water": "80-100 m³/day",
                "icon": "💦"
            },
            {
                "name": "1100W Solar Water Pump System (3DPC)",
                "hp": 1.5,
                "pump_model": "3DPC6-84-110-1100W",
                "pump_power": 1100,
                "pump_specs": {
                    "power": "1100W (1.5 HP)",
                    "voltage": "110V DC",
                    "max_flow": "6 m³/h",
                    "max_head": "84m",
                    "outlet": "1.5 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 2, "total_kw": 1.1},
                "controller": "MPPT Solar Pump Controller 110V",
                "description": "Deep well specialist",
                "applications": "Deep well pumping, high head applications",
                "daily_water": "25-35 m³/day",
                "icon": "⛏️"
            },
            {
                "name": "1500W Solar Water Pump System (4DPC)",
                "hp": 2,
                "pump_model": "4DPC9-85-110-1500W",
                "pump_power": 1500,
                "pump_specs": {
                    "power": "1500W (2 HP)",
                    "voltage": "110V DC",
                    "max_flow": "9 m³/h",
                    "max_head": "85m",
                    "outlet": "2 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 3, "total_kw": 1.65},
                "controller": "MPPT Solar Pump Controller 110V",
                "description": "Ideal for medium farms and irrigation",
                "applications": "Farm irrigation, fish ponds, water supply",
                "daily_water": "40-60 m³/day",
                "icon": "🌾"
            },
            {
                "name": "1500W Solar Water Pump System (DCPM)",
                "hp": 2,
                "pump_model": "DCPM50-17-110-1500W",
                "pump_power": 1500,
                "pump_specs": {
                    "power": "1500W (2 HP)",
                    "voltage": "110V DC",
                    "max_flow": "50 m³/h",
                    "max_head": "17m",
                    "outlet": "3 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 3, "total_kw": 1.65},
                "controller": "MPPT Solar Pump Controller 110V",
                "description": "High volume for surface water",
                "applications": "Large pond filling, surface irrigation",
                "daily_water": "200-250 m³/day",
                "icon": "🌊"
            },
            {
                "name": "2200W Solar Water Pump System (4DSC)",
                "hp": 3,
                "pump_model": "4DSC19-60-300-2200W",
                "pump_power": 2200,
                "pump_specs": {
                    "power": "2200W (3 HP)",
                    "voltage": "300V DC",
                    "max_flow": "19 m³/h",
                    "max_head": "60m",
                    "outlet": "3 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 5, "total_kw": 2.75},
                "controller": "MPPT Solar Pump Controller 300V",
                "description": "Great for large farms and commercial use",
                "applications": "Large-scale irrigation, water distribution",
                "daily_water": "80-100 m³/day",
                "icon": "🚜"
            },
            {
                "name": "2200W Solar Water Pump System (DCPM)",
                "hp": 3,
                "pump_model": "DCPM60-20-300-2200W-A/D",
                "pump_power": 2200,
                "pump_specs": {
                    "power": "2200W (3 HP)",
                    "voltage": "300V DC",
                    "max_flow": "60 m³/h",
                    "max_head": "20m",
                    "outlet": "4 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 5, "total_kw": 2.75},
                "controller": "MPPT Solar Pump Controller 300V",
                "description": "Ultra high flow for surface applications",
                "applications": "Flood irrigation, large pond systems",
                "daily_water": "250-300 m³/day",
                "icon": "🌊"
            },
            {
                "name": "4 HP Solar Water Pump System",
                "hp": 4,
                "pump_model": "4DSC19-98-380/550-3000W",
                "pump_power": 3000,
                "pump_specs": {
                    "power": "3000W (4 HP)",
                    "voltage": "380V AC / 550V DC",
                    "max_flow": "19 m³/h",
                    "max_head": "98m",
                    "outlet": "3 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 6, "total_kw": 3.3},
                "controller": "MPPT Solar Pump Controller 380V",
                "description": "Heavy-duty for deep wells and high head",
                "applications": "Deep well pumping, high-pressure irrigation",
                "daily_water": "100-120 m³/day",
                "icon": "🏭"
            },
            {
                "name": "5 HP Solar Water Pump System",
                "hp": 5,
                "pump_model": "4DSC19-135-380/550-4000W",
                "pump_power": 4000,
                "pump_specs": {
                    "power": "4000W (5 HP)",
                    "voltage": "380V AC / 550V DC",
                    "max_flow": "19 m³/h",
                    "max_head": "135m",
                    "outlet": "3 inch"
                },
                "solar_panels": {"name": "Lvtopsun 550W", "quantity": 8, "total_kw": 4.4},
                "controller": "MPPT Solar Pump Controller 380V",
                "description": "Industrial-grade for maximum performance",
                "applications": "Industrial water supply, large irrigation systems",
                "daily_water": "120-150 m³/day",
                "icon": "🏗️"
            }
        ]
        
        # Display each pump set
        for pump_set in pump_sets:
            with st.expander(f"{pump_set['icon']} {pump_set['name']} - {pump_set['hp']} HP"):
                # Display pump image using HTML
                img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
                with img_col2:
                    pump_img = product_images.get(pump_set['pump_model'], "https://via.placeholder.com/400x300.png?text=Water+Pump")
                    st.markdown(f"""
                    <div style='text-align: center;'>
                        <img src='{pump_img}' style='max-width: 400px; width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);' onerror="this.src='https://via.placeholder.com/400x300.png?text=Water+Pump'">
                        <p style='margin-top: 0.5rem; color: #666; font-size: 0.9rem;'>{pump_set['pump_model']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"**{pump_set['description']}**")
                st.markdown(f"**Applications:** {pump_set['applications']}")
                st.markdown("---")
                
                # Performance Summary
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                            padding: 1.2rem; border-radius: 10px; border-left: 4px solid #3b82f6; margin-bottom: 1rem;'>
                    <h3 style='margin: 0 0 0.8rem 0; color: #1e40af;'>💧 System Performance</h3>
                    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
                        <div style='text-align: center;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #1e40af;'><b>Pump Power</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #1e3a8a; font-weight: 700;'>{pump_set['pump_power']}W ({pump_set['hp']} HP)</p>
                        </div>
                        <div style='text-align: center; border-left: 2px solid #3b82f6; border-right: 2px solid #3b82f6;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #1e40af;'><b>Daily Water Output</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #1e3a8a; font-weight: 700;'>{pump_set['daily_water']}</p>
                        </div>
                        <div style='text-align: center;'>
                            <p style='margin: 0; font-size: 0.85rem; color: #1e40af;'><b>Solar Panels</b></p>
                            <p style='margin: 0.2rem 0; font-size: 1.3rem; color: #1e3a8a; font-weight: 700;'>{pump_set['solar_panels']['quantity']}x {pump_set['solar_panels']['total_kw']}kW</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Component Specifications
                st.markdown("### 🔧 System Components")
                
                spec_col1, spec_col2 = st.columns(2)
                
                with spec_col1:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #92400e;'>☀️ Solar Panels</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Model:</b> {pump_set['solar_panels']['name']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Quantity:</b> {pump_set['solar_panels']['quantity']} panels</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Total Power:</b> {pump_set['solar_panels']['total_kw']} kW</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Area Needed:</b> ~{pump_set['solar_panels']['quantity'] * 2.6:.1f} m²</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #6366f1;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #4338ca;'>⚡ Controller</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Type:</b> {pump_set['controller']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Features:</b> MPPT, Auto start/stop</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Protection:</b> Overload, dry-run, overvoltage</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with spec_col2:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;'>
                        <h4 style='margin: 0 0 0.8rem 0; color: #1e40af;'>💧 Water Pump</h4>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Model:</b> {pump_set['pump_model']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Power:</b> {pump_set['pump_specs']['power']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Voltage:</b> {pump_set['pump_specs']['voltage']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Max Flow:</b> {pump_set['pump_specs']['max_flow']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Max Head:</b> {pump_set['pump_specs']['max_head']}</p>
                        <p style='margin: 0.3rem 0; font-size: 0.85rem;'><b>Outlet:</b> {pump_set['pump_specs']['outlet']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Pricing calculation
                pump_price = pm.products.get(pump_set['pump_model'])
                pump_cost = pump_price.cost if pump_price else 200.00
                
                panel_price = pm.products.get(pump_set['solar_panels']['name'])
                panel_cost = panel_price.cost if panel_price else 66.00
                
                controller_cost = 150.00
                installation_cost = pump_set['pump_power'] * 0.15
                
                equipment_total = pump_cost + (panel_cost * pump_set['solar_panels']['quantity']) + controller_cost
                wholesale_total = equipment_total + installation_cost
                retail_total = wholesale_total * (1 + st.session_state.price_markup / 100)
                
                # Pricing display
                st.markdown("### 💰 System Pricing")
                
                price_col1, price_col2 = st.columns(2)
                
                with price_col1:
                    if not st.session_state.hide_wholesale:
                        st.markdown("#### 📊 Cost Breakdown")
                        st.write(f"💧 Water Pump: ${pump_cost:,.2f}")
                        st.write(f"☀️ Solar Panels ({pump_set['solar_panels']['quantity']}x): ${panel_cost * pump_set['solar_panels']['quantity']:,.2f}")
                        st.write(f"⚡ Controller: ${controller_cost:,.2f}")
                        st.write(f"👷 Installation: ${installation_cost:,.2f}")
                        st.markdown(f"**Total: ${equipment_total + installation_cost:,.2f}**")
                    else:
                        st.markdown("#### 📦 System Includes")
                        st.write(f"💧 {pump_set['pump_model']}")
                        st.write(f"☀️ {pump_set['solar_panels']['quantity']}x {pump_set['solar_panels']['name']}")
                        st.write(f"⚡ MPPT Controller")
                        st.write(f"👷 Professional installation")
                        st.write(f"📐 Area needed: ~{pump_set['solar_panels']['quantity'] * 2.6:.1f} m²")
                
                with price_col2:
                    if st.session_state.hide_wholesale:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                    padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3b82f6; text-align: center;'>
                            <h4 style='margin: 0 0 0.8rem 0; color: #1e40af;'>💵 System Price</h4>
                            <p style='margin: 0; font-size: 2rem; color: #1e3a8a; font-weight: 700;'>${retail_total:,.2f}</p>
                            <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #1e40af;'>Complete installed system</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                                    padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3b82f6;'>
                            <h4 style='margin: 0 0 0.8rem 0; color: #1e40af; text-align: center;'>💵 Final Pricing</h4>
                            <div style='margin: 0.5rem 0;'>
                                <p style='margin: 0.3rem 0; font-size: 0.9rem;'><b>💼 Wholesale:</b></p>
                                <p style='margin: 0; font-size: 1.3rem; color: #1e40af; font-weight: 600;'>${wholesale_total:,.2f}</p>
                            </div>
                            <hr style='margin: 0.8rem 0; border: 1px solid #3b82f6;'>
                            <div style='margin: 0.5rem 0;'>
                                <p style='margin: 0.3rem 0; font-size: 0.9rem;'><b>🏷️ Retail (+{st.session_state.price_markup:.0f}%):</b></p>
                                <p style='margin: 0; font-size: 1.8rem; color: #1e3a8a; font-weight: 700;'>${retail_total:,.2f}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.success("✅ **Includes:** Water pump, solar panels, MPPT controller, mounting structure, cables, and installation")
        
        st.markdown("---")
        st.info("💡 **Note:** All water pump systems are designed for optimal performance with 6-8 hours of peak sunlight. Actual water output may vary based on sunlight conditions and installation location.")

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

# ==================== TECHNICIAN CALCULATOR ====================
elif page == t('nav_technician'):
    st.title(t('tech_calc'))
    st.markdown(f"<p style='font-size: 1.1rem; color: #666; margin-bottom: 1rem;'>{t('tech_subtitle')}</p>", unsafe_allow_html=True)
    
    # Quick Reference Cards
    st.markdown("### 📋 Quick Reference")
    ref_col1, ref_col2, ref_col3, ref_col4 = st.columns(4)
    
    with ref_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; color: white; text-align: center;'>
            <div style='font-size: 0.8rem; opacity: 0.9;'>Common Voltages</div>
            <div style='font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0;'>12V / 24V / 48V</div>
            <div style='font-size: 0.75rem; opacity: 0.8;'>DC Systems</div>
        </div>
        """, unsafe_allow_html=True)
    
    with ref_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1rem; border-radius: 10px; color: white; text-align: center;'>
            <div style='font-size: 0.8rem; opacity: 0.9;'>Max Voltage Drop</div>
            <div style='font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0;'>3% - 5%</div>
            <div style='font-size: 0.75rem; opacity: 0.8;'>Acceptable Range</div>
        </div>
        """, unsafe_allow_html=True)
    
    with ref_col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1rem; border-radius: 10px; color: white; text-align: center;'>
            <div style='font-size: 0.8rem; opacity: 0.9;'>Battery DoD</div>
            <div style='font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0;'>50% - 80%</div>
            <div style='font-size: 0.75rem; opacity: 0.8;'>Recommended</div>
        </div>
        """, unsafe_allow_html=True)
    
    with ref_col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1rem; border-radius: 10px; color: white; text-align: center;'>
            <div style='font-size: 0.8rem; opacity: 0.9;'>Panel Voltage</div>
            <div style='font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0;'>18V - 36V</div>
            <div style='font-size: 0.75rem; opacity: 0.8;'>Typical Vmp</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Create tabs for different calculators
    calc_tabs = st.tabs([
        "☀️ Solar System",
        "🔋 Battery & Runtime",
        "📏 Wire Sizing",
        "⚡ Quick Calculations",
        "📊 Load Analysis"
    ])
    
    # ===== TAB 1: SOLAR SYSTEM CALCULATOR =====
    with calc_tabs[0]:
        st.markdown("### ☀️ Solar System Calculator")
        st.markdown("Calculate complete solar system specifications with presets.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Input")
            calc_type = st.radio("What do you want to calculate?", 
                               ["Voltage (V)", "Current (A)", "Resistance (Ω)", "Power (W)"])
            
            if calc_type == "Voltage (V)":
                current = st.number_input("Current (A)", min_value=0.0, value=10.0, step=0.1)
                resistance = st.number_input("Resistance (Ω)", min_value=0.0, value=12.0, step=0.1)
                if st.button(t('calculate'), key="ohm_v"):
                    voltage = current * resistance
                    power = voltage * current
                    st.session_state.ohm_result = {
                        'voltage': voltage,
                        'current': current,
                        'resistance': resistance,
                        'power': power
                    }
            
            elif calc_type == "Current (A)":
                voltage = st.number_input("Voltage (V)", min_value=0.0, value=12.0, step=0.1)
                resistance = st.number_input("Resistance (Ω)", min_value=0.01, value=1.2, step=0.1)
                if st.button(t('calculate'), key="ohm_i"):
                    current = voltage / resistance
                    power = voltage * current
                    st.session_state.ohm_result = {
                        'voltage': voltage,
                        'current': current,
                        'resistance': resistance,
                        'power': power
                    }
            
            elif calc_type == "Resistance (Ω)":
                voltage = st.number_input("Voltage (V)", min_value=0.0, value=12.0, step=0.1)
                current = st.number_input("Current (A)", min_value=0.01, value=10.0, step=0.1)
                if st.button(t('calculate'), key="ohm_r"):
                    resistance = voltage / current
                    power = voltage * current
                    st.session_state.ohm_result = {
                        'voltage': voltage,
                        'current': current,
                        'resistance': resistance,
                        'power': power
                    }
            
            else:  # Power
                voltage = st.number_input("Voltage (V)", min_value=0.0, value=12.0, step=0.1)
                current = st.number_input("Current (A)", min_value=0.0, value=10.0, step=0.1)
                if st.button(t('calculate'), key="ohm_p"):
                    power = voltage * current
                    resistance = voltage / current if current > 0 else 0
                    st.session_state.ohm_result = {
                        'voltage': voltage,
                        'current': current,
                        'resistance': resistance,
                        'power': power
                    }
        
        with col2:
            st.markdown("#### 📊 Results")
            if 'ohm_result' in st.session_state:
                result = st.session_state.ohm_result
                st.success(f"**Voltage:** {result['voltage']:.2f} V")
                st.info(f"**Current:** {result['current']:.2f} A")
                st.warning(f"**Resistance:** {result['resistance']:.2f} Ω")
                st.error(f"**Power:** {result['power']:.2f} W ({result['power']/1000:.2f} kW)")
                
                st.markdown("---")
                st.markdown("**📐 Formulas Used:**")
                st.code("V = I × R\nI = V / R\nR = V / I\nP = V × I")
    
    # ===== TAB 2: POWER CALCULATOR =====
    with calc_tabs[1]:
        st.markdown("### 💡 Power Calculator")
        st.markdown("Calculate power consumption and energy costs.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Device Information")
            device_power = st.number_input("Device Power (W)", min_value=0.0, value=1000.0, step=10.0)
            device_voltage = st.number_input("Operating Voltage (V)", min_value=0.0, value=220.0, step=1.0)
            usage_hours = st.number_input("Daily Usage (hours)", min_value=0.0, value=8.0, step=0.5)
            num_devices = st.number_input("Number of Devices", min_value=1, value=1, step=1)
            electricity_rate = st.number_input("Electricity Rate ($/kWh)", min_value=0.0, value=0.20, step=0.01)
            
            if st.button(t('calculate'), key="power_calc"):
                current_draw = device_power / device_voltage
                daily_kwh = (device_power * usage_hours * num_devices) / 1000
                monthly_kwh = daily_kwh * 30
                yearly_kwh = daily_kwh * 365
                daily_cost = daily_kwh * electricity_rate
                monthly_cost = monthly_kwh * electricity_rate
                yearly_cost = yearly_kwh * electricity_rate
                
                st.session_state.power_result = {
                    'current': current_draw,
                    'daily_kwh': daily_kwh,
                    'monthly_kwh': monthly_kwh,
                    'yearly_kwh': yearly_kwh,
                    'daily_cost': daily_cost,
                    'monthly_cost': monthly_cost,
                    'yearly_cost': yearly_cost
                }
        
        with col2:
            st.markdown("#### 📊 Results")
            if 'power_result' in st.session_state:
                result = st.session_state.power_result
                st.success(f"**Current Draw:** {result['current']:.2f} A")
                st.markdown("---")
                st.info(f"**Daily Energy:** {result['daily_kwh']:.2f} kWh (${result['daily_cost']:.2f})")
                st.info(f"**Monthly Energy:** {result['monthly_kwh']:.2f} kWh (${result['monthly_cost']:.2f})")
                st.info(f"**Yearly Energy:** {result['yearly_kwh']:.2f} kWh (${result['yearly_cost']:.2f})")
                
                st.markdown("---")
                st.warning(f"💰 **Annual Cost:** ${result['yearly_cost']:.2f}")
    
    # ===== TAB 3: WIRE SIZING CALCULATOR =====
    with calc_tabs[2]:
        st.markdown("### 📏 Wire Sizing Calculator")
        st.markdown("Calculate proper wire gauge for your installation.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Circuit Information")
            circuit_current = st.number_input("Circuit Current (A)", min_value=0.0, value=20.0, step=1.0)
            wire_length = st.number_input("One-Way Wire Length (m)", min_value=0.0, value=10.0, step=0.5)
            system_voltage = st.number_input("System Voltage (V)", min_value=0.0, value=12.0, step=1.0, 
                                           help="Common: 12V, 24V, 48V for DC systems")
            max_voltage_drop = st.number_input("Max Voltage Drop (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
            
            # Wire gauge reference table
            wire_data = {
                'AWG': [14, 12, 10, 8, 6, 4, 2, 1, 0, 00, 000, 0000],
                'mm²': [2.08, 3.31, 5.26, 8.37, 13.3, 21.2, 33.6, 42.4, 53.5, 67.4, 85.0, 107],
                'Max A': [15, 20, 30, 40, 55, 70, 95, 110, 125, 145, 165, 195],
                'Ω/km': [8.28, 5.21, 3.28, 2.06, 1.30, 0.815, 0.513, 0.407, 0.323, 0.256, 0.203, 0.161]
            }
            
            if st.button(t('calculate'), key="wire_calc"):
                # Calculate voltage drop for each wire size
                max_drop_voltage = system_voltage * (max_voltage_drop / 100)
                
                recommended_wire = None
                for i, awg in enumerate(wire_data['AWG']):
                    resistance_ohm = (wire_data['Ω/km'][i] / 1000) * wire_length * 2  # Round trip
                    voltage_drop = circuit_current * resistance_ohm
                    drop_percent = (voltage_drop / system_voltage) * 100
                    
                    if voltage_drop <= max_drop_voltage and wire_data['Max A'][i] >= circuit_current:
                        recommended_wire = {
                            'awg': awg,
                            'mm2': wire_data['mm²'][i],
                            'max_current': wire_data['Max A'][i],
                            'voltage_drop': voltage_drop,
                            'drop_percent': drop_percent
                        }
                        break
                
                st.session_state.wire_result = recommended_wire
        
        with col2:
            st.markdown("#### 📊 Recommendation")
            if 'wire_result' in st.session_state and st.session_state.wire_result:
                result = st.session_state.wire_result
                st.success(f"✅ **Recommended Wire Size**")
                st.markdown(f"### AWG {result['awg']} ({result['mm2']:.1f} mm²)")
                st.info(f"**Max Current Rating:** {result['max_current']} A")
                st.warning(f"**Voltage Drop:** {result['voltage_drop']:.2f} V ({result['drop_percent']:.2f}%)")
                
                st.markdown("---")
                st.markdown("**📋 Wire Gauge Reference:**")
                import pandas as pd
                df = pd.DataFrame(wire_data)
                st.dataframe(df, use_container_width=True)
            elif 'wire_result' in st.session_state:
                st.error("❌ No suitable wire found! Increase wire size or reduce length/current.")
    
    # ===== TAB 4: VOLTAGE DROP CALCULATOR =====
    with calc_tabs[3]:
        st.markdown("### 📉 Voltage Drop Calculator")
        st.markdown("Calculate voltage drop in your wire run.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Wire Specifications")
            wire_awg = st.selectbox("Wire Gauge (AWG)", [14, 12, 10, 8, 6, 4, 2, 1, 0, "00", "000", "0000"])
            wire_length_vd = st.number_input("One-Way Length (m)", min_value=0.0, value=10.0, step=0.5, key="vd_length")
            current_vd = st.number_input("Current (A)", min_value=0.0, value=20.0, step=1.0, key="vd_current")
            voltage_vd = st.number_input("System Voltage (V)", min_value=0.0, value=12.0, step=1.0, key="vd_voltage")
            
            # Resistance per km for different AWG
            resistance_map = {
                14: 8.28, 12: 5.21, 10: 3.28, 8: 2.06, 6: 1.30, 
                4: 0.815, 2: 0.513, 1: 0.407, 0: 0.323, 
                "00": 0.256, "000": 0.203, "0000": 0.161
            }
            
            if st.button(t('calculate'), key="vd_calc"):
                resistance_per_km = resistance_map[wire_awg]
                total_resistance = (resistance_per_km / 1000) * wire_length_vd * 2  # Round trip
                voltage_drop = current_vd * total_resistance
                drop_percent = (voltage_drop / voltage_vd) * 100
                voltage_at_load = voltage_vd - voltage_drop
                power_loss = current_vd * voltage_drop
                
                st.session_state.vd_result = {
                    'voltage_drop': voltage_drop,
                    'drop_percent': drop_percent,
                    'voltage_at_load': voltage_at_load,
                    'power_loss': power_loss,
                    'resistance': total_resistance
                }
        
        with col2:
            st.markdown("#### 📊 Results")
            if 'vd_result' in st.session_state:
                result = st.session_state.vd_result
                
                # Color code based on voltage drop percentage
                if result['drop_percent'] <= 3:
                    status = "✅ Excellent"
                    color = "green"
                elif result['drop_percent'] <= 5:
                    status = "⚠️ Acceptable"
                    color = "orange"
                else:
                    status = "❌ Too High"
                    color = "red"
                
                st.markdown(f"**Status:** :{color}[{status}]")
                st.success(f"**Voltage Drop:** {result['voltage_drop']:.2f} V ({result['drop_percent']:.2f}%)")
                st.info(f"**Voltage at Load:** {result['voltage_at_load']:.2f} V")
                st.warning(f"**Power Loss:** {result['power_loss']:.2f} W")
                st.error(f"**Wire Resistance:** {result['resistance']:.4f} Ω")
                
                st.markdown("---")
                st.markdown("**📐 Guidelines:**")
                st.markdown("- ✅ < 3%: Excellent")
                st.markdown("- ⚠️ 3-5%: Acceptable")
                st.markdown("- ❌ > 5%: Use larger wire")
    
    # ===== TAB 5: BATTERY CALCULATOR =====
    with calc_tabs[4]:
        st.markdown("### 🔋 Battery Calculator")
        st.markdown("Calculate battery capacity and runtime.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Battery & Load Information")
            calc_mode = st.radio("Calculate:", ["Runtime", "Required Capacity"])
            
            if calc_mode == "Runtime":
                battery_voltage = st.number_input("Battery Voltage (V)", min_value=0.0, value=12.0, step=1.0, key="bat_v")
                battery_ah = st.number_input("Battery Capacity (Ah)", min_value=0.0, value=100.0, step=10.0)
                load_watts = st.number_input("Load Power (W)", min_value=0.0, value=120.0, step=10.0)
                dod_percent = st.number_input("Depth of Discharge (%)", min_value=0.0, max_value=100.0, value=80.0, step=5.0)
                efficiency = st.number_input("System Efficiency (%)", min_value=0.0, max_value=100.0, value=85.0, step=5.0)
                
                if st.button(t('calculate'), key="bat_runtime"):
                    usable_capacity_ah = battery_ah * (dod_percent / 100)
                    usable_capacity_wh = battery_voltage * usable_capacity_ah
                    actual_usable_wh = usable_capacity_wh * (efficiency / 100)
                    runtime_hours = actual_usable_wh / load_watts if load_watts > 0 else 0
                    
                    st.session_state.bat_result = {
                        'mode': 'runtime',
                        'runtime': runtime_hours,
                        'usable_wh': actual_usable_wh,
                        'usable_ah': usable_capacity_ah
                    }
            
            else:  # Required Capacity
                battery_voltage_req = st.number_input("Battery Voltage (V)", min_value=0.0, value=12.0, step=1.0, key="bat_v_req")
                load_watts_req = st.number_input("Load Power (W)", min_value=0.0, value=120.0, step=10.0, key="load_req")
                runtime_hours_req = st.number_input("Desired Runtime (hours)", min_value=0.0, value=8.0, step=0.5)
                dod_percent_req = st.number_input("Depth of Discharge (%)", min_value=0.0, max_value=100.0, value=80.0, step=5.0, key="dod_req")
                efficiency_req = st.number_input("System Efficiency (%)", min_value=0.0, max_value=100.0, value=85.0, step=5.0, key="eff_req")
                
                if st.button(t('calculate'), key="bat_capacity"):
                    required_wh = load_watts_req * runtime_hours_req
                    required_wh_with_eff = required_wh / (efficiency_req / 100)
                    required_wh_with_dod = required_wh_with_eff / (dod_percent_req / 100)
                    required_ah = required_wh_with_dod / battery_voltage_req
                    
                    st.session_state.bat_result = {
                        'mode': 'capacity',
                        'required_ah': required_ah,
                        'required_wh': required_wh_with_dod,
                        'energy_needed': required_wh
                    }
        
        with col2:
            st.markdown("#### 📊 Results")
            if 'bat_result' in st.session_state:
                result = st.session_state.bat_result
                
                if result['mode'] == 'runtime':
                    hours = int(result['runtime'])
                    minutes = int((result['runtime'] - hours) * 60)
                    st.success(f"**Runtime:** {hours}h {minutes}m ({result['runtime']:.2f} hours)")
                    st.info(f"**Usable Energy:** {result['usable_wh']:.2f} Wh ({result['usable_wh']/1000:.2f} kWh)")
                    st.warning(f"**Usable Capacity:** {result['usable_ah']:.2f} Ah")
                else:
                    st.success(f"**Required Capacity:** {result['required_ah']:.2f} Ah")
                    st.info(f"**Total Energy Storage:** {result['required_wh']:.2f} Wh ({result['required_wh']/1000:.2f} kWh)")
                    st.warning(f"**Energy Needed:** {result['energy_needed']:.2f} Wh")
                    
                    # Suggest standard battery sizes
                    st.markdown("---")
                    st.markdown("**💡 Standard Battery Sizes:**")
                    standard_sizes = [50, 100, 150, 200, 250, 300]
                    for size in standard_sizes:
                        if size >= result['required_ah']:
                            st.markdown(f"- ✅ **{size} Ah** (Recommended)")
                            break
                        else:
                            st.markdown(f"- ❌ {size} Ah (Too small)")
    
    # ===== TAB 6: SOLAR ARRAY CALCULATOR =====
    with calc_tabs[5]:
        st.markdown("### ☀️ Solar Array Calculator")
        st.markdown("Calculate series/parallel configuration for solar panels.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 System Requirements")
            target_voltage = st.number_input("Target System Voltage (V)", min_value=0.0, value=48.0, step=1.0)
            target_power = st.number_input("Target Power (W)", min_value=0.0, value=3000.0, step=100.0)
            
            st.markdown("#### 📥 Panel Specifications")
            panel_voltage = st.number_input("Panel Voltage (Vmp)", min_value=0.0, value=18.0, step=0.1)
            panel_current = st.number_input("Panel Current (Imp)", min_value=0.0, value=9.0, step=0.1)
            panel_power = st.number_input("Panel Power (W)", min_value=0.0, value=160.0, step=10.0)
            
            if st.button(t('calculate'), key="solar_calc"):
                # Calculate series and parallel configuration
                panels_in_series = int(np.ceil(target_voltage / panel_voltage))
                string_voltage = panels_in_series * panel_voltage
                string_power = panels_in_series * panel_power
                
                num_strings = int(np.ceil(target_power / string_power))
                total_panels = panels_in_series * num_strings
                total_power = total_panels * panel_power
                total_current = num_strings * panel_current
                
                st.session_state.solar_result = {
                    'panels_series': panels_in_series,
                    'num_strings': num_strings,
                    'total_panels': total_panels,
                    'string_voltage': string_voltage,
                    'total_power': total_power,
                    'total_current': total_current
                }
        
        with col2:
            st.markdown("#### 📊 Configuration")
            if 'solar_result' in st.session_state:
                result = st.session_state.solar_result
                
                st.success(f"**Configuration:** {result['panels_series']}S × {result['num_strings']}P")
                st.info(f"**Total Panels:** {result['total_panels']} panels")
                st.warning(f"**Total Power:** {result['total_power']} W ({result['total_power']/1000:.2f} kW)")
                st.error(f"**System Voltage:** {result['string_voltage']:.1f} V")
                st.info(f"**Total Current:** {result['total_current']:.1f} A")
                
                st.markdown("---")
                st.markdown("**📐 Configuration Diagram:**")
                st.code(f"""
String 1: [{result['panels_series']} panels in series]
String 2: [{result['panels_series']} panels in series]
...
String {result['num_strings']}: [{result['panels_series']} panels in series]

All strings connected in parallel
                """)
                
                st.markdown("---")
                st.markdown("**🔌 Connection Details:**")
                st.markdown(f"- Each string: {result['panels_series']} panels × {panel_voltage}V = {result['string_voltage']:.1f}V")
                st.markdown(f"- Parallel strings: {result['num_strings']} × {panel_current}A = {result['total_current']:.1f}A")
                st.markdown(f"- Total power: {result['total_panels']} × {panel_power}W = {result['total_power']}W")

# Footer - Ultra Compact
st.sidebar.markdown("<div style='margin: 0.75rem 0;'><hr style='margin: 0; border: none; border-top: 1px solid #e5e7eb;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='text-align: center; padding: 0.3rem 0; color: #9ca3af; font-size: 0.65rem; line-height: 1.4;'>
    <div>📞 <b>0888836588</b></div>
    <div>💬 @chhanycls</div>
    <div style='margin-top: 0.3rem; opacity: 0.6;'>v2.0 © 2025</div>
</div>
""", unsafe_allow_html=True)
