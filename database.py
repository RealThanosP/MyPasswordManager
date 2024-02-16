import sqlite3
import encryption
import os
import hashlib

# NOTE: The name of the vault should not have spaces
def custom_hash(input_string):
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    return sha256.hexdigest()

def db_name(name:str):
    '''Returns the name version that can be a table name in the db'''
    name_elements = name.split(" ")
    shaped_name = "_".join(name_elements).lower()
    return shaped_name

def db_folder():
    '''Returns the app folder in the Documents'''
    #Get the user's User Folder
    user_folder = os.path.expanduser(f"~/Documents")
    app_folder = f"{user_folder}/Locker Pass"

    if not os.path.exists(app_folder):
        app_folder = os.makedirs(app_folder) 
    
    return app_folder

def db_path():
    '''Returns the db path for the connection'''
    DB_NAME = "Account_services.db"
    DB_FOLDER = db_folder()

    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    return DB_PATH

def show_name(name:str):
    '''Returns a string that reverses the the effect of db_name'''
    name_elements = name.split("_")
    shaped_name = " ".join(name_elements).capitalize()
    return shaped_name

def db_init():
    create_vault_pass()

def create_vault_table(vault_name:str):
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {db_name(vault_name)}(
                    username TEXT,
                    password TEXT,
                    service TEXT)''')

    conn.commit()
    return True

def create_vault_pass():
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS Passwords (
                name TEXT PRIMARY KEY,
                password TEXT,
                key TEXT
        )''')
    conn.commit()

def create_vault(vault_name:str, vault_pass:str):
    '''Creates the complete pair of new vault_table and security row in the Password_table'''
    create_vault_table(vault_name)
    save_vault_pass(vault_name, vault_pass)

def save_vault_pass(vault_name:str, vault_pass:str):
    '''Creates a row in the passwords table with the hashed password and the key tied up to the name of the vault'''
    key = encryption.generate_key()
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        cur.execute(f'''INSERT INTO Passwords (name, password, key) VALUES (?,?,?)''', (db_name(vault_name), custom_hash(vault_pass), key))
        
        conn.commit()
        return True
    
def get_all_vaults():
    '''Returns a list with all the vaults saved in the database'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        query = '''SELECT name FROM sqlite_master WHERE type='table';'''
        cur.execute(query)

        vaults = cur.fetchall()
        vaults = [show_name(x[0]) for x in vaults if (x[0] != "Passwords") and (x[0] != "sqlite_sequence")]

        return vaults

def get_vault_key(vault_name:str, vault_pass:str) -> bytes | None:
    '''Returns the key used to encrypt a vault. Returns NONE when there is no such vault'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        query = f'''SELECT key FROM Passwords WHERE name=? AND password=?'''
        cur.execute(query, (db_name(vault_name), custom_hash(vault_pass)))

        key = cur.fetchone()

    # Check for the key found
    if not key:
        return None
    key = key[0]

    return key

def is_correct_vault_pass(vault_name:str, vault_pass:str) -> True | False:
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        cur.execute('''SELECT password FROM Passwords WHERE name=?''', (db_name(vault_name),))
        hashed_pass = cur.fetchone()

        if not hashed_pass:
            # The vault doesn't exists
            return False
        
        if custom_hash(vault_pass) == hashed_pass[0]:
            return True

def is_duplicate_account(vault_name:str, vault_pass:str, account_list:list):
    '''Checks for duplicate account in db'''
    accounts_in_vault = get_username_service(vault_name, vault_pass)
    check_list = [account_list[0], account_list[2]]
    if check_list in accounts_in_vault:
        return True
    return False

def save_account(vault_name:str, vault_pass:str, account_list:list):
    '''Saves an encrypted list in the corresponding vault, with the key taken from the passwords vault. Returns the encrypted list'''
    # Makes sure the password is correct to proceed 
    is_correct_pass = is_correct_vault_pass(vault_name, vault_pass)
    if not is_correct_pass:
        return "Password"
    
    # Makes sure that there is no duplicate account in the vault
    is_already_saved = is_duplicate_account(vault_name, vault_pass, account_list)
    if is_already_saved:
        return "Already saved"
    
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        key = get_vault_key(vault_name, vault_pass)
        encrypted_account_list = encryption.encrypt_list(key, account_list)
        cur.execute(f'''INSERT INTO {db_name(vault_name)} (username, password, service) VALUES (?,?,?)''', encrypted_account_list)

        conn.commit()
        return encrypted_account_list

def get_vault_accounts(vault_name:str, vault_pass:str):
    '''Gets the contents of the vault'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        key = get_vault_key(vault_name, vault_pass)
        cur.execute(f'''SELECT * FROM {db_name(vault_name)}''')

        contents = cur.fetchall()
        dec_content = encryption.decrypt_nested_list(key, contents)

        return dec_content

def get_username_service(vault_name:str, vault_pass:str):
    accounts_in_vault = get_vault_accounts(vault_name, vault_pass)

    for account in accounts_in_vault:
        account.pop(1)
    return accounts_in_vault

def drop_vault(vault_name:str):
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        # is_correct_pass = is_correct_vault_pass(vault_name, vault_pass)
        # if not is_correct_pass:
        #     return
        
        cur.execute(f'''DROP TABLE {db_name(vault_name)}''')
        cur.execute(f'''DELETE FROM Passwords WHERE name=?''', (db_name(vault_name), ))

        conn.commit()

def drop_all_vaults():
    vaults = get_all_vaults()
    for vault in vaults:
        drop_vault(vault)

def delete_account(vault_name:str, vault_pass:str, account_list:list):

    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        # Encrypting
        key = get_vault_key(vault_name, vault_pass)

        if not key: return "Key Error"

        cur.execute(f'''SELECT * FROM {db_name(vault_name)}''')
        accounts = cur.fetchall()
        
        cur.execute(f'''SELECT rowid FROM {db_name(vault_name)}''')
        rowid_list = cur.fetchall()

        dec_accounts = encryption.decrypt_nested_list(key, accounts)
        # If the account is not in the database does not start
        if not (account_list in dec_accounts):
            return "Account not in db"
        
        # Searches the table for the correct rowid of the account.
        for index, account in enumerate(accounts):
            if account == account_list:
                rowid = rowid_list[index][0]
                cur.execute(f'''DELETE FROM {db_name(vault_name)} WHERE rowid=?''', (rowid,)) # Deletes the account
                return "Deleted"
        else:
            return "Not deleted. Something went wrong"
        
if __name__ == '__main__':

    vault_name = "Test"
    vault_pass = "1234"
    print(get_vault_key("tEsT", "1234"))
    