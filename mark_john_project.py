import datetime
import os
import pandas
import dbcreation
import sqlite3
import matplotlib.pyplot as plt


os.chdir(os.path.dirname(os.path.abspath(__file__)))
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)
pandas.set_option('display.max_colwidth', None)

class Product:
    def __init__(self, product_id, name, category, quantity, price, expiration_date, supplier):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.expiration_date = expiration_date
        self.supplier = supplier
        
    def add_stock(self, change_field, new_quantity, change_input):
        if str(change_input) in inv_df['name'].values:
            cursor.execute(f'UPDATE inventory SET {change_field} = "{new_quantity}" WHERE name = "{change_input}"')
        elif int(change_input) in inv_df['product_id'].value:
            cursor.execute(f'UPDATE inventory SET {change_field} = "{new_quantity}" WHERE product_id = "{change_input}"')
        conn.commit()
        print("New stock added successfully!")
    
    def remove_stock(self, change_field, new_quantity, change_input):
        if str(change_input) in inv_df['name'].values:
            cursor.execute(f'UPDATE inventory SET {change_field} = "{new_quantity}" WHERE name = "{change_input}"')
        elif int(change_input) in inv_df['product_id'].values:
            cursor.execute(f'UPDATE inventory SET {change_field} = "{new_quantity}" WHERE product_id = "{change_input}"')
        conn.commit()
        print("Specified stock removed successfully!")
    
    def update_price(self, change_field, update_price, change_input):
        if str(change_input) in inv_df['name'].values:
            cursor.execute(f'UPDATE inventory SET {change_field} = "{update_price}" WHERE name = "{change_input}"')
        elif str(change_input) in inv_df['product_id'].values:
            cursor.execute(f'UPDATE inventory SET {change_field} = "{update_price}" WHERE name = "{change_input}"')
        conn.commit()
        print("Price updated successfully!")
        
    def check_expiration(self, today, expiration_input):
        arg = 1
        match int(expiration_input):
            case 1:
                arg = 2
            case 2:
                arg = 14
            case 3:
                arg = 31
            case 4:
                arg = 62
            case 5:
                arg = 186
            case 6:
                arg = 365
            case _:
                arg = 7
        print("The following items are set to expire within the specified window: \n")
        for index, row in inv_df.iterrows():
            if datetime.datetime.strptime(row['expiration_date'], "%Y/%m/%d") < today + datetime.timedelta(days=arg):
                print(f"> {row['name']} at {datetime.datetime.strptime(row['expiration_date'], '%Y/%m/%d')}")
            else:
                pass
                        
class Filter:
    def __init__(self, price_above, price_below, categories_included, suppliers_included, products_included, filter_applied):
        self.price_above = price_above
        self.price_below = price_below
        self.categories_included = categories_included
        self.suppliers_included = suppliers_included
        self.products_included = products_included
        self.filter_applied = filter_applied
        
    def edit_filter(self, change_filter_input):
        match int(change_filter_input):
            case 1:
                new_min = float(input("\nWhat would you like the new minimum price to be (leave off the dollar sign, e.g. 19.99): "))
                newFilter.price_above = new_min
                print(f'Minimum included price successfully set to {new_min}!')
            case 2:
                new_max = float(input("\nWhat would you like the new maximum price to be (leave off the dollar sign, e.g. 19.99): "))
                newFilter.price_below = new_max
                print(f'Maximum included price successfully set to {new_max}!')
            case 3:
                new_categories_pre = input("\nWhat categories would you like to include (items separated by commas without spaces, e.g. dairy,toys,medicine): ").split(",")
                new_categories = []
                for item in new_categories_pre:
                    if item in cat_df.values:
                        new_categories.append(item)
                    else:
                        print(f'category {item} not found...')
                if len(new_categories) > 0:
                    newFilter.categories_included = new_categories
                    print(f'New categories {new_categories} successfully required!')
                else:
                    print("No valid categories detected, filter unchanged...")
            case 4:
                new_suppliers_pre = input("\nWhat suppliers would you like to include (items separated by commas without spaces, e.g. supplier1,supplier2,supplier3): ").split(",")
                new_suppliers = []
                for item in new_suppliers_pre:
                    if item in supp_df.values:
                        new_suppliers.append(item)
                    else:
                        print(f'Supplier {item} not found...')
                if len(new_suppliers) > 0:
                    newFilter.suppliers_included = new_suppliers
                    print(f'New suppliers {new_suppliers} successfully required!')
                else:
                    print("No valid suppliers detected, filter unchanged...")
            case 5:
                new_products_pre = input("\nWhat products would you like to include (items separated by commas without spaces, e.g. cheese,nutcracker,ibuprofen): ").split(",")
                new_products = []
                for item in new_products_pre:
                    if item in inv_df.values:
                        new_products.append(item)
                    else:
                        print(f'Product {item} not found...')
                if len(new_products) > 0:
                    newFilter.products_included = new_products
                    print(f'New products {new_products} successfully included!')
                else:
                    print("No valid products detected, filter unchanged...")
            case 6:
                prompt_user()
        
    def apply_filter(self):
        self.filter_applied = 'True'
        
    def remove_filter(self):
        self.filter_applied = 'False'

