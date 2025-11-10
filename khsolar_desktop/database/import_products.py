"""
Import products from web app to desktop database
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager

def categorize_product(product_name):
    """Categorize product based on name"""
    name_lower = product_name.lower()
    
    if 'inverter' in name_lower or 'deye' in name_lower or 'solis' in name_lower or 'sungrow' in name_lower or 'luxpower' in name_lower:
        return 'Inverters'
    elif 'panel' in name_lower or 'lvtopsun' in name_lower or 'longi' in name_lower:
        return 'Solar Panels'
    elif 'battery' in name_lower or 'lithium' in name_lower or 'gel' in name_lower or 'ah' in name_lower:
        return 'Batteries'
    elif 'pump' in name_lower or 'dpc' in name_lower or 'dsc' in name_lower or 'dcpm' in name_lower:
        return 'Water Pumps'
    elif 'meter' in name_lower or 'wifi' in name_lower or 'com100' in name_lower or 'winet' in name_lower:
        return 'Monitoring'
    elif 'cable' in name_lower or 'rail' in name_lower or 'clamp' in name_lower or 'connector' in name_lower or 'feet' in name_lower:
        return 'Accessories'
    else:
        return 'Other'

def generate_product_code(product_name, category):
    """Generate product code"""
    category_prefix = {
        'Inverters': 'INV',
        'Solar Panels': 'PNL',
        'Batteries': 'BAT',
        'Water Pumps': 'PMP',
        'Monitoring': 'MON',
        'Accessories': 'ACC',
        'Other': 'OTH'
    }
    
    prefix = category_prefix.get(category, 'PRD')
    # Use first 3 letters of product name as unique identifier
    unique = ''.join(filter(str.isalnum, product_name[:10])).upper()
    return f"{prefix}-{unique}"

def import_products_from_file(file_path='../../product_prices.txt'):
    """Import products from product_prices.txt"""
    db = DatabaseManager()
    
    # Get absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    
    if not os.path.exists(full_path):
        print(f"Error: File not found: {full_path}")
        return
    
    print("Importing products from web app...")
    count = 0
    
    with open(full_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            
            # Parse line: "Product Name: $Price"
            parts = line.split(':', 1)
            if len(parts) != 2:
                continue
            
            product_name = parts[0].strip()
            price_str = parts[1].strip().replace('$', '').replace(',', '')
            
            try:
                wholesale_price = float(price_str)
                retail_price = wholesale_price * 1.25  # 25% markup for retail
                
                category = categorize_product(product_name)
                product_code = generate_product_code(product_name, category)
                
                db.add_product(
                    product_code=product_code,
                    product_name=product_name,
                    category=category,
                    wholesale_price=wholesale_price,
                    retail_price=retail_price,
                    stock=100,  # Default stock
                    description=f"{product_name} - Imported from web catalog",
                    specs='',
                    image_url=''
                )
                
                count += 1
                print(f"✓ Imported: {product_name} (${wholesale_price:.2f})")
                
            except ValueError as e:
                print(f"✗ Error parsing price for {product_name}: {e}")
                continue
    
    print(f"\n✅ Successfully imported {count} products!")
    return count

def import_sample_customers():
    """Import sample customers"""
    db = DatabaseManager()
    
    customers = [
        ("Sok Pisey", "Business", "+855 12 345 678", "pisey@company.com", "Phnom Penh", "@pisey", "Solar Solutions Co.", "K001-123"),
        ("Chan Sophea", "Individual", "+855 87 654 321", "sophea@email.com", "Siem Reap", "", "", ""),
        ("Lim Dara", "VIP", "+855 98 765 432", "dara@business.com", "Battambang", "@dara", "Green Energy Ltd.", "K002-456"),
        ("Heng Srey", "Business", "+855 77 888 999", "srey@company.com", "Kampong Cham", "", "Solar Tech", "K003-789"),
        ("Pich Veasna", "Individual", "+855 12 111 222", "veasna@email.com", "Phnom Penh", "@veasna", "", ""),
        ("Mom Sothea", "VIP", "+855 99 333 444", "sothea@corp.com", "Phnom Penh", "@sothea", "Cambodia Solar Corp.", "K004-012"),
    ]
    
    count = 0
    for customer in customers:
        db.add_customer(*customer)
        count += 1
    
    print(f"✅ Imported {count} sample customers")
    return count

if __name__ == '__main__':
    print("=" * 60)
    print("KHSolar Desktop - Product Import Tool")
    print("=" * 60)
    print()
    
    # Import products
    import_products_from_file()
    print()
    
    # Import sample customers
    import_sample_customers()
    print()
    
    print("=" * 60)
    print("Import Complete!")
    print("=" * 60)
