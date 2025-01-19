import sqlite3
import threading
from domain.sales import Sales, SalesType

class SalesRepository:
    def __init__(self, db_path="sales.db", save_interval=300):
        """
        Initialize the repository and load data from the database.
        :param db_path: Path to the SQLite database file.
        :param save_interval: Time interval (in seconds) to save data to the database.
        """
        self.sales = []
        self.current_max_id = 0  # We'll use this to track the highest ID assigned
        self.dirty = False  # Track if there are unsaved changes
        self.db_path = db_path
        self.save_interval = save_interval
        self.load_from_db()
        self.start_auto_save()

    def get_next_id(self):
        """Returns the next available sales ID, incrementing the counter."""
        self.current_max_id += 1
        return self.current_max_id

    def add_sales(self, sale):
        if not isinstance(sale, Sales):
            raise TypeError("Only Sales objects can be added to the repository.")
        self.sales.append(sale)
        self.dirty = True

    def get_sales_by_id(self, sales_id):
        for sale in self.sales:
            if sale.sales_id == sales_id:
                return sale
        return None

    def update_sales(self, sales_id, customer_id=None, item_id=None, salestype=None, quantity=None):
        sale = self.get_sales_by_id(sales_id)
        if sale:
            if customer_id:
                sale.customer_id = customer_id
            if item_id:
                sale.item_id = item_id
            if salestype:
                if not isinstance(salestype, SalesType):
                    raise ValueError("Invalid sales type. Must be one of: 'Quote', 'Order', 'Invoice'.")
                sale.salestype = salestype
            if quantity!= None:
                sale.quantity = quantity
            self.dirty = True
            return sale
        return None

    def delete_sales(self, sales_id):
        sale = self.get_sales_by_id(sales_id)
        if sale:
            self.sales.remove(sale)
            self.dirty = True
            return sale
        return None

    def get_all_sales(self):
        return self.sales

    def save_to_db(self):
        """Save the current in-memory sales to the database."""
        if not self.dirty:
            return  # No changes to save

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales")  # Clear existing data

        for sale in self.sales:
            cursor.execute("INSERT INTO sales (id, customer_id, item_id, salestype, quantity, pricePerItem) VALUES (?, ?, ?, ?, ?, ?)",
                           (sale.sales_id, sale.customer_id, sale.item_id, sale.salestype.name, sale.quantity, sale.pricePerItem))

        conn.commit()
        conn.close()
        self.dirty = False

    def load_from_db(self):
        """Load sales from the database into memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer_id, item_id, salestype, quantity, pricePerItem FROM sales")
        
        for row in cursor.fetchall():
            sales_id, customer_id, item_id, salestype_str, quantity, pricePerItem = row
            try:
                salestype = SalesType[salestype_str]
            except KeyError:
                raise ValueError(f"Invalid sales type '{salestype_str}'. Must be one of: 'Quote', 'Order', 'Invoice'.")
            sale = Sales(sales_id, customer_id, item_id, salestype, quantity, pricePerItem)
            self.sales.append(sale)
            if sale.sales_id > self.current_max_id:
                self.current_max_id = sale.sales_id

        conn.close()

    def start_auto_save(self):
        """Start a timer to save data to the database at regular intervals."""
        self.timer = threading.Timer(self.save_interval, self.auto_save)
        self.timer.start()

    def auto_save(self):
        """Save data to the database and restart the timer."""
        self.save_to_db()
        self.start_auto_save()

    def stop_auto_save(self):
        """Stop the auto-save timer."""
        self.timer.cancel()
