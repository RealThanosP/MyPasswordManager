import sqlite3, os, hashlib, pathlib
from typing import List, Optional

from encryption import encrypt, decrypt_account_list, decrypt_nested_account_list, encrypt_account_dict

# Exceptions
class VaultAlreadyExistsException(Exception):
    pass

class InvalidPasswordException(Exception):
    pass

class InvalidVaultException(Exception):
    pass

class AccountAlreadyExistsException(Exception):
    pass

class AccountDoesNotExistException(Exception):
    pass

def custom_hash(input_string):
    '''Returns a hashed password to store in the db'''
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    return sha256.hexdigest()

def db_name(name:str):
    '''Returns the name version that can be a table name in the db'''
    name_elements = name.split(" ")
    shaped_name = "_".join(name_elements).lower()
    return shaped_name

def db_path() -> str | pathlib.Path:
    '''Returns the db path for the conn'''
    def db_folder() -> str:
        """Returns the default directory of the folder of the database

        Returns:
            (str | Path): The folder name of the Database
        """

        return pathlib.Path(os.getcwd())

    DB_NAME = "database.db"
    DB_FOLDER = db_folder()

    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    return DB_PATH

def show_name(name:str) -> str:
    '''Returns a string that reverses the the effect of db_name'''
    name_elements = name.split("_")
    shaped_name = " ".join(name_elements).capitalize()
    return shaped_name

def create_db() -> None:
    """
    Creates 2 tables. 

    1. The default_vault (stores multiple accounts and a vault_id for each account)
    2. The vaults (stores all the vault_names with their id)
    3. The default vault table, named "default_vault" where the first accounts of the user can saved
    """
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        # Create the Users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            vaults_ids TEXT -- Stores a JSON
        );
        """)

        # Create the Vaults table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vaults (
            vault_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """)

        # Create the default vault table
        try:
            cur.execute("""
            CREATE TABLE default_vault (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT,
                service TEXT
            );
            """)
            # Add the default_table into the vaults table with a random password
            cur.execute("""INSERT INTO vaults (name, password) VALUES (?, ?)""", ("default_vault", custom_hash("thanos"))) #! The key here has to change
        except sqlite3.OperationalError as e: # For the case that default_vault exists already and for some reason (probably I will be stupid) the create_db  gets called again
            print(e)

        conn.commit()

def create_vault_table(vault_name:str, vault_pass:str) -> None:
    """Creates a new vault table in the database and adds its id to the vaults table

    Args:
        vault_name (str): The name of the new vault in regular form
        vault_pass (str): The password of the vault

    Returns:
        _description_: None
    
    Raises:
        _type_: VaultAlreadyExistsException
    """
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        # Create the new vault table
        try:
            # Start a transaction
            cur.execute("BEGIN TRANSACTION;")
            
            # Check if the vault already exists
            cur.execute("SELECT COUNT(*) FROM vaults WHERE name = ?", (db_name(vault_name),))
            if cur.fetchone()[0] > 0:
                raise VaultAlreadyExistsException(f"{db_name(vault_name)} table already exists")
            
            # Insert the new vault into the 'vaults' table
            cur.execute("INSERT INTO vaults (name, password) VALUES (?, ?)", (db_name(vault_name), custom_hash(vault_pass),))

            # Create a new table for the vault with the corresponding 'vault_id'
            cur.execute(f"""
                CREATE TABLE {db_name(vault_name)} (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    email TEXT,
                    password TEXT,
                    service TEXT
                )
            """)


            # Commit the transaction
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f"An error occurred: {e}")
            # Rollback the transaction if an error occurs
            conn.rollback()
        except VaultAlreadyExistsException as e:
            print(e)
            conn.rollback()

