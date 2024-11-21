# This module is handling all the encryption of the app. 
# Uses a Proprietary encryption algorithm that I found on the web.
# Its crap, but for now (21/11/2024) it's looks fine to me

#* DONE
def encrypt(key: str , data: str) -> str:
    """Encrypts the data you put in with the key and Returns an encrypted string

    Args:
        key (str): A custom key that is used to encrypt the data
        data (str): The data you want to encrypt

    Returns:
        _type_: (str)
        _description_: Encrypted data
    """

    encrypted = []
    for i, c in enumerate(data):
        key_c = ord(key[i % len(key)])
        data_c = ord(c)
        encrypted.append(chr((data_c + key_c) % 127))
    return ''.join(encrypted)

#* DONE
def encrypt_account_dict(key: str, account_dict:dict[str:str]) -> dict[str:str]:
    """
    Returns:
        _type_: dict[str:str]
        _description_: Returns the encrypted version of the account dict
    """
    enc_account_dict = {}
    for keyword in account_dict: # loop over the keys of the dictionary
        if keyword == "account_id":
            continue
        enc_account_dict[keyword] = encrypt(key, account_dict[keyword])

    return enc_account_dict

#* DONE
def decrypt(key: str , encrypted:str) -> str:
    """The counter part of the encrypt function. It takes a key and an encrypted message and Returns,
    the original message

    Args:
        key (str): The key used to encrypt the original data
        encrypted (str): The encrypted message

    Returns:
        str: Original Message
    """
    
    data = []
    for i, c in enumerate(encrypted):
        key_c = ord(key[i % len(key)])
        enc_c = ord(c)
        data.append(chr((enc_c - key_c) % 127))
    return ''.join(data)

#* DONE
def decrypt_account_list(key: str, enc_account_list: list[str]) -> dict[str:str]:
    """It decrypts a list and maps the data in a dictionary with 
    (account_id, username, email, password, service) as the keys.
    Returns the decrypted dictionary

    Args:
        key (str): The encryption key used to encrypt
        enc_account_list (list[str]): The encrypted list returned from a sql query

    Returns:
        _type_: dict[str:str]
        _description_: Returns the dict with the attributes of the account mapped out_description_: Returns the dict with the attributes of the account mapped out
    """
    account_dict = {}

    attribute_list = ("account_id", "username", "email", "password", "service")
    for i, enc_attribute in enumerate(enc_account_list):
        attribute_key = attribute_list[i]
        if i == 0: # Does not include the account_id  in the encryption
            account_dict[attribute_key] = enc_attribute
        else:
            account_dict[attribute_key] = decrypt(key, enc_attribute)

    return account_dict

#* DONE
def decrypt_nested_account_list(key: str, enc_nested_list: list[list[str]]) -> list[dict[str:str]]:
    """Returns a decrypted list of dictionaries formatted as a regular account_dict
    Args:
        key (str): The key used to encrypt the accounts in the vault
        enc_nested_list (list[list[str]]): The result of a "SELECT * FROM ..." type query 

    Returns:
        _type_: (list[dict[str:str]])
        _description_: Returns a list of dictionaries
    """
    account_dict_list = []
    for account_list in enc_nested_list:
        account_dict = decrypt_account_list(key, account_list)

        account_dict_list.append(account_dict)
    
    return account_dict_list
