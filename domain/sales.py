from enum import Enum
# Define the SalesType Enum
class SalesType(Enum):
    QUOTE = 'Quote'
    ORDER = 'Order'
    INVOICE = 'Invoice'


class Sales:
    def __init__(self, sales_id, customer_id, item_id, salestype: SalesType,quantity,pricePerItem):
        if not isinstance(salestype, SalesType):
            raise ValueError("Invalid sales type. Must be one of: 'Quote', 'Order', 'Invoice'.")

        self.sales_id = sales_id
        self.customer_id = customer_id
        self.item_id = item_id
        self.salestype = salestype
        self.quantity = quantity
        self.pricePerItem=pricePerItem
    def __repr__(self):
        return f"Sales(sales_id={self.sales_id}, customer_id={self.customer_id}, item_id={self.item_id}, type={self.salestype.name}, quatity={self.quantity}, pricePerItem={self.pricePerItem})"
