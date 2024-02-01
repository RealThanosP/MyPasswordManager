import customtkinter as ctk
from PIL import Image
from PassGen import PassGenerator
import pyperclip
import encryption
import database
#Constants
# Window
WIN_WIDTH = 600
WIN_HEIGHT = 550

# Paths
GENERATOR_BUTTON_IMG = "Images/refresh.png"
COPY_BUTTON_IMG = "Images/copy.png"
APP_ICON = "Images/lock_icon.ico"
SAVE_IMG = "Images/save.png"

BUTTON_SIZE = (25,25)
BUTTON_BIG_SIZE = (100, 120)
# Fonts and colors
BUTTON_COLOR = "#333333"
BUTTON_TEXT_COLOR = "#AAAAAA"
BUTTON_COLOR_ON_HOVER = "#555555"
FONT_NAME = "Segui UI"

FONT_SIZE_LABELS = 15
FONT_SIZE_BUTTONS = 15
FONT_SIZE_ENTRIES = 17
FONT_SIZE_SUB_TITLES = 20
FONT_SIZE_TITLES = 24

# Paddings
PADDING_CHECKBOX = 5
PADDING_TEXT = 10
PADDING_SLIDER = 20

GENERATOR_ENTRY_WIDTH = WIN_WIDTH-4.9*BUTTON_SIZE[0]
SAVE_ENTRY_WIDTH = 250

SAVE_TEXT_BOX_HEIGHT = 100
SAVE_COMBOBOX_SIZE = (150, 30)
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
                                  width=WIN_WIDTH, height=WIN_HEIGHT,
                                  fg_color=("white", "#0F0F0F"))
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
        self.generatorSection()
        self.savePasswordSection()

    # Pass generator section ##DONE##
    def generatorSection(self):
        '''Defines the password generator UI and places it into the main frame'''
        # Generator Section frame
        self.frameGenerator = ctk.CTkFrame(master=self.frame, corner_radius=0)

        #Top frame:
        self.frameGeneratorTopBar = ctk.CTkFrame(master=self.frameGenerator, corner_radius=0)
        self.frameGeneratorTopBar.pack(fill="x")

        #Title label for generator
        self.generatorLabel = ctk.CTkLabel(master=self.frameGeneratorTopBar,
                                           text="Your Password is:",
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
        self.sliderLabel.grid(row=3, column=1, rowspan=4, padx=PADDING_SLIDER)

        #Error Label
        self.errorLabelGenerator = ctk.CTkLabel(master=self.frameGeneratorSettings, 
                                                text="",
                                                font=(FONT_NAME, FONT_SIZE_LABELS),
                                                justify="center")
        self.errorLabelGenerator.grid(row=0, column=2, sticky="e", rowspan=3)

        self.frameGenerator.pack(fill="x")
        self.frameGeneratorSettings.pack(fill="x")

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
            self.generatorProgressBar.configure(progress_color="red")
        elif pass_strongness > 5 and pass_strongness <= 10:
            self.generatorProgressBar.configure(progress_color="yellow")
        elif pass_strongness > 10  and pass_strongness <= 20:
            self.generatorProgressBar.configure(progress_color="lime")
        elif pass_strongness > 20 and pass_strongness < 30:
            self.generatorProgressBar.configure(progress_color="green")
        else:
            self.generatorProgressBar.configure(progress_color="darkgreen")

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
    def savePasswordSection(self):
        
        # Main frame
        self.frameSave = ctk.CTkFrame(master=self.frame, corner_radius=0)
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

        #Service entry:
        self.saveServiceEntry = ctk.CTkEntry(master = self.frameSave,
                                                width=SAVE_ENTRY_WIDTH,
                                                font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                                placeholder_text="Service:")
        self.saveServiceEntry.pack(pady=PADDING_TEXT, padx=PADDING_TEXT)

        # notes on the account (optional kind of intresting concept)
        self.saveNotes = ctk.CTkTextbox(master=self.frameSave,
                                        font=(FONT_NAME, FONT_SIZE_LABELS),
                                        width=SAVE_ENTRY_WIDTH, height=SAVE_TEXT_BOX_HEIGHT)
        self.saveNotes.insert(0.0, "Note: ")
        self.saveNotes.bind("<FocusIn>", lambda event: self.saveNotes.delete(0.0, "end"))
        self.saveNotes.pack()

        # Combobox with all the vaults already created
        vaults = database.get_all_vaults()
        self.saveVaultComboBox = ctk.CTkComboBox(master=self.frameSave,
                                                 values=vaults,
                                                 width=SAVE_COMBOBOX_SIZE[0], height=SAVE_COMBOBOX_SIZE[1],
                                                 font=(FONT_NAME, FONT_SIZE_LABELS),
                                                 button_color=BUTTON_COLOR,
                                                 border_color=BUTTON_COLOR,
                                                 button_hover_color=BUTTON_COLOR_ON_HOVER)
        self.saveVaultComboBox.pack(side="right")

        # Save Password button
        self.saveButton = ctk.CTkButton(master=self.frameSave,
                                        text="Save", 
                                        font=(FONT_NAME,FONT_SIZE_ENTRIES),
                                        fg_color=BUTTON_COLOR, hover_color=BUTTON_COLOR_ON_HOVER,
                                        text_color=BUTTON_TEXT_COLOR,
                                        width=BUTTON_BIG_SIZE[0], height=BUTTON_BIG_SIZE[1],
                                        image=self.saveIMG,
                                        command=self.saveAccount)
        self.saveButton.pack(pady=PADDING_TEXT)
        
    def saveAccount(self):
        '''Saves inputed account info into a database, using encryption for the data'''
        database.create_vault("Start Vault")
        
        # Takes the input from the fields
        username = self.saveUsernameEntry.get()
        password = self.savePasswordEntry.get()
        service = self.saveServiceEntry.get()
        notes = self.saveNotes.get(0.0, "end")

        element_list = [username, password, service, notes]

        # Checks for empty cells/input fields
        if not (username and password and service):
            self.errorLabelGenerator.configure(text="Please fill out all the \nfields before saving.")
            return 
        
        # Select the vault
        selected_vault = self.saveVaultComboBox.get()

        # Encryption key
        key = encryption.generate_key()

        # Encrypt the data_list with the key and store the
        # encrypted versiom into the database
        stored = database.store_account(key, selected_vault, element_list)
        already_stored_error_msg = "You have this\naccount already saved."
        success_error_msg = "You successfully\nsaved this account."

        # Checks the wanted error message based on the status of the storing
        if stored == None:
            self.errorLabelGenerator.configure(text=already_stored_error_msg)
        elif stored:
            self.errorLabelGenerator.configure(text=success_error_msg)

        # Resets the entries
        self.saveUsernameEntry.delete(0, "end")
        self.savePasswordEntry.delete(0, "end")
        self.saveServiceEntry.delete(0, "end")
        self.saveNotes.delete(0.0, "end")

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
