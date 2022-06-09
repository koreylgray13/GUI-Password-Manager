from tkinter import *
from PIL import ImageTk, Image
import sqlite3


root = Tk()
root.title('Password Manager')
root.geometry('400x400')

# Create Database
conn = sqlite3.connect('passwords.db')

# Create Cursor
c = conn.cursor()

# Create Table
c.execute("""CREATE TABLE passwords (
        name text, 
        username text,
        password text, 
        category text
        )""")

# Commit Changes
conn.commit()

# Close Connection
conn.close()

# Open GUI
root.mainloop()
