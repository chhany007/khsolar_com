"""
Main Window UI for KHSolar Desktop
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QStatusBar, QMenuBar, QAction,
                             QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from PyQt5.QtGui import QIcon, QFont, QPixmap

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.products_tab import ProductsTab
from ui.sales_tab import SalesTab
from ui.warranty_tab import WarrantyTab
from ui.customers_tab import CustomersTab
from database.db_manager import DatabaseManager

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Database
        self.db = DatabaseManager()
        
        # Window properties
        self.setWindowTitle("☀️ KHSolar Desktop - Professional Solar Business Management")
        self.setGeometry(50, 50, 1500, 950)
        self.setMinimumSize(1300, 850)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'assets', 'images', 'logo.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        
        # Add tabs
        self.tabs.addTab(self.create_dashboard(), "📊 Dashboard")
        self.tabs.addTab(ProductsTab(), "📦 Products & Prices")
        self.tabs.addTab(SalesTab(), "💰 Sales Management")
        self.tabs.addTab(WarrantyTab(), "🛡️ Warranty")
        self.tabs.addTab(CustomersTab(), "👥 Customers")
        
        # Set font size for tabs
        self.tabs.setFont(QFont("Segoe UI", 11))
        
        main_layout.addWidget(self.tabs)
        
        # Status bar with timer
        self.create_status_bar()
        
        # Update time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)
        
        # Apply stylesheet
        self.apply_stylesheet()
        
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        export_action = QAction('Export Data', self)
        export_action.setShortcut('Ctrl+E')
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('&Tools')
        
        settings_action = QAction('Settings', self)
        tools_menu.addAction(settings_action)
        
        backup_action = QAction('Backup Database', self)
        tools_menu.addAction(backup_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_header(self):
        """Create header widget with logo"""
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            padding: 20px;
            border-radius: 10px;
        """)
        
        # Logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 'assets', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            header_layout.addWidget(logo_label)
        
        # Title section
        title_layout = QVBoxLayout()
        
        # Main title
        title = QLabel("KHSolar Desktop")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-left: 15px;")
        title_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Professional Solar Business Management System")
        subtitle.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 13px; margin-left: 15px; margin-top: -5px;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Stats preview in header
        stats_layout = QVBoxLayout()
        
        # Get quick stats
        products = self.db.get_all_products()
        sales = self.db.get_all_sales()
        customers = self.db.get_all_customers()
        
        stats_label = QLabel(f"📦 {len(products)} Products  |  💰 {len(sales)} Sales  |  👥 {len(customers)} Customers")
        stats_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600;")
        stats_layout.addWidget(stats_label)
        
        time_label = QLabel()
        time_label.setObjectName("time_label")
        time_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 11px;")
        stats_layout.addWidget(time_label)
        self.time_label = time_label
        
        header_layout.addLayout(stats_layout)
        
        return header_widget
        
    def create_status_bar(self):
        """Create status bar"""
        self.status = self.statusBar()
        self.update_status_bar()
        
    def update_status_bar(self):
        """Update status bar with current time and info"""
        from datetime import datetime
        current_time = datetime.now().strftime("%A, %B %d, %Y  |  %I:%M:%S %p")
        self.status.showMessage(f"🕒 {current_time}  |  ✅ System Ready  |  💾 Database Connected")
        
        # Update header time if it exists
        if hasattr(self, 'time_label'):
            self.time_label.setText(datetime.now().strftime("%I:%M %p  •  %b %d, %Y"))
        
    def apply_stylesheet(self):
        """Apply custom stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #e8eaf6;
                color: #333;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
            }
            QTabBar::tab:hover {
                background: #c5cae9;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a4291);
            }
            QPushButton:pressed {
                background: #4a5a9c;
            }
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #667eea;
                color: white;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background: white;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #667eea;
            }
        """)
        
    def create_dashboard(self):
        """Create dashboard tab with statistics and quick actions"""
        from PyQt5.QtWidgets import QScrollArea
        
        # Main widget
        dashboard = QWidget()
        main_layout = QVBoxLayout()
        dashboard.setLayout(main_layout)
        
        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout()
        content.setLayout(layout)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome section with date
        from datetime import datetime
        welcome_widget = QWidget()
        welcome_layout = QHBoxLayout()
        welcome_widget.setLayout(welcome_layout)
        welcome_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
            border-radius: 10px;
            padding: 20px;
        """)
        
        welcome = QLabel("☀️ KHSolar Business Dashboard")
        welcome.setFont(QFont("Segoe UI", 22, QFont.Bold))
        welcome.setStyleSheet("color: white;")
        welcome_layout.addWidget(welcome)
        
        welcome_layout.addStretch()
        
        date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        date_label.setFont(QFont("Segoe UI", 12))
        date_label.setStyleSheet("color: rgba(255,255,255,0.9);")
        welcome_layout.addWidget(date_label)
        
        layout.addWidget(welcome_widget)
        
        # Get data
        products = self.db.get_all_products()
        sales = self.db.get_all_sales()
        customers = self.db.get_all_customers()
        warranties = self.db.get_all_warranties()
        
        # Calculate totals
        total_sales_value = sum(sale[4] for sale in sales) if sales else 0
        pending_sales = sum(1 for sale in sales if sale[6] == 'Pending') if sales else 0
        completed_sales = sum(1 for sale in sales if sale[6] == 'Completed') if sales else 0
        
        # Stats section label
        stats_header = QLabel("📊 Business Overview")
        stats_header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        stats_header.setStyleSheet("color: #1f2937; margin-top: 10px;")
        layout.addWidget(stats_header)
        
        # Stats cards - Row 1
        stats_row1 = QHBoxLayout()
        stats_row1.setSpacing(15)
        
        cards_row1 = [
            ("📦 Total Products", str(len(products)), "#3b82f6", "Items in catalog"),
            ("💰 Total Revenue", f"${total_sales_value:,.2f}", "#10b981", "All time sales"),
            ("👥 Customers", str(len(customers)), "#f59e0b", "Registered clients")
        ]
        
        for title, value, color, desc in cards_row1:
            card = self.create_stat_card(title, value, color, desc)
            card.setMinimumHeight(140)
            card.setMinimumWidth(250)
            stats_row1.addWidget(card)
        
        layout.addLayout(stats_row1)
        
        # Stats cards - Row 2
        stats_row2 = QHBoxLayout()
        stats_row2.setSpacing(15)
        
        cards_row2 = [
            ("⏳ Pending Orders", str(pending_sales), "#ef4444", "Awaiting processing"),
            ("✅ Completed", str(completed_sales), "#22c55e", "Orders fulfilled"),
            ("🛡️ Warranties", str(len(warranties)), "#8b5cf6", "Active coverage")
        ]
        
        for title, value, color, desc in cards_row2:
            card = self.create_stat_card(title, value, color, desc)
            card.setMinimumHeight(140)
            card.setMinimumWidth(250)
            stats_row2.addWidget(card)
        
        layout.addLayout(stats_row2)
        
        # Quick actions section
        actions_header = QLabel("⚡ Quick Actions")
        actions_header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        actions_header.setStyleSheet("color: #1f2937; margin-top: 20px;")
        layout.addWidget(actions_header)
        
        # Action buttons in 2 rows
        actions_row1 = QHBoxLayout()
        actions_row1.setSpacing(15)
        
        btn_new_sale = QPushButton("➕ Create New Sale")
        btn_new_sale.setMinimumHeight(60)
        btn_new_sale.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_new_sale.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        actions_row1.addWidget(btn_new_sale)
        
        btn_view_products = QPushButton("📦 View Products")
        btn_view_products.setMinimumHeight(60)
        btn_view_products.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_view_products.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        actions_row1.addWidget(btn_view_products)
        
        layout.addLayout(actions_row1)
        
        actions_row2 = QHBoxLayout()
        actions_row2.setSpacing(15)
        
        btn_customers = QPushButton("👥 Manage Customers")
        btn_customers.setMinimumHeight(60)
        btn_customers.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_customers.clicked.connect(lambda: self.tabs.setCurrentIndex(4))
        actions_row2.addWidget(btn_customers)
        
        btn_sync = QPushButton("🌐 Sync Online Orders")
        btn_sync.setMinimumHeight(60)
        btn_sync.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_sync.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #047857);
            }
        """)
        btn_sync.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        actions_row2.addWidget(btn_sync)
        
        layout.addLayout(actions_row2)
        
        # Add some bottom padding
        layout.addSpacing(20)
        layout.addStretch()
        
        # Set scroll content
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        return dashboard
    
    def create_stat_card(self, title, value, color, description):
        """Create a statistics card"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 2px solid {color};
                border-left: 6px solid {color};
                border-radius: 10px;
                padding: 20px;
            }}
            QFrame:hover {{
                background: #f9fafb;
                border: 2px solid {color};
                border-left: 6px solid {color};
            }}
        """)
        
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        card_layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title_label.setStyleSheet("color: #6b7280;")
        title_label.setWordWrap(True)
        card_layout.addWidget(title_label)
        
        # Spacer
        card_layout.addSpacing(10)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setWordWrap(True)
        card_layout.addWidget(value_label)
        
        # Spacer
        card_layout.addSpacing(5)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setStyleSheet("color: #9ca3af;")
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        card_layout.addStretch()
        
        return card
    
    def show_about(self):
        """Show about dialog"""
        from PyQt5.QtWidgets import QMessageBox
        
        # Get version info
        products = self.db.get_all_products()
        sales = self.db.get_all_sales()
        customers = self.db.get_all_customers()
        
        about_text = f"""<h2>☀️ KHSolar Desktop v1.0</h2>
        <p><b>Professional Solar Business Management System</b></p>
        <hr>
        <p><b>Current Statistics:</b></p>
        <ul>
            <li>📦 Products: {len(products)}</li>
            <li>💰 Sales: {len(sales)}</li>
            <li>👥 Customers: {len(customers)}</li>
        </ul>
        <hr>
        <p><b>Contact Information:</b></p>
        <p>📞 Phone: +855 888 836 588</p>
        <p>💬 Telegram: @chhanycls</p>
        <p>🌐 Website Integration: Active</p>
        <hr>
        <p style='color: #667eea;'><b>Powered by KHSolar © 2024</b></p>
        """
        
        msg = QMessageBox()
        msg.setWindowTitle("About KHSolar Desktop")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        msg.setIconPixmap(QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                                'assets', 'images', 'logo.png')).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        msg.exec_()
