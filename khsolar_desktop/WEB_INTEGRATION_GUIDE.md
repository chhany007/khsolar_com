# 🌐 Web Integration Guide - KHSolar Desktop

## 📋 Overview

The KHSolar Desktop app now integrates with your web app to:
1. **Import all 65 products** from the web catalog
2. **Sync online customer orders** automatically as pending invoices

---

## ✅ Features Implemented

### 1. Product Import from Web App ✨

**What it does:**
- Automatically imports all products from `product_prices.txt`
- Categorizes products (Inverters, Solar Panels, Batteries, etc.)
- Generates product codes
- Sets wholesale and retail prices (25% markup)

**Products Imported:** 65 products including:
- **Inverters:** Deye, Solis, Sungrow, Luxpower (15 products)
- **Solar Panels:** Lvtopsun, LONGi (5 products)
- **Batteries:** DEYE, LVtopsun, LV GEL (14 products)
- **Water Pumps:** DC pumps (9 products)
- **Monitoring:** Smart meters, WiFi (5 products)
- **Accessories:** Cables, rails, clamps (5 products)

**How to import:**
```bash
cd khsolar_desktop
python database\import_products.py
```

**Result:**
```
✓ Imported: Deye Hybrid 8kw EU 1P ($1320.00)
✓ Imported: Lvtopsun 550W ($66.00)
✓ Imported: DEYE 100AH 51.2v (5.12KWH) ($1440.00)
... (all 65 products)

✅ Successfully imported 65 products!
```

---

### 2. Online Order Synchronization 🌐

**What it does:**
- When customers generate reports on your website
- Their data automatically syncs to desktop app
- Creates pending invoices with customer information
- Marks orders as "Website" source (highlighted in blue)

**Flow:**
```
Customer uses website → Generates solar system report → 
Data exported → Desktop app imports → Pending invoice created
```

**Customer data captured:**
- Name, phone, email, address
- Selected products and quantities
- Total amount
- Full system report (saved as JSON)

---

## 🚀 How to Use

### A. Running the Desktop App with Web Products

**Step 1:** Import products (one-time setup)
```bash
cd khsolar_desktop
python database\import_products.py
```

**Step 2:** Run the desktop app
```bash
python main.py
```

**Step 3:** View products
- Go to **"📦 Products & Prices"** tab
- See all 65 products imported from web
- Search, filter by category
- View wholesale & retail prices

---

### B. Syncing Online Orders

**Method 1: Auto Sync (Demo)**
1. Open desktop app
2. Go to **"💰 Sales Management"** tab
3. Click **"🌐 Sync Online Orders"** button
4. Sample online order is imported
5. Shows as pending invoice with blue "Website" label

**Method 2: Manual Import (From Website)**
When you deploy website order export:

1. Customer fills out form on website
2. System exports order to JSON file
3. Place JSON file in `khsolar_desktop/sync_data/` folder
4. Click **"🌐 Sync Online Orders"**
5. Order appears as pending invoice

---

## 📊 Sales Management Features

### View Online Orders

**How to identify:**
- **Source** column shows "Website" (highlighted in blue)
- Invoice number: `INV-YYYYMMDD-####`
- Status: "Pending" (yellow)
- Payment: "Pending" (no payment yet)

**What you can do:**
1. **View Details** - See full customer info and report data
2. **Update Status** - Mark as "Completed" after confirmation
3. **Generate Invoice** - Create PDF invoice
4. **Process Payment** - Update payment percentage
5. **Contact Customer** - Phone/email available

---

## 📝 Order Data Format

When website exports customer report, it creates JSON:

```json
{
  "customer_name": "John Doe",
  "customer_phone": "+855 12 345 678",
  "customer_email": "john@email.com",
  "customer_address": "Phnom Penh",
  "items": [
    {
      "product_name": "Deye Hybrid 8kw EU 1P",
      "quantity": 1,
      "unit_price": 1320.00
    },
    {
      "product_name": "Lvtopsun 550W",
      "quantity": 16,
      "unit_price": 66.00
    }
  ],
  "total_amount": 2376.00,
  "notes": "Generated from website",
  "report_data": {
    "system_type": "8kW System",
    "daily_consumption": "25 kWh",
    ...
  }
}
```

