# 🚀 Quick System Designer - One Click Solution

## New Feature Added to Dashboard

### Overview
A powerful "one-click" system sizing wizard has been added to the **Dashboard** tab, right after the customer information section. This allows you to quickly design a complete solar system by simply entering monthly kWh usage.

## How It Works

### Step 1: Enter Customer Information
- Fill in customer details (name and phone are required)
- Save the information

### Step 2: Use Quick System Designer
After saving customer info, you'll see the **Quick System Designer** section with:

#### Input Fields:
1. **Monthly kWh Usage** (50 - 10,000 kWh)
   - Enter the customer's average monthly electricity consumption
   - Can be found on their electricity bill

2. **System Type** (3 options)
   - **Hybrid (Grid + Battery)** - Best for most homes, provides backup power
   - **On-Grid (No Battery)** - Lowest cost, no backup during outages
   - **Off-Grid (Full Battery)** - Complete independence from the grid

### Step 3: Calculate System
Click **"⚡ Calculate System"** button and instantly get:

## What You Get

### 1. Solar Panel Recommendations
- **Model**: Actual product from your catalog (e.g., Lvtopsun 550W)
- **Quantity**: Exact number of panels needed
- **Total Capacity**: Total kW installed
- **Installation Area**: Square meters required for installation
- **Cost**: Wholesale price

### 2. Battery Storage Recommendations
- **Model**: From your product catalog (e.g., DEYE 100AH 51.2v)
- **Quantity**: Number of battery units needed
- **Total Capacity**: Total kWh storage
- **Backup Time**: Hours of backup power available
- **Cost**: Wholesale price per unit

### 3. Inverter Recommendations
- **Model**: Matched from your catalog (Sungrow, Deye, Solis, etc.)
- **Power Rating**: kW capacity
- **Type**: Hybrid/On-Grid/Off-Grid based on selection
- **Cost**: Wholesale price

### 4. Complete Pricing Breakdown
Detailed cost table showing:
- Solar panels cost
- Battery storage cost
- Inverter cost
- Labor cost (automatically calculated: $250 for ≤5kW, $500 for >5kW)
- Support materials cost (automatically scaled: $450-$600)

**Two pricing columns:**
- **Wholesale Price** - Your internal cost
- **Customer Price (+30%)** - Retail price with markup

### 5. Total Investment Summary
Beautiful card showing:
- **Wholesale Total**: Your cost
- **Customer Price Total**: Retail price with 30% markup
- **Est. Monthly Savings**: Based on current grid rates

### 6. Installation Area
Automatically calculated square footage needed for panel installation

## Smart Calculations

### System Sizing Logic:
- **PV Capacity**: Based on daily usage ÷ sunlight hours × 1.25 (safety margin)
- **Battery Capacity**:
  - Hybrid: 70% of daily usage (night coverage)
  - Off-Grid: 200% of daily usage (2 days autonomy)
  - On-Grid: 0 (no battery)
- **Inverter Size**: Peak load estimate (3× average) × 1.25 (margin)

### Product Selection:
- Uses **actual products** from your `product_prices.txt`
- Finds **best value** products matching requirements
- Falls back to generic estimates if specific products unavailable

## Apply to System

After reviewing recommendations, click **"✅ Apply This Configuration to System"** to:
- Automatically configure solar panels in System Config
- Set up battery storage (if applicable)
- Configure inverter
- All settings are ready for simulation and reporting

## Benefits

✅ **Fast**: Get complete system design in seconds
✅ **Accurate**: Uses actual products from your catalog
✅ **Professional**: Complete pricing breakdown with markup
✅ **Flexible**: All recommendations are adjustable in System Config
✅ **Easy**: Customer only needs to provide monthly kWh usage

## Example Use Case

**Customer says**: "My monthly electricity bill shows 300 kWh usage"

**You enter**: 
- Monthly kWh: 300
- System Type: Hybrid (Grid + Battery)

**Click Calculate** → Get instant recommendations:
- 10× Lvtopsun 550W panels (5.5 kW)
- 2× DEYE 51.2v batteries (10.24 kWh)
- 1× Deye Hybrid 8kw inverter
- Installation area: ~20 m²
- Wholesale: $3,450
- Customer Price: $4,485
- Monthly savings: ~$60

**Click Apply** → System is configured and ready for simulation!

## Location in App

**Dashboard Tab** → After Customer Information Section → "🚀 Quick System Designer"

---

This feature streamlines your workflow and provides professional, accurate quotes in seconds while using only products from your actual inventory.
