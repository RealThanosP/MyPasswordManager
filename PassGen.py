import secrets
import json

class PassGenerator:
    '''Generates passwords using python.secrets'''
    def __init__(self, length:int, easy_to_remember:bool, hasLetters:bool, hasNumbers:bool, hasSymbols:bool):
        self.easy_to_remember = easy_to_remember
        self.hasNumbers = hasNumbers
        self.hasSymbols = hasSymbols
        self.hasLetters = hasLetters
        self.length = length

    def __repr__(self):
        return f"""password:{self.generate_password()}, attributes:[{self.length}, 
                            {self.easy_to_remember}, 
                            {self.hasLetters},
                            {self.hasNumbers},
                            {self.hasSymbols}]"""
    
    def load_characters(self, file_name):
        '''Opens a json file with file_name and unloads all the keys as a list'''
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        words = [x for x in data.keys()]
        return words
    
    def selected_characters(self):
        #Lists
        self.uppercase = self.load_characters("Symbols_Folder/uppercase.json")
        self.lowercase = self.load_characters("Symbols_Folder/lowercase.json")
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.symbols = self.load_characters("Symbols_Folder/symbols.json")
        self.real_words = self.load_characters("Symbols_Folder/words.json")

        #Checks for allowed characters in the password
        allowed_characters = []

        if self.easy_to_remember:
            allowed_characters += self.real_words + self.uppercase
        
        if self.hasNumbers:
            allowed_characters += self.numbers
        
        if self.hasSymbols:
            allowed_characters += self.symbols
        
        if self.hasLetters:
            allowed_characters += self.uppercase + self.lowercase

        return allowed_characters
    
    def generate_password(self):
        '''Generates a random password'''
        password = ""
        random_choice = ""
        allowed_characters = self.selected_characters()

        if not allowed_characters:
            return None
        
        while len(password) < self.length:
            random_choice = secrets.choice(allowed_characters)
            if random_choice in self.real_words:
                random_choice = f"{random_choice}-"

            if len(random_choice + password) <= self.length:
                password += random_choice

        return password
