"""
Sales Management Tab
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QLineEdit, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor

from database.db_manager import DatabaseManager
from modules.web_sync import WebSync, create_sample_online_order
from modules.invoice_generator import InvoiceGenerator
from modules.reports import ReportGenerator

class SalesTab(QWidget):
    """Sales management tab"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.web_sync = WebSync(self.db)
        self.invoice_gen = InvoiceGenerator()
        self.report_gen = ReportGenerator()
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
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Source", "Total Amount",
            "Payment %", "Payment", "Status", "Actions"
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
        
        sync_btn = QPushButton("🌐 Sync Online Orders")
        sync_btn.clicked.connect(self.sync_online_orders)
        sync_btn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);")
        button_layout.addWidget(sync_btn)
        
        export_btn = QPushButton("📤 Export Report")
        export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
    def load_sales(self):
        """Load sales data from database"""
        # Get sales from database
        db_sales = self.db.get_all_sales()
        
        self.table.setRowCount(len(db_sales))
        for row, sale in enumerate(db_sales):
            # sale = (id, invoice_number, sale_date, customer_name, total_amount, payment_percentage, sale_status, source)
            
            # Invoice #
            item = QTableWidgetItem(sale[1])
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item)
            
            # Date
            item = QTableWidgetItem(sale[2])
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item)
            
            # Customer
            item = QTableWidgetItem(sale[3])
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item)
            
            # Source
            source = sale[7] if len(sale) > 7 else 'Desktop'
            item = QTableWidgetItem(source)
            item.setTextAlignment(Qt.AlignCenter)
            # Highlight online orders
            if source == 'Website':
                item.setBackground(QColor("#e0f2fe"))  # Light blue
                item.setForeground(QColor("#0369a1"))  # Dark blue
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            self.table.setItem(row, 3, item)
            
            # Total Amount
            item = QTableWidgetItem(f"${sale[4]:,.2f}")
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, item)
            
            # Payment %
            item = QTableWidgetItem(f"{sale[5]:.0f}%")
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, item)
            
            # Payment Status
            payment_status = "Paid" if sale[5] >= 100 else "Partial" if sale[5] > 0 else "Pending"
            item = QTableWidgetItem(payment_status)
            item.setTextAlignment(Qt.AlignCenter)
            if payment_status == "Paid":
                item.setBackground(Qt.green)
                item.setForeground(Qt.white)
            elif payment_status == "Partial":
                item.setBackground(Qt.yellow)
            self.table.setItem(row, 6, item)
            
            # Status
            item = QTableWidgetItem(sale[6])
            item.setTextAlignment(Qt.AlignCenter)
            if sale[6] == "Completed":
                item.setBackground(Qt.green)
                item.setForeground(Qt.white)
            elif sale[6] == "Pending":
                item.setBackground(Qt.yellow)
            elif sale[6] == "Cancelled":
                item.setBackground(Qt.red)
                item.setForeground(Qt.white)
            self.table.setItem(row, 7, item)
                
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
        import os
        import subprocess
        
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a sale to generate invoice")
            return
        
        try:
            # Get sale data from table
            db_sales = self.db.get_all_sales()
            sale_data = db_sales[selected]
            sale_id = sale_data[0]
            
            # Get sale details with items
            sale, items = self.db.get_sale_details(sale_id)
            
            if not items:
                QMessageBox.warning(self, "No Items", "This sale has no items to generate invoice")
                return
            
            # Generate PDF
            filepath = self.invoice_gen.generate_invoice(sale, items)
            
            # Show success message
            result = QMessageBox.question(self, "Invoice Generated", 
                f"✅ Invoice PDF generated successfully!\n\n"
                f"File: {os.path.basename(filepath)}\n\n"
                f"Would you like to open it now?",
                QMessageBox.Yes | QMessageBox.No)
            
            if result == QMessageBox.Yes:
                # Open PDF with default application
                if os.name == 'nt':  # Windows
                    os.startfile(filepath)
                else:  # Mac/Linux
                    subprocess.call(['open', filepath])
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate invoice:\n{str(e)}")
            
    def sync_online_orders(self):
        """Sync online orders from website"""
        from PyQt5.QtWidgets import QMessageBox
        
        # For demo, create a sample online order
        sample_order = create_sample_online_order()
        success, result, sale_id = self.web_sync.import_online_order(sample_order)
        
        if success:
            QMessageBox.information(self, "Sync Complete", 
                f"✅ Online order imported successfully!\n\nInvoice: {result}\n\n"
                f"Customer: {sample_order['customer_name']}\n"
                f"Total: ${sample_order['total_amount']:,.2f}\n\n"
                f"Status: Pending (awaiting confirmation)")
            self.load_sales()  # Refresh table
            self.update_summary()
        else:
            QMessageBox.warning(self, "Sync Error", f"Failed to import order: {result}")
    
    def export_report(self):
        """Export sales report to Excel"""
        from PyQt5.QtWidgets import QMessageBox, QFileDialog
        import pandas as pd
        
        try:
            # Get sales data
            db_sales = self.db.get_all_sales()
            
            if not db_sales:
                QMessageBox.warning(self, "No Data", "No sales data to export")
                return
            
            # Convert to list of dicts for pandas
            sales_data = []
            for sale in db_sales:
                sales_data.append({
                    'Invoice #': sale[1],
                    'Date': sale[2],
                    'Customer': sale[3],
                    'Source': sale[7] if len(sale) > 7 else 'Desktop',
                    'Total Amount': f"${sale[4]:,.2f}",
                    'Payment %': f"{sale[5]:.0f}%",
                    'Payment Status': 'Paid' if sale[5] >= 100 else 'Partial' if sale[5] > 0 else 'Pending',
                    'Status': sale[6]
                })
            
            # Create DataFrame
            df = pd.DataFrame(sales_data)
            
            # Ask where to save
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export Sales Report", 
                f"Sales_Report_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
                "Excel Files (*.xlsx)"
            )
            
            if filename:
                # Export to Excel
                df.to_excel(filename, index=False, engine='openpyxl')
                
                result = QMessageBox.question(self, "Export Complete", 
                    f"✅ Sales report exported successfully!\n\n"
                    f"File: {os.path.basename(filename)}\n"
                    f"Records: {len(sales_data)}\n\n"
                    f"Would you like to open it now?",
                    QMessageBox.Yes | QMessageBox.No)
                
                if result == QMessageBox.Yes:
                    if os.name == 'nt':  # Windows
                        os.startfile(filename)
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export report:\n{str(e)}")
