# infrastructure/sales_repository.py
from domain.sales import *

class SalesRepository:
    def __init__(self):
        self.sales = []
        self.current_max_id = 0  

    def get_next_id(self):
        """Returns the next available customer ID, incrementing the counter."""
        self.current_max_id += 1
        return self.current_max_id
    
    def add_sales(self, sale):
        if not isinstance(sale, Sales):
            raise TypeError("Only Sales objects can be added to the repository.")
        self.sales.append(sale)

    def get_sales_by_id(self, sales_id):
        for sale in self.sales:
            if sale.sales_id == sales_id:
                return sale
        return None

    def update_sales(self, sales_id, customer_id=None, item_id=None, salestype=None,quantity=None):
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
                sale.quantity = quantity
            return sale
        return None

    def delete_sales(self, sales_id):
        sale = self.get_sales_by_id(sales_id)
        if sale:
            self.sales.remove(sale)
            return sale
        return None

    def get_all_sales(self):
        return self.sales
