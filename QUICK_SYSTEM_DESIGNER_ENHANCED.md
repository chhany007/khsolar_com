# 🚀 Quick System Designer - Enhanced Features

## Overview
The Quick System Designer has been enhanced with brand selection capabilities and flexible auto-recommend mode, giving users full control over component selection while maintaining intelligent recommendations.

## New Features

### 1. ⚡ kWh Usage Input (Required)
- **Field:** Monthly kWh Usage
- **Range:** 50 - 10,000 kWh
- **Step:** 50 kWh
- **Default:** 300 kWh
- **Required:** Yes (marked with *)
- **Help:** Enter your average monthly electricity consumption in kWh

### 2. 📊 Usage Status (New)
- **Field:** Usage Status dropdown
- **Options:**
  - Average
  - Low Usage
  - High Usage
  - Peak Season
- **Purpose:** Helps categorize customer usage patterns
- **Default:** Average

### 3. 🔧 System Type
- **Field:** System Type dropdown
- **Options:**
  - Hybrid (Grid + Battery)
  - On-Grid (No Battery)
  - Off-Grid (Full Battery)
- **Purpose:** Determines battery requirements

### 4. 🏷️ Component Selection (Optional)

#### ☀️ Solar Panel Brand
- **Type:** Dropdown selector
- **Options:**
  - Auto-Recommend (Best Value) - Default
  - All PV panels from your product catalog
- **Smart Behavior:**
  - If "Auto-Recommend": System finds best value panel ≥500W
  - If specific brand selected: Uses that exact product

#### 🔋 Battery Brand
- **Type:** Dropdown selector
- **Options:**
  - Auto-Recommend (Best Value) - Default
  - All batteries from your product catalog
- **Smart Behavior:**
  - If "Auto-Recommend": System finds best value battery ≥5kWh
  - If specific brand selected: Uses that exact product
  - Automatically hidden for On-Grid systems

#### ⚡ Inverter Brand
- **Type:** Dropdown selector
- **Options:**
  - Auto-Recommend (Best Value) - Default
  - All inverters from your product catalog
- **Smart Behavior:**
  - If "Auto-Recommend": System finds suitable inverter for load
  - If specific brand selected: Uses that exact product
  - Matches system type (Hybrid/On-Grid/Off-Grid)

---

## User Workflow

### Simple Mode (Auto-Recommend)
1. Enter monthly kWh usage
2. Select usage status
3. Select system type
4. Leave all brands as "Auto-Recommend"
5. Click "⚡ Calculate System"
6. Get instant recommendations

**Result:** System automatically selects best value components based on requirements.

### Advanced Mode (Brand Selection)
1. Enter monthly kWh usage
2. Select usage status
3. Select system type
4. Choose specific PV panel brand (optional)
5. Choose specific battery brand (optional)
6. Choose specific inverter brand (optional)
7. Click "⚡ Calculate System"
8. Get system sized with your selected brands

**Result:** System uses your selected brands and calculates quantities needed.

### Mixed Mode
You can mix and match:
- Auto-recommend PV + Select specific battery + Auto-recommend inverter
- Any combination you want!

---

## Configuration Summary Display

After calculation, a new summary card shows:

```
📋 Configuration Summary
├── MONTHLY USAGE: 300 kWh (Average)
├── SYSTEM TYPE: Hybrid (Grid + Battery)
└── SELECTION MODE: 🤖 Auto-Recommended OR 👤 User-Selected Components
```

**Selection Mode Badge:**
- 🤖 Auto-Recommended - All components auto-selected
- 👤 User-Selected Components - At least one component manually chosen

---

## Technical Details

### Brand List Generation
Brands are dynamically loaded from `product_prices.txt` via `ProductManager`:
- **PV Panels:** All products with category='pv_panel'
- **Batteries:** All products with category='battery'
- **Inverters:** All products with category='inverter'

### Selection Logic

#### Solar Panels:
```python
if selected_pv == "Auto-Recommend (Best Value)":
    # Find best value panel ≥500W
    rec_panel = pm.get_recommended_panel(min_wattage=500)
else:
    # Use selected panel from catalog
    selected_panel_product = pm.products.get(selected_pv)
```

#### Batteries:
```python
if selected_battery == "Auto-Recommend (Best Value)":
    # Find best value battery ≥5kWh
    rec_battery = pm.get_recommended_battery(min_capacity_kwh=5.0)
else:
    # Use selected battery from catalog
    selected_battery_product = pm.products.get(selected_battery)
```

