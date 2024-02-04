import tkinter as tk
from tkinter import ttk
import customtkinter as ctk 
import database

class VaultPopUp(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        # Main frame
        self.frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.frame.pack(expand=True, fill="both")
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
        heading_names = ("Username/Email", "Password", "Service", "Note")
        
        self.frameSeeTable = ctk.CTkFrame(master=self.frame)
        self.frameSeeTable.pack()

        self.seeTable = ttk.Treeview(master=self.frameSeeTable)
        self.seeTable["columns"] = heading_names 
        
        # Format the columns
        self.seeTable.column("#0", width=0, stretch="NO")
        self.seeTable.column(heading_names[0], width=120)
        self.seeTable.column(heading_names[1], width=120)
        self.seeTable.column(heading_names[2], width=80)
        self.seeTable.column(heading_names[3], width=130)

        #Format the headings
        self.seeTable.heading("#0", text="", anchor="w")
        self.seeTable.heading(heading_names[0], text=heading_names[0], anchor="w")
        self.seeTable.heading(heading_names[1], text=heading_names[1], anchor="w")
        self.seeTable.heading(heading_names[2], text=heading_names[2], anchor="w")
        self.seeTable.heading(heading_names[3], text=heading_names[3], anchor="w")

        self.seeTableFill
        self.seeTable.pack(side="right")
    
    def seeTableFill(self):
        selected_vault = self.seeVaultComboBox.get()
        if not selected_vault:
            self.errorLabelGenerator.configure(text="Please select a\nvault to reveal")
            return 
        
        vault = database.get_vault(selected_vault)
        for element in vault:
            self.seeTable.insert("", "end", value=element)

if __name__ == '__main__':
    app = VaultPopUp()
    app.mainloop()