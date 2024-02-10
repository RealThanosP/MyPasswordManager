import tkinter as tk
from tkinter import ttk
import customtkinter as ctk 
import database


class VaultPopUp(ctk.CTk):

    def __init__(self, vault_name):
        super().__init__()
        self.name = vault_name
        self.resizable(False,False)
        self.geometry("700x600")

        # Main frame
        self.frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.frame.pack(expand=True, fill="both")

        self.tableSection()

    # Defines the table section 1145566
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
        heading_names = ("Username/Email", "Password", "Service", "Note")
        
        self.frametable = ctk.CTkFrame(master=self.frame)
        self.frametable.pack(expand=True)

        self.table = ttk.Treeview(master=self.frametable)
        self.table["columns"] = heading_names 
        
        # Format the columns
        self.table.column("#0", width=0, stretch="NO")
        self.table.column(heading_names[0], width=150)
        self.table.column(heading_names[1], width=150)
        self.table.column(heading_names[2], width=200)
        self.table.column(heading_names[3], width=200)

        #Format the headings
        self.table.heading("#0", text="", anchor="w")
        self.table.heading(heading_names[0], text=heading_names[0], anchor="w")
        self.table.heading(heading_names[1], text=heading_names[1], anchor="w")
        self.table.heading(heading_names[2], text=heading_names[2], anchor="w")
        self.table.heading(heading_names[3], text=heading_names[3], anchor="w")

        self.tableFill()
        self.table.pack(side="top")

    def tableFill(self):
        if not self.name:
            self.errorLabelGenerator.configure(text="Please select a\nvault to reveal")
            return 
        
        vault = database.get_vault(self.name)
        for element in vault:
            self.table.insert("", "end", value=element)

if __name__ == '__main__':
    app = VaultPopUp("Thanos")
    app.mainloop()