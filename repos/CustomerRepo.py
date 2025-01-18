# infrastructure/customer_repository.py
from domain.customer import Customer

class CustomerRepository:
    def __init__(self):
        self.customers = []
        self.current_max_id = 0  # We'll use this to track the highest ID assigned

    def get_next_id(self):
        """Returns the next available customer ID, incrementing the counter."""
        self.current_max_id += 1
        return self.current_max_id

    def add_customer(self, customer):
        self.customers.append(customer)

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
            return customer
        return None

    def delete_customer(self, customer_id):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            self.customers.remove(customer)
            return customer
        return None

    def get_all_customers(self):
        return self.customers
