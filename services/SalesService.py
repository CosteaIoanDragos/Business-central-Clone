# service/sales_service.py
from repos.CustomerRepo import CustomerRepository
from repos.InventoryRepo import InventoryRepository
from repos.SalesRepo import SalesRepository
from domain.customer import Customer
from domain.inventory import Inventory
from domain.sales import *
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class SalesService:
    def __init__(self):
        self.customer_repo = CustomerRepository()
        self.inventory_repo = InventoryRepository()
        self.sales_repo = SalesRepository()

    def create_customer(self, customer_id, name, email, address):
        customer_id=self.customer_repo.get_next_id()
        customer = Customer(customer_id, name, email, address)
        self.customer_repo.add_customer(customer)
        return customer

    def create_inventory_item(self, inventory_id, name, nr, price, type):
        inventory_id=self.inventory_repo.get_next_id()
        inventory = Inventory(inventory_id, name, nr, price, type)
        self.inventory_repo.add_inventory(inventory)
        return inventory

    def create_sales(self, sales_id, customer_id, item_id, salestype,quantity):
        # Check if the customer exists
        customer = self.customer_repo.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist.")

        # Check if the item exists
        item = self.inventory_repo.get_inventory_by_id(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} does not exist.")

        # If both customer and item exist, create the sale
        sales_id = self.sales_repo.get_next_id()
        pricePerItem=item.price
        sales = Sales(sales_id, customer_id, item_id, salestype,quantity,pricePerItem)
        self.sales_repo.add_sales(sales)
        return sales

    def get_customer_by_id(self, customer_id):
        return self.customer_repo.get_customer_by_id(customer_id)

    def get_inventory_by_id(self, inventory_id):
        return self.inventory_repo.get_inventory_by_id(inventory_id)

    def get_sales_by_id(self, sales_id):
        return self.sales_repo.get_sales_by_id(sales_id)

    def update_customer(self, customer_id, name=None, email=None, address=None):
        return self.customer_repo.update_customer(customer_id, name, email, address)

    def update_inventory(self, inventory_id, name=None, nr=None, price=None, type=None):
        return self.inventory_repo.update_inventory(inventory_id, name, nr, price, type)

    def update_sales(self, sales_id, customer_id=None, item_id=None, salestype=None,quantity=None):
        return self.sales_repo.update_sales(sales_id, customer_id, item_id, salestype,quantity)

    def delete_customer(self, customer_id):
        return self.customer_repo.delete_customer(customer_id)

    def delete_inventory(self, inventory_id):
        return self.inventory_repo.delete_inventory(inventory_id)

    def delete_sales(self, sales_id):
        return self.sales_repo.delete_sales(sales_id)

    def get_all_customers(self):
        return self.customer_repo.get_all_customers()

    def get_all_inventory(self):
        return self.inventory_repo.get_all_inventory()

    def get_all_sales(self):
        return self.sales_repo.get_all_sales()
  # Sorting and filtering methods
    def get_customers_sorted(self, key, reverse=False):
        """
        Sorts customers based on the given key.
        :param key: Attribute to sort by (e.g., 'name', 'email').
        :param reverse: True for descending order, False for ascending.
        """
        customers = self.get_all_customers()
        return sorted(customers, key=lambda x: getattr(x, key), reverse=reverse)

    def get_inventory_sorted(self, key, reverse=False):
        """
        Sorts inventory based on the given key.
        :param key: Attribute to sort by (e.g., 'price', 'nr').
        :param reverse: True for descending order, False for ascending.
        """
        inventory = self.get_all_inventory()
        return sorted(inventory, key=lambda x: getattr(x, key), reverse=reverse)

    def get_sales_sorted(self, key, reverse=False):
        """
        Sorts sales based on the given key.
        :param key: Attribute to sort by (e.g., 'sales_id', 'customer_id').
        :param reverse: True for descending order, False for ascending.
        """
        sales = self.get_all_sales()
        return sorted(sales, key=lambda x: getattr(x, key), reverse=reverse)

    def filter_customers_with_regex(self, regex):
        """Filters customers by name, email, or address using a regular expression."""
        filtered = []
        pattern = re.compile(regex, re.IGNORECASE)  # Compile the regex pattern for case-insensitive search

        for customer in self.get_all_customers():
            if pattern.search(customer.name) or pattern.search(customer.email) or pattern.search(customer.address):
                filtered.append(customer)

        return filtered


    def filter_inventory_with_regex(self, regex):
        """
        Filters inventory based on key-value pairs.
        :param filters: Attributes and their desired values.
        """
        filtered = []
        pattern = re.compile(regex, re.IGNORECASE)  # Compile the regex pattern for case-insensitive search

        for item in self.get_all_inventory():
            # Ensure each attribute is treated as a string
            if (pattern.search(str(item.name)) or 
                pattern.search(str(item.nr)) or 
                pattern.search(str(item.price)) or 
                pattern.search(str(item.type))):
                filtered.append(item)  

        return filtered

    def filter_sales_with_regex(self, regex):
        """
        Filters sales based on key-value pairs.
        :param filters: Attributes and their desired values.
        """
        filtered = []
        pattern = re.compile(regex, re.IGNORECASE)  # Compile the regex pattern for case-insensitive search

        for sale in self.get_all_sales():
            if pattern.search(str(sale.sales_id)) or pattern.search(str(sale.customer_id)) or pattern.search(str(sale.item_id))or pattern.search(str(sale.salestype)):
                filtered.append(sale)

        return filtered
    
    #invetory should be updated when a sale is made
    def transform_quote_to_order(self, sales_id):
        sale = self.get_sales_by_id(sales_id)
        print('hello',sale)
        if sale.salestype == SalesType.QUOTE:
            sale.salestype = SalesType.ORDER
            item=self.get_inventory_by_id(sale.item_id)
            self.update_inventory(sale.item_id,item.name, item.nr-sale.quantity,item.price,item.type)
            return sale
        return None
    
    #invoice should be generated when a sale is made
    def transform_order_to_invoice(self, sales_id, output_dir="invoices"):
        sale = self.get_sales_by_id(sales_id)
        
        if sale is None:
            raise ValueError(f"Sale with ID {sales_id} does not exist.")

        # Ensure the sale is of type ORDER
        if sale.salestype != SalesType.ORDER:
            raise ValueError("Only sales of type 'ORDER' can be transformed into an invoice.")
        
        # Update the sale type to INVOICE
        sale.salestype = SalesType.INVOICE
        self.sales_repo.update_sales(sale.sales_id, sale.customer_id, sale.item_id, sale.salestype, sale.quantity)

        # Generate the invoice as a PDF
        self._generate_invoice_pdf(sale, output_dir)

        return sale

    def _generate_invoice_pdf(self, sale, output_dir):
        """
        Generates a PDF invoice for a given sale.
        :param sale: The sale object for which the invoice is generated.
        :param output_dir: Directory where the invoice PDF will be saved.
        """
        # Ensure the output directory exists
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Fetch related details for the invoice
        customer = self.get_customer_by_id(sale.customer_id)
        item = self.get_inventory_by_id(sale.item_id)

        if not customer or not item:
            raise ValueError("Invalid customer or item ID in the sales record.")

        # Define the PDF filename and create the canvas
        invoice_file = os.path.join(output_dir, f"Invoice_{sale.sales_id}.pdf")
        c = canvas.Canvas(invoice_file, pagesize=letter)

        # Add invoice details
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "Invoice")
        c.setFont("Helvetica", 12)

        # Invoice metadata
        c.drawString(50, 700, f"Invoice ID: {sale.sales_id}")
        c.drawString(50, 680, f"Customer Name: {customer.name}")
        c.drawString(50, 660, f"Customer Email: {customer.email}")
        c.drawString(50, 640, f"Address: {customer.address}")
        c.drawString(50, 620, f"Item: {item.name}")
        c.drawString(50, 600, f"Quantity: {sale.quantity}")
        c.drawString(50, 580, f"Price per Unit: ${item.price:.2f}")
        c.drawString(50, 560, f"Total: ${item.price * sale.quantity:.2f}")
        c.drawString(50, 540, f"Sale Type: {sale.salestype.name}")
        
        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, 500, "Thank you for your business!")
        
        # Save the PDF
        c.save()
        print(f"Invoice saved as: {invoice_file}")
