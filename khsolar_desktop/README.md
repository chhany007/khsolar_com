# KHSolar Desktop - Sales & Customer Management System

## 📋 Overview

Standalone desktop application for solar business management including:
- 📦 Product Price Management
- 💰 Sales Management
- 🛡️ Warranty Tracking
- 👥 Customer Database
- 📊 Reports & Analytics

## 🎯 Features

### 1. Product Management
- View all solar products with prices
- Wholesale and retail pricing
- Product specifications
- Inventory tracking

### 2. Sales Management
- Create new sales orders
- Track sales history
- Invoice generation
- Payment tracking
- Sales reports

### 3. Warranty Management
- Register product warranties
- Track warranty expiration
- Warranty claim processing
- Service history

### 4. Customer Database
- Customer information management
- Purchase history
- Contact details
- Project tracking

## 🚀 Installation

### Requirements:
- Python 3.11+
- Windows 10/11

### Install:
```bash
cd khsolar_desktop
pip install -r requirements.txt
```

### Run:
```bash
python main.py
```

## 📁 Project Structure

```
khsolar_desktop/
├── main.py                 # Main application entry
├── requirements.txt        # Python dependencies
├── config/
│   └── settings.py        # Application settings
├── database/
│   ├── db_manager.py      # Database operations
│   └── schema.sql         # Database schema
├── modules/
│   ├── products.py        # Product management
│   ├── sales.py           # Sales management
│   ├── warranty.py        # Warranty management
│   └── customers.py       # Customer management
├── ui/
│   ├── main_window.py     # Main UI window
│   ├── products_tab.py    # Products interface
│   ├── sales_tab.py       # Sales interface
│   ├── warranty_tab.py    # Warranty interface
│   └── customers_tab.py   # Customers interface
├── assets/
│   ├── images/            # Images and icons
│   └── styles/            # CSS styles
└── data/
    ├── products.db        # Product database
    └── customers.db       # Customer database
```

## 🔧 Technology Stack

- **GUI Framework:** PyQt5 / Tkinter
- **Database:** SQLite
- **Reports:** ReportLab (PDF)
- **Data:** Pandas, NumPy
- **Excel Export:** openpyxl

## 📞 Support

For support, contact:
- 📞 +855 888 836 588
- 💬 @chhanycls