class Transaction:
    """Transaction Class"""

    def __init__(self, transaction_id, total_cost, items_purchased, transaction_date, payment_method):
        self.transaction_id = transaction_id
        self.total_cost = total_cost
        self.items_purchased = items_purchased
        self.transaction_date = transaction_date
        self.payment_method = payment_method
        
    def add_transaction(self):
        cursor.execute("INSERT INTO transactions (transaction_id, total_cost, items_purchased, transaction_date, payment_method) VALUES (?, ?, ?, ?, ?)", (self.transaction_id, self.total_cost, self.items_purchased, self.transaction_date, self.payment_method))
        conn.commit()
        print(f'New transaction {self.transaction_id} added successfully!')
        
    def edit_transaction(self, transaction_change_input):
        try:
            cursor.execute(f'SELECT * FROM transactions WHERE transaction_id = "{transaction_change_input}"')
            print("Current changeable parts of this product: \n")
            for column in tran_df.columns.tolist():
                print(column)
            transaction_change_field = input("\nWhat would you like to change about this transaction?: ")
            if transaction_change_field in tran_df.columns.tolist():
                transaction_new_field = input(f"What should the new value of {transaction_change_field} be?: ")
                cursor.execute(f'UPDATE transactions SET {transaction_change_field} = "{transaction_new_field}" WHERE transaction_id = {transaction_change_input}')
                conn.commit()
                print(f"Transaction with ID {transaction_change_input} successfully updated!")
        except sqlite3.OperationalError:
            print("That transaction ID seems invalid...")
            prompt_user()

