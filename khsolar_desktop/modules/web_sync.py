"""
Web Synchronization Module
Syncs online customer reports to desktop app as pending invoices
"""

import json
import os
from datetime import datetime

class WebSync:
    """Handle synchronization with web app"""
    
    def __init__(self, db_manager):
        """Initialize web sync"""
        self.db = db_manager
        self.sync_folder = 'sync_data'
        os.makedirs(self.sync_folder, exist_ok=True)
    
    def import_online_order(self, order_data):
        """
        Import online customer report as pending invoice
        
        order_data format:
        {
            'customer_name': str,
            'customer_phone': str,
            'customer_email': str,
            'customer_address': str,
            'items': [
                {
                    'product_name': str,
                    'quantity': int,
                    'unit_price': float
                },
                ...
            ],
            'total_amount': float,
            'notes': str,
            'report_data': {...}  # Full report JSON
        }
        """
        try:
            # Create pending sale
            sale_id, invoice_number = self.db.add_sale(
                customer_name=order_data.get('customer_name', 'Online Customer'),
                customer_phone=order_data.get('customer_phone', ''),
                customer_email=order_data.get('customer_email', ''),
                customer_address=order_data.get('customer_address', ''),
                total_amount=order_data.get('total_amount', 0),
                sale_status='Pending',
                payment_status='Pending',
                payment_percentage=0,
                notes=order_data.get('notes', 'Imported from website'),
                source='Website',
                web_report_data=json.dumps(order_data.get('report_data', {}))
            )
            
            # Add sale items
            for item in order_data.get('items', []):
                self.db.add_sale_item(
                    sale_id=sale_id,
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    discount=item.get('discount', 0)
                )
            
            return True, invoice_number, sale_id
            
        except Exception as e:
            return False, str(e), None
    
    def save_order_to_file(self, order_data):
        """Save order data to JSON file for manual import"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"online_order_{timestamp}.json"
        filepath = os.path.join(self.sync_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(order_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_pending_orders(self):
        """Load all pending orders from sync folder"""
        if not os.path.exists(self.sync_folder):
            return []
        
        orders = []
        for filename in os.listdir(self.sync_folder):
            if filename.endswith('.json'):
                filepath = os.path.join(self.sync_folder, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        order_data = json.load(f)
                        orders.append({
                            'file': filename,
                            'data': order_data
                        })
                except:
                    continue
        
        return orders
    
    def import_order_from_file(self, filename):
        """Import order from JSON file"""
        filepath = os.path.join(self.sync_folder, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            order_data = json.load(f)
        
        success, result, sale_id = self.import_online_order(order_data)
        
        if success:
            # Archive the file
            archive_folder = os.path.join(self.sync_folder, 'imported')
            os.makedirs(archive_folder, exist_ok=True)
            os.rename(filepath, os.path.join(archive_folder, filename))
        
        return success, result, sale_id
    
    def parse_web_report(self, report_html_or_json):
        """
        Parse web report data into order format
        This can be called from web app export
        """
        # Example implementation - customize based on your web app format
        order_data = {
            'customer_name': '',
            'customer_phone': '',
            'customer_email': '',
            'customer_address': '',
            'items': [],
            'total_amount': 0,
            'notes': '',
            'report_data': {}
        }
        
        return order_data

def create_sample_online_order():
    """Create sample online order for testing"""
    return {
        'customer_name': 'Online Customer - Web Report',
        'customer_phone': '+855 12 999 888',
        'customer_email': 'customer@email.com',
        'customer_address': 'Phnom Penh, Cambodia',
        'items': [
            {
                'product_name': 'Deye Hybrid 8kw EU 1P',
                'quantity': 1,
                'unit_price': 1320.00,
                'discount': 0
            },
            {
                'product_name': 'Lvtopsun 550W',
                'quantity': 16,
                'unit_price': 66.00,
                'discount': 0
            },
            {
                'product_name': 'DEYE 100AH 51.2v (5.12KWH)',
                'quantity': 2,
                'unit_price': 1440.00,
                'discount': 0
            }
        ],
        'total_amount': 5856.00,
        'notes': 'Generated from website solar system report. Customer requested quote for 8kW hybrid system.',
        'report_data': {
            'system_type': '8kW Hybrid Solar System',
            'daily_consumption': '25 kWh',
            'panel_count': 16,
            'battery_count': 2,
            'generated_date': datetime.now().isoformat()
        }
    }
