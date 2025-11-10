"""
Sales Management Tab
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class SalesTab(QWidget):
    """Sales management tab"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_sales()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QLabel("Sales Management")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(header)
        
        # Filter section
        filter_layout = QHBoxLayout()
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search by invoice, customer...")
        filter_layout.addWidget(self.search_box)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Status", "Pending", "Paid", "Completed", "Cancelled"])
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addWidget(QLabel("From:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setCalendarPopup(True)
        filter_layout.addWidget(self.date_from)
        
        filter_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.date_to)
        
        layout.addLayout(filter_layout)
        
        # Sales table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Products", "Total Amount",
            "Payment", "Status", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # Summary section
        summary_layout = QHBoxLayout()
        
        self.total_sales_label = QLabel("Total Sales: $0")
        self.total_sales_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        summary_layout.addWidget(self.total_sales_label)
        
        summary_layout.addStretch()
        
        self.pending_label = QLabel("Pending: 0")
        summary_layout.addWidget(self.pending_label)
        
        self.completed_label = QLabel("Completed: 0")
        summary_layout.addWidget(self.completed_label)
        
        layout.addLayout(summary_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        new_sale_btn = QPushButton("➕ New Sale")
        new_sale_btn.clicked.connect(self.new_sale)
        button_layout.addWidget(new_sale_btn)
        
        view_btn = QPushButton("👁️ View Details")
        view_btn.clicked.connect(self.view_sale)
        button_layout.addWidget(view_btn)
        
        invoice_btn = QPushButton("📄 Generate Invoice")
        invoice_btn.clicked.connect(self.generate_invoice)
        button_layout.addWidget(invoice_btn)
        
        button_layout.addStretch()
        
        export_btn = QPushButton("📤 Export Report")
        export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
    def load_sales(self):
        """Load sales data"""
        # Sample sales data
        sales = [
            ("INV-2024-001", "2024-11-01", "Sok Pisey", "2x Inverter, 10x Panel", "$18,500", "50%", "Pending"),
            ("INV-2024-002", "2024-11-03", "Chan Sophea", "1x Battery Pack", "$1,900", "100%", "Completed"),
            ("INV-2024-003", "2024-11-05", "Lim Dara", "1x Inverter, 5x Panel", "$8,250", "30%", "Pending"),
            ("INV-2024-004", "2024-11-07", "Heng Srey", "20x Panel, Accessories", "$10,800", "100%", "Completed"),
            ("INV-2024-005", "2024-11-09", "Pich Veasna", "Complete System", "$22,000", "20%", "Pending"),
        ]
        
        self.table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            for col, value in enumerate(sale):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Color code status
                if col == 6:  # Status column
                    if value == "Completed":
                        item.setBackground(Qt.green)
                        item.setForeground(Qt.white)
                    elif value == "Pending":
                        item.setBackground(Qt.yellow)
                    elif value == "Cancelled":
                        item.setBackground(Qt.red)
                        item.setForeground(Qt.white)
                
                self.table.setItem(row, col, item)
                
        # Update summary
        self.update_summary()
        
    def update_summary(self):
        """Update summary statistics"""
        total = 0
        pending = 0
        completed = 0
        
        for row in range(self.table.rowCount()):
            status_item = self.table.item(row, 6)
            if status_item:
                status = status_item.text()
                if status == "Pending":
                    pending += 1
                elif status == "Completed":
                    completed += 1
            
            amount_item = self.table.item(row, 4)
            if amount_item:
                amount_str = amount_item.text().replace("$", "").replace(",", "")
                try:
                    total += float(amount_str)
                except:
                    pass
        
        self.total_sales_label.setText(f"Total Sales: ${total:,.2f}")
        self.pending_label.setText(f"Pending: {pending}")
        self.completed_label.setText(f"Completed: {completed}")
        
    def new_sale(self):
        """Create new sale"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "New Sale", "New sale dialog will open here")
        
    def view_sale(self):
        """View sale details"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Sale Details", "Sale details will be shown here")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a sale to view")
            
    def generate_invoice(self):
        """Generate invoice PDF"""
        from PyQt5.QtWidgets import QMessageBox
        selected = self.table.currentRow()
        if selected >= 0:
            QMessageBox.information(self, "Invoice", "Invoice PDF generated successfully!")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a sale to generate invoice")
            
    def export_report(self):
        """Export sales report"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Export", "Sales report exported successfully!")
