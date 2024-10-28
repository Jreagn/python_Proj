import sqlite3
import os
""" Creates Final Project Database Layout """

# Set Current Working Directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def create_database(db_name):
    """ Create Database if it does not exist """
    print(f'Creating {db_name} Database.')
    with open(db_name, 'w') as fp:
        print('Database has been created.')


def create_table(db_name):
    """ Create insurance table without any data """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        query = '''CREATE TABLE IF NOT EXISTS inventory
                        (product_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price FLOAT NOT NULL,
                        expiration_date TEXT NOT NULL,
                        supplier TEXT DEFAULT 0);'''
        
        query2 = '''CREATE TABLE IF NOT EXISTS suppliers
                        (supplier_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        contact_info TEXT NOT NULL);'''
        
        query3 = '''CREATE TABLE IF NOT EXISTS categories
                        (category_name TEXT PRIMARY KEY,
                        description TEXT NOT NULL);'''
        
        query4 = '''CREATE TABLE IF NOT EXISTS transactions
                        (transaction_id INTEGER PRIMARY KEY,
                        total_cost FLOAT NOT NULL,
                        items_purchased TEXT NOT NULL,
                        transaction_date TEXT NOT NULL,
                        payment_method TEXT NOT NULL);'''

                
        cursor.execute(query)
        cursor.execute(query2)
        cursor.execute(query3)
        cursor.execute(query4)
        print('The tables have been created')

    except sqlite3.Error as error:
        print(f'Error ocured - {error}')

    finally:
        if conn:
            conn.close()
            print('Table has been created')
            print('SQLite Connection closed')
    

def main():
    """ Create or refresh database """
    
    dbname = 'csi_260_Mark_John.db'
    
    exist_chk = os.path.exists(os.path.join(os.getcwd(), dbname))

    if exist_chk:
        print('Warning this will wipe out any existing data.')
        imp = input('Do you want to overwrite database? (y/n)')
        if imp.lower() == 'y':
            create_table(dbname)
        else:
            print('Exited program without Database being touched')

    else:
        create_database(dbname)
        create_table(dbname)


if __name__ == '__main__':
    main()
