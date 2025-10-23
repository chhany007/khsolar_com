"""
Test script to verify battery categorization is correct
"""
from product_manager import ProductManager

# Initialize product manager (products load automatically)
pm = ProductManager()

print("=" * 80)
print("BATTERY CATEGORIZATION TEST")
print("=" * 80)

# Get all products
all_products = list(pm.products.values())

# Check specific battery products
battery_names = [
    "LVtopsun-51.2V100AH Lithium",
    "LVtopsun-51.2V200AH Lithium",
    "LVtopsun-51.2V300AH Lithium",
    "LVtopsun-51.2V100AH Lithium HV",
    "DEYE 100AH 51.2v (5.12KWH)",
    "LV 100AH 12V GEL",
    "LV 150AH 12V GEL BATTERY",
    "LV 200AH 12V GEL BATTERY",
    "LV 250AH 12V GEL BATTERY"
]

print("\n✅ CHECKING BATTERY PRODUCTS:\n")
for product in all_products:
    if any(name.lower() in product.name.lower() for name in battery_names):
        status = "✅ CORRECT" if product.category == "battery" else "❌ WRONG"
        print(f"{status} | {product.name:<45} | Category: {product.category:<15} | Capacity: {product.specifications.get('capacity', 'N/A')} kWh")

# Check PV panels
print("\n" + "=" * 80)
print("✅ CHECKING PV PANELS:\n")
pv_names = ["Lvtopsun 340W", "Lvtopsun 550W", "Lvtopsun 620W", "LONGi Panel 360w", "LONGi Panel 585w"]
for product in all_products:
    if any(name.lower() in product.name.lower() for name in pv_names):
        status = "✅ CORRECT" if product.category == "pv_panel" else "❌ WRONG"
        print(f"{status} | {product.name:<45} | Category: {product.category:<15} | Power: {product.specifications.get('power', 'N/A')} W")

# Summary by category
print("\n" + "=" * 80)
print("📊 CATEGORY SUMMARY:\n")
categories = {}
for product in all_products:
    if product.category not in categories:
        categories[product.category] = []
    categories[product.category].append(product.name)

for category in sorted(categories.keys()):
    print(f"\n{category.upper()} ({len(categories[category])} products):")
    for product_name in sorted(categories[category]):
        print(f"  • {product_name}")

print("\n" + "=" * 80)
print("TEST COMPLETE!")
print("=" * 80)