def get_all_vaults() -> List[str]:
    '''Returns a list with all the vaults saved in the database'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        query = '''SELECT name FROM sqlite_master WHERE type='table';'''
        cur.execute(query)

        vaults = cur.fetchall()
        vaults = [show_name(x[0]) for x in vaults if (x[0] != "sqlite_sequence")]

        return vaults

def check_for_valid_vault_password(vault_name:str, vault_pass:str) -> bool:
    """Checks if the hash of vault_pass is equal to the hash that is being stored in the vaults table

    Args:
        vault_name (str): The name of the vault in regular form
        vault_pass (str): The vault of the password to be tested if matched

    Returns:
        bool: true or false
    
    Raises:
        _description_: InvalidPasswordException
    """
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        
        cur.execute("SELECT password FROM vaults WHERE name = ?", (db_name(vault_name), ) )
        hashed_pass = cur.fetchone()

        try:
            if not hashed_pass:
                # The vault doesn't exists
                raise InvalidPasswordException("The vault doesn't exists")
            
            if custom_hash(vault_pass) == hashed_pass[0]:
                return True
        except InvalidPasswordException as e:
            pass
    
    return False

def check_for_duplicate_account(vault_name: str, account_dict:dict[str, str]) -> bool:
    """Returns true if the account already exists in vault with name vault_name else returns false.
    A duplicate is considered an account with the same combination of email and service as most online
    services do not allow to create a 2 account with 2 emails.

    Args:
        vault_name (str): Name of the vault
        account_dict (dict[str, str]): The dictionary containing the username email password and service as keys
        NOTE it's important to pass the encrypted data here 

    Returns:
        bool: True or False
    """
    email = account_dict['email']
    service = account_dict['service']

    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        try:
            # Check if the vault table exists
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{db_name(vault_name)}';")
            if cur.fetchone() is None:
                raise InvalidVaultException(f"Vault with ID '{db_name(vault_name)}' does not exist.")
            
            # Search for the account by email
            cur.execute(f"""
                SELECT account_id, username, email, password, service 
                FROM {db_name(vault_name)}
                WHERE email LIKE ? AND service LIKE ?;
            """, (email, service, ))
            
            # Fetch the matching account
            result = cur.fetchone()
            if result is None:
                return False # The account does not exists in the vault

            return True # The account was found

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
        except InvalidVaultException as e:
            print(e)
            return False

def save_account(vault_name:str, vault_pass:str, account_dict: dict) -> Optional[str | dict]:
    """Unpacks the account_dict of the account details and saves them into the database.

    Args:
        vault_name (str): The name of the vault
        vault_pass (str): The password of the vault
        account_dict (dict): A list in the form of [username, email, password, service]

    Returns:
        str | dict: Returns the error messages | encrypted account_dict
    """
    
    # NOTE LOOK into the format
    username = account_dict['username']
    email = account_dict['email']
    password = account_dict['password']
    service = account_dict['service']

    key = custom_hash(vault_pass)

    enc_account_dict = {
        "username": encrypt(key, username),
        "email": encrypt(key, email),
        "password": encrypt(key, password),
        "service": encrypt(key, service)
    }

    enc_username = enc_account_dict["username"]
    enc_email = enc_account_dict["email"]
    enc_password = enc_account_dict["password"]
    enc_service = enc_account_dict["service"]

    try:
        # Check if the vault password is matching
        is_vault_pass_valid = check_for_valid_vault_password(vault_name, vault_pass)
        if not is_vault_pass_valid:
            raise InvalidPasswordException("Wrong Password")

        # Check if the account already exists in the vault
        is_account_duplicate = check_for_duplicate_account(vault_name, enc_account_dict)
        if is_account_duplicate:
            raise AccountAlreadyExistsException("The account is already stored in the vault")
    
    except InvalidPasswordException as e:
        print(e)
        return str(e)
    
    except AccountAlreadyExistsException as e:
        print(e)
        return str(e)
        
    try:
        # Connect to the db and insert the account into the correct vault
        with sqlite3.connect(db_path()) as conn:
            cur = conn.cursor()

            cur.execute("BEGIN TRANSACTION;")

            cur.execute(f"""INSERT INTO {db_name(vault_name)} 
                        (username, email, password, service)
                        VALUES (?,?,?,?)"""
                        ,(enc_username, enc_email, enc_password, enc_service,) 
                        )
            
            conn.commit()
    except sqlite3.OperationalError as e:
        print(e)
        return str(e)




    # Actual storing of the account in the corresponding vault of the db

def get_vault_id(vault_name:str) -> int:
    """Gets the vault_id of the vault_name specified

    Args:
        vault_name (str): The regular name of the vault table
    Returns:
        int: The vault_id
    """

    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        cur.execute(f"""SELECT vault_id FROM vaults WHERE name = ?""", (db_name(vault_name), ) )
        vault_id = cur.fetchone()[0]

        if not vault_id:
            raise InvalidVaultException("This vaults does not exist in vaults")

        print(f"vault_name={db_name(vault_name)}, vault_id={vault_id}", )
    
    return vault_id

def get_all_accounts_from_vault(vault_name:str, vault_pass:str) -> list[dict[str, str]]:
    """Decrypts all of the contents of the vault and returns them as a list of nicely mapped dictionaries

    Args:
        vault_name (str): The name of the vault in regular format
        vault_pass (str): The password of the vault

    Returns:
        _type_: list[dict[str, str]]
        _description_: Returns a list of the decrypted accounts of the vault
    """
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        key = custom_hash(vault_pass)
        cur.execute(f'''SELECT * FROM {db_name(vault_name)}''')

        contents = cur.fetchall()
        dec_content = decrypt_nested_account_list(key, contents)

        return dec_content

def get_account_from_vault(vault_name: str, vault_pass: str, account_dict: dict[str, str]) -> dict[str, str]:
    """Returns the decrypted version of the account stored in the db. The account_dict  

    Args:
        vault_name (str): The name of the vault
        vault_pass (str): The password of the vault
        account_dict (dict[str, str]): The standard account_dict with 
        (account_id:optional, username:optional, email:VITAL, password:optional, service:VITAL) as 
        its keys. NOTE you need to input the unencrypted dictionary
        

    Returns:
        _type_: dict[str, str]
        _description_: Returns the unencrypted account off of the vault. If it exists. If not returns the equivalent error message
    """

    # Check if vault_pass is valid
    is_valid_vault_pass = check_for_valid_vault_password(vault_name, vault_pass)
    try:
        if not is_valid_vault_pass: 
            raise InvalidPasswordException("The password of the vault is not correct.")       
    except InvalidPasswordException as e:
        print(e)
        return str(e)

    # Encrypt the dictionary for the search. I only really need email and service for that purpose
    key = custom_hash(vault_pass)
    enc_email = encrypt(key, account_dict["email"])
    enc_service = encrypt(key, account_dict["service"])
    
    enc_account_dict = {
        "email": enc_email,
        "service": enc_service
    }
    # Check if the account exists
    does_account_exists_in_vault = check_for_duplicate_account(vault_name, enc_account_dict)
    try:
        if not does_account_exists_in_vault:
            raise AccountDoesNotExistException("The account you are looking for does not exist.")
    except AccountDoesNotExistException as e:
        return str(e)

    # Connect to the db
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        # Search for the matching encrypted account
        cur.execute(f"""SELECT * FROM {db_name(vault_name)}
                    WHERE email LIKE ? AND service LIKE ?""",
                    (enc_email, enc_service, ) )
        enc_account_list = cur.fetchone()

        # Decrypt the account
        account_dict = decrypt_account_list(key, enc_account_list)
        return account_dict
        # Return the decrypted account

def drop_vault(vault_name:str):
    '''Deletes a vault(table) from the database'''
    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()
        
        # is_correct_pass = check_for_valid_vault_password(vault_name, vault_pass)
        # if not is_correct_pass:
        #     return
        cur.execute("BEGIN TRANSACTION;")
        try:
            cur.execute("DELETE FROM vaults WHERE name = ?", (db_name(vault_name), ))
            cur.execute(f'''DROP TABLE {db_name(vault_name)}''')
        except sqlite3.Error as e:
            print(e)
            conn.rollback()
        conn.commit()

def drop_all_vaults():
    '''Drops all the vaults'''
    vaults = get_all_vaults()
    for vault in vaults:
        drop_vault(vault)

def delete_account(vault_name:str, vault_pass:str, account_dict:dict[str, str]) -> str | None:
    """Deletes the account provided from the vault, if it exists.

    Args:
        vault_name (str): The name of the vault
        vault_pass (str): The password of the vault
        account_dict (_type_): A dictionary with the following keys -->
        (account_id:optional, username:optional, email:VITAL, password:optional, service:VITAL)

    Returns:
        _type_: str
        _description_: Returns only when there is an exception and it returns the error message
    """    

    key = custom_hash(vault_pass)
    enc_account_dict = encrypt_account_dict(key, account_dict)

    enc_email_to_delete = enc_account_dict["email"]
    enc_service_to_delete = enc_account_dict["service"]

    # Check if the account is stored in the vault
    is_account_in_vault = check_for_duplicate_account(vault_name, enc_account_dict)
    try:
        if not is_account_in_vault:
            raise AccountDoesNotExistException("The account you are trying to delete doesn't exist.")
    except AccountDoesNotExistException as e:
        print(e)
        return str(e)

    with sqlite3.connect(db_path()) as conn:
        cur = conn.cursor()

        cur.execute("BEGIN TRANSACTION;")
        try:
            cur.execute(f"""DELETE FROM {db_name(vault_name)} 
                    WHERE email LIKE ? AND service LIKE ?"""
                    , (enc_email_to_delete, enc_service_to_delete, ) )
        except sqlite3.OperationalError as e:
            conn.rollback()
            return str(e)
        
        conn.commit()