#### Inverters:
```python
if selected_inverter == "Auto-Recommend (Best Value)":
    # Find suitable inverter for calculated load
    rec_inverter = pm.get_recommended_inverter(min_power_kw=inverter_kw_needed)
else:
    # Use selected inverter from catalog
    selected_inverter_product = pm.products.get(selected_inverter)
```

---

## Stored Results

The system stores these fields in session state:

```python
quick_sizing_results = {
    'monthly_kwh': int,          # User input
    'daily_kwh': float,          # Calculated
    'usage_status': str,         # NEW - User selection
    'system_type': str,          # User selection
    'selected_pv': str,          # NEW - Selected or "Auto-Recommend"
    'selected_battery': str,     # NEW - Selected or "Auto-Recommend"
    'selected_inverter': str,    # NEW - Selected or "Auto-Recommend"
    'num_panels': int,           # Calculated quantity
    'panel_name': str,           # Product name used
    'panel_wattage': float,      # Specs
    'panel_cost': float,         # Wholesale price
    'num_batteries': int,        # Calculated quantity
    'battery_name': str,         # Product name used
    'battery_unit_capacity': float,
    'battery_voltage': float,
    'battery_cost_per_unit': float,
    'inverter_kw': float,        # Power rating
    'inverter_name': str,        # Product name used
    'inverter_cost': float,      # Wholesale price
    'area_needed': float,        # m² for installation
    'equipment_cost': float,     # Total equipment
    'labor_cost': float,         # Installation labor
    'support_cost': float,       # Support materials
    'total_wholesale': float,    # Your cost
    'total_customer': float      # Customer price (+30%)
}
```

---

## UI Layout

### Form Structure:
```
📊 System Configuration
├── Row 1: kWh Usage* | Usage Status
├── Row 2: System Type (full width)
└── Row 3: Brand Selection (3 columns)
    ├── Solar Panel Brand
    ├── Battery Brand
    └── Inverter Brand
```

### Visual Hierarchy:
1. **Golden banner** - Quick System Designer header
2. **Blue card** - Quick Tips (right column)
3. **Form inputs** - Organized in sections
4. **Purple summary** - Configuration summary after calc
5. **Component cards** - Solar, Battery, Inverter details
6. **Pricing table** - Cost breakdown
7. **Green investment card** - Total with ROI

---

## Benefits

### For Users:
✅ **Flexibility** - Can auto-recommend or manually select
✅ **Control** - Choose specific brands if preferred
✅ **Speed** - Still fast with auto-recommend mode
✅ **Transparency** - See what was selected

### For Business:
✅ **Customer preference** - Honor brand requests
✅ **Inventory management** - Select specific stock
✅ **Margin control** - Use preferred products
✅ **Professional** - More options = more credible

---

## Example Use Cases

### Case 1: Quick Quote (Auto Mode)
**Customer:** "I use 400 kWh per month"
**You:** 
1. Input 400 kWh
2. Leave all as Auto-Recommend
3. Calculate
4. Show instant professional quote

### Case 2: Customer Brand Preference
**Customer:** "I want Deye inverter specifically"
**You:**
1. Input kWh usage
2. Auto-recommend solar and battery
3. Select "Deye Hybrid 8kw" from inverter dropdown
4. Calculate with customer's preferred brand

### Case 3: Inventory Management
**You:** "I have excess LONGi 585W panels in stock"
**Action:**
1. Select "LONGi Panel 585w" from PV dropdown
2. Auto-recommend other components
3. System sizes using your available stock

### Case 4: Mixed Approach
**Customer:** "I want DEYE battery but you choose the rest"
**You:**
1. Auto-recommend PV
2. Select "DEYE 100AH 51.2v" battery
3. Auto-recommend inverter
4. Get balanced system with customer choice

---

## Location in App

**Dashboard Tab** → After Customer Info → Quick System Designer

---

## Files Modified

- `app.py` - Enhanced Quick System Designer section
  - Added usage status field
  - Added brand selection dropdowns
  - Implemented auto-recommend vs manual selection logic
  - Added configuration summary display

- `QUICK_SYSTEM_DESIGNER_ENHANCED.md` - This documentation

---

## Future Enhancements (Potential)

- Save favorite configurations
- Compare different brand combinations
- Show brand availability status
- Brand-specific warranties display
- Price comparison mode

---

The Quick System Designer now provides **professional-grade flexibility** while maintaining the **one-click simplicity** that makes it so powerful! 🚀