class Inventory:
    """Inventory Class"""

    def __init__(self, inventory_list):
        self.inventory_list = inventory_list
        
    def add_product(self, newProduct):
        cursor.execute("INSERT INTO inventory (product_id, name, category, quantity, price, expiration_date, supplier) VALUES (?, ?, ?, ?, ?, ?, ?)", (newProduct.product_id, newProduct.name, newProduct.category, newProduct.quantity, newProduct.price, newProduct.expiration_date, newProduct.supplier))
        conn.commit()
        print(f'New product {newProduct.name} added successfully!')
        
    def remove_product(self, removal_input):
        try:
            cursor.execute(f'SELECT * FROM inventory WHERE name = "{removal_input}"')
            if cursor.fetchall() == []:
                cursor.execute(f'SELECT * FROM inventory WHERE product_id = {removal_input}')
                if cursor.fetchall() == []:
                    print("Item with name or ID {removal_input} not found, database unaffected...")
                else:
                    cursor.execute(f'DELETE FROM inventory WHERE product_id = {removal_input}')
                    conn.commit()
                    print(f'Product with ID {removal_input} removed successfully.')
            else:
                cursor.execute(f'DELETE FROM suppliers WHERE name = "{removal_input}"')
                conn.commit()
                print(f'Product with name {removal_input} removed successfully.')
        except sqlite3.OperationalError:
            print("That product doesn't seem to exist...")
        
    def search_product(self, search_term):
        if str(search_term) in inv_df.values or int(search_term) in inv_df.values:
            for index, row in inv_df.iterrows():
                if str(search_term) in row.values or str(search_term) in row.values:
                    print("\nRelevant product ID: ", row['product_id'])
                    print("Relevant product name: ", row['name'])
                    print("Relevant product category: ", row['category'])
                    print("Relevant product expiration: ", row['expiration_date'])
                    print("Relevant product supplier: ", row['supplier'])
                    print("\n========================================")
        
    def update_inventory(self, change_input):
        try:
            cursor.execute(f'SELECT * FROM inventory WHERE name = "{change_input}"')
            if cursor.fetchall() == []:
                cursor.execute(f'SELECT * FROM inventory WHERE product_id = {change_input}')
                if cursor.fetchall() == []:
                    print("Product with name or ID {change_input} not found, database unaffected...")
                else:
                    print("Current changeable parts of this product: \n")
                    newProduct = Product('','','','','','','')
                    for column in inv_df.columns.tolist():
                        print(column)
                    change_field = input("\nWhat would you like to change about this product?: ")
                    if change_field in inv_df.columns.tolist():
                        if str(change_field) != "quantity" and str(change_field) != "price":
                            print(str(change_field))
                            new_field = input("What would you like the new value to be?: ")
                            cursor.execute(f'UPDATE inventory SET {change_field} = "{new_field}" WHERE product_id = "{change_input}"')
                        elif str(change_field) == "quantity":
                            for index, row in inv_df.iterrows():
                                if row['product_id'] == int(change_input):
                                    item_quantity = row['quantity']
                            update_quantity = input(f'This item currently has {item_quantity} in stock, how many are being added/removed (use a negative symbol in front if removing product): ')
                            new_quantity = int(update_quantity) + int(item_quantity)
                            print(change_input)
                            if int(update_quantity) > 0:
                                newProduct.add_stock(change_field, new_quantity, change_input)
                            elif int(update_quantity) < 0:
                                newProduct.remove_stock(change_field, new_quantity, change_input)
                        elif str(change_field) == "price":
                            for index, row in inv_df.iterrows():
                                if row['product_id'] == change_input:
                                    item_price = row['price']
                            update_price = float(input(f'This item is currently priced at ${item_price}, what would you like the new price to be (leave off the dollar sign, e.g. 19.99)?: '))
                            newProduct.update_price(change_field, update_price, change_input)
                        print(f'Product with ID {change_input} successfully updated!\n')
                    else:
                        print("Please select one of the changeable parts listed above...")
            else:
                print("Current changeable parts of this product: \n")
                newProduct = Product('','','','','','','')
                for column in inv_df.columns.tolist():
                    print(column)
                change_field = input("\nWhat would you like to change about this product?: ")
                if change_field in inv_df.columns.tolist():
                    if str(change_field) != "quantity" and str(change_field) != "price":
                        print(str(change_field))
                        new_field = input("What would you like the new value to be?: ")
                        cursor.execute(f'UPDATE inventory SET {change_field} = "{new_field}" WHERE name = "{change_input}"')
                    elif str(change_field) == "quantity":
                        for index, row in inv_df.iterrows():
                            if row['name'] == change_input:
                                item_quantity = row['quantity']
                        update_quantity = input(f'This item currently has {item_quantity} in stock, how many are being added/removed (use a negative symbol in front if removing product): ')
                        new_quantity = int(update_quantity) + int(item_quantity)
                        print(change_input)
                        if int(update_quantity) > 0:
                            newProduct.add_stock(change_field, new_quantity, change_input)
                        elif int(update_quantity) < 0:
                            newProduct.remove_stock(change_field, new_quantity, change_input)
                    elif str(change_field) == "price":
                        for index, row in inv_df.iterrows():
                            if row['name'] == change_input:
                                item_price = row['price']
                        update_price = float(input(f'This item is currently priced at ${item_price}, what would you like the new price to be (leave off the dollar sign, e.g. 19.99)?: '))
                        newProduct.update_price(change_field, update_price, change_input)
                    print(f'Product with name {change_input} successfully updated!\n')
                else:
                    print("Please select one of the changeable parts listed above...")
        except sqlite3.OperationalError:
            print("That product doesn't seem to exist...")
        
    def generate_report(self):
        print("\n")
        stock_count = 0
        if newFilter.filter_applied == 'True' and len(newFilter.products_included) > 0:
            for index,row in inv_df.iterrows():
                if row["name"] in newFilter.products_included:
                    stock_count += int(row["quantity"])
                    print(f'The current stock of {row["name"]} is {row["quantity"]}')
            print(f'The current total stock of all products in the filter is: {stock_count}')
        else:
            for index,row in inv_df.iterrows():
                stock_count += int(row["quantity"])
                print(f'The current stock of {row["name"]} is {row["quantity"]}')
            print(f'The current total stock of all products in inventory is: {stock_count}')
            print("Showing a pop-out window graph of products in inventory...")
            
        figure,ax = plt.subplots()
        if newFilter.filter_applied == 'True' and len(newFilter.products_included) > 0:
            figure_items = newFilter.products_included
            figure_values = []
            for index,row in inv_df.iterrows():
                if row["name"] in newFilter.products_included:
                    figure_values.append(row["quantity"])
        else:
            figure_items = [row["name"] for index,row in inv_df.iterrows()]
            figure_values = [row["quantity"] for index,row in inv_df.iterrows()]
            
        ax.bar(figure_items, figure_values)
        ax.set_ylabel('Products in inventory')
        ax.set_xlabel('Count')
        plt.show()
        
