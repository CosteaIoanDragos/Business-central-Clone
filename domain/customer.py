class Customer:
    def __init__(self, customer_id, name, email, address):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.address = address

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.name}, {self.email}, {self.address})"
