import sqlite3

def create_connection():
    conn = sqlite3.connect("sales.db")
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      email TEXT NOT NULL,
                      address TEXT NOT NULL)''')

    # Create inventory table
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      nr INTEGER NOT NULL,
                      price REAL NOT NULL,
                      type TEXT NOT NULL)''')

    # Create sales table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                      id INTEGER PRIMARY KEY,
                      customer_id INTEGER NOT NULL,
                      item_id INTEGER NOT NULL,
                      salestype TEXT NOT NULL,
                      quantity INTEGER NOT NULL,
                      pricePerItem REAL NOT NULL,
                      FOREIGN KEY (customer_id) REFERENCES customers(id),
                      FOREIGN KEY (item_id) REFERENCES inventory(id))''')
    
    conn.commit()

if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)
    conn.close()
