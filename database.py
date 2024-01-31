from encryption import db_folder, generate_key, decrypt_data, encrypt_data
import sqlite3 as sql 
import os

def db_path():
    DB_NAME = "Account_services.db"
    DB_FOLDER = db_folder()

    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    return DB_PATH
print(db_path())
def create_database():
    pass

