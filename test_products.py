"""
Test script to verify product loading from product_prices.txt
"""
from product_manager import ProductManager

# Initialize product manager
print("Initializing ProductManager...")
pm = ProductManager()

print(f"\nTotal products loaded: {len(pm.products)}")

# Show products by category
categories = {}
for product in pm.products.values():
    if product.category not in categories:
        categories[product.category] = []
    categories[product.category].append(product)

print("\n=== Products by Category ===")
for category, products in sorted(categories.items()):
    print(f"\n{category.upper()} ({len(products)} products):")
    for p in products[:3]:  # Show first 3 of each category
        print(f"  - {p.name}: ${p.cost:.2f}")
    if len(products) > 3:
        print(f"  ... and {len(products) - 3} more")

# Test recommendation methods
print("\n=== Testing Recommendation Methods ===")
recommended_panel = pm.get_recommended_panel(min_wattage=500)
print(f"\nRecommended Panel (≥500W): {recommended_panel.name if recommended_panel else 'None found'}")
if recommended_panel:
    print(f"  Price: ${recommended_panel.cost:.2f}, Power: {recommended_panel.specifications.get('power')}W")

recommended_battery = pm.get_recommended_battery(min_capacity_kwh=5.0)
print(f"\nRecommended Battery (≥5kWh): {recommended_battery.name if recommended_battery else 'None found'}")
if recommended_battery:
    print(f"  Price: ${recommended_battery.cost:.2f}, Capacity: {recommended_battery.specifications.get('capacity')}kWh")

recommended_inverter = pm.get_recommended_inverter(min_power_kw=5.0, inverter_type="Hybrid")
print(f"\nRecommended Inverter (≥5kW Hybrid): {recommended_inverter.name if recommended_inverter else 'None found'}")
if recommended_inverter:
    print(f"  Price: ${recommended_inverter.cost:.2f}, Power: {recommended_inverter.specifications.get('power')}kW")

print("\n✅ Product loading test completed!")
