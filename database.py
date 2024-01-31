import encryption
import sqlite3
import os

def db_path():
    '''Returns the db path for the connection'''
    DB_NAME = "Account_services.db"
    DB_FOLDER = encryption.db_folder()

    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    return DB_PATH

def create_vault(vault_name):
    '''Initialize the vault table'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        cur.execute(f'''CREATE TABLE IF NOT EXISTS {vault_name}(
                    username TEXT,
                    password TEXT,
                    service TEXT,
                    key TEXT
        )''')
        conn.commit()

def store_account(key:bytes, vault_name:str, account:list):
    '''Stores an account details with the key '''
    encrypted_list = encryption.encrypt_list(key, account)
    create_vault(vault_name)
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        cur.execute(f'''INSERT INTO {vault_name} VALUES (?,?,?,?)''', tuple(encrypted_list))

        conn.commit()   

def get_vault(vault_name:str):
    '''Returns a nested list with all the vaults accounts'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        cur.execute(f'''SELECT * FROM {vault_name}''')

        
        accounts = cur.fetchall()
        acc = encryption.decrypt_nested_list(accounts)
             
        conn.commit()

    return acc
                             
def drop_table(table_name):
    '''Delete the table you insert'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        cur.execute(f'''DROP TABLE {table_name}''')

def drop_all_tables():
    '''Deletes all the tables in the database'''
    database_file = db_path()

    # Connect to the SQLite database
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()

        # Get the list of tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Drop each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

        # Commit the changes
        conn.commit()

if __name__ == '__main__':
    key = encryption.generate_key("Vault")



