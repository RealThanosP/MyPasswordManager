import customtkinter as ctk
from PIL import Image

#Constants
# Window
WIN_WIDTH = 600
WIN_HEIGHT = 500

# Paths
GENERATOR_BUTTON_IMG = "Images/refresh.png"
COPY_BUTTON_IMG = "Images/copy.png"
APP_ICON = "Images/lock_icon.ico"

# Sizes
BUTTON_SIZE = (25,25)

#Fonts and colors
BUTTON_COLOR = "#333333"

FONT_NAME = "Segui UI"

FONT_SIZE_BUTTONS = 15
FONT_SIZE_ENTRIES = 17
FONT_SIZE_TITLES = 24


class MainApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.iconbitmap(APP_ICON)
        self.resizable(False, False)

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
        self.generatorSection()
    def generatorSection(self):
        
        # Generator Section frame
        self.frameGenerator = ctk.CTkFrame(master=self.frame,
                                           corner_radius=0)

        #Title label for generator
        self.generatorLabel = ctk.CTkLabel(master=self.frameGenerator,
                                           text="Your Password is:",
                                           font=(FONT_NAME, FONT_SIZE_TITLES))
        self.generatorLabel.grid(row=0, column=0, columnspan=3)
        #Password entrybox
        self.generatorEntry = ctk.CTkEntry(master=self.frameGenerator,
                                           width=WIN_WIDTH-3*BUTTON_SIZE[0],
                                           corner_radius=0)
        self.generatorEntry.grid(row=1, column=0)

        # Copy Button
        self.copyButton = ctk.CTkButton(master=self.frameGenerator,
                                        image=self.clipboardIMG,
                                        width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                        text="",
                                        fg_color=BUTTON_COLOR,
                                        corner_radius=0)
        self.copyButton.grid(row=1, column=1)

        # Generator Button
        self.generatorButton = ctk.CTkButton(master=self.frameGenerator,
                                             image=self.generatorIMG,
                                             text="",
                                             width=BUTTON_SIZE[0], height=BUTTON_SIZE[1],
                                             fg_color=BUTTON_COLOR,
                                             corner_radius=0)
        self.generatorButton.grid(row=1, column=2)

        self.frameGenerator.pack()
if __name__ == '__main__':
    app = MainApp()
    app.mainloop()