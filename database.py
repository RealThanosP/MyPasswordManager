import encryption
import sqlite3
import os

# NOTE: The name of the vault should not have spaces
def db_name(name:str):
    '''Returns the name version that can be a table name in the db'''
    name_elements = name.split(" ")
    shaped_name = "_".join(name_elements)
    return shaped_name

def db_path():
    '''Returns the db path for the connection'''
    DB_NAME = "Account_services.db"
    DB_FOLDER = encryption.db_folder()

    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    return DB_PATH

def get_all_vaults():
    '''Returns a nested list with all the vaults in the database'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table'")

        vaults = cur.fetchall()
        
        for index, vault in enumerate(vaults):
            vaults[index] = vault[0].replace("_", " ")

    return vaults

def create_vault(vault_name:str):
    '''Initialize the vault table'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        cur.execute(f'''CREATE TABLE IF NOT EXISTS {db_name(vault_name)}(
                    username TEXT,
                    password TEXT,
                    service TEXT,
                    notes TEXT,
                    key TEXT
        )''')
        conn.commit()

def check_for_dublicate_account(vault_name:str, username:str, service:str):
    '''Returns True when there is another account in the db and False when there is not another acc'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        cur.execute(f'SELECT * FROM {db_name(vault_name)}')

        acc = cur.fetchall()
        accounts = encryption.decrypt_nested_list(acc)
        name_service_db = []

        for acc in accounts:
            acc.pop(1)
            acc.pop(-1)
            name_service_db.append(acc)
        
        if [username, service] in name_service_db:
            return True
        
        return False

def store_account(key:bytes, vault_name:str, decrypted_account:list):
    '''Stores the encrypted account details with the key. Returns None when the account is not saved and True when it is.'''
    is_account_in_db = check_for_dublicate_account(vault_name, decrypted_account[0], decrypted_account[2])
    encrypted_list = encryption.encrypt_list(key, decrypted_account)

    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        # Checks for dublicate accounts in the db
        if is_account_in_db: 
            return None

        cur.execute(f'''INSERT INTO {db_name(vault_name)} VALUES (?,?,?,?,?)''', tuple(encrypted_list))
        conn.commit()

        return True

def get_vault(vault_name:str):
    '''Returns a nested list with all the vaults accounts'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        cur.execute(f'''SELECT * FROM {db_name(vault_name)}''')

        accounts = cur.fetchall()
        acc = encryption.decrypt_nested_list(accounts)
             
        conn.commit()

    return acc

def get_username_and_service_values(vault_name:str):
    vault = get_vault(vault_name)
    wanted = []
    for row in vault:
        row.pop(1)
        row.pop(2)
        wanted.append(row)
    
    return wanted

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

# Just for testing
if __name__ == '__main__':
    vault_name = "Start Vault"
    account = ["123", "123asdasd", "1232", "123asdasd"]

    key = encryption.generate_key()

    create_vault(vault_name)
    store_account(key, vault_name, account)
    print(get_vault(vault_name))




