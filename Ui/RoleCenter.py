# gui/role_center.py
import tkinter as tk
from tkinter import ttk
from Ui.CustomerList import CustomerList
from Ui.ItemList import ItemList
from Ui.SalesList import SalesList

class RoleCenter:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("Role Center")
        self.tabControl = ttk.Notebook(root)
        self.customer_frame = ttk.Frame(self.tabControl)
        self.item_frame = ttk.Frame(self.tabControl)
        self.sales_frame = ttk.Frame(self.tabControl)
        self.tabControl.add(self.customer_frame, text='Customer List')
        self.tabControl.add(self.item_frame, text='Item List')
        self.tabControl.add(self.sales_frame, text='Sales List')
        self.tabControl.pack(expand=1, fill="both")
        self.customer_list = CustomerList(self.customer_frame, self.service)
        self.item_list = ItemList(self.item_frame, self.service)
        self.sales_list = SalesList(self.sales_frame, self.service)
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def open_customer_list(self):
        customer_list_window = tk.Toplevel(self.root)
        CustomerList(customer_list_window, self.service)

    def open_item_list(self):
        item_list_window = tk.Toplevel(self.root)
        ItemList(item_list_window, self.service)

    def open_sales_list(self):
        sales_list_window = tk.Toplevel(self.root)
        SalesList(sales_list_window, self.service)

import tkinter as tk
from tkinter import ttk
from Ui.CustomerList import CustomerList
from Ui.ItemList import ItemList
from Ui.SalesList import SalesList

class RoleCenter:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("Role Center")
        self.tabControl = ttk.Notebook(root)
        self.customer_frame = ttk.Frame(self.tabControl)
        self.item_frame = ttk.Frame(self.tabControl)
        self.sales_frame = ttk.Frame(self.tabControl)
        self.tabControl.add(self.customer_frame, text='Customer List')
        self.tabControl.add(self.item_frame, text='Item List')
        self.tabControl.add(self.sales_frame, text='Sales List')
        self.tabControl.pack(expand=1, fill="both")
        self.customer_list = CustomerList(self.customer_frame, self.service)
        self.item_list = ItemList(self.item_frame, self.service)
        self.sales_list = SalesList(self.sales_frame, self.service)
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def open_customer_list(self):
        customer_list_window = tk.Toplevel(self.root)
        CustomerList(customer_list_window, self.service)

    def open_item_list(self):
        item_list_window = tk.Toplevel(self.root)
        ItemList(item_list_window, self.service)

    def open_sales_list(self):
        sales_list_window = tk.Toplevel(self.root)
        SalesList(sales_list_window, self.service)

    def on_tab_changed(self, event):
        """Handle tab switching events."""
        selected_tab = self.tabControl.tab(self.tabControl.select(), "text")
        if selected_tab == "Item List":
            self.item_list.refresh_item_list()  # Refresh the inventory list when the Item List tab is selected
        elif selected_tab == "Customer List":
            self.customer_list.refresh_customer_list()  # If needed, refresh customer list
        elif selected_tab == "Sales List":
            self.sales_list.refresh_sales_list()  # If needed, refresh sales list