class Supplier:
    def __init__(self, supplier_id, name, contact_info):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info
        
    def add_supplier(self, newSupplier):
        cursor.execute("INSERT INTO suppliers (supplier_id, name, contact_info) VALUES (?, ?, ?)", (newSupplier.supplier_id, newSupplier.name, newSupplier.contact_info))
        conn.commit()
        print(f'New supplier {newSupplier.name} added successfully!\n')
        
    def remove_supplier(self, removal_input):
        try:
            cursor.execute(f'SELECT * FROM suppliers WHERE name = "{removal_input}"')
            if cursor.fetchall() == []:
                cursor.execute(f'SELECT * FROM suppliers WHERE supplier_id = {removal_input}')
                if cursor.fetchall() == []:
                    print("Item with name or ID {removal_input} not found, database unaffected...")
                else:
                    cursor.execute(f'DELETE FROM suppliers WHERE supplier_id = {removal_input}')
                    conn.commit()
                    print(f'Supplier with ID {removal_input} removed successfully.')
            else:
                cursor.execute(f'DELETE FROM suppliers WHERE name = "{removal_input}"')
                conn.commit()
                print(f'Supplier with name {removal_input} removed successfully.')
        except sqlite3.OperationalError:
            print("That supplier doesn't seem to exist...")
    def update_supplier_info(self, change_input):
        try:
            cursor.execute(f'SELECT * FROM suppliers WHERE name = "{change_input}"')
            if cursor.fetchall() == []:
                cursor.execute(f'SELECT * FROM suppliers WHERE supplier_id = {change_input}')
                if cursor.fetchall() == []:
                    print("Supplier with name or ID {change_input} not found, database unaffected...")
                else:
                    print("Current changeable parts of this supplier: \n")
                    for column in supp_df.columns.tolist():
                        print(column)
                    change_field = input("\nWhat would you like to change about this supplier?: ")
                    if change_field in supp_df.columns.tolist():
                        new_field = input("What would you like the new value to be?: ")
                        cursor.execute(f'UPDATE suppliers SET {change_field} = "{new_field}" WHERE supplier_id = {change_input}')
                        conn.commit()
                        print("Supplier with ID {change_input} successfully changed!\n")
                    else:
                        print("Please select one of the changeable parts listed above...")
            else:
                print("Current changeable parts of this supplier: \n")
                for column in supp_df.columns.tolist():
                    print(column)
                change_field = input("\nWhat would you like to change about this supplier?: ")
                if change_field in supp_df.columns.tolist():
                    new_field = input("What would you like the new value to be?: ")
                    cursor.execute(f'UPDATE suppliers SET {change_field} = "{new_field}" WHERE name = {change_input}')
                    conn.commit()
                    print("Supplier with name {change_input} successfully changed!\n")
                else:
                    print("Please select one of the changeable parts listed above...")
        except sqlite3.OperationalError:
            print("That supplier doesn't seem to exist...")
            
