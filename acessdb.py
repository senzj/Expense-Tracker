import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class Expenses:
    def __init__(self, master):
        self.master = master
        self.date = datetime.datetime.today()
        self.year = tk.StringVar(value=self.date.strftime('%Y'))
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.item_month = tk.StringVar(value=self.date.strftime('%B'))
        self.entries = tk.Frame(master)
        self.entries.pack()

        self.date_year = tk.Entry(self.entries, textvariable=self.year, relief=tk.SUNKEN, width=10)
        self.date_year.grid(row=1, column=2, sticky=tk.W)

        self.date_month = ttk.Combobox(self.entries, textvariable=self.item_month, values=self.months, width=10)
        self.date_month.grid(row=1, column=1, pady=10, sticky=tk.W)

        self.conn = None
        self.cur = None
        self.connect_to_db()

    def connect_to_db(self):
        if self.conn:
            self.conn.close()  # close previous connection if it exists

        db_name = f"{self.year.get()}.db"
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

        # Here you can add code to handle the case where the database does not exist

root = tk.Tk()
app = Expenses(root)
root.mainloop()
