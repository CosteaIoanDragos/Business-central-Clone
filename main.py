# main.py
from domain.inventory import Inventory
from repos.InventoryRepo import InventoryRepository
from domain.customer import Customer
from repos.CustomerRepo import CustomerRepository
from domain.sales import *
from repos.SalesRepo import SalesRepository
from services.SalesService import SalesService

def InventoryTest():
    repo = InventoryRepository()

    # Create inventory items
    item1 = Inventory(1, "Laptop", 10, 999.99, "Electronics")
    item2 = Inventory(2, "Desk Chair", 25, 79.99, "Furniture")

    # Add inventory items to repository
    repo.add_inventory(item1)
    repo.add_inventory(item2)

    # Read inventory items
    print("All Inventory Items:")
    for item in repo.get_all_inventory():
        print(item)

    # Attempt to add an invalid item (uncomment to test)
    # invalid_item = "This is not an Inventory object"
    # repo.add_inventory(invalid_item)

    # Update an inventory item
    repo.update_inventory(1, price=949.99)
    print("\nUpdated Inventory Item:")
    print(repo.get_inventory_by_id(1))

    # Delete an inventory item
    repo.delete_inventory(2)
    print("\nAll Inventory Items After Deletion:")
    for item in repo.get_all_inventory():
        print(item)

def CustomerTest():
    repo = CustomerRepository()

    # Create customers
    customer1 = Customer(1, "Alice Smith", "alice@example.com", "123 Maple Street")
    customer2 = Customer(2, "Bob Johnson", "bob@example.com", "456 Oak Avenue")

    # Add customers to repository
    repo.add_customer(customer1)
    repo.add_customer(customer2)

    # Read customers
    print("All Customers:")
    for customer in repo.get_all_customers():
        print(customer)

    # Update a customer
    repo.update_customer(1, email="alice_new@example.com")
    print("\nUpdated Customer:")
    print(repo.get_customer_by_id(1))

    # Delete a customer
    repo.delete_customer(2)
    print("\nAll Customers After Deletion:")
    for customer in repo.get_all_customers():
        print(customer)
# main.py

def SalesTest():
    repo = SalesRepository()

    # Create sales items
    sale1 = Sales(1, 101, 1001, SalesType.ORDER)
    sale2 = Sales(2, 102, 1002, SalesType.ORDER)

    # Add sales items to repository
    repo.add_sales(sale1)
    repo.add_sales(sale2)

    # Read sales items
    print("All Sales Items:")
    for sale in repo.get_all_sales():
        print(sale)

    # Update a sales item
    repo.update_sales(1, salestype=SalesType.INVOICE)
    print("\nUpdated Sales Item:")
    print(repo.get_sales_by_id(1))

    # Delete a sales item
    repo.delete_sales(2)
    print("\nAll Sales Items After Deletion:")
    for sale in repo.get_all_sales():
        print(sale)

def ServiceTest():
    service = SalesService()

    # Create customers
    customer1 = service.create_customer(1, "Alice Smith", "alice@example.com", "123 Maple Street")
    customer2 = service.create_customer(2, "Bob Johnson", "bob@example.com", "456 Oak Avenue")

    # Create inventory items
    item1 = service.create_inventory_item(1, "Laptop", 10, 999.99, "Electronics")
    item2 = service.create_inventory_item(2, "Desk Chair", 25, 79.99, "Furniture")

    # Create sales items
    sale1 = service.create_sales(1, customer1.customer_id, item1.inventory_id, SalesType.QUOTE,5)
    sale2 = service.create_sales(2, customer2.customer_id, item2.inventory_id, SalesType.ORDER,3)

    # Read and display all customers, inventory, and sales
    print("All Customers:")
    for customer in service.get_all_customers():
        print(customer)

    print("\nAll Inventory Items:")
    for item in service.get_all_inventory():
        print(item)

    print("\nAll Sales Items:")
    for sale in service.get_all_sales():
        print(sale)
    # service.transform_order_to_invoice(2)
    return service
    
from Ui.CustomerList import CustomerList
import tkinter as tk
from Ui.RoleCenter import RoleCenter

if __name__ == "__main__":
    # InventoryTest()
    # CustomerTest()
    # SalesTest()
    service=ServiceTest()
    root = tk.Tk()
    app = RoleCenter(root, service)
    root.mainloop()