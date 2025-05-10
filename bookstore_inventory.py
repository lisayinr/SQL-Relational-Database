from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

cnx = mysql.connector.connect(
    user = os.getenv("DB_USER"), 
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"))

cursor = cnx.cursor()

# Create and use bookstore_inventory database
cursor.execute("CREATE DATABASE IF NOT EXISTS bookstore_inventory")
cursor.execute("USE bookstore_inventory")

# Create category table
cursor.execute("CREATE TABLE IF NOT EXISTS category(category_id INT AUTO_INCREMENT, category_name VARCHAR(45) NOT NULL, PRIMARY KEY(category_id))")

# Create product table
cursor.execute("CREATE TABLE IF NOT EXISTS product(product_id INT AUTO_INCREMENT, name VARCHAR(60) NOT NULL, quantity INT NOT NULL, price DECIMAL(10, 2) NOT NULL, category_id INT, PRIMARY KEY(product_id), FOREIGN KEY (category_id) REFERENCES category(category_id))")

# Check if category table is empty and if so populate the table
cursor.execute("SELECT COUNT(*) FROM category")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO category(category_name) VALUES('Fantasy'),('Romance'),('Mystery'),('Children'),('Religious')")

# Check if product table is empty and if so populate the table
cursor.execute("SELECT COUNT(*) FROM product")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO product(name, quantity, price, category_id) VALUES ('Three Little Pigs', 5, 7.50, 4),('The Cat in the Hat', 11, 6.50, 4), ('The Giving Tree', 18, 13.50, 4),('The Very Hungry Caterpillar', 14, 10.99, 4), ('The Rainbow Fish', 6, 5.99, 4),('The Hobbit', 11, 14.99, 1), ('Harry Potter and the Prisoner of Azkaban',21, 16.75, 1), ('Percy Jackson: the Last Olympian', 16, 15.00, 1), ('Iron Flame', 8, 12.99, 1),('The Wind Weaver', 9, 8.50, 1), ('The Woman in White', 15, 13.00, 3),('The Disappearing Act', 8, 10.99, 3), ('Romeo and Juliet', 17, 18.50, 2),('Yours Truly', 11, 13.00, 2), ('The Fault in Our Stars', 19, 18.75, 2), ('Things We Never Got Over', 8, 9.50, 2), ('Just Like Magic', 15, 12.99, 2),('The Book of Mormon', 14, 7.00, 5),('Quran', 10, 7.50, 5), ('Loved to Life', 10, 11.00, 5)")

# Commit changes
cnx.commit()


# Insert function definition
def insert_product(cursor):
    name = input("Enter book name: ").strip().title()
    quantity = int(input("Enter quantity: "))
    price = round(float(input("Enter price: ")), 2)
    category_name = input("Enter category name: ").strip().lower()

    cursor.execute("SELECT category_id FROM category WHERE LOWER(category_name) = %s", (category_name,))
    result = cursor.fetchone()

    if result:
        category_id = result[0]
        query = "INSERT INTO product(name, quantity, price, category_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, quantity, price, category_id))
        print(f"Product {name} inserted successfully.")
    else:
        print(f"Category unrecognized. Please enter a valid response.")


# Delete function definition
def delete_product(cursor):
    name = input("Enter the name of the product you wish to delete: ").strip().lower()

    cursor.execute("SELECT product_id FROM product WHERE LOWER(name) = %s", (name,))
    result = cursor.fetchone()

    if result:
        confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").strip().lower()
        if confirm == "y":
            cursor.execute("DELETE FROM product WHERE name = %s", (name,))
            print(f"Product deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("No product found with that name.")


# Modify funtion definition
def modify_product(cursor):
    name = input("Enter the name of the product you would like to update: ").strip().lower()

    cursor.execute("SELECT product_id FROM product WHERE LOWER(name) = %s", (name,))
    result = cursor.fetchone()

    if result:
        product_id = result[0]
        action = input("What would you like to update? (name, price, quantity): ").strip().lower()
        if action == "name":
            new_name = input("Enter the new name: ").strip().title()
            cursor.execute("UPDATE product SET name = %s WHERE product_id = %s", (new_name, product_id))
            print(f"Product name updated to '{new_name}'")
        elif action == "price":
            new_price = round(float(input("Enter the new price: ")), 2)
            cursor.execute("UPDATE product SET price = %s WHERE product_id = %s", (new_price, product_id))
            print(f"Product price changed to ${new_price}")
        elif action == "quantity":
            new_quantity = int(input("What is the new quantity? "))
            cursor.execute("UPDATE product SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
            print(f"Quantity changed to {new_quantity}")
        else:
            print("Invalid option.")
    else:
        print("Product not found.")


# Search function definition
def search_products(cursor):
    while True:
        print("\n--- Search Products ---")
        name = input("Enter part of the book name (or leave blank): ").strip().lower()
        category = input("Enter category name (or leave blank): ").strip().lower()
        min_quantity = input("Enter minimum quantity (or leave blank): ")
        max_quantity = input("Enter maximum quantity (or leave blank): ")

        query = "SELECT p.name, p.quantity, p.price, c.category_name FROM product p JOIN category c ON p.category_id = c.category_id"

        conditions = []
        parameters = []

        if name:
            conditions.append("LOWER(p.name) LIKE %s")
            parameters.append(f"%{name}%")
        if category:
            conditions.append("LOWER(c.category_name) = %s")
            parameters.append(category)
        if min_quantity.isdigit():
            conditions.append("p.quantity >= %s")
            parameters.append(int(min_quantity))
        if max_quantity.isdigit():
            conditions.append("p.quantity <= %s")
            parameters.append(int(max_quantity))
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, tuple(parameters))
        results = cursor.fetchall()

        if results:
            print("\nSearch Results: ")
            for name, quantity, price, category_name in results:
                print(f"{name} | Qty: {quantity} | Price: ${price} | Category: {category_name}")
        else:
            print("No matching results found.")
        
        again = input("Search again? (y/n): ").strip().lower()
        if again != "y":
            break


# View Products function definition
def view_products(cursor):
    cursor.execute("SELECT p.name, p.quantity, p.price, c.category_name FROM product p JOIN category c ON p.category_id = c.category_id")
    print("\n--- All Products ---")
    for name, quantity, price, category in cursor:
        print(f"{name} | Qty: {quantity} | Price: ${price} | Category: {category}")


# Summarize Inventory function definition
def summarize_inventory(cursor):
    cursor.execute("SELECT COUNT(*), SUM(quantity * price) FROM product")
    count, total_value = cursor.fetchone()
    print("\n--- Inventory Summary ---")
    print(f"Total Products: {count}")
    print(f"Total Inventory Value: ${total_value:,.2f}")



# Main Menu
while True:
    print("\n=== Bookstore Inventory Menu ===")
    print("1. View Products")
    print("2. Search Products")
    print("3. Insert Product")
    print("4. Delete Product")
    print("5. Modify Product")
    print("6. View Inventory Summary")
    print("7. Exit")

    answer = input("Choose an option (1-7): ")

    if answer == "1":
        view_products(cursor)
    elif answer == "2":
        search_products(cursor)
    elif answer == "3":
        insert_product(cursor)
        cnx.commit()
    elif answer == "4":
        delete_product(cursor)
        cnx.commit()
    elif answer == "5":
        modify_product(cursor)
        cnx.commit()
    elif answer == "6":
        summarize_inventory(cursor)
    elif answer == "7":
        print("Thank you, and see you next time!")
        break
    else:
        print("Invalid answer. Please try again.")



cursor.close()
cnx.close()