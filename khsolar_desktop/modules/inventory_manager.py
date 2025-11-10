"""
Inventory Management System
Track stock, alerts, and reorder points
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager

class InventoryManager:
    """Manage product inventory and stock levels"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.low_stock_threshold = 10  # Alert when stock below this
        self.critical_stock_threshold = 5  # Critical alert
    
    def get_low_stock_items(self):
        """Get products with low stock"""
        products = self.db.get_all_products()
        low_stock = []
        
        for p in products:
            # p = (id, code, name, category, wholesale, retail, stock, desc, specs, image, created, updated)
            stock = p[6]
            if stock <= self.low_stock_threshold:
                status = 'CRITICAL' if stock <= self.critical_stock_threshold else 'LOW'
                low_stock.append({
                    'product_code': p[1],
                    'product_name': p[2],
                    'category': p[3],
                    'current_stock': stock,
                    'status': status,
                    'reorder_qty': max(50, stock * 5)  # Suggest reorder quantity
                })
        
        return low_stock
    
    def get_out_of_stock_items(self):
        """Get products that are out of stock"""
        products = self.db.get_all_products()
        return [p for p in products if p[6] <= 0]
    
    def update_stock(self, product_code, quantity_change, reason=''):
        """
        Update product stock
        quantity_change: positive for adding stock, negative for removing
        """
        self.db.update_product_stock(product_code, quantity_change)
        
        # Log the change (could add to a stock_movements table later)
        return True
    
    def get_stock_value(self):
        """Calculate total inventory value"""
        products = self.db.get_all_products()
        total_wholesale = sum(p[4] * p[6] for p in products)  # wholesale_price * stock
        total_retail = sum(p[5] * p[6] for p in products)  # retail_price * stock
        
        return {
            'wholesale_value': total_wholesale,
            'retail_value': total_retail,
            'potential_profit': total_retail - total_wholesale
        }
    
    def get_stock_summary_by_category(self):
        """Get stock summary grouped by category"""
        products = self.db.get_all_products()
        summary = {}
        
        for p in products:
            category = p[3]
            if category not in summary:
                summary[category] = {
                    'count': 0,
                    'total_stock': 0,
                    'value': 0
                }
            
            summary[category]['count'] += 1
            summary[category]['total_stock'] += p[6]
            summary[category]['value'] += p[5] * p[6]
        
        return summary
    
    def get_fast_moving_items(self, days=30):
        """Get products that sell frequently (based on sales data)"""
        # This would require tracking sale_items over time
        # For now, return empty list - implement when sales history is available
        return []
    
    def get_slow_moving_items(self, days=90):
        """Get products that rarely sell"""
        # Similar to fast_moving - needs sales history
        return []
    
    def generate_stock_report(self):
        """Generate comprehensive stock report"""
        products = self.db.get_all_products()
        low_stock = self.get_low_stock_items()
        out_of_stock = self.get_out_of_stock_items()
        stock_value = self.get_stock_value()
        category_summary = self.get_stock_summary_by_category()
        
        report = {
            'total_products': len(products),
            'total_stock_items': sum(p[6] for p in products),
            'low_stock_count': len(low_stock),
            'out_of_stock_count': len(out_of_stock),
            'inventory_value': stock_value,
            'category_breakdown': category_summary,
            'alerts': low_stock,
            'critical_items': [item for item in low_stock if item['status'] == 'CRITICAL']
        }
        
        return report
    
    def predict_restock_date(self, product_code, current_stock, avg_daily_sales):
        """Predict when product will run out"""
        if avg_daily_sales <= 0:
            return None
        
        days_remaining = current_stock / avg_daily_sales
        return int(days_remaining)
    
    def generate_reorder_list(self):
        """Generate list of products that need reordering"""
        low_stock = self.get_low_stock_items()
        
        reorder_list = []
        for item in low_stock:
            reorder_list.append({
                'product_code': item['product_code'],
                'product_name': item['product_name'],
                'current_stock': item['current_stock'],
                'suggested_qty': item['reorder_qty'],
                'priority': 'HIGH' if item['status'] == 'CRITICAL' else 'MEDIUM'
            })
        
        return reorder_list
