import mysql.connector
from mysql.connector import Error
from datetime import datetime

class ShopBillPro:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root", 
                password="aliva", # your password
                database="joy_guru_bhandar"
            )
            self.cursor = self.connection.cursor()
            print("Connected to Database: joy_guru_bhandar")
        except Error as e:
            print("DB Error:", e)
            exit()

    def add_product(self):
        pname = input("Enter Product Name: ")
        try:
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock Qty: "))
        except ValueError:
            print("Price and Stock must be numbers")
            return
        category = input("Enter Category: ")
        
        sql = "INSERT INTO products (pname, price, stock, category) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (pname, price, stock, category))
        self.connection.commit()
        print("Product added successfully!")

    def show_products(self):
        self.cursor.execute("SELECT pid, pname, price, stock, category FROM products")
        results = self.cursor.fetchall()
        if not results:
            print("No products found")
            return
        print("\nPID | Product Name | Price | Stock | Category")
        print("-"*65)
        for row in results:
            print(f"{row[0]} | {row[1]} | Rs.{row[2]} | {row[3]} | {row[4]}")

    def search_product(self):
        term = input("Enter product name to search: ")
        sql = "SELECT pid, pname, price, stock, category FROM products WHERE pname LIKE %s"
        self.cursor.execute(sql, ('%'+term+'%',))
        results = self.cursor.fetchall()
        for row in results:
            print(row)
        if not results: print("Product not found")

    def low_stock_alert(self):
        self.cursor.execute("SELECT pid, pname, stock FROM products WHERE stock < 10")
        results = self.cursor.fetchall()
        print("\nLOW STOCK ALERT:")
        for row in results:
            print(f"{row[1]} - Only {row[2]} left")
        if not results: print("All stocks are good")

    def make_bill(self):
     from decimal import Decimal # ADD THIS
    
     customer = input("Enter Customer Name: ")
     if customer == "": customer = "Walk-in Customer"
    
     cart = []
     total_amount = Decimal('0') # Changed to Decimal
     GST_RATE = Decimal('0.18') # 18% GST as Decimal
    
     while True:
        self.show_products()
        pid = input("Enter Product PID to add to bill, or 'done': ")
        if pid.lower() == 'done': break
        
        try: qty = int(input("Enter Quantity: "))
        except: print("Invalid quantity"); continue

        self.cursor.execute("SELECT pname, price, stock FROM products WHERE pid = %s", (pid,))
        prod = self.cursor.fetchone()
        
        if prod and prod[2] >= qty:
            rate = prod[1] # This is Decimal
            amount = rate * qty
            gst = amount * GST_RATE # Now Decimal * Decimal = OK
            cart.append((pid, prod[0], qty, rate, amount, gst))
            total_amount += amount + gst
            
            # Update stock
            new_stock = prod[2] - qty
            self.cursor.execute("UPDATE products SET stock = %s WHERE pid = %s", (new_stock, pid))
        else:
            print("Invalid PID or Not enough stock")
    
     if not cart:
        print("Bill cancelled - no items added")
        return

     # 1. Insert into bills table
     sql_bill = "INSERT INTO bills (customer_name, total_amount, gst_amount) VALUES (%s, %s, %s)"
     gst_total = sum(item[5] for item in cart)
     self.cursor.execute(sql_bill, (customer, float(total_amount), float(gst_total))) # Convert to float for MySQL
     bill_id = self.cursor.lastrowid

     # 2. Insert into bill_items table
     sql_item = """INSERT INTO bill_items 
     (bill_id, pid, quantity, rate, amount, gst_amt, cgst, sgst) 
     VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
     for item in cart:
        pid, pname, qty, rate, amount, gst = item
        cgst = sgst = gst/Decimal('2') # Split GST
        self.cursor.execute(sql_item, (bill_id, pid, qty, float(rate), float(amount), float(gst), float(cgst), float(sgst)))
    
     self.connection.commit()
     print(f"\n--- BILL ID: {bill_id} for {customer} ---")
     print(f"Grand Total with GST: Rs.{total_amount:.2f}")
     print("Bill saved successfully!")

    def daily_sales_report(self):
        today = datetime.now().strftime('%Y-%m-%d')
        sql = "SELECT SUM(total_amount) FROM bills WHERE DATE(bill_date) = %s"
        self.cursor.execute(sql, (today,))
        total = self.cursor.fetchone()[0]
        print(f"Today's Sales: Rs.{total if total else 0:.2f}")

    def close(self):
        if hasattr(self, 'cursor'): self.cursor.close()
        if hasattr(self, 'connection'): self.connection.close()
        print("Connection closed")

def main_menu():
    app = ShopBillPro()
    while True:
        print("\n--- SHOPBILL PRO - JOY GURU BHANDAR ---")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Low Stock Alert")
        print("5. Make New Bill")
        print("6. Daily Sales Report")
        print("7. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1': app.add_product()
        elif choice == '2': app.show_products()
        elif choice == '3': app.search_product()
        elif choice == '4': app.low_stock_alert()
        elif choice == '5': app.make_bill()
        elif choice == '6': app.daily_sales_report()
        elif choice == '7': app.close(); break
        else: print("Invalid choice")

if __name__ == "__main__":
    main_menu()
