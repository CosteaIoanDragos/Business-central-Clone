import sqlite3
import threading
from domain.inventory import Inventory

class InventoryRepository:
    def __init__(self, db_path="sales.db", save_interval=60):
        """
        Initialize the repository and load data from the database.
        :param db_path: Path to the SQLite database file.
        :param save_interval: Time interval (in seconds) to save data to the database.
        """
        self.inventory_items = []
        self.current_max_id = 0  # We'll use this to track the highest ID assigned
        self.dirty = False  # Track if there are unsaved changes
        self.db_path = db_path
        self.save_interval = save_interval
        self.load_from_db()
        self.start_auto_save()

    def get_next_id(self):
        """Returns the next available inventory ID, incrementing the counter."""
        self.current_max_id += 1
        return self.current_max_id

    def add_inventory(self, inventory):
        self.inventory_items.append(inventory)
        self.dirty = True

    def get_inventory_by_id(self, inventory_id):
        for item in self.inventory_items:
            if item.inventory_id == inventory_id:
                return item
        return None

    def update_inventory(self, inventory_id, name=None, nr=None, price=None, type=None):
        inventory = self.get_inventory_by_id(inventory_id)
        if inventory:
            if name:
                inventory.name = name
            if nr != None:
                inventory.nr = nr
            if price:
                inventory.price = price
            if type:
                inventory.type = type
            self.dirty = True
            return inventory
        return None

    def delete_inventory(self, inventory_id):
        inventory = self.get_inventory_by_id(inventory_id)
        if inventory:
            self.inventory_items.remove(inventory)
            self.dirty = True
            return inventory
        return None

    def get_all_inventory(self):
        return self.inventory_items

    def save_to_db(self):
        """Save the current in-memory inventory items to the database."""
        if not self.dirty:
            return  # No changes to save

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory")  # Clear existing data

        for item in self.inventory_items:
            cursor.execute("INSERT INTO inventory (id, name, nr, price, type) VALUES (?, ?, ?, ?, ?)",
                           (item.inventory_id, item.name, item.nr, item.price, item.type))

        conn.commit()
        conn.close()
        self.dirty = False

    def load_from_db(self):
        """Load inventory items from the database into memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, nr, price, type FROM inventory")
        
        for row in cursor.fetchall():
            item = Inventory(*row)
            self.inventory_items.append(item)
            if item.inventory_id > self.current_max_id:
                self.current_max_id = item.inventory_id

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
