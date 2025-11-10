"""
Inventory Alerts Dialog
Shows low stock and out of stock alerts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from modules.inventory_manager import InventoryManager

class InventoryAlertsDialog(QDialog):
    """Dialog showing inventory alerts and warnings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inventory = InventoryManager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("📦 Inventory Alerts & Stock Management")
        self.setGeometry(200, 200, 900, 600)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QLabel("Inventory Management & Alerts")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color: #667eea; padding: 10px;")
        layout.addWidget(header)
        
        # Get inventory report
        report = self.inventory.generate_stock_report()
        
        # Summary cards
        summary_layout = QHBoxLayout()
        
        # Total products card
        summary_layout.addWidget(self.create_summary_card(
            "Total Products", 
            str(report['total_products']), 
            "#3b82f6"
        ))
        
        # Total stock card
        summary_layout.addWidget(self.create_summary_card(
            "Total Stock Items", 
            str(report['total_stock_items']), 
            "#10b981"
        ))
        
        # Low stock alerts card
        summary_layout.addWidget(self.create_summary_card(
            "Low Stock Alerts", 
            str(report['low_stock_count']), 
            "#f59e0b"
        ))
        
        # Critical alerts card
        summary_layout.addWidget(self.create_summary_card(
            "Critical Alerts", 
            str(len(report['critical_items'])), 
            "#ef4444"
        ))
        
        layout.addLayout(summary_layout)
        
        # Inventory value
        value_info = report['inventory_value']
        value_label = QLabel(
            f"💰 Inventory Value: Wholesale ${value_info['wholesale_value']:,.2f} | "
            f"Retail ${value_info['retail_value']:,.2f} | "
            f"Potential Profit ${value_info['potential_profit']:,.2f}"
        )
        value_label.setStyleSheet("padding: 10px; background: #f0f9ff; border-radius: 8px; font-weight: 600;")
        layout.addWidget(value_label)
        
        # Tabs
        tabs = QTabWidget()
        
        # Low Stock tab
        if report['alerts']:
            low_stock_widget = self.create_alerts_table(report['alerts'])
            tabs.addTab(low_stock_widget, f"⚠️ Low Stock ({report['low_stock_count']})")
        
        # Critical tab
        if report['critical_items']:
            critical_widget = self.create_alerts_table(report['critical_items'])
            tabs.addTab(critical_widget, f"🚨 Critical ({len(report['critical_items'])})")
        
        # Category breakdown tab
        category_widget = self.create_category_table(report['category_breakdown'])
        tabs.addTab(category_widget, "📊 Category Summary")
        
        # Reorder list tab
        reorder_list = self.inventory.generate_reorder_list()
        if reorder_list:
            reorder_widget = self.create_reorder_table(reorder_list)
            tabs.addTab(reorder_widget, f"🛒 Reorder List ({len(reorder_list)})")
        
        layout.addWidget(tabs)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh)
        btn_layout.addWidget(refresh_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def create_summary_card(self, title, value, color):
        """Create a summary card"""
        from PyQt5.QtWidgets import QFrame
        
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #6b7280;")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 24px; color: {color}; font-weight: bold;")
        card_layout.addWidget(value_label)
        
        return card
    
    def create_alerts_table(self, alerts):
        """Create table for low/critical stock alerts"""
        from PyQt5.QtWidgets import QWidget
        
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Product Code", "Product Name", "Category", "Current Stock", "Reorder Qty"
        ])
        table.setRowCount(len(alerts))
        
        for row, alert in enumerate(alerts):
            # Product code
            item = QTableWidgetItem(alert['product_code'])
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, item)
            
            # Product name
            item = QTableWidgetItem(alert['product_name'])
            table.setItem(row, 1, item)
            
            # Category
            item = QTableWidgetItem(alert['category'])
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, item)
            
            # Current stock
            item = QTableWidgetItem(str(alert['current_stock']))
            item.setTextAlignment(Qt.AlignCenter)
            if alert['status'] == 'CRITICAL':
                item.setBackground(QColor("#fee2e2"))
                item.setForeground(QColor("#dc2626"))
            else:
                item.setBackground(QColor("#fef3c7"))
                item.setForeground(QColor("#d97706"))
            item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            table.setItem(row, 3, item)
            
            # Reorder quantity
            item = QTableWidgetItem(str(alert['reorder_qty']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#dcfce7"))
            table.setItem(row, 4, item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        return widget
    
    def create_category_table(self, category_breakdown):
        """Create table for category breakdown"""
        from PyQt5.QtWidgets import QWidget
        
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels([
            "Category", "Product Count", "Total Stock", "Total Value"
        ])
        table.setRowCount(len(category_breakdown))
        
        for row, (category, data) in enumerate(category_breakdown.items()):
            # Category
            item = QTableWidgetItem(category)
            item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            table.setItem(row, 0, item)
            
            # Product count
            item = QTableWidgetItem(str(data['count']))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, item)
            
            # Total stock
            item = QTableWidgetItem(str(data['total_stock']))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, item)
            
            # Total value
            item = QTableWidgetItem(f"${data['value']:,.2f}")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 3, item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        return widget
    
    def create_reorder_table(self, reorder_list):
        """Create table for reorder recommendations"""
        from PyQt5.QtWidgets import QWidget
        
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        info = QLabel("💡 Suggested reorder quantities based on current stock levels")
        info.setStyleSheet("padding: 10px; background: #eff6ff; border-radius: 6px;")
        layout.addWidget(info)
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Priority", "Product Code", "Product Name", "Current Stock", "Suggested Qty"
        ])
        table.setRowCount(len(reorder_list))
        
        for row, item_data in enumerate(reorder_list):
            # Priority
            item = QTableWidgetItem(item_data['priority'])
            item.setTextAlignment(Qt.AlignCenter)
            if item_data['priority'] == 'HIGH':
                item.setBackground(QColor("#fee2e2"))
                item.setForeground(QColor("#dc2626"))
            else:
                item.setBackground(QColor("#fef3c7"))
                item.setForeground(QColor("#d97706"))
            item.setFont(QFont("Segoe UI", 9, QFont.Bold))
            table.setItem(row, 0, item)
            
            # Product code
            item = QTableWidgetItem(item_data['product_code'])
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, item)
            
            # Product name
            item = QTableWidgetItem(item_data['product_name'])
            table.setItem(row, 2, item)
            
            # Current stock
            item = QTableWidgetItem(str(item_data['current_stock']))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 3, item)
            
            # Suggested quantity
            item = QTableWidgetItem(str(item_data['suggested_qty']))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#dcfce7"))
            item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            table.setItem(row, 4, item)
        
        table.resizeColumnsToContents()
        layout.addWidget(table)
        
        return widget
    
    def refresh(self):
        """Refresh the dialog"""
        self.close()
        new_dialog = InventoryAlertsDialog(self.parent())
        new_dialog.exec_()
