import sqlite3

def verify_database():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    # Verify customers table
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    print("Customers Table:")
    for row in customers:
        print(row)

    # Verify inventory table
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    print("\nInventory Table:")
    for row in inventory:
        print(row)

    # Verify sales table
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    print("\nSales Table:")
    for row in sales:
        print(row)

    conn.close()

if __name__ == "__main__":
    verify_database()
