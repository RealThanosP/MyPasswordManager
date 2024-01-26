
import tkinter as tk
from tkinter import ttk

def on_enter(event):
    tooltip_label.place(x=event.x_root, y=event.y_root)
    tooltip_var.set("Click this button to perform a specific action.")

# Create the main window
app = tk.Tk()
app.title("Tooltip Example")

# Create a ttk.Button with a style
style = ttk.Style()
style.configure('TButton', padding=(10, 5))
action_button = ttk.Button(app, text="Click me", style='TButton')

# Create a StringVar for the tooltip text
tooltip_var = tk.StringVar()
tooltip_var.set("Hover over the button to see a tooltip.")

# Create a ttk.Label for the tooltip
tooltip_label = ttk.Label(app, textvariable=tooltip_var, background='#FFFFDD', relief='solid', borderwidth=1)

# Bind the enter and leave events to the functions
action_button.bind("<Enter>", on_enter)

action_button.pack(pady=20)

# Run the application
app.mainloop()