"""
Main Window UI for KHSolar Desktop
"""

from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QStatusBar, QMenuBar, QAction)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from ui.products_tab import ProductsTab
from ui.sales_tab import SalesTab
from ui.warranty_tab import WarrantyTab
from ui.customers_tab import CustomersTab

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Window properties
        self.setWindowTitle("KHSolar Desktop - Sales & Customer Management")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
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
        self.tabs.addTab(ProductsTab(), "📦 Products & Prices")
        self.tabs.addTab(SalesTab(), "💰 Sales Management")
        self.tabs.addTab(WarrantyTab(), "🛡️ Warranty")
        self.tabs.addTab(CustomersTab(), "👥 Customers")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.create_status_bar()
        
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
        """Create header widget"""
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            padding: 15px;
            border-radius: 10px;
        """)
        
        # Title
        title = QLabel("☀️ KHSolar Desktop")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Info
        info = QLabel("Sales & Customer Management System")
        info.setStyleSheet("color: white; font-size: 14px;")
        header_layout.addWidget(info)
        
        return header_widget
        
    def create_status_bar(self):
        """Create status bar"""
        self.status = self.statusBar()
        self.status.showMessage('Ready', 3000)
        
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
        """)
        
    def show_about(self):
        """Show about dialog"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "About KHSolar Desktop",
            "KHSolar Desktop v1.0\n\n"
            "Sales & Customer Management System\n\n"
            "Contact:\n"
            "📞 +855 888 836 588\n"
            "💬 @chhanycls"
        )
