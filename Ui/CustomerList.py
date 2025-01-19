import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import re  # Import re for regular expression support
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.SalesService import SalesService


class CustomerList:
    def __init__(self, parent, service):
        self.parent = parent
        self.service = service
        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")  # Use a modern theme
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5, background="#1e81b0", foreground="white")
        style.map("TButton", background=[("active", "#16658a")])  # Darker blue on hover
        style.configure("TLabel", font=("Arial", 10), background="#f0f4fc", foreground="#1e3a5f")
        style.configure("TEntry", padding=5, background="white")
        style.configure("TFrame", background="#f0f4fc")
        style.configure("TCheckbutton", background="#f0f4fc", font=("Arial", 10), foreground="#1e3a5f")
        style.configure("TOptionMenu", background="white", foreground="#1e3a5f", font=("Arial", 10))

        # Main container frame
        self.container = ttk.Frame(parent, padding=10)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Title Section
        self.title_label = ttk.Label(self.container, text="Customer Management Dashboard", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Filter Section
        self.filter_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)

        self.filter_key_label = ttk.Label(self.filter_frame, text="Filter (Regex allowed):")
        self.filter_key_label.pack(side=tk.LEFT, padx=5)

        self.filter_name = ttk.Entry(self.filter_frame, width=30)
        self.filter_name.pack(side=tk.LEFT, padx=5)

        self.filter_button = ttk.Button(self.filter_frame, text="Filter", command=self.filter_customers)
        self.filter_button.pack(side=tk.LEFT, padx=5)

        # Sort Section
        self.sort_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.sort_frame.pack(fill=tk.X, padx=5, pady=5)

        self.sort_key_label = ttk.Label(self.sort_frame, text="Sort By:")
        self.sort_key_label.pack(side=tk.LEFT, padx=5)

        self.sort_key = tk.StringVar(self.parent)
        self.sort_key.set("name")  # Default sorting by 'name'
        self.sort_key_menu = ttk.OptionMenu(self.sort_frame, self.sort_key, "name",'name', "email", "address")
        self.sort_key_menu.pack(side=tk.LEFT, padx=5)

        self.sort_order_var = tk.BooleanVar(self.parent, value=False)  # False for ascending, True for descending
        self.sort_order_checkbox = ttk.Checkbutton(self.sort_frame, text="Descending Order", variable=self.sort_order_var)
        self.sort_order_checkbox.pack(side=tk.LEFT, padx=5)

        self.sort_button = ttk.Button(self.sort_frame, text="Sort", command=self.sort_customers)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        # Customer List Section
        self.list_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.listbox_label = ttk.Label(self.list_frame, text="Customer List", font=("Arial", 12, "bold"))
        self.listbox_label.pack(anchor=tk.W, pady=5)

        self.listbox = tk.Listbox(self.list_frame, width=100, height=20, font=("Arial", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar for the listbox
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button Section
        self.button_frame = ttk.Frame(self.container, padding=10)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_button = ttk.Button(self.button_frame, text="Add Customer", command=self.add_customer)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Customer", command=self.edit_customer)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self.button_frame, text="Remove Customer", command=self.remove_customer)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.refresh_customer_list()

    def refresh_customer_list(self):
        """Refresh the listbox to display the current list of customers."""
        self.listbox.delete(0, tk.END)
        for customer in self.service.get_all_customers():
            self.listbox.insert(tk.END, f"{customer.customer_id}: {customer.name} - {customer.email}, {customer.address}")

    def add_customer(self):
        """Opens a dialog to add a new customer."""
        self.add_customer_dialog("Add Customer")

    def edit_customer(self):
        """Edits the selected customer from the list."""
        selected = self.listbox.curselection()
        if selected:
            customer_info = self.listbox.get(selected[0]).split(":")
            customer_id = customer_info[0].strip()
            customer_id = int(customer_id)
            self.Edit_customer_dialog("Edit Customer", customer_id)
        else:
            messagebox.showwarning("Select Customer", "Please select a customer to edit.")

    def remove_customer(self):
        """Removes the selected customer."""
        selected = self.listbox.curselection()
        if selected:
            customer_info = self.listbox.get(selected[0]).split(":")
            customer_id = customer_info[0].strip()
            confirmation = messagebox.askyesno("Delete Customer", f"Are you sure you want to delete this customer? Id: {customer_id}")
            if confirmation:
                customer_id = int(customer_id)
                self.service.delete_customer(customer_id)
                self.refresh_customer_list()
        else:
            messagebox.showwarning("Select Customer", "Please select a customer to remove.")

    def add_customer_dialog(self, title):
        """Opens a dialog for adding a customer."""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x250")

        # Fields for Name, Email, Address
        fields = {"Name": None, "Email": None, "Address": None}
        for i, field in enumerate(fields.keys()):
            label = ttk.Label(dialog, text=f"{field}:")
            label.grid(row=i, column=0, padx=10, pady=10)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=10)
            fields[field] = entry

        def save_customer():
            name = fields["Name"].get()
            email = fields["Email"].get()
            address = fields["Address"].get()

            # Check if all fields are filled
            if not name or not email or not address:
                messagebox.showwarning("Input Error", "All fields must be filled in.")
                return

            # Validate the name (if it should only contain alphabetic characters)
            if not name.isalpha() and not name.replace(" ", "").isalpha():
                messagebox.showwarning("Input Error", "Name must only contain letters and spaces.")
                return

            # Validate email format using regex
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                messagebox.showwarning("Input Error", "Invalid email format.")
                return

            # Optionally validate address (e.g., length check)
            if len(address) < 10:
                messagebox.showwarning("Input Error", "Address must be at least 10 characters long.")
                return

            # If all validations pass, proceed with saving the customer
            messagebox.showinfo("Success", "Customer details saved successfully.")

            new_customer = self.service.create_customer(None, name, email, address)
            dialog.destroy()
            self.refresh_customer_list()

        ttk.Button(dialog, text="Save", command=save_customer).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def Edit_customer_dialog(self, title, customer_id):
        """Opens a dialog for editing a customer."""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x250")

        # Fields for Name, Email, Address
        fields = {"Name": None, "Email": None, "Address": None}
        customer = self.service.get_customer_by_id(customer_id)
        for i, field in enumerate(fields.keys()):
            label = ttk.Label(dialog, text=f"{field}:")
            label.grid(row=i, column=0, padx=10, pady=10)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=10)
            fields[field] = entry

        fields["Name"].insert(0, customer.name)
        fields["Email"].insert(0, customer.email)
        fields["Address"].insert(0, customer.address)

        def save_customer():
            name = fields["Name"].get()
            email = fields["Email"].get()
            address = fields["Address"].get()

            if not name or not email or not address:
                messagebox.showwarning("Input Error", "All fields must be filled in.")
                return

            # Validate the name (if it should only contain alphabetic characters)
            if not name.isalpha() and not name.replace(" ", "").isalpha():
                messagebox.showwarning("Input Error", "Name must only contain letters and spaces.")
                return

            # Validate email format using regex
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                messagebox.showwarning("Input Error", "Invalid email format.")
                return

            # Optionally validate address (e.g., length check)
            if len(address) < 10:
                messagebox.showwarning("Input Error", "Address must be at least 10 characters long.")
                return

            # If all validations pass, proceed with saving the customer
            messagebox.showinfo("Success", "Customer details saved successfully.")

            self.service.update_customer(customer_id, name, email, address)
            dialog.destroy()
            self.refresh_customer_list()

        ttk.Button(dialog, text="Save", command=save_customer).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def filter_customers(self):
        """Filters customers using regex."""
        filter_value = self.filter_name.get()
        if not filter_value:
            self.refresh_customer_list()
            return

        try:
            filtered_customers = self.service.filter_customers_with_regex(filter_value)
        except re.error:
            messagebox.showerror("Invalid Regex", "The regular expression is invalid.")
            return

        self.listbox.delete(0, tk.END)
        for customer in filtered_customers:
            self.listbox.insert(tk.END, f"{customer.customer_id}: {customer.name} - {customer.email}, {customer.address}")

    def sort_customers(self):
        """Sorts the customers."""
        sort_key = self.sort_key.get()
        sort_reverse = self.sort_order_var.get()
        sorted_customers = self.service.get_customers_sorted(sort_key, sort_reverse)

        self.listbox.delete(0, tk.END)
        for customer in sorted_customers:
            self.listbox.insert(tk.END, f"{customer.customer_id}: {customer.name} - {customer.email}, {customer.address}")


if __name__ == "__main__":
    root = tk.Tk()
    service = SalesService()
    app = CustomerList(root, service)
    root.mainloop()
