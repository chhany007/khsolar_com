"""
Customer Management Tab
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CustomersTab(QWidget):
    """Customer database management tab"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_customers()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QLabel("Customer Database")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)
        
        # Search and filter
        search_layout = QHBoxLayout()
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search by name, phone, email...")
        self.search_box.textChanged.connect(self.filter_customers)
        search_layout.addWidget(self.search_box)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Customers", "Individual", "Business", "VIP"])
        self.type_filter.currentTextChanged.connect(self.filter_customers)
        search_layout.addWidget(self.type_filter)
        
        layout.addLayout(search_layout)
        
        # Customer table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Customer ID", "Name", "Type", "Phone", "Email",
            "Total Purchases", "Last Purchase", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # Summary
        summary_layout = QHBoxLayout()
        
        self.total_customers_label = QLabel("Total Customers: 0")
        self.total_customers_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        summary_layout.addWidget(self.total_customers_label)
        
        summary_layout.addStretch()
        
        self.individual_label = QLabel("Individual: 0")
        summary_layout.addWidget(self.individual_label)
        
        self.business_label = QLabel("Business: 0")
        summary_layout.addWidget(self.business_label)
        
        self.vip_label = QLabel("VIP: 0")
        summary_layout.addWidget(self.vip_label)
        
        layout.addLayout(summary_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Customer")
        add_btn.clicked.connect(self.add_customer)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit Customer")
        edit_btn.clicked.connect(self.edit_customer)
        button_layout.addWidget(edit_btn)
        
        view_btn = QPushButton("👁️ View Details")
        view_btn.clicked.connect(self.view_customer)
        button_layout.addWidget(view_btn)
        
        history_btn = QPushButton("📋 Purchase History")
        history_btn.clicked.connect(self.view_history)
        button_layout.addWidget(history_btn)
        
        button_layout.addStretch()
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self.export_customers)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
    def load_customers(self):
        """Load customer data"""
        # Sample customer data
        customers = [
            ("CUS-001", "Sok Pisey", "Business", "+855 12 345 678", "pisey@company.com", "$18,500", "2024-11-01"),
            ("CUS-002", "Chan Sophea", "Individual", "+855 87 654 321", "sophea@email.com", "$1,900", "2024-11-03"),
            ("CUS-003", "Lim Dara", "VIP", "+855 98 765 432", "dara@business.com", "$28,250", "2024-11-05"),
            ("CUS-004", "Heng Srey", "Business", "+855 77 888 999", "srey@company.com", "$10,800", "2024-11-07"),
            ("CUS-005", "Pich Veasna", "Individual", "+855 12 111 222", "veasna@email.com", "$5,200", "2024-11-09"),
            ("CUS-006", "Mom Sothea", "VIP", "+855 99 333 444", "sothea@corp.com", "$42,000", "2024-11-10"),
            ("CUS-007", "Kim Reach", "Individual", "+855 88 555 666", "reach@email.com", "$3,800", "2024-11-08"),
            ("CUS-008", "Ly Bopha", "Business", "+855 78 777 888", "bopha@company.com", "$15,600", "2024-11-06"),
        ]
        
        self.table.setRowCount(len(customers))
        for row, customer in enumerate(customers):
            for col, value in enumerate(customer):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Highlight VIP customers
                if col == 2 and value == "VIP":
                    item.setBackground(Qt.yellow)
                    item.setForeground(Qt.darkBlue)
                    # Make entire row bold for VIP
                    for c in range(self.table.columnCount() - 1):
                        if self.table.item(row, c):
                            font = self.table.item(row, c).font()
                            font.setBold(True)
                            self.table.item(row, c).setFont(font)
                
                self.table.setItem(row, col, item)
                
        self.update_summary()
        
    def update_summary(self):
        """Update customer summary"""
        total = self.table.rowCount()
        individual = 0
        business = 0
        vip = 0
        
        for row in range(self.table.rowCount()):
            type_item = self.table.item(row, 2)
            if type_item:
                customer_type = type_item.text()
                if customer_type == "Individual":
                    individual += 1
                elif customer_type == "Business":
                    business += 1
                elif customer_type == "VIP":
                    vip += 1
        
        self.total_customers_label.setText(f"Total Customers: {total}")
        self.individual_label.setText(f"Individual: {individual}")
        self.business_label.setText(f"Business: {business}")
        self.vip_label.setText(f"VIP: {vip}")
        
    def filter_customers(self):
        """Filter customers based on search and type"""
        search_text = self.search_box.text().lower()
        customer_type = self.type_filter.currentText()
        
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
            
            # Check type filter
            if customer_type != "All Customers":
                type_item = self.table.item(row, 2)
                if type_item and type_item.text() != customer_type:
                    show_row = False
            
            self.table.setRowHidden(row, not show_row)
        
    def add_customer(self):
        """Add new customer"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Add Customer", "Add customer dialog will open here")
        
    def edit_customer(self):
        """Edit customer information"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Edit Customer", "Edit customer dialog will open here")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a customer to edit")
            
    def view_customer(self):
        """View customer details"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Customer Details", "Detailed customer information will be shown here")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a customer to view")
            
    def view_history(self):
        """View purchase history"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Purchase History", "Purchase history will be shown here")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a customer to view history")
            
    def export_customers(self):
        """Export customer data"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Export", "Customer data exported successfully!")
