from cryptography.fernet import Fernet
import os

# NOTE: Every time you access the key do it into binary mode
# NOTE: The encrtyption of the files is being done in the db folder
# All the keys will be passed in the db folder and be loaded from there

def generate_key(vault_name:str):
    '''Generates a key into the app folderto use to encrypt/decrypt'''
    APP_FOLDER = db_folder()
    key = Fernet.generate_key()
    key_name = f"{vault_name}.key"
    key_dir = os.path.join(APP_FOLDER, key_name)

    # Check for the key (CHANGE IT TO LINK TO A DATABASE TABLE)
    if os.path.exists(key_dir):
        with open(key_dir, "rb") as vault_key:
            key = vault_key.read()
    else:
        key = Fernet.generate_key()
        with open(key_dir, "wb") as vault_key:
            vault_key.write(key)
    
    return key

def encrypt_data(key, data:str):
    '''Encryptes the data you pass in with the key you pass inn'''
    data = bytes(data, 'utf-8')
    encrypted_data = Fernet(key).encrypt(data)
    
    return encrypted_data

def decrypt_data(key, data:bytes):
    '''Decrypts the data you pass in'''
    decrypted_data = Fernet(key).decrypt(data)
    return decrypted_data.decode('utf-8')

def db_folder():
    '''Returns the app folder in the Documents'''
    #Get the user's User Folder
    user_folder = os.path.expanduser(f"~/Documents")
    app_folder = f"{user_folder}/Locker Pass"

    if not os.path.exists(app_folder):
        app_folder = os.makedirs(app_folder) 
    

    return app_folder

if __name__ == '__main__':
    # Example code for actual use
    APP_FOLDER = db_folder()
    VAULT_NAME = "Test"
    
    key = generate_key(VAULT_NAME)
    print(key)
    data = "I am a hacker"

    encrypted = encrypt_data(key, data)
    print(encrypted)
    decrypted = decrypt_data(key, encrypted)
    print(decrypted)

    
    




    
    

            
