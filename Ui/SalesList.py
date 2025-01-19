import tkinter as tk
from tkinter import messagebox, ttk
import sys

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.sales import SalesType 
from services.SalesService import SalesService


class SalesList:
    def __init__(self, parent, service):
        self.parent = parent
        self.service = service

        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5, background="#1e81b0", foreground="white")
        style.map("TButton", background=[("active", "#16658a")])
        style.configure("TLabel", font=("Arial", 10), background="#f0f4fc", foreground="#1e3a5f")
        style.configure("TEntry", padding=5, background="white")
        style.configure("TFrame", background="#f0f4fc")
        style.configure("TCheckbutton", background="#f0f4fc", font=("Arial", 10), foreground="#1e3a5f")
        style.configure("TOptionMenu", background="white", foreground="#1e3a5f", font=("Arial", 10))

        # Main container frame
        self.container = ttk.Frame(parent, padding=10)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Title Section
        self.title_label = ttk.Label(self.container, text="Sales Management Dashboard", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Filter Section
        self.filter_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.filter_frame.pack(fill=tk.X, padx=5, pady=5)

        self.filter_key_label = ttk.Label(self.filter_frame, text="Filter (Regex allowed):")
        self.filter_key_label.pack(side=tk.LEFT, padx=5)

        self.filter_entry = ttk.Entry(self.filter_frame, width=30)
        self.filter_entry.pack(side=tk.LEFT, padx=5)

        self.filter_button = ttk.Button(self.filter_frame, text="Filter", command=self.filter_sales)
        self.filter_button.pack(side=tk.LEFT, padx=5)

        # Sort Section
        self.sort_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.sort_frame.pack(fill=tk.X, padx=5, pady=5)

        self.sort_key_label = ttk.Label(self.sort_frame, text="Sort By:")
        self.sort_key_label.pack(side=tk.LEFT, padx=5)

        self.sort_key = tk.StringVar(self.parent)
        self.sort_key.set("date")  # Default sorting by 'date'
        self.sort_key_menu = ttk.OptionMenu(self.sort_frame, self.sort_key, "sales_id", "customer_id", "item_id")
        self.sort_key_menu.pack(side=tk.LEFT, padx=5)

        self.sort_order_var = tk.BooleanVar(self.parent, value=False)
        self.sort_order_checkbox = ttk.Checkbutton(self.sort_frame, text="Descending Order", variable=self.sort_order_var)
        self.sort_order_checkbox.pack(side=tk.LEFT, padx=5)

        self.sort_button = ttk.Button(self.sort_frame, text="Sort", command=self.sort_sales)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        # Sales List Section
        self.list_frame = ttk.Frame(self.container, padding=10, relief="solid")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.listbox_label = ttk.Label(self.list_frame, text="Sales List", font=("Arial", 12, "bold"))
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

        self.add_button = ttk.Button(self.button_frame, text="Add Sale", command=self.add_sale)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Sale", command=self.edit_sale)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self.button_frame, text="Remove Sale", command=self.remove_sale)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.transform_button = ttk.Button(self.button_frame, text="Transform Quote to Order", command=self.transform_quote_to_order)
        self.transform_button.pack(side=tk.LEFT, padx=5)
        self.transform_button2 = ttk.Button(self.button_frame, text="Transform Order to Invoice", command=self.transform_order_to_invoice)
        self.transform_button2.pack(side=tk.LEFT, padx=5)

        # Bind listbox selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        self.refresh_sales_list()

    def refresh_sales_list(self):
        """Refresh the listbox to display the current list of sales."""
        self.listbox.delete(0, tk.END)
        for sale in self.service.get_all_sales():
            self.listbox.insert(tk.END, f"{sale.sales_id}: Customer {sale.customer_id} bought Item {sale.item_id}, {sale.salestype.name}, quantity:{sale.quantity}, Price Per Item:{sale.pricePerItem:.2f}, Total Price:{(sale.pricePerItem*sale.quantity):.2f}")

    def add_sale(self):
        """Opens a dialog to add a new sale."""
        self.add_sale_dialog("Add Sale")

    def edit_sale(self):
        """Edits the selected sale from the list."""
        selected = self.listbox.curselection()
        if selected:
            sale_info = self.listbox.get(selected[0]).split(":")
            sale_id = sale_info[0].strip()
            sale_id = int(sale_id)
            self.edit_sale_dialog("Edit Sale", sale_id)
        else:
            messagebox.showwarning("Select Sale", "Please select a sale to edit.")

    def remove_sale(self):
        """Removes the selected sale."""
        selected = self.listbox.curselection()
        if selected:
            sale_info = self.listbox.get(selected[0]).split(":")
            sale_id = sale_info[0].strip()
            confirmation = messagebox.askyesno("Delete Sale", f"Are you sure you want to delete this sale? Id: {sale_id}")
            if confirmation:
                sale_id = int(sale_id)
                self.service.delete_sales(sale_id)
                self.refresh_sales_list()
        else:
            messagebox.showwarning("Select Sale", "Please select a sale to remove.")

    def add_sale_dialog(self, title):
        """Opens a dialog for adding/editing a sale."""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x250")

        # Create labels and entry fields for sale details (sales_id, customer_id, item_id, salestype)
        label_customer_id = ttk.Label(dialog, text="Customer ID:")
        label_customer_id.grid(row=1, column=0, padx=10, pady=10)
        entry_customer_id = ttk.Entry(dialog,width=30)
        entry_customer_id.grid(row=1, column=1, padx=10, pady=10)

        label_item_id = ttk.Label(dialog, text="Item ID:")
        label_item_id.grid(row=2, column=0, padx=10, pady=10)
        entry_item_id = ttk.Entry(dialog,width=30)
        entry_item_id.grid(row=2, column=1, padx=10, pady=10)

        label_salestype = ttk.Label(dialog, text="Sale Type:")
        label_salestype.grid(row=3, column=0, padx=10, pady=10)
        
        label_quantity = ttk.Label(dialog, text="Quantity :")
        label_quantity.grid(row=4, column=0, padx=10, pady=10)
        entry_quantity = ttk.Entry(dialog,width=30)
        entry_quantity.grid(row=4, column=1, padx=10, pady=10)

        # OptionMenu for SalesType
        salestype_var = tk.StringVar(dialog)
        salestype_var.set(SalesType.QUOTE.name)  # Default selection
        salestype_menu = ttk.OptionMenu(dialog, salestype_var, *[st.name for st in SalesType])
        salestype_menu.grid(row=3, column=1)

        def save_sale():
            customer_id = entry_customer_id.get()
            item_id = entry_item_id.get()
            salestype = salestype_var.get()
            quantity = entry_quantity.get()
            if not customer_id or not item_id or not salestype:
                messagebox.showwarning("Input Error", "All fields must be filled in.")
                return
            try:
                # Create sale and pass None for sales_id (it will be generated automatically)
                new_sale = self.service.create_sales(None, int(customer_id), int(item_id), SalesType[salestype], int(quantity))  # Convert to SalesType enum
                dialog.destroy()
                self.refresh_sales_list()
            except ValueError as e:
                # Display error message from service
                messagebox.showerror("Error", str(e))

        save_button = ttk.Button(dialog, text="Save", command=save_sale)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_sale_dialog(self, title, sale_id):
        """Opens a dialog for editing a sale."""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)

        label_customer_id = ttk.Label(dialog, text="Customer ID:")
        label_customer_id.grid(row=1, column=0, padx=10, pady=10)
        entry_customer_id = ttk.Entry(dialog,width=30)
        entry_customer_id.grid(row=1, column=1, padx=10, pady=10)

        label_item_id = ttk.Label(dialog, text="Item ID:")
        label_item_id.grid(row=2, column=0, padx=10, pady=10)
        entry_item_id = ttk.Entry(dialog,width=30)
        entry_item_id.grid(row=2, column=1, padx=10, pady=10)

        label_salestype = ttk.Label(dialog, text="Sale Type:")
        label_salestype.grid(row=3, column=0, padx=10, pady=10)

        label_quantity = ttk.Label(dialog, text="Quantity :")
        label_quantity.grid(row=4, column=0, padx=10, pady=10)
        entry_quantity = ttk.Entry(dialog,width=30)
        entry_quantity.grid(row=4, column=1, padx=10, pady=10)

        salestype_var = tk.StringVar(dialog)
        sale = self.service.get_sales_by_id(sale_id)
        salestype_var.set(sale.salestype.name)  # Set current sale type

        salestype_menu = ttk.OptionMenu(dialog, salestype_var, *[st.name for st in SalesType])
        salestype_menu.grid(row=3, column=1, padx=10, pady=10)

        entry_customer_id.insert(0, str(sale.customer_id))
        entry_item_id.insert(0, str(sale.item_id))
        entry_quantity.insert(0, str(sale.quantity))
        def save_sale():
            customer_id = entry_customer_id.get()
            item_id = entry_item_id.get()
            salestype = salestype_var.get()
            quantity = entry_quantity.get()
            if not customer_id or not item_id or not salestype:
                messagebox.showwarning("Input Error", "All fields must be filled in.")
                return
            self.service.update_sales(sale_id, int(customer_id), int(item_id), SalesType[salestype], int(quantity))
            dialog.destroy()
            self.refresh_sales_list()

        save_button = ttk.Button(dialog, text="Save", command=save_sale)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def filter_sales(self):
        """Filters sales using regex and updates the listbox."""
        filter_value = self.filter_entry.get()  # Get the value from the filter entry field
        if filter_value == "":  # If the filter is empty, refresh the list
            self.refresh_sales_list()
            return
        else:
            try:
                filtered_sales = self.service.filter_sales_with_regex(filter_value)  # Call filter_sales_with_regex from service
            except re.error:
                messagebox.showerror("Invalid Regex", "The regular expression is invalid. Please try again.")
                return

        # Update listbox with filtered sales
        self.listbox.delete(0, tk.END)
        for sale in filtered_sales:
            self.listbox.insert(tk.END, f"{sale.sales_id}: Customer {sale.customer_id} ordered Item {sale.item_id}, {sale.salestype.name}, quantity:{sale.quantity}, price:{sale.pricePerItem:.2f}")

    def sort_sales(self):
        """Sorts the sales by the selected attribute and order."""
        sort_key = self.sort_key.get()  # Get the selected sort attribute (sales_id, customer_id, item_id, salestype)
        sort_reverse = self.sort_order_var.get()  # Get whether it's in descending order or not
        sorted_sales = self.service.get_sales_sorted(sort_key, sort_reverse)

        # Update listbox with sorted sales
        self.listbox.delete(0, tk.END)
        for sale in sorted_sales:
            self.listbox.insert(tk.END, f"{sale.sales_id}: Customer {sale.customer_id} With Item {sale.item_id}, {sale.salestype.name}, quantity:{sale.quantity}, price:{sale.pricePerItem:.2f}")
    
    def on_listbox_select(self, event):
        """Show or hide the transform button based on selection."""
        selected = self.listbox.curselection()
        if not selected:
            self.hide_transform_button()
            return
        
        # Get selected item and check its type
        sale_info = self.listbox.get(selected[0]).split(":")
        sale_id = int(sale_info[0].strip())
        sale = self.service.get_sales_by_id(sale_id)
        
        if sale.salestype == SalesType.QUOTE:
            self.show_transform_button()
        else:
            self.hide_transform_button()
        if sale.salestype == SalesType.ORDER:
            self.show_transform2_button()
        else:
            self.hide_transform2_button()


    def show_transform_button(self):
        """Displays the Transform Quote to Order button.""" 
        self.transform_button.pack(padx=5, pady=5, side=tk.LEFT)

    def hide_transform_button(self):
        """Hides the Transform Quote to Order button.""" 
        self.transform_button.pack_forget()

    def transform_quote_to_order(self):
        """Transforms the selected quote to an order."""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a quote to transform.")
            return

        # Get selected item details
        sale_info = self.listbox.get(selected[0]).split(":")
        sale_id = int(sale_info[0].strip())
        sale = self.service.get_sales_by_id(sale_id)
        
        if sale.salestype != SalesType.QUOTE:
            messagebox.showerror("Invalid Selection", "The selected sale is not a quote.")
            return

        # Confirm the transformation
        confirmation = messagebox.askyesno("Transform Quote", f"Are you sure you want to transform quote {sale_id} to an order?")
        if confirmation:
            try:
                self.service.transform_quote_to_order(sale_id)
                self.refresh_sales_list()
                messagebox.showinfo("Success", f"Quote {sale_id} has been successfully transformed to an order.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to transform quote: {str(e)}")

    def show_transform2_button(self):
        self.transform_button2.pack(padx=5, pady=5, side=tk.LEFT)

    def hide_transform2_button(self):
        self.transform_button2.pack_forget()

    def transform_order_to_invoice(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an Order to transform.")
            return

        # Get selected item details
        sale_info = self.listbox.get(selected[0]).split(":")
        sale_id = int(sale_info[0].strip())
        sale = self.service.get_sales_by_id(sale_id)
        
        if sale.salestype != SalesType.ORDER:
            messagebox.showerror("Invalid Selection", "The selected sale is not an Order.")
            return

        # Confirm the transformation
        confirmation = messagebox.askyesno("Transform Order", f"Are you sure you want to transform Order to an invoice {sale_id} to an order?")
        if confirmation:
            try:
                self.service.transform_order_to_invoice(sale_id)
                self.refresh_sales_list()
                messagebox.showinfo("Success", f"Order {sale_id} has been successfully transformed to an invoice.")
            except Exception as e:
                messagebox.showinfo
                ("Error", f"Failed to transform order: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    service = SalesService()  # Assuming SalesService is imported
    app = SalesList(root, service)

    root.mainloop()
