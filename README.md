# ☀️ Ultimate Solar Planning & Business Software

Comprehensive solar system planning, simulation, and business management tool designed for Khmer households and solar businesses.

## 🎯 Features

### Core Functionality
- **Device Management**: Add and manage electrical devices with power consumption tracking
- **System Configuration**: Configure solar panels, batteries, and inverters
- **24-Hour Simulation**: Detailed hourly energy flow simulation with battery state tracking
- **Financial Analysis**: ROI, payback period, and lifetime savings calculations
- **Product Catalog**: Built-in database of solar products with cost management
- **AI Recommendations**: Smart device scheduling and system optimization advice

### Business Features
- **Cost Calculator**: Total system cost breakdown with installation and additional costs
- **Product Management**: Add, browse, and compare solar equipment
- **Quote Generation**: Generate customer proposals and quotes
- **Multi-currency Support**: Flexible pricing for different markets

### Visualization & Reporting
- **Interactive Charts**: 24-hour energy flow graphs with Plotly
- **Battery SoC Tracking**: Real-time state of charge visualization
- **Energy Balance**: Pie charts showing energy sources
- **Export Options**: PDF, Excel, and CSV report generation

### Advanced Features
- **Hybrid Input Methods**: Device-based, monthly usage, or system specs
- **Day/Night Load Analysis**: Intelligent load splitting
- **Priority Devices**: Mark essential devices for backup planning
- **Self-Sufficiency Metrics**: Track grid independence percentage
- **CO₂ Reduction**: Environmental impact calculations

## 📋 Requirements

```txt
Python 3.8+
streamlit==1.28.0
pandas==2.1.0
numpy==1.24.3
plotly==5.17.0
matplotlib==3.7.2
openpyxl==3.1.2
reportlab==4.0.5
Pillow==10.0.0
scipy==1.11.2
python-dotenv==1.0.0
```

## 🚀 Installation

1. **Clone or download the project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

4. **Access the web interface**:
   - Browser will open automatically at `http://localhost:8501`
   - If not, manually navigate to the URL

## 📖 User Guide

### Step 1: Add Devices
1. Navigate to **⚡ Devices** page
2. Click **Add Device** tab
3. Enter device details:
   - Device name (e.g., "Refrigerator")
   - Power consumption in Watts
   - Daily usage hours
   - Device type and priority
4. Click **Add Device**

**Quick Option**: Use "Import from Monthly Usage" to generate typical household devices

### Step 2: Configure System
1. Go to **🔧 System Config** page
2. Configure each component:
   - **Solar Panels**: Model, power rating, quantity, cost
   - **Battery**: Capacity, voltage, depth of discharge
   - **Inverter**: Power rating, efficiency
3. Save each configuration

### Step 3: Browse Products (Optional)
1. Visit **🛒 Products** page
2. Browse pre-loaded solar products
3. Use cost calculator to estimate system expenses
4. Add custom products if needed

### Step 4: Run Simulation
1. Navigate to **📊 Simulation** page
2. Click **Run Simulation**
3. View results:
   - 24-hour energy flow graphs
   - Battery state of charge
   - Daily energy summary
   - Financial analysis
   - AI recommendations

### Step 5: Export Reports
1. Go to **📈 Reports** page
2. Choose export format:
   - **Excel**: Complete data with multiple sheets
   - **CSV**: Simulation data for analysis
   - **PDF**: Professional report for customers
3. Files saved in project directory

## 🏗️ Project Structure

```
solar-software/
├── app.py                      # Main Streamlit application
├── models.py                   # Data models and classes
├── calculations.py             # Solar calculation engine
├── product_manager.py          # Product catalog management
├── visualization.py            # Charts and graphs
├── export_utils.py             # Report export functionality
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── Ultimate_Solar_Software_Roadmap.txt  # Project roadmap
```

## 💡 Usage Examples

