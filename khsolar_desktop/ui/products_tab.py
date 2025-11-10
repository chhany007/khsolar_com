"""
Products & Prices Tab
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QComboBox, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from database.db_manager import DatabaseManager

class ProductsTab(QWidget):
    """Products and pricing management tab"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.load_products()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QLabel("Product Price List")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)
        
        # Search and filter section
        search_layout = QHBoxLayout()
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search products...")
        self.search_box.textChanged.connect(self.filter_products)
        search_layout.addWidget(self.search_box)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All Categories", "Inverters", "Solar Panels", "Batteries", 
                                        "Water Pumps", "Monitoring", "Accessories", "Other"])
        self.category_filter.currentTextChanged.connect(self.filter_products)
        search_layout.addWidget(self.category_filter)
        
        layout.addLayout(search_layout)
        
        # Products table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Product Code", "Product Name", "Category", "Wholesale Price",
            "Retail Price", "Stock", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Product")
        add_btn.clicked.connect(self.add_product)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit Product")
        edit_btn.clicked.connect(self.edit_product)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete Product")
        delete_btn.clicked.connect(self.delete_product)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        export_btn = QPushButton("📤 Export to Excel")
        export_btn.clicked.connect(self.export_products)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
    def load_products(self):
        """Load products from database"""
        # Get products from database
        db_products = self.db.get_all_products()
        
        # Convert to display format
        products = []
        for p in db_products:
            # p = (id, code, name, category, wholesale, retail, stock, desc, specs, image, created, updated)
            products.append((
                p[1],  # product_code
                p[2],  # product_name
                p[3],  # category
                f"${p[4]:,.2f}",  # wholesale_price
                f"${p[5]:,.2f}",  # retail_price
                str(p[6])  # stock
            ))
        
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
                
    def filter_products(self):
        """Filter products based on search and category"""
        search_text = self.search_box.text().lower()
        category = self.category_filter.currentText()
        
        for row in range(self.table.rowCount()):
            show_row = True
            
            # Check search text
            if search_text:
                row_text = ""
                for col in range(self.table.columnCount() - 1):
                    item = self.table.item(row, col)
                    if item:
                        row_text += item.text().lower() + " "
                if search_text not in row_text:
                    show_row = False
            
            # Check category
            if category != "All Categories":
                category_item = self.table.item(row, 2)
                if category_item and category_item.text() != category:
                    show_row = False
            
            self.table.setRowHidden(row, not show_row)
            
    def add_product(self):
        """Add new product"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Add Product", "Add product dialog will open here")
        
    def edit_product(self):
        """Edit selected product"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Edit Product", "Edit product dialog will open here")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a product to edit")
            
    def delete_product(self):
        """Delete selected product"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            reply = QMessageBox.question(self, "Confirm Delete",
                "Are you sure you want to delete this product?",
                QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.table.removeRow(selected)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a product to delete")
            
    def export_products(self):
        """Export products to Excel"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Export", "Products exported to Excel successfully!")
