import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

#Variables 
WINDOW_GEOMETRY = "600x500"

GENERATOR_BUTTON_IMG = "Images/refresh.png"


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry(WINDOW_GEOMETRY)

        #Main frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill="both")

        #Generate password section
        self.GeneratorSection()

    def GeneratorSection(self):
        #Long frame with an entry/Text onj to show the generated password and 2 buttons(generate, copy to clipboard)
        self.frameGenerator = tk.Frame(self.frame)
        
        #Password generator title label
        self.generatorLabel = tk.Label(self.frameGenerator,
                                       text="Your Password is:",
                                       font=("Helvetica", 20))
        self.generatorLabel.pack()

        #Generator button IMG

        #Generator button
        self.generationButton = ttk.Button(self.frameGenerator,
                                          )
        #Password entry
        self.GeneratorEntry = tk.Entry(self.frameGenerator
                                            )

        self.frameGenerator.pack()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