### Example 1: Typical Khmer Household
```
Devices:
- Refrigerator: 150W, 24h
- Air Conditioner: 1500W, 8h
- LED Lights: 60W, 5h
- TV: 100W, 4h
- Rice Cooker: 500W, 1h

System:
- 10x 450W Solar Panels (4.5 kW)
- 5 kWh LiFePO4 Battery
- 5 kW Hybrid Inverter

Result:
- Daily Load: ~20 kWh
- Self-Sufficiency: 85%
- Payback Period: 6-8 years
```

### Example 2: Small Business/Shop
```
Devices:
- Freezer: 200W, 24h
- Lights: 150W, 12h
- Fans: 150W, 10h
- Computer: 300W, 8h

System:
- 8x 450W Panels (3.6 kW)
- 10 kWh Battery
- 5 kW Inverter

Result:
- Daily Load: ~15 kWh
- Self-Sufficiency: 95%
- Annual Savings: $700+
```

## 🔧 Configuration

### Location Settings
Default: Phnom Penh, Cambodia (5.5 peak sun hours)

Adjust in **System Config → Location** tab:
- Peak sunlight hours (3-7 hours)
- Grid availability
- Electricity rate (USD/kWh)

### System Efficiency
Default parameters:
- PV System Efficiency: 85%
- Battery Efficiency: 95%
- Inverter Efficiency: 97%
- Battery DoD: 80%

## 📊 Calculation Methodology

### PV Sizing
```
PV Size (kW) = Daily Load (kWh) / (Sunlight Hours × System Efficiency)
```

### Battery Sizing
```
Battery Size (kWh) = (Night Load × Autonomy Days) / Depth of Discharge
```

### Financial Analysis
```
Payback Period = System Cost / Annual Savings
ROI = ((Lifetime Savings - System Cost) / System Cost) × 100%
Annual Savings = Annual Solar Energy × Electricity Rate
```

### Self-Sufficiency
```
Self-Sufficiency (%) = ((Total Load - Grid Import) / Total Load) × 100
```

## 🌟 Best Practices

1. **Device Scheduling**:
   - Run high-power devices (AC, washing machine) during peak sun hours (10 AM - 2 PM)
   - Use battery storage for evening/night loads
   - Prioritize essential devices for backup

2. **System Sizing**:
   - PV capacity should cover daily load + battery charging
   - Battery should cover night consumption + safety margin
   - Inverter rating ≥ peak load

3. **Cost Optimization**:
   - Compare multiple product options
   - Consider warranty and lifecycle costs
   - Factor in installation and maintenance

4. **Energy Efficiency**:
   - Replace old appliances with energy-efficient models
   - Use LED lighting
   - Proper insulation reduces AC load

## 🐛 Troubleshooting

**Issue**: Simulation shows high grid import
- **Solution**: Increase PV capacity or reduce daytime load

**Issue**: Battery depletes quickly at night
- **Solution**: Add battery capacity or shift loads to daytime

**Issue**: System cost too high
- **Solution**: Browse budget products in catalog or reduce system size

**Issue**: Charts not displaying
- **Solution**: Ensure all dependencies installed correctly

## 🔮 Future Enhancements

Roadmap includes:
- Real-time monitoring integration
- Weather forecast integration
- Smart device/IoT control
- Mobile app version
- Multi-building management
- Cloud synchronization
- Voice assistant integration
- Gamification features

## 📞 Support

For technical support or feature requests:
- Review the roadmap: `Ultimate_Solar_Software_Roadmap.txt`
- Check calculation modules: `calculations.py`
- Explore data models: `models.py`

## 📄 License

This software is designed for solar planning and business management. 
Customize and extend as needed for your specific requirements.

## 🙏 Acknowledgments

Built for Khmer households and solar businesses to enable:
- Affordable solar adoption
- Energy independence
- Reduced carbon footprint
- Professional solar system design

---

**Version**: 1.0  
**Last Updated**: 2025  
**Supported By**: Comprehensive calculation engine with 24-hour simulation capability
