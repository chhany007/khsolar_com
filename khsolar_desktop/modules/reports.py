"""
Business Reports and Analytics
Generate sales reports, financial summaries, and insights
"""

import sys
import os
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager

class ReportGenerator:
    """Generate business reports and analytics"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.reports_folder = 'reports'
        os.makedirs(self.reports_folder, exist_ok=True)
    
    def generate_sales_report(self, start_date=None, end_date=None):
        """Generate sales report for date range"""
        sales = self.db.get_all_sales()
        
        if not sales:
            return {'error': 'No sales data available'}
        
        # Filter by date if provided
        if start_date or end_date:
            # Date filtering logic here
            pass
        
        total_sales = len(sales)
        total_revenue = sum(sale[4] for sale in sales)
        total_paid = sum(sale[4] * (sale[5] / 100) for sale in sales)
        total_pending = total_revenue - total_paid
        
        # Status breakdown
        pending = sum(1 for sale in sales if sale[6] == 'Pending')
        completed = sum(1 for sale in sales if sale[6] == 'Completed')
        cancelled = sum(1 for sale in sales if sale[6] == 'Cancelled')
        
        # Source breakdown
        web_sales = sum(1 for sale in sales if len(sale) > 7 and sale[7] == 'Website')
        desktop_sales = total_sales - web_sales
        
        report = {
            'period': f"{start_date or 'All'} to {end_date or 'All'}",
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'total_paid': total_paid,
            'total_pending': total_pending,
            'payment_rate': (total_paid / total_revenue * 100) if total_revenue > 0 else 0,
            'status_breakdown': {
                'pending': pending,
                'completed': completed,
                'cancelled': cancelled
            },
            'source_breakdown': {
                'website': web_sales,
                'desktop': desktop_sales
            },
            'average_sale_value': total_revenue / total_sales if total_sales > 0 else 0
        }
        
        return report
    
    def generate_customer_report(self):
        """Generate customer analytics"""
        customers = self.db.get_all_customers()
        sales = self.db.get_all_sales()
        
        total_customers = len(customers)
        
        # Customer type breakdown
        customer_types = {}
        for customer in customers:
            ctype = customer[3]  # customer_type
            customer_types[ctype] = customer_types.get(ctype, 0) + 1
        
        # Top customers (by purchase count)
        customer_purchases = {}
        for sale in sales:
            customer_name = sale[3]
            customer_purchases[customer_name] = customer_purchases.get(customer_name, 0) + 1
        
        top_customers = sorted(customer_purchases.items(), key=lambda x: x[1], reverse=True)[:10]
        
        report = {
            'total_customers': total_customers,
            'customer_types': customer_types,
            'top_customers': top_customers,
            'average_purchases_per_customer': len(sales) / total_customers if total_customers > 0 else 0
        }
        
        return report
    
    def generate_product_performance_report(self):
        """Analyze product performance"""
        products = self.db.get_all_products()
        sales = self.db.get_all_sales()
        
        # Get all sale items to see what's selling
        product_sales = {}
        for sale in sales:
            sale_id = sale[0]
            _, items = self.db.get_sale_details(sale_id)
            
            for item in items:
                product_name = item[2]  # product_name from sale_items
                quantity = item[3]  # quantity
                revenue = item[6]  # subtotal
                
                if product_name not in product_sales:
                    product_sales[product_name] = {
                        'quantity_sold': 0,
                        'revenue': 0,
                        'sales_count': 0
                    }
                
                product_sales[product_name]['quantity_sold'] += quantity
                product_sales[product_name]['revenue'] += revenue
                product_sales[product_name]['sales_count'] += 1
        
        # Sort by revenue
        top_products = sorted(product_sales.items(), 
                            key=lambda x: x[1]['revenue'], 
                            reverse=True)[:10]
        
        report = {
            'total_products': len(products),
            'products_sold': len(product_sales),
            'top_products_by_revenue': top_products,
            'total_units_sold': sum(p['quantity_sold'] for p in product_sales.values())
        }
        
        return report
    
    def generate_profit_analysis(self):
        """Calculate profit margins and profitability"""
        products = self.db.get_all_products()
        sales = self.db.get_all_sales()
        
        total_cost = 0
        total_revenue = 0
        
        for sale in sales:
            sale_id = sale[0]
            _, items = self.db.get_sale_details(sale_id)
            
            for item in items:
                product_name = item[2]
                quantity = item[3]
                revenue = item[6]  # subtotal
                
                # Find product to get cost
                product = next((p for p in products if p[2] == product_name), None)
                if product:
                    cost = product[4] * quantity  # wholesale_price * quantity
                    total_cost += cost
                    total_revenue += revenue
        
        profit = total_revenue - total_cost
        profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
        
        report = {
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'gross_profit': profit,
            'profit_margin': profit_margin,
            'markup_percentage': (profit / total_cost * 100) if total_cost > 0 else 0
        }
        
        return report
    
    def generate_monthly_summary(self, year=None, month=None):
        """Generate monthly business summary"""
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        
        sales_report = self.generate_sales_report()
        customer_report = self.generate_customer_report()
        product_report = self.generate_product_performance_report()
        profit_report = self.generate_profit_analysis()
        
        summary = {
            'period': f"{year}-{month:02d}",
            'sales': sales_report,
            'customers': customer_report,
            'products': product_report,
            'profitability': profit_report
        }
        
        return summary
    
    def export_to_excel(self, data, filename):
        """Export data to Excel file"""
        filepath = os.path.join(self.reports_folder, filename)
        
        # Convert to DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # Export
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return filepath
    
    def generate_dashboard_metrics(self):
        """Generate key metrics for dashboard"""
        sales = self.db.get_all_sales()
        products = self.db.get_all_products()
        customers = self.db.get_all_customers()
        
        # Today's sales
        today = datetime.now().strftime('%Y-%m-%d')
        today_sales = [s for s in sales if s[2] == today]
        
        # This month's sales
        current_month = datetime.now().strftime('%Y-%m')
        month_sales = [s for s in sales if s[2].startswith(current_month)]
        
        # Pending orders
        pending = [s for s in sales if s[6] == 'Pending']
        
        # Low stock items
        low_stock = [p for p in products if p[6] <= 10]
        
        metrics = {
            'today_sales_count': len(today_sales),
            'today_revenue': sum(s[4] for s in today_sales),
            'month_sales_count': len(month_sales),
            'month_revenue': sum(s[4] for s in month_sales),
            'pending_orders': len(pending),
            'low_stock_alerts': len(low_stock),
            'total_customers': len(customers),
            'total_products': len(products)
        }
        
        return metrics
    
    def get_sales_trend(self, days=30):
        """Get sales trend for last N days"""
        sales = self.db.get_all_sales()
        
        # Group by date
        daily_sales = {}
        for sale in sales:
            date = sale[2]
            if date not in daily_sales:
                daily_sales[date] = {'count': 0, 'revenue': 0}
            daily_sales[date]['count'] += 1
            daily_sales[date]['revenue'] += sale[4]
        
        # Sort by date
        sorted_sales = sorted(daily_sales.items())
        
        return sorted_sales
