# infrastructure/inventory_repository.py
from domain.inventory import Inventory

class InventoryRepository:
    def __init__(self):
        self.inventory_items = []
        self.current_max_id = 0  

    def get_next_id(self):
        """Returns the next available customer ID, incrementing the counter."""
        self.current_max_id += 1
        return self.current_max_id

    def add_inventory(self, inventory):
        self.inventory_items.append(inventory)

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
            if nr:
                inventory.nr = nr
            if price:
                inventory.price = price
            if type:
                inventory.type = type
            return inventory
        return None

    def delete_inventory(self, inventory_id):
        inventory = self.get_inventory_by_id(inventory_id)
        if inventory:
            self.inventory_items.remove(inventory)
            return inventory
        return None

    def get_all_inventory(self):
        return self.inventory_items