class Category:
    def __init__(self, category_name, description):
        self.category_name = category_name
        self.description = description
        
    def add_category(self, newCategory):
        cursor.execute("INSERT INTO categories (category_name, description) VALUES (?, ?)", (newCategory.category_name, newCategory.description))
        conn.commit()
        print(f'New supplier {newCategory.category_name} added successfully!\n')
        
    def remove_category(self, removal_input):
        try:
            cursor.execute(f'SELECT * FROM categories WHERE category_name = "{removal_input}"')
            cursor.execute(f'DELETE FROM categories WHERE category_name = "{removal_input}"')
            conn.commit()
            print(f'Category with name {removal_input} removed successfully.')
        except sqlite3.OperationalError:
            print("That category doesn't seem to exist...")
        
    def list_products_by_category(self):
        print("list_products_by_category ran")
        
def prompt_user():
    first_menu_input = input("\nWhich of the following would you like to do (select using only the number): \n(1) Manage/view suppliers \n(2) Manage/view product information or stock \n(3) Manage/view product categories \n(4) Manage/view filter settings \n(6) Manage/view transactions \n(7) Export data to CSV file \n(8) Generate Report: ")
    try:
        match int(first_menu_input):
            case 1:
                second_menu_input = input("\nWhat would you like to do with your supplier(s)? (select using only the number): \n(1) View current suppliers \n(2) Add a new supplier \n(3) Remove existing supplier(s) \n(4) Alter an existing supplier \n(5) Go back: ")
                match int(second_menu_input):
                    case 1:
                        if newFilter.filter_applied == 'True':
                            print("The current list of suppliers (with the current filter applied) is: \n")
                            for index, row in supp_df.iterrows():
                                if row['name'] in newFilter.suppliers_included:
                                    print(row)
                                else:
                                    continue
                        else:
                            print("The current list of suppliers is:")
                            print("\n",supp_df)
                    case 2:
                        if len(supp_df) > 0:
                            supplier_id = (int(supp_df.iloc[-1].supplier_id) + 1)
                        else:
                            supplier_id = 1
                        name = input("What is the supplier name?: ")
                        contact_info = input("What is the supplier's contact info? Separate methods by commas without spaces e.g. exemail@gmail.com,931-999-9999: ")
                        newSupplier = Supplier(supplier_id, name, contact_info)
                        newSupplier.add_supplier(newSupplier)
                    case 3:
                        removal_input = input("What supplier would you like to remove? (specify using case-sensitive name or ID): ")
                        newSupplier = Supplier(removal_input, removal_input, 'None')
                        newSupplier.remove_supplier(removal_input)
                    case 4:
                        change_input = input("What supplier would you like to change? (specify using case-sensitive name or ID): ")
                        newSupplier = Supplier(change_input, change_input, 'None')
                        newSupplier.update_supplier_info(change_input)
                    case 5:
                        prompt_user()
            case 2:
                second_menu_input = input("\nWhat would you like to do with the item(s)? (select using only the number): \n(1) View current products/inventory \n(2) Add a new product \n(3) Remove existing products \n(4) Alter an existing product \n(5) Verify expiration dates \n(6) Search for a specific product \n(7) Go Back: ")
                match int(second_menu_input):
                    case 1:
                        if newFilter.filter_applied == 'True':
                            print("The current list of products and inventory (with the current filter applied) is: \n")
                            for index, row in inv_df.iterrows():
                                if row['name'] in newFilter.products_included:
                                    print(row)
                                else:
                                    continue
                        else:
                            print("The current list of products and inventory is:")
                            print("\n",inv_df)
                    case 2:
                        product_id = (len(inv_df) + 1)
                        name = input("What is the name of the new product?: ")
                        try:
                            print(f'Current product categories: \n\n{cat_df}\n')
                        except KeyError:
                            print("No categories detected! ")
                        category = input("What category is the item part of?: ")
                        if category in cat_df.values:
                            pass
                        else:
                            print(f'The category \"{category}\" does not exist...')
                            prompt_user()
                        quantity = input("How many of the item do we have to start with (0 if none)?: ")
                        if int(quantity) < 0:
                            print("Quantity must be a positive number...")
                            prompt_user()
                        price = input("What is the starting price of the item (leave off the dollar sign, e.g. 19.99)?: ")
                        if float(price) <= 0:
                            print("Price must be a positive number...")
                        expiration_date = input("When does the oldest stock of this item expire? (format YYYY/MM/DD): ")
                        print(f'\nCurrent suppliers: \n{supp_df}\n')
                        supplier = input("What supplier did the item come from?: ")
                        if supplier in supp_df.values:
                            pass
                        else:
                            print(f'The supplier \"{supplier}\" does not exist...')
                            prompt_user()
                        newProduct = Product(product_id, name, category, quantity, price, expiration_date, supplier)
                        newInventory.add_product(newProduct)
                    case 3:
                        removal_input = input("What product would you like to remove? (specify using case-sensitive name or ID): ")
                        newInventory.remove_product(removal_input)
                    case 4:
                        change_input = input("What product would you like to change? (specify using case-sensitive name or ID): ")
                        newInventory.update_inventory(change_input)
                    case 5:
                        today_pre = str(datetime.date.today())
                        today = datetime.datetime.today().strptime(today_pre, '%Y-%m-%d')
                        expiration_input = input("\nHow far away would you like to check if there are any expirations for? (select using only the number): (1) One week (2) Two weeks (3) One month (4) Two months (5) Six Months (6) One year: ")
                        newProduct = Product(0, 'None', 'None',  0, 0, 'None', 'None')
                        newProduct.check_expiration(today, expiration_input)
                    case 6:
                        search_term = str(input("Please input the name of the item to be searched for: "))
                        newInventory.search_product(search_term)
                    case 7:
                        prompt_user()
            case 3:
                second_menu_input = input("\nWhat would you like to do with the product categories? \n(1) View current categories \n(2) Add a new category \n(3) Remove an existing category \n(4) List products by category \n(5) Go back: ")
                match int(second_menu_input):
                    case 1:
                        if newFilter.filter_applied == 'True':
                            print("The current list of categories (with the current filter applied) is: \n")
                            for index, row in cat_df.iterrows():
                                if row['name'] in newFilter.categories_included:
                                    print(row)
                                else:
                                    continue
                        else:
                            print("The current list of categories is:")
                            print("\n",cat_df)
                    case 2:
                        name = input("What is the new category going to be called?: ")
                        description = input("Briefly describe the category: ")
                        newCategory = Category(name, description)
                        newCategory.add_category(newCategory)
                    case 3:
                        removal_input = input("What is the name of the category you wish to remove?: ")
                        newCategory = Category(removal_input, removal_input)
                        newCategory.remove_category(removal_input)
                    case 4:
                        print("The current list of product categories is: ")
                        print("\n", cat_df)
                        list_input = input("\nWhich category would you like to see the products within?:")
                        print(f'The products within the \"{list_input}\" category are: \n')
                        for index, row in inv_df.iterrows():
                            if row['category'] == str(list_input):
                                print("> ", row['name'])
                            else:
                                continue
                    case 5:
                        prompt_user()
            case 4:
                second_menu_input = input("\nWhat would you like to do with the filter? (select using only the number): \n(1) View current filter settings \n(2) Create/edit filter settings \n(3) Apply filter \n(4) Disable filter \n(5) Go back: ")
                match int(second_menu_input):
                    case 1:
                        if any(getattr(newFilter, attr, '') for attr in ['price_above', 'price_below', 'categories_included', 'suppliers_included', 'products_included', 'filter_applied']):
                            print(f'\nPrice range: ${newFilter.price_above} - ${newFilter.price_below}')
                            print(f'Categories included:')
                            for item in newFilter.categories_included:
                                print(f'- {item}')
                            print(f'Suppliers included:')
                            for item in newFilter.suppliers_included:
                                print(f'- {item}')
                            print(f'Products included:')
                            for item in newFilter.products_included:
                                print(f'- {item}')
                            if newFilter.filter_applied == 'True':
                                print("> Filter is applied <")
                            else:
                                print("\n> Filter is not applied <")
                        else:
                            print("There is currently no filter configured...")
                    case 2:
                        if not any(getattr(newFilter, attr, '') for attr in ['price_above', 'price_below', 'categories_included', 'suppliers_included', 'products_included', 'filter_applied']):
                            #newFilter = Filter('Not configured', 'Not configured', 'Not configured', 'Not configured', 'Not configured', 'False')
                            filter_confirmation = input("There is not currently a filter configured. Would you like to make one? (Y)es (N)o: ")
                            if str(filter_confirmation).upper() == "YES" or str(filter_confirmation).upper() == "Y":
                                price_input_confirm = input("Would you like to set a price floor and ceiling? (Y)es (N)o: ")
                                if str(price_input_confirm).upper() == "YES" or str(price_input_confirm).upper() == "Y":
                                    newFilter.price_above = float(input("What is the minimum price you would like to include? (leave off the dollar sign, e.g. 19.99): "))
                                    newFilter.price_below = float(input("What is the maximum price you would like to include? (leave off the dollar sign, e.g. 19.99): "))
                                else:
                                    newFilter.price_above = 'Not configured'
                                    newFilter.price_below = 'Not configured'
                                category_input_confirm = input("Would you like to set a predefined list of categories to include? (Y)es (N)o: ")
                                if str(category_input_confirm).upper() == "YES" or str(category_input_confirm).upper() == "Y":
                                    print(f'The current list of categories is: \n{cat_df}\n')
                                    categories_included_pre = input("Please input the list of categories you would like to include (items separated by commas without spaces, e.g. dairy,toys,medicine): ").split(",")
                                    new_categories = []
                                    for item in categories_included_pre:
                                        if item in cat_df.values:
                                            new_categories.append(item)
                                        else:
                                            print(f'Category {item} not found...')
                                    if len(new_categories) > 0:
                                        newFilter.categories_included = new_categories
                                        print(f'Categories {new_categories} successfully required!')
                                    else:
                                        print("No valid categories detected, filter unchanged...")
                                else:
                                    categories_included = 'Not configured'
                                supplier_input_confirm = input("Would you like to set a predefined list of suppliers to include? (Y)es (N)o: ")
                                if str(supplier_input_confirm).upper() == "YES" or str(supplier_input_confirm).upper() == "Y":
                                    print(f'The current list of suppliers is: \n{supp_df}\n')
                                    suppliers_included_pre = input("Please input the list of suppliers you would like to include (items separated by commas without spaces, e.g. supplier1,supplier2,supplier3): ").split(",")
                                    new_suppliers = []
                                    for item in suppliers_included_pre:
                                        if item in supp_df.values:
                                            new_suppliers.append(item)
                                        else:
                                            print(f'Supplier {item} not found...')
                                    if len(new_suppliers) > 0:
                                        newFilter.suppliers_included = new_suppliers
                                        print(f'Supplier(s) {new_suppliers} successfully required!')
                                    else:
                                        print("No valid suppliers detected, filter unchanged...")
                                else:
                                    suppliers_included = 'Not configured'
                                product_input_confirm = input("Would you like to set a predefined list of products to include? (Y)es (N)o: ")
                                if str(product_input_confirm).upper() == "YES" or str(product_input_confirm).upper() == "Y":
                                    print(f'The current list of products is: \n{inv_df}\n')
                                    products_included_pre = input("Please input the list of products you would like to include (items separated by commas without spaces, e.g. cheese,nutcracker,ibuprofen): ").split(",")
                                    new_products = []
                                    for item in products_included_pre:
                                        if item in inv_df.values:
                                            new_products.append(item)
                                        else:
                                            print(f'Product {item} not found...')
                                    if len(new_products) > 0:
                                        newFilter.products_included = new_products
                                        print(f'Product(s) {new_products} successfully required!')
                                    else:
                                        print("No valid products detected, filter unchanged...")
                                else:
                                    products_included = 'Not configured'
                                filter_applied_confirm = input("Would you like to apply this new filter after it is created? (Y)es (N)o: ")
                                if str(filter_applied_confirm).upper() == "YES" or str(filter_applied_confirm).upper() == "Y":
                                    newFilter.apply_filter()
                                else:
                                    newFilter.remove_filter()
                            else:
                                prompt_user()
                        else:
                            change_filter_input = input("\nWhat would you like to change about the filter (select using only the number)? (1) Minimum price to include (2) Maximum price to include (3) Categories to include (4) Suppliers to include (5) Products to include (6) Go back: ")
                            newFilter.edit_filter(change_filter_input)
                    case 3:
                        newFilter.apply_filter()
                        print("Filter is now applied!")
                    case 4:
                        newFilter.remove_filter()
                        print("Filter has been disabled")
            case 6:
                second_menu_input = input("\nWhat would you like to do with your transaction(s)? (select using only the number): \n(1) View past transactions \n(2) Add a new transaction \n(3) Edit a tranaction \n(4) Go back: ")
                match int(second_menu_input):
                    case 1:
                        print("The current record of transactions is: ")
                        print("\n", tran_df)
                    case 2:
                        transaction_id = len(tran_df) + 1
                        items_purchased = input("What items were purchased? Separate items using commas without spaces e.g. cheese,nutcracker,ibuprofen: ")
                        items_purchased_list = items_purchased.split(",")
                        price = 0.00
                        total_cost = 0.00
                        for item in items_purchased_list:
                            prior_quantity = 0
                            if item in inv_df.values:
                                item_quantity = int(input(f'How much {item} was purchased?: '))
                            else:
                                print("Please input a valid existing product name...")
                                prompt_user()
                            for index,row in inv_df.iterrows():
                                if row['name'] == item:
                                    if item_quantity > int(row['quantity']):
                                        print("Purchase is for more items than in stock! Halting transaction...")
                                        prompt_user()
                                    price = float(row['price'])
                                    prior_quantity = int(row['quantity'])
                                    new_quantity = prior_quantity - item_quantity
                                    cursor.execute(f"UPDATE inventory SET quantity = {new_quantity} WHERE name = '{row['name']}'")
                            total_cost += (price * item_quantity)
                        today = datetime.datetime.today().strptime(str(datetime.date.today()), '%Y-%m-%d')
                        transaction_date = str(today)
                        payment_method = input("What method did the customer use to purchase the item(s)?: ")
                        newTransaction = Transaction(transaction_id, total_cost, items_purchased, transaction_date, payment_method)
                        newTransaction.add_transaction()
                        conn.commit()
                        print("Quantity of item(s) purchased updated...")
                    case 3:
                        newTransaction = Transaction("","","","","")
                        print("The record of past transactions is: ")
                        print(tran_df)
                        transaction_change_input = input("\nWhat transaction would you like to change? (specify using only transaction ID): ")
                        newTransaction.edit_transaction(transaction_change_input)
                    case 4:
                        prompt_user()
            case 7:
                db_export()
            case 8:
                newInventory.generate_report()
            case _:
                print("Please select an option from the menu using just the option's number...")
    except ValueError:
        print("Invalid input...")
    except UnboundLocalError:
        print("Unidentified error, transaction halted...")