---

## 🔄 Website Integration (Future)

### Phase 1: Manual Export (Current)
- Customer generates report on website
- Download JSON export
- Manually place in `sync_data/` folder
- Click sync button

### Phase 2: Email Integration (Planned)
- Customer submits form
- Email sent to you with JSON attachment
- Desktop app auto-detects emails
- One-click import

### Phase 3: API Integration (Future)
- Real-time sync via REST API
- Webhook notifications
- Automatic order creation
- Live status updates

---

## 📁 File Structure

```
khsolar_desktop/
├── database/
│   ├── db_manager.py         # ✅ Database operations
│   ├── import_products.py    # ✅ Import from web
│   └── schema.sql            # Database schema
├── modules/
│   └── web_sync.py           # ✅ Web order sync
├── ui/
│   ├── products_tab.py       # ✅ Shows web products
│   └── sales_tab.py          # ✅ Sync button + online orders
├── data/
│   └── khsolar.db            # SQLite database (created automatically)
└── sync_data/
    ├── online_order_*.json   # Pending orders to import
    └── imported/             # Archived imported orders
```

---

## 💡 Usage Examples

### Example 1: Customer Generated Report on Website

**Website Flow:**
1. Customer: "I need 8kW solar system"
2. Fills in daily consumption: 25 kWh
3. Website calculates: 1x 8kW inverter, 16x 550W panels, 2x batteries
4. Customer submits: name, phone, email, address
5. Website exports order JSON

**Desktop Flow:**
1. You receive JSON file (via email or download)
2. Place in `sync_data/` folder
3. Open desktop app → Sales tab
4. Click "🌐 Sync Online Orders"
5. See new pending invoice:
   ```
   Invoice: INV-20241111-0001
   Customer: John Doe (+855 12 345 678)
   Source: Website (blue badge)
   Total: $5,856.00
   Status: Pending
   ```
6. Call customer to confirm
7. Update status to "Completed"
8. Generate invoice PDF

---

### Example 2: Viewing Product Catalog

**Desktop App:**
1. Go to Products tab
2. See all 65 products from web
3. Search "Deye" → See all Deye inverters
4. Filter by "Inverters" → See 15 inverter models
5. Check prices:
   - Wholesale: $888.00
   - Retail: $1,110.00 (25% markup)

---

## 🎯 Benefits

### For You:
✅ **No manual data entry** - Products auto-imported  
✅ **Centralized pricing** - One source of truth (web app)  
✅ **Online leads captured** - Every website visitor becomes a lead  
✅ **Efficient workflow** - Desktop for office, web for customers  
✅ **Better tracking** - Know which orders came from website  

### For Customers:
✅ **24/7 access** - Generate reports anytime  
✅ **Instant quotes** - See prices immediately  
✅ **Easy submission** - Just fill a form  
✅ **Professional** - Automated system  

---

## 🔧 Troubleshooting

### Products not showing?
**Run import script:**
```bash
cd khsolar_desktop
python database\import_products.py
```

### Sync button not working?
**Check:**
1. Database exists: `data/khsolar.db`
2. `sync_data/` folder exists
3. JSON format is correct

### Need to re-import products?
**Delete database and re-import:**
```bash
del data\khsolar.db
python database\import_products.py
```

---

## 📞 Summary

✅ **Imported:** 65 products from web catalog  
✅ **Feature:** Online order sync  
✅ **Database:** SQLite with full product catalog  
✅ **UI:** Updated to show web products & online orders  
✅ **Ready:** For testing and production use  

**Total Products:** 65  
**Categories:** 6  
**Integration:** Web → Desktop  
**Status:** Fully Functional ✨  

---

**Contact:** 📞 +855 888 836 588 | 💬 @chhanycls
