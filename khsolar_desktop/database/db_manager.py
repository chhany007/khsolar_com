"""
Database Manager for KHSolar Desktop
Handles all database operations
"""

import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """Manage SQLite database operations"""
    
    def __init__(self, db_folder='data'):
        """Initialize database manager"""
        self.db_folder = db_folder
        os.makedirs(db_folder, exist_ok=True)
        self.db_path = os.path.join(db_folder, 'khsolar.db')
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code TEXT UNIQUE NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                wholesale_price REAL NOT NULL,
                retail_price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                description TEXT,
                specifications TEXT,
                image_url TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                customer_type TEXT CHECK(customer_type IN ('Individual', 'Business', 'VIP')),
                phone TEXT,
                email TEXT,
                address TEXT,
                telegram TEXT,
                company_name TEXT,
                tax_id TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                customer_name TEXT,
                customer_phone TEXT,
                customer_email TEXT,
                customer_address TEXT,
                sale_date DATE NOT NULL,
                total_amount REAL NOT NULL,
                payment_percentage REAL DEFAULT 0,
                payment_status TEXT CHECK(payment_status IN ('Pending', 'Partial', 'Paid')),
                sale_status TEXT CHECK(sale_status IN ('Pending', 'Completed', 'Cancelled')),
                notes TEXT,
                source TEXT DEFAULT 'Desktop',
                web_report_data TEXT,
                created_by TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Sale items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                discount REAL DEFAULT 0,
                subtotal REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        # Warranties table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warranties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT UNIQUE NOT NULL,
                product_id INTEGER,
                product_name TEXT NOT NULL,
                customer_id INTEGER,
                customer_name TEXT NOT NULL,
                sale_id INTEGER,
                purchase_date DATE NOT NULL,
                warranty_end_date DATE NOT NULL,
                warranty_period_years INTEGER DEFAULT 5,
                status TEXT CHECK(status IN ('Active', 'Expired', 'Claimed')),
                notes TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (sale_id) REFERENCES sales(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ==================== PRODUCT OPERATIONS ====================
    
    def add_product(self, product_code, product_name, category, wholesale_price, 
                   retail_price, stock=0, description='', specs='', image_url=''):
        """Add a new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (product_code, product_name, category, 
                                    wholesale_price, retail_price, stock_quantity,
                                    description, specifications, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product_code, product_name, category, wholesale_price, 
                  retail_price, stock, description, specs, image_url))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Product already exists, update it
            cursor.execute('''
                UPDATE products 
                SET product_name=?, category=?, wholesale_price=?, retail_price=?,
                    stock_quantity=?, description=?, specifications=?, image_url=?,
                    updated_date=CURRENT_TIMESTAMP
                WHERE product_code=?
            ''', (product_name, category, wholesale_price, retail_price, stock,
                  description, specs, image_url, product_code))
            conn.commit()
            return None
        finally:
            conn.close()
    
    def get_all_products(self):
        """Get all products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products ORDER BY category, product_name')
        products = cursor.fetchall()
        conn.close()
        return products
    
    def get_product_by_code(self, product_code):
        """Get product by code"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_code=?', (product_code,))
        product = cursor.fetchone()
        conn.close()
        return product
    
    def update_product_stock(self, product_code, quantity_change):
        """Update product stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products 
            SET stock_quantity = stock_quantity + ?,
                updated_date = CURRENT_TIMESTAMP
            WHERE product_code = ?
        ''', (quantity_change, product_code))
        conn.commit()
        conn.close()
    
    # ==================== CUSTOMER OPERATIONS ====================
    
    def add_customer(self, name, customer_type, phone='', email='', address='', 
                    telegram='', company_name='', tax_id=''):
        """Add a new customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate customer code
        cursor.execute('SELECT COUNT(*) FROM customers')
        count = cursor.fetchone()[0] + 1
        customer_code = f"CUS-{count:04d}"
        
        cursor.execute('''
            INSERT INTO customers (customer_code, name, customer_type, phone, email,
                                 address, telegram, company_name, tax_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (customer_code, name, customer_type, phone, email, address, 
              telegram, company_name, tax_id))
        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()
        return customer_id, customer_code
    
    def get_all_customers(self):
        """Get all customers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers ORDER BY name')
        customers = cursor.fetchall()
        conn.close()
        return customers
    
    # ==================== SALES OPERATIONS ====================
    
    def add_sale(self, customer_name, customer_phone='', customer_email='', 
                customer_address='', total_amount=0, sale_status='Pending',
                payment_status='Pending', payment_percentage=0, notes='', 
                source='Desktop', web_report_data=''):
        """Add a new sale"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate invoice number
        today = datetime.now().strftime('%Y%m%d')
        cursor.execute('SELECT COUNT(*) FROM sales WHERE invoice_number LIKE ?', (f'INV-{today}-%',))
        count = cursor.fetchone()[0] + 1
        invoice_number = f"INV-{today}-{count:04d}"
        
        cursor.execute('''
            INSERT INTO sales (invoice_number, customer_name, customer_phone, 
                             customer_email, customer_address, sale_date, total_amount,
                             payment_percentage, payment_status, sale_status, notes,
                             source, web_report_data)
            VALUES (?, ?, ?, ?, ?, DATE('now'), ?, ?, ?, ?, ?, ?, ?)
        ''', (invoice_number, customer_name, customer_phone, customer_email,
              customer_address, total_amount, payment_percentage, payment_status,
              sale_status, notes, source, web_report_data))
        conn.commit()
        sale_id = cursor.lastrowid
        conn.close()
        return sale_id, invoice_number
    
    def add_sale_item(self, sale_id, product_name, quantity, unit_price, discount=0):
        """Add item to sale"""
        conn = self.get_connection()
        cursor = conn.cursor()
        subtotal = (unit_price * quantity) - discount
        cursor.execute('''
            INSERT INTO sale_items (sale_id, product_name, quantity, unit_price, discount, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sale_id, product_name, quantity, unit_price, discount, subtotal))
        conn.commit()
        conn.close()
    
    def get_all_sales(self):
        """Get all sales"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, invoice_number, sale_date, customer_name, 
                   total_amount, payment_percentage, sale_status, source
            FROM sales 
            ORDER BY sale_date DESC
        ''')
        sales = cursor.fetchall()
        conn.close()
        return sales
    
    def get_sale_details(self, sale_id):
        """Get sale details with items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get sale
        cursor.execute('SELECT * FROM sales WHERE id=?', (sale_id,))
        sale = cursor.fetchone()
        
        # Get items
        cursor.execute('SELECT * FROM sale_items WHERE sale_id=?', (sale_id,))
        items = cursor.fetchall()
        
        conn.close()
        return sale, items
    
    def update_sale_status(self, sale_id, sale_status, payment_status=None, payment_percentage=None):
        """Update sale status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if payment_status and payment_percentage is not None:
            cursor.execute('''
                UPDATE sales 
                SET sale_status=?, payment_status=?, payment_percentage=?,
                    updated_date=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (sale_status, payment_status, payment_percentage, sale_id))
        else:
            cursor.execute('''
                UPDATE sales 
                SET sale_status=?, updated_date=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (sale_status, sale_id))
        
        conn.commit()
        conn.close()
    
    # ==================== WARRANTY OPERATIONS ====================
    
    def add_warranty(self, serial_number, product_name, customer_name, 
                    purchase_date, warranty_years=5, notes=''):
        """Add a new warranty"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        from datetime import datetime, timedelta
        purchase_dt = datetime.strptime(purchase_date, '%Y-%m-%d')
        warranty_end = purchase_dt + timedelta(days=warranty_years*365)
        
        cursor.execute('''
            INSERT INTO warranties (serial_number, product_name, customer_name,
                                  purchase_date, warranty_end_date, warranty_period_years,
                                  status, notes)
            VALUES (?, ?, ?, ?, ?, ?, 'Active', ?)
        ''', (serial_number, product_name, customer_name, purchase_date,
              warranty_end.strftime('%Y-%m-%d'), warranty_years, notes))
        conn.commit()
        warranty_id = cursor.lastrowid
        conn.close()
        return warranty_id
    
    def get_all_warranties(self):
        """Get all warranties"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT serial_number, product_name, customer_name, purchase_date,
                   warranty_end_date, status
            FROM warranties 
            ORDER BY warranty_end_date
        ''')
        warranties = cursor.fetchall()
        conn.close()
        return warranties