def db_create():
    if os.path.isfile("csi_260_Mark_John.db"):
        pass
    else:
        dbcreation.main()
    
def db_export():
    print("\nThe current list of database tables that can be exported is: \nsuppliers \ninventory \ncategories \ntransactions")
    export_input = input("Which database table(s) would you like to export? Separate items using commas without spaces, e.g. suppliers,inventory,categories,transactions: ").split(",")
    for item in export_input:
        match item.lower():
            case 'suppliers':
                supp_df.to_csv('suppliers.csv', index=False)
            case 'inventory':
                inv_df.to_csv('inventory.csv', index=False)
            case 'categories':
                cat_df.to_csv('categories.csv', index=False)
            case 'transactions':
                tran_df.to_csv('transactions.csv', index=False)
            case _:
                print("Invalid database table name(s) detected...")
                
        print(f"Database table {item} exported as a CSV file!")
        
newFilter = Filter('', '', '', '', '', '')
if __name__ == '__main__':
    os.system("@ECHO OFF > python3 -m pip install pandas")
    db_create()
    conn = sqlite3.connect('csi_260_Mark_John.db')
    cursor = conn.cursor()
    
    while True:
        supp_df = pandas.read_sql_query("SELECT * FROM suppliers", conn)
        inv_df = pandas.read_sql_query("SELECT * FROM inventory", conn)
        cat_df = pandas.read_sql_query("SELECT * FROM categories", conn)
        tran_df = pandas.read_sql_query("SELECT * FROM transactions", conn)
        newInventory = Inventory(inv_df)
        prompt_user()
