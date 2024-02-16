import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PassGen import PassGenerator
import pyperclip
from tkinter import messagebox
import database

#Constants
# Window
WIN_WIDTH = 700
WIN_HEIGHT = 550

# Paths
GENERATOR_BUTTON_IMG = "Images/refresh.png"
COPY_BUTTON_IMG = "Images/copy.png"
APP_ICON = "Images/lock_icon.ico"
SAVE_IMG = "Images/save.png"
ADD_VAULT_IMG = "Images/add.png"
ENTER_VAULT_IMG = "Images/enter.png"
SEE_PASSWORD_IMG = "Images/see.png"
HIDE_PASSWORD_IMG = "Images/hide.png"
TRASH_CAN_IMG = "Images/trash-can.png"

BUTTON_SIZE = (25,25)
BUTTON_MEDIUM_SIZE = (40,40)
BUTTON_BIG_SIZE = (100, 120)

# Fonts and colors
BUTTON_COLOR = "#333333"
BUTTON_TEXT_COLOR = "#AAAAAA"
BUTTON_COLOR_ON_HOVER = "#555555"
FONT_NAME = "Segui UI"

# Password colors
RED = "#FF5733"
YELLOW = "#FFD700"
ORANGE = "#FF8C00"
DARK_GREEN = "#006400"
GREEN = "#228B22"
LIGHT_GREEN = "#7FFF00"

SAVE_COLOR = "#1F1F1F"   
SEE_COLOR = "#292929"     
ADD_COLOR = "#383838"     
DELETE_COLOR = "#454545"  

FONT_SIZE_LABELS = 15
FONT_SIZE_COMBOBOX = 13
FONT_SIZE_BUTTONS = 15
FONT_SIZE_ENTRIES = 17
FONT_SIZE_SUB_TITLES = 20 
FONT_SIZE_TITLES = 24

# Paddings
PADDING_CHECKBOX = 5
PADDING_TEXT = 10
PADDING_SLIDER = 60
PADDING_SAVE_GAP = 50
PADDING_COMBOBOX = 30
PADDING_SLIDER_LABEL = 20
PADDING_VAULT_ENTRY = 13

GENERATOR_ENTRY_WIDTH = WIN_WIDTH-4.9*BUTTON_SIZE[0]
SAVE_ENTRY_WIDTH = 250

SAVE_TEXT_BOX_HEIGHT = 100
SAVE_COMBOBOX_SIZE = (150, 30)

SEE_ENTRY_WIDTH = 300
SEE_COMBOBOX_SIZE = (80, 33)

ADD_ENTRY_WIDTH = 330

DELETE_COMBOBOX_SIZE = (50, 33)


class MainApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.iconbitmap(APP_ICON)
        self.resizable(False, False)

        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("dark-blue")

        # Main frame
        self.frame = ctk.CTkFrame(master=self,
                                  width=WIN_WIDTH, height=WIN_HEIGHT)
        self.frame.pack(expand=True, fill="both")

        # Generator Button image
        self.generatorIMG = ctk.CTkImage(dark_image=Image.open(GENERATOR_BUTTON_IMG),
                                         light_image=Image.open(GENERATOR_BUTTON_IMG),
                                         size=BUTTON_SIZE)
        
        # Copy Button Image
        self.clipboardIMG = ctk.CTkImage(dark_image=Image.open(COPY_BUTTON_IMG),
                                    light_image=Image.open(COPY_BUTTON_IMG),
                                    size=BUTTON_SIZE)
        
        # Save button Image
        self.saveIMG = ctk.CTkImage(dark_image=Image.open(SAVE_IMG),
                                    light_image=Image.open(SAVE_IMG),
                                    size=BUTTON_SIZE)
        
        # Add vault button IMG
        self.addVaultIMG = ctk.CTkImage(dark_image=Image.open(ADD_VAULT_IMG),
                                        light_image=Image.open(ADD_VAULT_IMG),
                                        size=BUTTON_MEDIUM_SIZE)
        
        # Enter vault button IMG
        self.enterVaultIMG = ctk.CTkImage(dark_image=Image.open(ENTER_VAULT_IMG),
                                        light_image=Image.open(ENTER_VAULT_IMG),
                                        size=BUTTON_SIZE)
        
        # See password button IMG
        self.showPassIMG = ctk.CTkImage(dark_image=Image.open(SEE_PASSWORD_IMG),
                                       light_image=Image.open(SEE_PASSWORD_IMG),
                                       size=BUTTON_SIZE)
        
        # Hide password button IMG
        self.hidePassIMG = ctk.CTkImage(dark_image=Image.open(HIDE_PASSWORD_IMG),
                                       light_image=Image.open(HIDE_PASSWORD_IMG),
                                       size=BUTTON_SIZE)
        
        # Delete password button IMG
        self.deleteVaultIMG = ctk.CTkImage(dark_image=Image.open(TRASH_CAN_IMG),
                                       light_image=Image.open(TRASH_CAN_IMG),
                                       size=BUTTON_SIZE)

        self.vaultTabs = ctk.CTkTabview(master=self.frame,
                                        segmented_button_fg_color=BUTTON_COLOR,
                                        segmented_button_selected_hover_color=BUTTON_COLOR_ON_HOVER,
                                        segmented_button_selected_color=BUTTON_COLOR_ON_HOVER,
                                        segmented_button_unselected_color=BUTTON_COLOR,
                                        anchor="w")

        # Defining the tabs
        self.showVaultTab = self.vaultTabs.add("Show Vault")
        self.addVaultTab = self.vaultTabs.add("Add New Vault")
        self.deleteVaultTab = self.vaultTabs.add("Delete Vault")

        # Putting stuff on the tabs
        self.addVaultSection()
        self.generatorSection()
        self.savePasswordSection()
        self.seeVaultSection()
        self.deleteVaultSection()
        self.vaultTabs.pack(fill="both", expand=True)

    # Pass generator section ##DONE##
    def generatorSection(self):
        '''Defines the password generator UI and places it into the main frame'''
        # Generator Section frame
        self.frameGenerator = ctk.CTkFrame(master=self.frame, corner_radius=0)
        self.frameGenerator.pack(fill="x")

        #Top frame:
        self.frameGeneratorTopBar = ctk.CTkFrame(master=self.frameGenerator, corner_radius=0)
        self.frameGeneratorTopBar.pack(fill="x")

        #Title label for generator
        self.generatorLabel = ctk.CTkLabel(master=self.frameGeneratorTopBar,
                                           text="Generate Random Password: ",
                                           font=(FONT_NAME, FONT_SIZE_TITLES))
        self.generatorLabel.grid(row=0, column=0, columnspan=3)

        #Password entrybox
        self.generatorEntry = ctk.CTkEntry(master=self.frameGeneratorTopBar,
                                           font=(FONT_NAME, FONT_SIZE_ENTRIES),
                                           width=GENERATOR_ENTRY_WIDTH,
                                           corner_radius=5,
                                           insertofftime=999999999, insertontime=0)
        self.generatorEntry.grid(row=1, column=0, padx=PADDING_CHECKBOX)

        # Copy Button
        self.copyButton = ctk.CTkButton(master=self.frameGeneratorTopBar,
                                        image=self.clipboardIMG,
                                        width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                        text="", hover_color=BUTTON_COLOR_ON_HOVER,
                                        fg_color=BUTTON_COLOR,
                                        corner_radius=10,
                                        command=self.copy_clipboard)
        self.copyButton.grid(row=1, column=1, padx=PADDING_CHECKBOX)

        # Generator Button
        self.generatorButton = ctk.CTkButton(master=self.frameGeneratorTopBar,
                                             image=self.generatorIMG,
                                             text="",
                                             width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                             fg_color=BUTTON_COLOR, hover_color=BUTTON_COLOR_ON_HOVER,
                                             corner_radius=10,
                                             command=self.generatePassword)
        self.generatorButton.grid(row=1, column=2, padx=(0,PADDING_CHECKBOX))

        # Password progressbar
        self.generatorProgressBar = ctk.CTkProgressBar(master = self.frameGeneratorTopBar,
                                                       orientation="horizontal",
                                                       width=GENERATOR_ENTRY_WIDTH,
                                                       )
        
        self.generatorProgressBar.grid(row=2, column=0)
        #Checkbox/Settitngs frame
        
        self.frameGeneratorSettings = ctk.CTkFrame(master=self.frameGenerator, corner_radius=0)
        self.frameGeneratorSettings.pack(fill="x")

        # Checkbox variables:
        self.easyToRememberVar = ctk.StringVar(value=False)
        self.hasLettersVar = ctk.StringVar(value=False)
        self.hasNumbersVar = ctk.StringVar(value=False)
        self.hasSymbolsVar = ctk.StringVar(value=False)

        # Generator Checkboxes:
        self.easyToRememberBox = ctk.CTkCheckBox(master=self.frameGeneratorSettings,
                                                 text="Easy to remember",
                                                 font=(FONT_NAME, FONT_SIZE_LABELS),
                                                 onvalue=True, offvalue=False,
                                                 fg_color=BUTTON_COLOR_ON_HOVER,
                                                 variable=self.easyToRememberVar)
        self.easyToRememberBox.grid(row=0, column=0, sticky="w", pady=PADDING_CHECKBOX, padx=PADDING_CHECKBOX)

        self.hasLettersBox = ctk.CTkCheckBox(master=self.frameGeneratorSettings,
                                             text="Has letters",
                                             font=(FONT_NAME, FONT_SIZE_LABELS),
                                             onvalue=True, offvalue=False,
                                             fg_color=BUTTON_COLOR_ON_HOVER,
                                             variable=self.hasLettersVar)
        self.hasLettersBox.grid(row=1, column=0, sticky="w", pady=PADDING_CHECKBOX, padx=PADDING_CHECKBOX)

        self.hasNumbersBox = ctk.CTkCheckBox(master=self.frameGeneratorSettings,
                                             text="Has Numbers",
                                             font=(FONT_NAME, FONT_SIZE_LABELS),
                                             onvalue=True, offvalue=False,
                                             fg_color=BUTTON_COLOR_ON_HOVER,
                                             variable=self.hasNumbersVar)
        self.hasNumbersBox.grid(row=2, column=0, sticky="w", pady=PADDING_CHECKBOX, padx=PADDING_CHECKBOX)

        self.hasSymbolsBox = ctk.CTkCheckBox(master=self.frameGeneratorSettings,
                                             text="Has symbols",
                                             font=(FONT_NAME, FONT_SIZE_LABELS),
                                             onvalue=True, offvalue=False,
                                             fg_color=BUTTON_COLOR_ON_HOVER,
                                             variable=self.hasSymbolsVar)
        self.hasSymbolsBox.grid(row=3, column=0, sticky="w", pady=PADDING_CHECKBOX, padx=PADDING_CHECKBOX)

        # Length bar topLabel
        self.lengthLabel = ctk.CTkLabel(master=self.frameGeneratorSettings,
                                        text="Length",
                                        font=(FONT_NAME, FONT_SIZE_BUTTONS))
        self.lengthLabel.grid(row=0, column=1, rowspan=2)

        # Length bar
        self.slider = ctk.CTkSlider(master =self.frameGeneratorSettings,
                                    from_=0, to=50,
                                    fg_color=BUTTON_COLOR_ON_HOVER,
                                    width=250, button_color= BUTTON_COLOR,
                                    command=self.slidingLength)
        self.slider.grid(row=0, column=1, rowspan=4, padx=PADDING_SLIDER)

        # Length bar label
        self.sliderLabel = ctk.CTkLabel(master=self.frameGeneratorSettings,
                                          text="25", justify="center",
                                          font=(FONT_NAME, FONT_SIZE_LABELS))
        self.sliderLabel.grid(row=3, column=1, rowspan=4, padx=PADDING_SLIDER_LABEL)

        #Error Label
        self.errorLabelGenerator = ctk.CTkLabel(master=self.frameGeneratorSettings, 
                                                text="",
                                                font=(FONT_NAME, FONT_SIZE_LABELS),
                                                justify="center")
        self.errorLabelGenerator.grid(row=0, column=2, sticky="e", rowspan=4)
        
    def slidingLength(self, value):
        '''Handles the change of values and colors of both the slider and the progressBar'''
        # Makes the slider feel more cut rather that a scroller
        rounded_value = round(value / 2) * 2
        self.slider.set(rounded_value)
        self.sliderLabel.configure(text=int(value))
        
        # This if/elif/else monstrosity detemines the color of the progress bar based on the
        # length of the password selected
        pass_strongness = self.sliderLabel.cget("text")
        if pass_strongness <= 5:
            self.generatorProgressBar.configure(progress_color=RED)
        elif pass_strongness > 5 and pass_strongness <= 10:
            self.generatorProgressBar.configure(progress_color=ORANGE)
        elif pass_strongness > 10  and pass_strongness <= 20:
            self.generatorProgressBar.configure(progress_color=LIGHT_GREEN)
        elif pass_strongness > 20 and pass_strongness < 30:
            self.generatorProgressBar.configure(progress_color=GREEN)
        elif pass_strongness >= 30:
            self.generatorProgressBar.configure(progress_color=DARK_GREEN)

        # Determines the value of the progressbar
        bar_color = self.generatorProgressBar.cget("progress_color")
        self.slider.configure(button_hover_color=bar_color, button_color=bar_color)
        self.generatorProgressBar.set(pass_strongness/20)

    def generatePassword(self):
        '''Generate a random password and pops it into the generatorEntry'''
        bool_dictionary = {"0": False, "1":True}
        # Resets the error label and entry values
        self.errorLabelGenerator.configure(text="")
        self.generatorEntry.delete(0,"end")

        generator = PassGenerator(int(self.slider.get()), 
                                  bool_dictionary[self.easyToRememberVar.get()], 
                                  bool_dictionary[self.hasLettersVar.get()],
                                  bool_dictionary[self.hasNumbersVar.get()],
                                  bool_dictionary[self.hasSymbolsVar.get()])
        
        random_password = generator.generate_password()
        
        if random_password == None:
            self.errorLabelGenerator.configure(text=f"Please check \none of the checkboxes \nto generate a \npassword")
            return

        if random_password == "":
            self.errorLabelGenerator.configure(text=f"You cannot \ngenerate a password \nlength 0.")
            return
        
        self.generatorEntry.delete(0, "end")
        self.generatorEntry.insert(0, random_password)
    
    def copy_clipboard(self):
        '''Copies the entry input to the user's clipboard'''
        generated_password = self.generatorEntry.get()
        pyperclip.copy(generated_password)
  
    # Saving password ##DONE##
    def savePasswordSection (self):
        '''Defines the section of the password saving in the main frame'''
        # Main frame
        self.frameSave = ctk.CTkFrame(master=self.frame, corner_radius=0,
                                      fg_color=SAVE_COLOR)
        self.frameSave.pack(side="left", fill="y")

        #Title label
        self.saveTopLabel = ctk.CTkLabel(master=self.frameSave, 
                                         text="Save account details:",
                                         font=(FONT_NAME, FONT_SIZE_SUB_TITLES))
        self.saveTopLabel.pack(pady=PADDING_TEXT)

        # Username entry
        self.saveUsernameEntry = ctk.CTkEntry(master = self.frameSave,
                                                width=SAVE_ENTRY_WIDTH,
                                                font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                                placeholder_text="Username/Email: ")
        self.saveUsernameEntry.pack(pady=PADDING_TEXT, padx=PADDING_TEXT)

        # Password entry
        self.savePasswordEntry = ctk.CTkEntry(master = self.frameSave,
                                                width=SAVE_ENTRY_WIDTH,
                                                font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                                placeholder_text="Password:",
                                                show="*")
        self.savePasswordEntry.pack(pady=PADDING_TEXT, padx=PADDING_TEXT)

        # Service entry:
        self.saveServiceEntry = ctk.CTkEntry(master = self.frameSave,
                                                width=SAVE_ENTRY_WIDTH,
                                                font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                                placeholder_text="Service:")
        self.saveServiceEntry.pack(pady=PADDING_TEXT, padx=PADDING_TEXT)

        # Vault pass entry:
        self.saveVaultPassEntry = ctk.CTkEntry(master=self.frameSave, 
                                               width=SAVE_ENTRY_WIDTH,
                                               font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                               placeholder_text="Secret vault password: ",
                                               show="*")
        self.saveVaultPassEntry.pack(pady=(PADDING_SLIDER,0), padx=PADDING_TEXT)

        # Combobox with all the vaults already created
        vaults = database.get_all_vaults()
        self.saveVaultComboBox = ctk.CTkComboBox(master=self.frameSave,
                                                 values=vaults,
                                                 width=SAVE_COMBOBOX_SIZE[0], height=SAVE_COMBOBOX_SIZE[1],
                                                 font=(FONT_NAME, FONT_SIZE_LABELS),
                                                 dropdown_fg_color=BUTTON_COLOR,
                                                 dropdown_font=(FONT_NAME, FONT_SIZE_COMBOBOX),
                                                 button_color=BUTTON_COLOR,
                                                 border_color=BUTTON_COLOR,
                                                 button_hover_color=BUTTON_COLOR_ON_HOVER,
                                                 state="readonly")
        self.saveVaultComboBox.pack(side="right", padx=(PADDING_CHECKBOX,PADDING_TEXT))

        # Save Password button
        self.saveButton = ctk.CTkButton(master=self.frameSave,
                                        text="Save", 
                                        font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                        fg_color=BUTTON_COLOR, hover_color=BUTTON_COLOR_ON_HOVER,
                                        text_color=BUTTON_TEXT_COLOR,
                                        width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                        image=self.saveIMG,
                                        command=self.saveAccount)
        self.saveButton.pack(side="left", padx=(PADDING_TEXT,0))
        
    def saveAccount(self):
        '''Saves account info into a database, using encryption for all the data.'''
        
        # Takes the input from the fields
        username = self.saveUsernameEntry.get()
        password = self.savePasswordEntry.get()
        service = self.saveServiceEntry.get()
        vault_pass = self.saveVaultPassEntry.get()

        account_list = [username, password, service]

        # Checks for empty cells/input fields
        if not (username and password and service):
            self.errorLabelGenerator.configure(text="Please fill out all the\nfields before saving.")
            return 
        
        # Select the vault
        selected_vault = self.saveVaultComboBox.get()

        if not selected_vault:
            self.errorLabelGenerator.configure(text="Please choose a vault\nto store the password")
            return
        
        # Encrypt the data_list with the key and store the
        # encrypted version into the database
        stored = database.save_account(selected_vault, vault_pass, account_list)

        already_stored_error_msg = "You have this\naccount already saved."
        wrong_pass_error_msg = "Wrong vault password.\nPlease try again."
        success_error_msg = "You successfully\nsaved this account."

        # Checks the wanted error message based on the status of the storing
        if stored == "Password":
            self.errorLabelGenerator.configure(text=wrong_pass_error_msg)
        elif stored == "Already saved":
            self.errorLabelGenerator.configure(text=already_stored_error_msg)
        else:
            self.errorLabelGenerator.configure(text=success_error_msg)

        # Resets the entries
        self.saveUsernameEntry.delete(0, "end")
        self.savePasswordEntry.delete(0, "end")
        self.saveServiceEntry.delete(0, "end")
        self.saveVaultPassEntry.delete(0, "end")

    # See saved password of the diff vaults ###DONE###
    # NOTE: The table window is NOT done
    def seeVaultSection(self):
        '''Defines the section of the vault revealing the accounts saved in the database'''
        # Main frame 
        self.frameSeePass = ctk.CTkFrame(master=self.showVaultTab, corner_radius=0,
                                         fg_color=SEE_COLOR)
        self.frameSeePass.pack(fill="x")

        # Vault name selection box
        vaults = database.get_all_vaults()
        self.seeVaultComboBox = ctk.CTkComboBox(master=self.frameSeePass,
                                                 values=vaults,
                                                 width=SEE_ENTRY_WIDTH, height=SEE_COMBOBOX_SIZE[1],
                                                 font=(FONT_NAME, FONT_SIZE_LABELS),
                                                 dropdown_fg_color=BUTTON_COLOR,
                                                 dropdown_font=(FONT_NAME, FONT_SIZE_COMBOBOX),
                                                 button_color=BUTTON_COLOR,
                                                 border_color=BUTTON_COLOR,
                                                 button_hover_color=BUTTON_COLOR_ON_HOVER,
                                                 state="readonly")
        self.seeVaultComboBox.pack(pady=(50,0), padx=(0,35))

        # Vault password entry (secret phrase for each vault)
        self.seeVaultPassEntry = ctk.CTkEntry(master=self.frameSeePass,
                                          width=SEE_ENTRY_WIDTH,
                                          font=(FONT_NAME, FONT_SIZE_ENTRIES),
                                          placeholder_text="Vault Secret Password:",
                                          show="*")
        self.seeVaultPassEntry.pack(side="left", padx=(40,PADDING_TEXT), pady=PADDING_TEXT)

        # Frame for the button
        self.frameSeeButton = ctk.CTkFrame(master=self.showVaultTab,
                                           fg_color=BUTTON_COLOR,)
        self.frameSeeButton.pack()

        # Button for the pop up
        self.showPassButton = ctk.CTkButton(master=self.frameSeeButton,
                                            image=self.enterVaultIMG,
                                            text="Show Vault",
                                            font=(FONT_NAME, FONT_SIZE_BUTTONS),
                                            text_color=BUTTON_TEXT_COLOR,
                                            fg_color=BUTTON_COLOR,
                                            hover_color=BUTTON_COLOR_ON_HOVER,
                                            corner_radius=0,
                                            command=self.showVaultWindow)
        self.showPassButton.pack()

        # Hide/Show password button
        self.seeHidePassButton = ctk.CTkButton(master=self.frameSeePass,
                                               width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                               text="", image=self.showPassIMG,
                                               fg_color=BUTTON_COLOR, hover_color=BUTTON_COLOR_ON_HOVER,
                                               command=self.hide_show_password)
        self.seeHidePassButton.pack(side="right", padx=(0,30))

    def showVaultWindow(self):
        vault_pass = self.seeVaultPassEntry.get()
        vault_name = self.seeVaultComboBox.get()
        
        if not (vault_name and vault_pass):
            self.errorLabelGenerator.configure(text="Please select\na vault to open.")
            return
        is_correct_pass = database.is_correct_vault_pass(vault_name, vault_pass)

        if not is_correct_pass:
            self.errorLabelGenerator.configure(text="Wrong Password\nPlease try again.")
            self.seeVaultPassEntry.delete(0, "end")
            return
        
        self.destroy()
        app = VaultPopUp(vault_name, vault_pass)
        app.mainloop()     

    def hide_show_password(self):
        state = self.seeVaultPassEntry.cget("show")
        if state == "*":
            self.seeVaultPassEntry.configure(show="")
            self.seeHidePassButton.configure(image=self.hidePassIMG)
        else:
            self.seeVaultPassEntry.configure(show="*")
            self.seeHidePassButton.configure(image=self.showPassIMG)

    # Add new vaults ##DONE##
    def addVaultSection(self):
        # Main frame
        self.frameAddVault = ctk.CTkFrame(master=self.addVaultTab, corner_radius=0,
                                          fg_color=SEE_COLOR)
        self.frameAddVault.pack(fill="both", padx=20, pady=20)

        # Add vault entry 
        self.addVaultNameEntry = ctk.CTkEntry(master=self.frameAddVault,
                                              width=ADD_ENTRY_WIDTH,
                                              font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                              placeholder_text="Vault name: ")
        self.addVaultNameEntry.bind("<Key>", lambda event: self.entry_on_click(event))
        self.addVaultNameEntry.pack(pady=PADDING_CHECKBOX)

        # Add vault secret password
        self.addVaultPassEntry = ctk.CTkEntry(master=self.frameAddVault,
                                         width=ADD_ENTRY_WIDTH,
                                         font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                         placeholder_text="Secret password: ",
                                         show="*")
        self.addVaultPassEntry.pack(pady=PADDING_CHECKBOX)

        # Add vault secret password
        self.addVaultReEnterPassEntry = ctk.CTkEntry(master=self.frameAddVault,
                                         width=ADD_ENTRY_WIDTH,
                                         font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                         placeholder_text="Repeat Password: ",
                                         show="*")
        self.addVaultReEnterPassEntry.pack(pady=PADDING_CHECKBOX)

        # Add vault button
        self.addVaultButton = ctk.CTkButton(master=self.frameAddVault,
                                               text="Create new Vault",
                                               text_color=BUTTON_TEXT_COLOR,
                                               font=(FONT_NAME, FONT_SIZE_BUTTONS),
                                               width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                               fg_color=BUTTON_COLOR, hover_color=BUTTON_COLOR_ON_HOVER,
                                               corner_radius=5,
                                               image=self.addVaultIMG,
                                               command=self.addVault)
        self.addVaultButton.pack(padx=PADDING_TEXT, pady=(PADDING_TEXT, 30))

    def entry_on_click(self, event):
        if event.char.isdigit():
            return "break"
        
    def addVault(self):
        # Take data from the entries
        vault_name = self.addVaultNameEntry.get()
        vault_pass = self.addVaultPassEntry.get()
        vault_repeat_pass = self.addVaultReEnterPassEntry.get()

        if not (vault_name and vault_pass):
            self.errorLabelGenerator.configure(text="Please enter both\nname and password\nto the vault.")
            self.addVaultNameEntry.delete(0, "end")
            self.addVaultPassEntry.delete(0, "end")
            return
        
        if vault_pass != vault_repeat_pass:
            self.errorLabelGenerator.configure(text="The passwords\ndon't match")
            self.addVaultNameEntry.delete(0,"end")
            self.addVaultPassEntry.delete(0, "end")
            self.addVaultReEnterPassEntry.delete(0, "end")
            return
        
        # Check for any existing vault name like that
        all_vaults = database.get_all_vaults()
        if database.show_name(vault_name) in all_vaults:
            self.errorLabelGenerator.configure(text="This vault\nalready exist.")
            self.addVaultNameEntry.delete(0, "end")
            self.addVaultPassEntry.delete(0, "end")
            self.addVaultReEnterPassEntry.delete(0, "end")
            return
        
        # Create the table with the  in the database
        database.create_vault(vault_name, vault_pass)
        self.errorLabelGenerator.configure(text=f"{vault_name} vault has been\nadded succefully.")
        
        
        new_vault_list = database.get_all_vaults()
        self.seeVaultComboBox.configure(values=new_vault_list)
        self.saveVaultComboBox.configure(values=new_vault_list)
        self.deleteVaultComboBox.configure(values=new_vault_list)

        self.addVaultNameEntry.delete(0, "end")
        self.addVaultPassEntry.delete(0, "end")
        self.addVaultReEnterPassEntry.delete(0, "end")

    # Delete vaults
    def deleteVaultSection(self):
        # Main frame 
        self.frameDelete = ctk.CTkFrame(master=self.deleteVaultTab, corner_radius=0, 
                                        fg_color=SEE_COLOR)
        self.frameDelete.pack(fill="both", expand=True)

        # Combobox for vault selection
        vaults = database.get_all_vaults()
        self.deleteVaultComboBox = ctk.CTkComboBox(master=self.frameDelete,
                                                    values=vaults,
                                                    width=ADD_ENTRY_WIDTH, height=DELETE_COMBOBOX_SIZE[1],
                                                    font=(FONT_NAME, FONT_SIZE_LABELS),
                                                    dropdown_fg_color=BUTTON_COLOR,
                                                    dropdown_font=(FONT_NAME, FONT_SIZE_COMBOBOX),
                                                    button_color=BUTTON_COLOR,
                                                    border_color=BUTTON_COLOR,
                                                    button_hover_color=BUTTON_COLOR_ON_HOVER,
                                                    state="readonly")
        self.deleteVaultComboBox.pack(pady=(40,PADDING_TEXT))

        # Secret Password entry
        self.deletePasswordEntry = ctk.CTkEntry(master=self.frameDelete,
                                                width=ADD_ENTRY_WIDTH,
                                                font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                                placeholder_text="Secret Password of the vault: ",
                                                show="*")
        self.deletePasswordEntry.pack(padx=PADDING_TEXT)

        # Delete button
        self.deleteVaultButton = ctk.CTkButton(master=self.frameDelete,
                                               text="Delete Vault", 
                                               font=(FONT_NAME, FONT_SIZE_BUTTONS),
                                               text_color=BUTTON_TEXT_COLOR,
                                               image=self.deleteVaultIMG,
                                               fg_color=BUTTON_COLOR, hover_color=BUTTON_COLOR_ON_HOVER,
                                               width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                               command=self.deleteVault)
        self.deleteVaultButton.pack(pady=PADDING_TEXT)

    def deleteVault(self):
        selected_vault = database.db_name(self.deleteVaultComboBox.get())
        vault_pass = self.deletePasswordEntry.get()

        # Empty entry check
        if not (vault_pass and selected_vault):
            self.errorLabelGenerator.configure(text="Please select\na vault to delete.")
            return
        
        # Correct vault password check:
        is_correct_pass = database.is_correct_vault_pass(selected_vault, vault_pass)
        if not is_correct_pass: 
            self.errorLabelGenerator.configure(text="Wrong vault password\nPlease try again.")
            self.deletePasswordEntry.delete(0, "end")
            return
        
        # Deleting:
        database.drop_vault(selected_vault)
        self.deletePasswordEntry.delete(0, "end")
        self.errorLabelGenerator.configure(text=f"The {selected_vault}\nvault has been\nsuccefully deleted")

        # Reset the GUI entries and boxes
        self.deleteVaultComboBox.set("")
        self.deleteVaultComboBox.configure(values=database.get_all_vaults())
        self.seeVaultComboBox.configure(values=database.get_all_vaults())
        self.saveVaultComboBox.configure(values=database.get_all_vaults())

