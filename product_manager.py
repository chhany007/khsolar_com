"""
Product and Cost Management Module
"""
import json
import os
import re
from typing import List, Dict
from models import Product

class ProductManager:
    """Manages solar system products and pricing"""
    
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.load_default_products()
    
    def load_default_products(self):
        """Load products from product_prices.txt file"""
        # Try to load from product_prices.txt
        prices_file = "product_prices.txt"
        if os.path.exists(prices_file):
            self._load_from_file(prices_file)
        else:
            # Fallback to empty catalog if file not found
            print(f"Warning: {prices_file} not found. Product catalog will be empty.")
    
    def _parse_price_line(self, line: str) -> tuple:
        """Parse a line from product_prices.txt"""
        # Format: "Product Name: $Price"
        if ':' in line and '$' in line:
            parts = line.split(':')
            name = parts[0].strip()
            price_str = parts[1].strip().replace('$', '').replace(',', '')
            try:
                price = float(price_str)
                return name, price
            except ValueError:
                return None, None
        return None, None
    
    def _categorize_product(self, name: str, price: float) -> tuple:
        """Categorize product and extract specifications"""
        name_lower = name.lower()
        
        # Batteries - Check FIRST before PV panels to avoid misclassification
        if any(word in name_lower for word in ['battery', 'ah', 'gel', 'lithium']):
            # Extract capacity
            if 'kwh' in name_lower:
                kwh_match = re.search(r'([\d.]+)kwh', name_lower)
                capacity_kwh = float(kwh_match.group(1)) if kwh_match else 5.0
            elif 'ah' in name_lower:
                ah_match = re.search(r'(\d+)ah', name_lower)
                ah = int(ah_match.group(1)) if ah_match else 100
                voltage_match = re.search(r'([\d.]+)v', name_lower)
                voltage = float(voltage_match.group(1)) if voltage_match else 12
                capacity_kwh = (ah * voltage) / 1000
            else:
                capacity_kwh = 5.0
            
            # Extract voltage
            voltage_match = re.search(r'([\d.]+)v', name_lower)
            voltage = float(voltage_match.group(1)) if voltage_match else 48
            
            # Battery type
            battery_type = "Lithium" if "lithium" in name_lower else "Gel" if "gel" in name_lower else "Lead-Acid"
            dod = 0.9 if battery_type == "Lithium" else 0.5
            cycles = 6000 if battery_type == "Lithium" else 1500
            
            specs = {"capacity": capacity_kwh, "voltage": voltage, "dod": dod, "cycles": cycles, "type": battery_type}
            supplier = "Deye" if "deye" in name_lower else "Lvtopsun" if "lvtopsun" in name_lower else "LV"
            
            return "battery", specs, supplier, f"{battery_type} battery for energy storage"
        
        # Solar Panels - Now safe to check for lvtopsun since batteries are already filtered
        elif any(brand in name_lower for brand in ['lvtopsun', 'longi', 'panel']) and 'w' in name_lower:
            # Extract wattage
            wattage_match = re.search(r'(\d+)w', name_lower)
            wattage = int(wattage_match.group(1)) if wattage_match else 400
            
            # Determine voltage and efficiency based on wattage
            voltage = 48 if wattage >= 400 else 24
            efficiency = 0.22 if wattage >= 500 else 0.21
            
            specs = {"power": wattage, "efficiency": efficiency, "voltage": voltage}
            supplier = "Lvtopsun" if "lvtopsun" in name_lower else "LONGi" if "longi" in name_lower else "Generic"
            
            return "pv_panel", specs, supplier, "High efficiency monocrystalline solar panel"
        
        # Inverters
        elif any(brand in name_lower for brand in ['sungrow', 'solis', 'deye', 'luxpower', 'inverter']):
            # Extract power rating in kW
            kw_match = re.search(r'(\d+)kw', name_lower)
            if kw_match:
                power_kw = int(kw_match.group(1))
            else:
                # Try to extract from model number (e.g., SG33CX = 33kW)
                model_match = re.search(r'sg(\d+)cx', name_lower)
                if model_match:
                    power_kw = int(model_match.group(1))
                else:
                    power_kw = 5  # Default
            
            # Determine inverter type and specs
            inv_type = "Hybrid" if "hybrid" in name_lower else "On-Grid" if any(x in name_lower for x in ['ongrid', 'sungrow', 'solis']) else "Off-Grid"
            voltage = 48 if "low voltage" not in name_lower else 380 if "high voltage" in name_lower else 48
            efficiency = 0.98 if "sungrow" in name_lower else 0.97
            
            specs = {"power": power_kw, "efficiency": efficiency, "voltage": voltage, "type": inv_type}
            supplier = "Sungrow" if "sungrow" in name_lower else "Solis" if "solis" in name_lower else "Deye" if "deye" in name_lower else "Luxpower" if "luxpower" in name_lower else "LV"
            
            return "inverter", specs, supplier, f"{inv_type} inverter for solar systems"
        
        # Controllers
        elif "controller" in name_lower:
            specs = {"capacity": 100, "voltage": 51.2}
            supplier = "Deye" if "deye" in name_lower else "Lvtopsun" if "lvtopsun" in name_lower else "Generic"
            return "controller", specs, supplier, "Battery management controller"
        
        # Cables
        elif "cable" in name_lower:
            mm_match = re.search(r'(\d+)mm', name_lower)
            mm_size = int(mm_match.group(1)) if mm_match else 4
            specs = {"size_mm": mm_size, "length_m": 100}
            return "cable", specs, "LV", "PV cable for solar installations"
        
        # Mounting accessories
        elif any(word in name_lower for word in ['rail', 'clamp', 'feet', 'connector']):
            specs = {"type": "mounting"}
            return "mounting", specs, "Generic", "Mounting hardware for solar panels"
        
        # Smart Meters and Monitoring
        elif any(word in name_lower for word in ['meter', 'wifi', 'winet', 'eyema', 'com100e']):
            specs = {"type": "monitoring"}
            supplier = "Weidmuller" if "weidmuller" in name_lower else "Acrel" if "acrel" in name_lower else "Generic"
            return "monitoring", specs, supplier, "Smart meter for energy monitoring"
        
        # Battery Racks
        elif "rack" in name_lower:
            capacity_match = re.search(r'(\d+)\+1', name)
            capacity = int(capacity_match.group(1)) if capacity_match else 8
            specs = {"capacity": capacity, "type": "battery_rack"}
            return "accessory", specs, "Deye", f"Battery rack for {capacity}+1 units"
        
        # Water Pumps
        elif any(code in name for code in ['DPC', 'DSC', 'DCPM']):
            wattage_match = re.search(r'(\d+)w', name_lower)
            wattage = int(wattage_match.group(1)) if wattage_match else 1000
            specs = {"power": wattage, "type": "dc_pump"}
            return "pump", specs, "DC Solar", "DC solar water pump"
        
        # Default
        else:
            specs = {}
            return "accessory", specs, "Generic", "Solar system accessory"
    
    def _load_from_file(self, filepath: str):
        """Load products from the price file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            product_id_counter = 1
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                name, price = self._parse_price_line(line)
                if name and price:
                    category, specs, supplier, notes = self._categorize_product(name, price)
                    
                    # Generate product ID
                    category_prefix = category[:3].upper()
                    product_id = f"{category_prefix}{product_id_counter:03d}"
                    product_id_counter += 1
                    
                    # Determine warranty based on category
                    warranty_years = 25 if category == "pv_panel" else 10 if category == "battery" else 5 if category == "inverter" else 2
                    
                    product = Product(
                        product_id=product_id,
                        name=name,
                        category=category,
                        specifications=specs,
                        cost=price,
                        warranty_years=warranty_years,
                        supplier=supplier,
                        notes=notes
                    )
                    
                    self.products[product_id] = product
            
            print(f"Loaded {len(self.products)} products from {filepath}")
        except Exception as e:
            print(f"Error loading products from {filepath}: {e}")
    
    def add_product(self, product: Product):
        """Add a new product to the catalog"""
        self.products[product.product_id] = product
    
    def get_product(self, product_id: str) -> Product:
        """Get product by ID"""
        return self.products.get(product_id)
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get all products in a category"""
        return [p for p in self.products.values() if p.category == category]
    
    def calculate_system_cost(self, pv_id: str, pv_quantity: int, 
                            battery_id: str, inverter_id: str,
                            installation_cost: float = 0.0,
                            additional_costs: float = 0.0) -> Dict:
        """Calculate total system cost with breakdown"""
        pv = self.get_product(pv_id)
        battery = self.get_product(battery_id)
        inverter = self.get_product(inverter_id)
        
        pv_cost = pv.cost * pv_quantity if pv else 0
        battery_cost = battery.cost if battery else 0
        inverter_cost = inverter.cost if inverter else 0
        
        subtotal = pv_cost + battery_cost + inverter_cost
        total = subtotal + installation_cost + additional_costs
        
        return {
            "pv_cost": pv_cost,
            "pv_quantity": pv_quantity,
            "battery_cost": battery_cost,
            "inverter_cost": inverter_cost,
            "installation_cost": installation_cost,
            "additional_costs": additional_costs,
            "subtotal": subtotal,
            "total": total
        }
    
    def generate_quote(self, customer_name: str, system_config: Dict, 
                      cost_breakdown: Dict, currency: str = "USD") -> str:
        """Generate a customer quote/proposal"""
        quote = f"""
{'='*60}
SOLAR SYSTEM PROPOSAL
{'='*60}

Customer: {customer_name}
Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}
Currency: {currency}

SYSTEM CONFIGURATION:
------------------------------------------------------------
"""
        
        for key, value in system_config.items():
            quote += f"{key}: {value}\n"
        
        quote += f"""
COST BREAKDOWN:
------------------------------------------------------------
Solar Panels: {currency} {cost_breakdown['pv_cost']:,.2f} (x{cost_breakdown['pv_quantity']})
Battery: {currency} {cost_breakdown['battery_cost']:,.2f}
Inverter: {currency} {cost_breakdown['inverter_cost']:,.2f}
Installation: {currency} {cost_breakdown['installation_cost']:,.2f}
Additional Costs: {currency} {cost_breakdown['additional_costs']:,.2f}
------------------------------------------------------------
SUBTOTAL: {currency} {cost_breakdown['subtotal']:,.2f}
------------------------------------------------------------
TOTAL: {currency} {cost_breakdown['total']:,.2f}
{'='*60}

Thank you for considering solar energy!
"""
        return quote
    
    def compare_products(self, product_ids: List[str]) -> str:
        """Compare multiple products side by side"""
        products = [self.get_product(pid) for pid in product_ids if self.get_product(pid)]
        
        if not products:
            return "No products to compare"
        
        comparison = "PRODUCT COMPARISON\n" + "="*80 + "\n\n"
        
        # Table header
        comparison += f"{'Attribute':<20}"
        for p in products:
            comparison += f"{p.name:<25}"
        comparison += "\n" + "-"*80 + "\n"
        
        # Compare attributes
        attributes = ["cost", "warranty_years", "supplier"]
        for attr in attributes:
            comparison += f"{attr:<20}"
            for p in products:
                value = getattr(p, attr, "N/A")
                comparison += f"{str(value):<25}"
            comparison += "\n"
        
        # Specifications
        comparison += "\nSPECIFICATIONS:\n" + "-"*80 + "\n"
        all_spec_keys = set()
        for p in products:
            all_spec_keys.update(p.specifications.keys())
        
        for key in all_spec_keys:
            comparison += f"{key:<20}"
            for p in products:
                value = p.specifications.get(key, "N/A")
                comparison += f"{str(value):<25}"
            comparison += "\n"
        
        return comparison
    
    def get_recommended_panel(self, min_wattage: int = 400) -> Product:
        """Get a recommended solar panel based on minimum wattage"""
        panels = self.get_products_by_category("pv_panel")
        # Filter panels by minimum wattage and sort by best value (price per watt)
        suitable = [p for p in panels if p.specifications.get("power", 0) >= min_wattage]
        if suitable:
            # Sort by price per watt (lower is better)
            suitable.sort(key=lambda p: p.cost / p.specifications.get("power", 1))
            return suitable[0]
        # Fallback to any panel
        return panels[0] if panels else None
    
    def get_recommended_battery(self, min_capacity_kwh: float = 5.0) -> Product:
        """Get a recommended battery based on minimum capacity"""
        batteries = self.get_products_by_category("battery")
        # Filter by lithium batteries first (better for solar), then by capacity
        lithium = [b for b in batteries if b.specifications.get("type") == "Lithium" 
                   and b.specifications.get("capacity", 0) >= min_capacity_kwh]
        if lithium:
            # Sort by price per kWh
            lithium.sort(key=lambda b: b.cost / b.specifications.get("capacity", 1))
            return lithium[0]
        # Fallback to any battery meeting capacity
        suitable = [b for b in batteries if b.specifications.get("capacity", 0) >= min_capacity_kwh]
        return suitable[0] if suitable else (batteries[0] if batteries else None)
    
    def get_recommended_inverter(self, min_power_kw: float = 5.0, inverter_type: str = "Hybrid") -> Product:
        """Get a recommended inverter based on minimum power and type"""
        inverters = self.get_products_by_category("inverter")
        # Filter by type and power
        suitable = [inv for inv in inverters 
                    if inv.specifications.get("power", 0) >= min_power_kw
                    and inverter_type.lower() in inv.specifications.get("type", "").lower()]
        if suitable:
            # Sort by price per kW
            suitable.sort(key=lambda inv: inv.cost / inv.specifications.get("power", 1))
            return suitable[0]
        # Fallback to any inverter meeting power requirement
        any_suitable = [inv for inv in inverters if inv.specifications.get("power", 0) >= min_power_kw]
        return any_suitable[0] if any_suitable else (inverters[0] if inverters else None)
