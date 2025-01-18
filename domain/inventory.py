class Inventory:
    def __init__(self, inventory_id, name, nr, price,type):
        self.inventory_id = inventory_id
        self.name = name
        self.nr = nr
        self.price = price
        self.type = type
        
    def __repr__(self):
        return f"InventoryItem({self.inventory_id},{self.name},{self.nr},{self.price},{self.type})"