class VaultPopUp(ctk.CTk):

    def __init__(self, vault_name, vault_pass):
        super().__init__()
        self.name = vault_name
        self.password = vault_pass
        self.resizable(False,False)
        self.title(f"{vault_name} Vault")
        self.iconbitmap(APP_ICON)

        # Main frame
        self.frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.frame.pack(expand=True, fill="both")
        
        # Images
        self.generatorIMG = ctk.CTkImage(dark_image=Image.open(GENERATOR_BUTTON_IMG),
                                         light_image=Image.open(GENERATOR_BUTTON_IMG),
                                         size=BUTTON_SIZE)
        
        # Copy Button Image
        self.clipboardIMG = ctk.CTkImage(dark_image=Image.open(COPY_BUTTON_IMG),
                                    light_image=Image.open(COPY_BUTTON_IMG),
                                    size=BUTTON_SIZE)
        
        # Save button Image
        self.saveIMG = ctk.CTkImage(dark_image=Image.open(SAVE_IMG),
                                    light_image=Image.open(SAVE_IMG),
                                    size=BUTTON_SIZE)
        
        # Add vault button IMG
        self.addVaultIMG = ctk.CTkImage(dark_image=Image.open(ADD_VAULT_IMG),
                                        light_image=Image.open(ADD_VAULT_IMG),
                                        size=BUTTON_MEDIUM_SIZE)
        
        # Enter vault button IMG
        self.enterVaultIMG = ctk.CTkImage(dark_image=Image.open(ENTER_VAULT_IMG),
                                        light_image=Image.open(ENTER_VAULT_IMG),
                                        size=BUTTON_SIZE)
        
        # See password button IMG
        self.showPassIMG = ctk.CTkImage(dark_image=Image.open(SEE_PASSWORD_IMG),
                                       light_image=Image.open(SEE_PASSWORD_IMG),
                                       size=BUTTON_SIZE)
        
        # Hide password button IMG
        self.hidePassIMG = ctk.CTkImage(dark_image=Image.open(HIDE_PASSWORD_IMG),
                                       light_image=Image.open(HIDE_PASSWORD_IMG),
                                       size=BUTTON_SIZE)
        
        # Delete password button IMG
        self.deletePassIMG = ctk.CTkImage(dark_image=Image.open(TRASH_CAN_IMG),
                                       light_image=Image.open(TRASH_CAN_IMG),
                                       size=BUTTON_SIZE)

        self.tableSection()
        self.editVaultSection()

    # Defines the table section
    def tableSection(self):
        # Table style 
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])
        
        # Password table for the vault showing
        heading_names = ("Username/Email", "Password", "Service")
        
        self.frametable = ctk.CTkFrame(master=self.frame)
        self.frametable.pack(expand=True)

        self.table = ttk.Treeview(master=self.frametable)
        self.table.pack(padx=10, pady=10)
        self.table["columns"] = heading_names 
        
        # Format the columns
        self.table.column("#0", width=0, stretch="NO")
        self.table.column(heading_names[0], width=150)
        self.table.column(heading_names[1], width=150)
        self.table.column(heading_names[2], width=200)

        #Format the headings
        self.table.heading("#0", text="", anchor="w")
        self.table.heading(heading_names[0], text=heading_names[0], anchor="w", command= lambda: self.sort_column(heading_names[0], False))
        self.table.heading(heading_names[1], text=heading_names[1], anchor="w", command= lambda: self.sort_column(heading_names[1], False))
        self.table.heading(heading_names[2], text=heading_names[2], anchor="w", command= lambda: self.sort_column(heading_names[2], False))

        self.tableFill()

    def tableFill(self):
        '''Fills up the table with the passwords of the user'''
        if not self.name:
            self.errorLabelGenerator.configure(text="Please select a\nvault to reveal")
            return 
        
        vault = database.get_vault_accounts(self.name, self.password)
        for element in vault:
            self.table.insert("", "end", value=element)

    def sort_column(self, column, reverse):
        '''Sorts the content of the column when heading is pressed'''
        data = [(self.table.set(child, column), child) for child in self.table.get_children("")]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            self.table.move(child, "", index)

        self.table.heading(column, command=lambda: self.sort_column(column, not reverse))
    
    # Edit section of the password
    def editVaultSection(self):

        # Main frame
        self.frameEdit = ctk.CTkFrame(master=self.frame)
        self.frameEdit.pack()
        
        # Delete selected password button
        self.deleteAccountButton = ctk.CTkButton(master=self.frameEdit, 
                                                 text="Delete Account",
                                                 image=self.deletePassIMG,
                                                 fg_color=BUTTON_COLOR,
                                                 hover_color=BUTTON_COLOR_ON_HOVER,
                                                 font=(FONT_NAME, FONT_SIZE_BUTTONS),
                                                 command=self.deleteAccount)
        self.deleteAccountButton.pack()

        # Copy password button

    def deleteAccount(self):
        vault_name = self.name
        vault_pass = self.password
        try:
            selected_ID = self.table.selection()[0]
        except IndexError:
            return
        
        # Does the delete process
        selected_row = self.table.item(selected_ID)["values"]
        selected_row = [str(x) for x in selected_row] # Makes sure every item in the list is a string

        deleted = database.delete_account(vault_name, vault_pass, selected_row)

        # Error messages
        account_not_found_error_msg = f"Account not found.\nPlease try again"
        account_not_deleted = f"Something went wrong please try again."
        account_deleted_successfully = f"Account deleted successfully"

        if deleted == "Account not in db": 
            messagebox.showerror(account_not_found_error_msg)
        elif deleted == "Not deleted. Something went wrong":
            messagebox.showerror(account_not_deleted)
        elif deleted == "Deleted":
            messagebox.showinfo(account_deleted_successfully)


        self.refresh_table()

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        self.tableFill()

if __name__ == '__main__':
    # app = MainApp()
    app = VaultPopUp("Test", "1234")
    app.mainloop()