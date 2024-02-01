from cryptography.fernet import Fernet
import os

# NOTE: Every time you access the key do it into binary mode
# NOTE: The encrtyption of the files is being done in the db folder
# All the keys will be passed in the db folder and be loaded from there

def generate_key():
    '''Generates a key into the app folder to use to encrypt/decrypt'''
    key = Fernet.generate_key()
    return key

def encrypt_data(key:bytes, data:str):
    '''Encryptes the data you pass in with the key you pass inn'''
    data = bytes(data, 'utf-8')
    encrypted_data = Fernet(key).encrypt(data)
    
    return encrypted_data

def encrypt_list(key, input_list:list):
    for index, info in enumerate(input_list):
        input_list[index] = encrypt_data(key, info)
    
    return input_list + [key]

def decrypt_data(key:bytes, data:bytes):
    '''Decrypts the data you pass in'''
    decrypted_data = Fernet(key).decrypt(data)
    return decrypted_data.decode('utf-8')

def decrypt_nested_list(accounts:list):# acounts is :[(username, password, service, notes, key), (...)]
    for i, account_info in enumerate(accounts):
            accounts[i] = list(account_info)
            for index, element in enumerate(account_info[:-1]):
                accounts[i][index] = decrypt_data(account_info[-1], element)
            
            accounts[i].pop(-1)

    return accounts

def db_folder():
    '''Returns the app folder in the Documents'''
    #Get the user's User Folder
    user_folder = os.path.expanduser(f"~/Documents")
    app_folder = f"{user_folder}/Locker Pass"

    if not os.path.exists(app_folder):
        app_folder = os.makedirs(app_folder) 
    

    return app_folder
