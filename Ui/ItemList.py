import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import re  # Import re for regular expression support
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.SalesService import SalesService

class ItemList:
    def __init__(self, parent, service):
        self.parent = parent
        self.service = service

        # Set window title and size
        # self.parent.title("Item Management System")
        # self.parent.geometry("900x650")
        # self.parent.configure(bg="#f0f4fc")  # Light blue background

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
        self.title_label = ttk.Label(self.container, text="Item Management Dashboard", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Filter Section
        self.filter_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)

        self.filter_key_label = ttk.Label(self.filter_frame, text="Filter (Regex allowed):")
        self.filter_key_label.pack(side=tk.LEFT, padx=5)

        self.filter_name = ttk.Entry(self.filter_frame, width=30)
        self.filter_name.pack(side=tk.LEFT, padx=5)
        
        self.filter_button = ttk.Button(self.filter_frame, text="Filter", command=self.filter_items)
        self.filter_button.pack(side=tk.LEFT, padx=5)

        # Sort Section
        self.sort_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.sort_frame.pack(fill=tk.X, padx=5, pady=5)

        self.sort_key_label = ttk.Label(self.sort_frame, text="Sort By:")
        self.sort_key_label.pack(side=tk.LEFT, padx=5)

        self.sort_key = tk.StringVar(self.parent)
        self.sort_key.set("name")  # Default sorting by 'name'
        self.sort_key_menu = ttk.OptionMenu(self.sort_frame, self.sort_key, "name", "name", "price", "type")
        self.sort_key_menu.pack(side=tk.LEFT, padx=5)

        self.sort_order_var = tk.BooleanVar(self.parent, value=False)  # False for ascending, True for descending
        self.sort_order_checkbox = ttk.Checkbutton(self.sort_frame, text="Descending Order", variable=self.sort_order_var)
        self.sort_order_checkbox.pack(side=tk.LEFT, padx=5)
        
        self.sort_button = ttk.Button(self.sort_frame, text="Sort", command=self.sort_items)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        # Customer List Section
        self.list_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.listbox_label = ttk.Label(self.list_frame, text="Item List", font=("Arial", 12, "bold"))
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

        self.add_button = ttk.Button(self.button_frame, text="Add Item", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Item", command=self.edit_item)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self.button_frame, text="Remove Item", command=self.remove_item)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.refresh_item_list()

    def refresh_item_list(self):
        """Refresh the listbox to display the current list of items."""
        self.listbox.delete(0, tk.END)
        for item in self.service.get_all_inventory():
            self.listbox.insert(tk.END, f"{item.inventory_id}: {item.name} - {item.nr} units, ${item.price}, {item.type}")

    def add_item(self):
        """Opens a dialog to add a new item."""
        self.add_item_dialog("Add Item")

    def edit_item(self):
        """Edits the selected item from the list."""
        selected = self.listbox.curselection()
        if selected:
            item_info = self.listbox.get(selected[0]).split(":")
            item_id = item_info[0].strip()
            item_id = int(item_id)
            self.edit_item_dialog("Edit Item", item_id)
        else:
            messagebox.showwarning("Select Item", "Please select an item to edit.")

    def remove_item(self):
        """Removes the selected item."""
        selected = self.listbox.curselection()
        if selected:
            item_info = self.listbox.get(selected[0]).split(":")
            item_id = item_info[0].strip()
            confirmation = messagebox.askyesno("Delete Item", f"Are you sure you want to delete this item? Id: {item_id}")
            if confirmation:
                item_id = int(item_id)
                self.service.delete_inventory(item_id)
                self.refresh_item_list()
        else:
            messagebox.showwarning("Select Item", "Please select an item to remove.")

    def add_item_dialog(self, title):
        """Opens a dialog for adding/editing an item."""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)

        # Create labels and entry fields for item ID, Name, Price, Quantity, Type
        label_name = ttk.Label(dialog, text="Name:")
        label_name.grid(row=1, column=0, padx=10, pady=10)
        entry_name = ttk.Entry(dialog)
        entry_name.grid(row=1, column=1, padx=10, pady=10)

        label_price = ttk.Label(dialog, text="Price:")
        label_price.grid(row=2, column=0, padx=10, pady=10)
        entry_price = ttk.Entry(dialog)
        entry_price.grid(row=2, column=1, padx=10, pady=10)

        label_quantity = ttk.Label(dialog, text="Quantity:")
        label_quantity.grid(row=3, column=0, padx=10, pady=10)
        entry_quantity = ttk.Entry(dialog)
        entry_quantity.grid(row=3, column=1, padx=10, pady=10)

        label_type = ttk.Label(dialog, text="Type:")
        label_type.grid(row=4, column=0, padx=10, pady=10)
        entry_type = ttk.Entry(dialog)
        entry_type.grid(row=4, column=1, padx=10, pady=10)

        def save_item():
            name = entry_name.get()
            price = entry_price.get()
            quantity = entry_quantity.get()
            item_type = entry_type.get()
            if not name or not price or not quantity or not item_type:
                messagebox.showwarning("Input Error", "All fields must be filled in.")
                return

            if not name.isalpha():
                messagebox.showwarning("Input Error", "Name must only contain letters.")
                return

            try:
                price = float(price)
                if price <= 0:
                    messagebox.showwarning("Input Error", "Price must be a positive number.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Price must be a valid number.")
                return

            try:
                quantity = int(quantity)
                if quantity <= 0:
                    messagebox.showwarning("Input Error", "Quantity must be a positive integer.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Quantity must be a valid integer.")
                return
            messagebox.showinfo("Success", "Item saved successfully!")
            new_item = self.service.create_inventory_item(None, name,  int(quantity),float(price), item_type)
            dialog.destroy()
            self.refresh_item_list()

        # Add Save button for both adding and editing items
        save_button = ttk.Button(dialog, text="Save", command=save_item)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_item_dialog(self, title, item_id):
        """Opens a dialog for editing an item."""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)

        # Create labels and entry fields for item ID, Name, Price, Quantity, Type
        label_name = ttk.Label(dialog, text="Name:")
        label_name.grid(row=1, column=0, padx=10, pady=10)
        entry_name = ttk.Entry(dialog)
        entry_name.grid(row=1, column=1, padx=10, pady=10)

        label_price = ttk.Label(dialog, text="Price:")
        label_price.grid(row=2, column=0, padx=10, pady=10)
        entry_price = ttk.Entry(dialog)
        entry_price.grid(row=2, column=1, padx=10, pady=10)

        label_quantity = ttk.Label(dialog, text="Quantity:")
        label_quantity.grid(row=3, column=0, padx=10, pady=10)
        entry_quantity = ttk.Entry(dialog)
        entry_quantity.grid(row=3, column=1, padx=10, pady=10)

        label_type = ttk.Label(dialog, text="Type:")
        label_type.grid(row=4, column=0, padx=10, pady=10)
        entry_type = ttk.Entry(dialog)
        entry_type.grid(row=4, column=1, padx=10, pady=10)

        item = self.service.get_inventory_by_id(item_id)
        entry_name.insert(0, item.name)
        entry_price.insert(0, str(item.price))
        entry_quantity.insert(0, str(item.nr))
        entry_type.insert(0, item.type)

        def save_item():
            name = entry_name.get()
            price = entry_price.get()
            quantity = entry_quantity.get()
            item_type = entry_type.get()

            if not name or not price or not quantity or not item_type:
                messagebox.showwarning("Input Error", "All fields must be filled in.")
                return

            if not name.isalpha():
                messagebox.showwarning("Input Error", "Name must only contain letters.")
                return

            try:
                price = float(price)
                if price <= 0:
                    messagebox.showwarning("Input Error", "Price must be a positive number.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Price must be a valid number.")
                return

            try:
                quantity = int(quantity)
                if quantity <= 0:
                    messagebox.showwarning("Input Error", "Quantity must be a positive integer.")
                    return
            except ValueError:
                messagebox.showwarning("Input Error", "Quantity must be a valid integer.")
                return
            messagebox.showinfo("Success", "Item saved successfully!")

            self.service.update_inventory(item_id, name,  int(quantity),float(price), item_type)
            dialog.destroy()
            self.refresh_item_list()

        save_button = ttk.Button(dialog, text="Save", command=save_item)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def filter_items(self):
        """Filters items using regex and updates the listbox."""
        filter_value = self.filter_name.get()  # Get the value from the filter entry field
        if filter_value == "":  # If the filter is empty, refresh the list
            self.refresh_item_list()
            return
        else:
            try:
                filtered_items = self.service.filter_inventory_with_regex(filter_value)  # Call filter_items_with_regex from service
            except re.error:
                messagebox.showerror("Invalid Regex", "The regular expression is invalid. Please try again.")
                return

        # Update listbox with filtered items
        self.listbox.delete(0, tk.END)
        for item in filtered_items:
            self.listbox.insert(tk.END, f"{item.inventory_id}: {item.name} - {item.nr} units, ${item.price}, {item.type}")

    def sort_items(self):
        """Sorts the items by the selected attribute and order."""
        sort_key = self.sort_key.get()  # Get the selected sort attribute (name, price, type)
        sort_reverse = self.sort_order_var.get()  # Get whether it's in descending order or not
        sorted_items = self.service.get_inventory_sorted(sort_key, sort_reverse)

        # Update listbox with sorted items
        self.listbox.delete(0, tk.END)
        for item in sorted_items:
            self.listbox.insert(tk.END, f"{item.inventory_id}: {item.name} - {item.nr} units, ${item.price}, {item.type}")


if __name__ == "__main__":
    root = tk.Tk()
    service = SalesService()  # Assuming SalesService is imported
    app = ItemList(root, service)
    root.mainloop()
