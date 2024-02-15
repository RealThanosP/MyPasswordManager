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
    '''Returns a encrypted list. The key does NOT return'''
    for index, info in enumerate(input_list):
        input_list[index] = encrypt_data(key, info)
    
    return input_list

def decrypt_data(key:bytes, data:bytes):
    '''Decrypts the data you pass in'''
    decrypted_data = Fernet(key).decrypt(data)
    return decrypted_data.decode('utf-8')

def decrypt_list(key:bytes, account:list):
    '''Returns the decrypted list with the key in the last place'''
    for i, account_info in enumerate(account):
        account[i] = decrypt_data(key, account_info)

    return account

def decrypt_nested_list(key:bytes, accounts:list):
    '''Returns all the the accounts info with the key in the last place of the list'''
    for i, account_info in enumerate(accounts):
            accounts[i] = list(account_info)
            for index, element in enumerate(account_info):
                accounts[i][index] = decrypt_data(key, element)
    return accounts
