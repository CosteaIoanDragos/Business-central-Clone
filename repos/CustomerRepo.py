import sqlite3
import threading
from domain.customer import Customer

class CustomerRepository:
    def __init__(self, db_path="sales.db", save_interval=60):
        """
        Initialize the repository and load data from the database.
        :param db_path: Path to the SQLite database file.
        :param save_interval: Time interval (in seconds) to save data to the database.
        """
        self.customers = []
        self.current_max_id = 0  # We'll use this to track the highest ID assigned
        self.dirty = False  # Track if there are unsaved changes
        self.db_path = db_path
        self.save_interval = save_interval
        self.load_from_db()
        self.start_auto_save()

    def get_next_id(self):
        """Returns the next available customer ID, incrementing the counter."""
        self.current_max_id += 1
        return self.current_max_id

    def add_customer(self, customer):
        self.customers.append(customer)
        self.dirty = True

    def get_customer_by_id(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def update_customer(self, customer_id, name=None, email=None, address=None):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            if name:
                customer.name = name
            if email:
                customer.email = email
            if address:
                customer.address = address
            self.dirty = True
            return customer
        return None

    def delete_customer(self, customer_id):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            self.customers.remove(customer)
            self.dirty = True
            return customer
        return None

    def get_all_customers(self):
        return self.customers

    def save_to_db(self):
        """Save the current in-memory customers to the database."""
        if not self.dirty:
            return  # No changes to save

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")  # Clear existing data

        for customer in self.customers:
            cursor.execute("INSERT INTO customers (id, name, email, address) VALUES (?, ?, ?, ?)",
                           (customer.customer_id, customer.name, customer.email, customer.address))

        conn.commit()
        conn.close()
        self.dirty = False

    def load_from_db(self):
        """Load customers from the database into memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, address FROM customers")
        
        for row in cursor.fetchall():
            customer = Customer(*row)
            self.customers.append(customer)
            if customer.customer_id > self.current_max_id:
                self.current_max_id = customer.customer_id

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
