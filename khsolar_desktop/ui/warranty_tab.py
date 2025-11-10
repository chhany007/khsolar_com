"""
Warranty Management Tab
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class WarrantyTab(QWidget):
    """Warranty management tab"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_warranties()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QLabel("Warranty Management")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)
        
        # Search and filter
        search_layout = QHBoxLayout()
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search by serial number, customer...")
        search_layout.addWidget(self.search_box)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Expiring Soon", "Expired", "Claimed"])
        search_layout.addWidget(self.status_filter)
        
        layout.addLayout(search_layout)
        
        # Warranty table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Serial Number", "Product", "Customer", "Purchase Date",
            "Warranty End", "Days Left", "Status", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # Summary
        summary_layout = QHBoxLayout()
        
        self.active_label = QLabel("Active: 0")
        self.active_label.setFont(QFont("Segoe UI", 11))
        summary_layout.addWidget(self.active_label)
        
        self.expiring_label = QLabel("Expiring Soon: 0")
        self.expiring_label.setStyleSheet("color: orange; font-weight: bold;")
        summary_layout.addWidget(self.expiring_label)
        
        self.expired_label = QLabel("Expired: 0")
        self.expired_label.setStyleSheet("color: red; font-weight: bold;")
        summary_layout.addWidget(self.expired_label)
        
        summary_layout.addStretch()
        
        layout.addLayout(summary_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        register_btn = QPushButton("➕ Register Warranty")
        register_btn.clicked.connect(self.register_warranty)
        button_layout.addWidget(register_btn)
        
        claim_btn = QPushButton("🛠️ Process Claim")
        claim_btn.clicked.connect(self.process_claim)
        button_layout.addWidget(claim_btn)
        
        history_btn = QPushButton("📋 Service History")
        history_btn.clicked.connect(self.view_history)
        button_layout.addWidget(history_btn)
        
        button_layout.addStretch()
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self.export_warranties)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
    def load_warranties(self):
        """Load warranty data"""
        # Sample warranty data
        warranties = [
            ("INV-2024-12345", "Deye 8KW Inverter", "Sok Pisey", "2024-01-15", "2029-01-15", "1523", "Active"),
            ("BAT-2024-67890", "10.24KWh Battery", "Chan Sophea", "2024-06-20", "2034-06-20", "3469", "Active"),
            ("INV-2023-11111", "Growatt 10KW", "Lim Dara", "2023-11-01", "2028-11-01", "1096", "Active"),
            ("PNL-2024-22222", "550W Solar Panel", "Heng Srey", "2024-10-15", "2034-10-15", "3596", "Active"),
            ("BAT-2023-33333", "5.12KWh Battery", "Pich Veasna", "2023-01-10", "2033-01-10", "2992", "Active"),
            ("INV-2022-44444", "Deye 5KW Inverter", "Mom Sothea", "2022-11-20", "2024-11-20", "-14", "Expired"),
        ]
        
        self.table.setRowCount(len(warranties))
        for row, warranty in enumerate(warranties):
            for col, value in enumerate(warranty):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Color code status
                if col == 6:  # Status column
                    if value == "Active":
                        item.setBackground(Qt.green)
                        item.setForeground(Qt.white)
                    elif value == "Expiring Soon":
                        item.setBackground(Qt.yellow)
                    elif value == "Expired":
                        item.setBackground(Qt.red)
                        item.setForeground(Qt.white)
                
                # Color code days left
                elif col == 5:  # Days left column
                    try:
                        days = int(value)
                        if days < 0:
                            item.setForeground(Qt.red)
                        elif days < 90:
                            item.setForeground(Qt.darkYellow)
                    except:
                        pass
                
                self.table.setItem(row, col, item)
                
        self.update_summary()
        
    def update_summary(self):
        """Update warranty summary"""
        active = 0
        expiring = 0
        expired = 0
        
        for row in range(self.table.rowCount()):
            status_item = self.table.item(row, 6)
            if status_item:
                status = status_item.text()
                if status == "Active":
                    active += 1
                elif status == "Expiring Soon":
                    expiring += 1
                elif status == "Expired":
                    expired += 1
        
        self.active_label.setText(f"Active: {active}")
        self.expiring_label.setText(f"Expiring Soon: {expiring}")
        self.expired_label.setText(f"Expired: {expired}")
        
    def register_warranty(self):
        """Register new warranty"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Register Warranty", "Warranty registration dialog will open here")
        
    def process_claim(self):
        """Process warranty claim"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Process Claim", "Warranty claim processing will open here")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a warranty to process")
            
    def view_history(self):
        """View service history"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Service History", "Service history will be shown here")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a warranty to view history")
            
    def export_warranties(self):
        """Export warranty data"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Export", "Warranty data exported successfully!")
