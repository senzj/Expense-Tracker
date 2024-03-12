import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkinter import messagebox
import os

# date = datetime.today()
# year = date.strftime('%Y')

# db_name = f"{year}.db"

# conn = sqlite3.connect(db_name)
# cur = conn.cursor()
    
class Expense:
    def __init__(self, window):
        #declarations
        self.window = window
        
        self.date = datetime.today()
        self.item_date = StringVar()
        self.item_month = StringVar()
        self.item_day = StringVar()
        self.item_year = StringVar()
        self.item_qty = tk.IntVar()
        self.item_ctgy = tk.StringVar()
        self.item_name = tk.StringVar()
        self.item_prc = tk.DoubleVar()
        self.display_m = tk.StringVar()
        self.display_d = tk.StringVar()
        self.display_y = tk.StringVar()
        self.display_c = tk.StringVar()
        self.total_expenses = tk.DoubleVar()
        self.total_month_expenses = tk.DoubleVar()
        self.display_yr_entry = tk.StringVar()
        self.delete_name = StringVar()
        self.delete_m = StringVar()
        self.delete_y = StringVar()
        self.delete_d = StringVar()
        self.catgs = [ 'Cash', 'GCash', 'Cheque', 'Others',]
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.days = [str(i) for i in range(1, 32)]
        self.table_name = "expenses"

        self.dbname = StringVar()
        self.conn = None
        self.cur = None
        self.connect_to_db(self.dbname)

        

        #Item Entry
        entries = LabelFrame(self.window, bd=10, relief=GROOVE, text="Item Entry", font=("times new roman", 20, "bold"), fg="black", bg="sky blue")
        entries.place(x=453, y=1, width=345, height=250)

        date_label = tk.Label(entries, text="Date ", bg="sky blue").grid(row=1,column=0, pady=10, sticky="e")
        
        date_month = ttk.Combobox(entries, textvariable = self.item_month, values=self.months, width=10)
        date_month.grid(row=1, column=1, pady=10,sticky=W)
        date_month.insert(0, self.date.strftime('%B'))
        
        date_day = ttk.Combobox(entries, textvariable = self.item_day, values=self.days, width=3)
        date_day.grid(row=1, column=1,sticky=E)
        date_day.insert(0, self.date.strftime('%d'))
        
        date_year = tk.Entry(entries, textvariable = self.item_year, relief=SUNKEN, width=10)
        date_year.insert(0, self.date.strftime('%Y'))
        date_year.grid(row=1, column=2,sticky=W)
        
        self.item_date = f"{self.item_month.get()} {self.item_day.get()}, {self.item_year.get()}"
        

        qnty_label = tk.Label(entries, text="Item Quantity", bg="sky blue").grid(row=2, column=0, sticky="w")
        qnty_entry = tk.Spinbox(entries, textvariable = self.item_qty,from_=1, to=9999, width=18, relief=SUNKEN).grid(row=2, column=1,pady=4)

        ctgy_label = tk.Label(entries, text="Payment Method", bg="sky blue").grid(row=3,column=0, sticky="w")
        ctgy_entry = ttk.Combobox(entries, textvariable = self.item_ctgy, width=17, values=self.catgs)
        ctgy_entry.grid(row=3,column=1,pady=4)
        ctgy_entry.insert(0, "Cash")

        item_label = tk.Label(entries, text="Item Name", bg="sky blue").grid(row=4,column=0, sticky="w")
        item_entry = tk.Entry(entries, textvariable = self.item_name, relief=SUNKEN).grid(row=4,column=1,pady=4)

        prc_label = tk.Label(entries, text="Item Price", bg="sky blue").grid(row=5,column=0, sticky="w")
        prc_entry = tk.Entry(entries, textvariable = self.item_prc, relief=SUNKEN).grid(row=5, column=1)

        #add more items
        add_btn = tk.Button(entries, text="Add Item", command=self.add_item, width=11).grid(row=6,column=2, sticky=E, padx=5)
        display_btn = tk.Button(entries, text="Display All", command=self.display_item, width=11).grid(row=7,column=2, sticky=E, padx=5)


        #display list of items by month
        display_chng = LabelFrame(self.window, bd=10, relief=GROOVE, text="Display Specified Items", font=("times new roman", 20, "bold"), fg="black", bg="sky blue")
        display_chng.place(x=453, y=250, width=345, height=140)

        display_c_label = tk.Label(display_chng, text="Category(Optional)", bg="sky blue").grid(row=1, column=1, sticky=W)
        display_c_entry = ttk.Combobox(display_chng, textvariable = self.display_c, width=17, values = self.catgs).grid(row=1, column=2, sticky=E)
        
        display_m_label = tk.Label(display_chng, text="Month", bg="sky blue").grid(row=2, column=1, sticky=W)
        display_m_entry = ttk.Combobox(display_chng, textvariable = self.display_m, width=17, values = self.months)
        display_m_entry.grid(row=2, column=2, sticky=E)
        display_m_entry.insert(0, self.date.strftime('%B'))
        
        display_d_label = tk.Label(display_chng, text="Day (Optional)", bg="sky blue").grid(row=3, column=1, sticky=W)
        display_d_entry = ttk.Combobox(display_chng, textvariable = self.display_d, width=17, values = self.days)
        display_d_entry.grid(row=3, column=2, sticky=E)
        
        display_yr_label = tk.Label(display_chng, text="Year", bg="sky blue").grid(row=4, column=1, sticky=W)
        display_yr_entry = tk.Entry(display_chng, textvariable = self.display_y)
        display_yr_entry.grid(row=4, column=2, sticky=E)
        display_yr_entry.insert(0, self.date.strftime('%Y'))
        
        display_btn = tk.Button(display_chng, text="Show", command=self.display_specified, width=10).grid(row=4,column=3, sticky=E, padx=5)
        
        
        #delete an item from database specified by name and date including month day year
        delete = LabelFrame(self.window, bd=10, relief=GROOVE, text="Delete Item", font=("times new roman", 20,"bold"), fg="black", bg="sky blue")
        delete.place(x=453, y=391, width=345, height=210)

        delete_item_label = tk.Label(delete, text="Enter an Item", bg="sky blue").grid(row=1, column=1, sticky=W)
        delete_item_entry = tk.Entry(delete, textvariable=self.delete_name).grid(row=1, column=2, sticky=W, pady=4)
        
        delete_m_label = tk.Label(delete, text="Enter Month", bg="sky blue").grid(row=2, column=1, sticky=W)
        delete_m_entry = ttk.Combobox(delete, textvariable = self.delete_m, values=self.months, width=17)
        delete_m_entry.grid(row=2, column=2, sticky=E)
        delete_m_entry.insert(0, self.date.strftime('%B'))
        
        delete_y_label = tk.Label(delete, text="Enter Day", bg="sky blue").grid(row=3, column=1, sticky=W)
        delete_d_entry = ttk.Combobox(delete, textvariable = self.delete_d, values=self.days, width=17)
        delete_d_entry.grid(row=3, column=2,sticky=E)
        delete_d_entry.insert(0, self.date.strftime('%d'))
        
        delete_y_label = tk.Label(delete, text="Enter Year", bg="sky blue").grid(row=4, column=1, sticky=W)
        delete_y_entry = tk.Entry(delete, textvariable=self.delete_y)
        delete_y_entry.grid(row=4, column=2, sticky=E)
        delete_y_entry.insert(0, self.date.strftime('%Y'))
        
        display_btn = tk.Button(delete, text="Delete Item", command=self.delete_item, width=15).grid(row=4,column=3, sticky=E, padx=5)
        #clearing input field
        clr_btn = tk.Button(delete, text="Clear Entries", command=self.clear_item, width=15).grid(row=5,column=3, sticky=E, padx=5)
        #refresh
        display_btn = tk.Button(delete, text="Refresh List", command=self.display_specified, width=15).grid(row=6,column=3, sticky=E, padx=5)
    
    
        #display items list area + by months and year
        #frame
        display = LabelFrame(self.window, bd=10, relief=GROOVE, text="Expenses List", font=("times new roman", 20,"bold"), fg="black", bg="sky blue")
        display.place(x=3, y=1, width=450, height=600)
        
        #display
        display = LabelFrame(window, bd=10, relief=GROOVE)
        display.place(x=20, y=40, width=410, height=535)
        bill_title=Label(display, text="Your List of Expenses", font="arial 15 bold", bd=7, relief=GROOVE).pack(fill=X)

        scrol_y = Scrollbar(display, orient=VERTICAL) 
        self.txtarea = Text(display, yscrollcommand=scrol_y.set)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)

#================================================================================================================================
#creating db by year input

    # def connect_to_db(self, dbname):
    #     if self.conn:
    #         self.conn.close()  # close previous connection if it exists

    #     db_name = f"{dbname}.db"
    #     # db_name = f"2024.db"
    #     self.conn = sqlite3.connect(db_name)
    #     self.cur = self.conn.cursor()
        
    #     # Here you can add code to handle the case where the database does not exist
    #     if not os.path.exists(db_name):
    #         print(f"Creating Database {db_name}...")
    #         print(f"Creating table {self.table_name}...")
    #         query = f'''CREATE TABLE IF NOT EXISTS "{self.table_name}" (
    #                     date TEXT,
    #                     quantity INTEGER,
    #                     category TEXT,
    #                     name TEXT,
    #                     price REAL
    #                     )'''

    #         # Execute the query
    #         self.cur.execute(query)
    #     else:
    #         print(f"Database {db_name} already exist")
    #         print(f"The table {self.table_name} already exists.")

#================================================================================================================================

    def add_item(self):
        date = f"{self.item_month.get()} {self.item_day.get()}, {self.item_year.get()}"
        date_month = f"{self.item_month.get()}"
        date_day = f"{self.item_day.get()}"
        date_year = f"{self.item_year.get()}"
        num = self.item_qty.get()
        ctgy = self.item_ctgy.get()
        name = self.item_name.get()
        prc = self.item_prc.get()
        today = datetime.today()
        table_name = self.table_name
        self.connect_to_db(date_year)

        if num == 0 or num < 0:
            messagebox.showerror("Invalid Quantity", "Please Enter a Valid Item Quantity.")
        elif date == "" or date_month == "" or date_day == "" or date_year == "" or date == " " or date_month == " "  or date_day == " " or date_year == " ":
            messagebox.showerror("Invalid Date", "Please Enter a Valid Date")
        elif ctgy == "" or ctgy == " ":
            messagebox.showerror("Invalid Category", "Please Enter a Valid Category")
        elif name == "" or name == " ":
            messagebox.showerror("Invalid Item", "Please Enter a Valid Item.")
        elif prc == 0 or prc < 0 or prc == "" or prc == " ":
            messagebox.showerror("Invalid Price", "Please Enter a Valid Item Price.")
        else:
            #db data transfer debugging
            print("\nAdding item details...")
            print(f"Date: {date}")
            print(f"Quantity: {num}")
            print(f"Item name: {name}")
            print(f"Price: {prc}")
            print(f"Payment Method: {ctgy}")
            

            query = f'INSERT INTO "{table_name}" (date, quantity, category, name, price) VALUES (?, ?, ?, ?, ?)'
            self.cur.execute(query, (date, num, ctgy ,name, prc))
            self.conn.commit()
            messagebox.showinfo('Success', 'Item added successfully!')
            
            self.item_qty.set("1")
            self.item_ctgy.set("")
            self.item_name.set("")
            self.item_prc.set("")
            self.item_day.set(today.day)
            self.item_month.set(today.strftime('%B'))
            self.item_year.set(today.year)

#================================================================================================================================
        
    def display_item(self):
        self.txtarea.delete('1.0',END)
        self.header()
        self.cur.execute("""SELECT * FROM expenses""")
        expenses = self.cur.fetchall()

        self.cur.execute("""SELECT date, SUM(price) FROM expenses""")
        self.total_expenses = self.cur.fetchone()

        # Group expenses by month and date
        expenses_by_month_and_date = {}
        for expense in expenses:
            date = expense[1]
            month = date.split(' ')[0]
            if month not in expenses_by_month_and_date:
                expenses_by_month_and_date[month] = {}
            if date not in expenses_by_month_and_date[month]:
                expenses_by_month_and_date[month][date] = []
            expenses_by_month_and_date[month][date].append(expense)

        # Create a dictionary to convert month names to numbers
        month_converter = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

        # Sort months and dates in ascending order
        sorted_months = sorted(expenses_by_month_and_date.keys(), key=lambda x: month_converter[x])
        for month in sorted_months:
            sorted_dates = sorted(expenses_by_month_and_date[month].keys(), key=lambda x: datetime.strptime(x.strip(), '%B %d, %Y'))

            # Display expenses grouped by month and date
            for date in sorted_dates:
                expenses = expenses_by_month_and_date[month][date]
                self.txtarea.insert(END, f"{date} \n")
                for expense in expenses:
                    self.txtarea.insert(END, f">[{expense[3]}]\n  ~ {expense[2]}x {expense[4]}\t\t\t\t- ₱{expense[5]}\n")
                self.txtarea.insert(END, f"\n")

        self.txtarea.insert(END, f"\n------------------------------------------\n")
        self.txtarea.insert(END, f"Total Monthly expenses \t\t\t\t= ₱{self.total_expenses[1]}\n")

#================================================================================================================================

    def display_specified(self):
        self.txtarea.delete('1.0', END)
        month = self.display_m.get()
        year = self.display_y.get()
        day = self.display_d.get()
        category = self.display_c.get()

        if month == "" or month == " ":
            messagebox.showerror("Invalid Month", "Please Enter a Valid Month (E.G. June, July, March, April).")
        elif year == "" or year == " ":
            messagebox.showerror("Invalid Year", "Please Enter a Valid Year (E.G. 2020).")
        else:
            if day == "" or day == " ":
                if category == "" or category == " ":
                    self.header_month()
                    self.cur.execute("""SELECT * FROM expenses WHERE date LIKE ?""", (f'%{month}%, {year}',))
                    expenses = self.cur.fetchall()

                    self.cur.execute("""SELECT date, SUM(price) FROM expenses WHERE date LIKE ?""", (f'%{month}%, {year}',))
                    self.total_expenses = self.cur.fetchone()
                else:
                    self.header_ctgy()
                    self.cur.execute("""SELECT * FROM expenses WHERE date LIKE ? AND category = ?""", (f'%{month}%, {year}', category))
                    expenses = self.cur.fetchall()

                    self.cur.execute("""SELECT date, SUM(price) FROM expenses WHERE date LIKE ? AND category = ?""", (f'%{month}%, {year}', category))
                    self.total_expenses = self.cur.fetchone()
            else:
                if category == "" or category == " ":
                    self.header_month()
                    self.cur.execute("""SELECT * FROM expenses WHERE date LIKE ?""", (f'%{month} {day}, {year}',))
                    expenses = self.cur.fetchall()

                    self.cur.execute("""SELECT date, SUM(price) FROM expenses WHERE date LIKE ?""", (f'%{month} {day}, {year}',))
                    self.total_expenses = self.cur.fetchone()
                else:
                    self.header_ctgy()
                    self.cur.execute("""SELECT * FROM expenses WHERE date LIKE ? AND category = ?""", (f'%{month} {day}, {year}', category))
                    expenses = self.cur.fetchall()

                    self.cur.execute("""SELECT date, SUM(price) FROM expenses WHERE date LIKE ? AND category = ?""", (f'%{month} {day}, {year}', category))
                    self.total_expenses = self.cur.fetchone()

            # Group expenses by date
            expenses_by_date = {}
            for expense in expenses:
                date = expense[1]
                if date not in expenses_by_date:
                    expenses_by_date[date] = []
                expenses_by_date[date].append(expense)

            # Sort dates in ascending order
            sorted_dates = sorted(expenses_by_date.keys(), key=lambda x: datetime.strptime(x.strip(), '%B %d, %Y'))

            # Display expenses grouped by date
            for date in sorted_dates:
                expenses = expenses_by_date[date]
                self.txtarea.insert(END, f"{date} \n")
                for expense in expenses:
                    #expense[0] - key ID
                    #expense[1] - date
                    #expense[2] - qty
                    #expense[3] - category
                    #expense[4] - item name
                    #expense[5] - price
                    self.txtarea.insert(END, f">[{expense[3]}]\n  ~ {expense[2]}x {expense[4]}\t\t\t\t- ₱{expense[5]}\n")
                self.txtarea.insert(END, f"\n")

            if day == "" or day == " ":
                self.txtarea.insert(END, f"\n------------------------------------------\n")
                self.txtarea.insert(END, f"Total Expenses for {month}\t\t\t\t= ₱{self.total_expenses[1]}\n")
            else:
                self.txtarea.insert(END, f"\n------------------------------------------\n")
                self.txtarea.insert(END, f"Total Expenses for {month} {day}\t\t\t\t= ₱{self.total_expenses[1]}\n")
        self.display_c.set("")

#================================================================================================================================
               
    def delete_item(self):
        name = self.delete_name.get()
        month = self.delete_m.get()
        day = self.delete_d.get()
        year = self.delete_y.get()
        today_delete = datetime.today()
        date = f"{month} {day}, {year}"
        if name == "" or name == " ":
            alertm = messagebox.showerror("Invalid Item", "Kindly Enter a Valid Item.")
        elif month == "" or month == " ":
            alertm = messagebox.showerror("Invalid Month", "Kindly Enter a Valid Month.")
        elif day == "" or day == " ":
            alertd = messagebox.showerror("Invalid Date","Kindly Enter a Valid Day.")
        elif year == "" or year == " ":
            alerty = messagebox.showerror("Invalid Year", "Kindly Enter a Valid Year.")
        else:
            q = messagebox.askyesno("Deleting an Item...", "Do you want to Delete This Item?")
            if q > 0:
                print(name)
                print(date)
                self.cur.execute('DELETE FROM expenses WHERE name = ? AND date = ?', (name, date))
                self.conn.commit()
                messagebox.showinfo('Success', 'Item deleted successfully!')
                self.delete_name.set("")
                self.delete_d.set(today_delete.day)
                self.delete_m.set(today_delete.strftime('%B'))
                self.delete_y.set(today_delete.year)

#================================================================================================================================
        
    def clear_item(self):
        op = messagebox.askyesno("Clearing input fields..","Do you want to Clear Everything?")
        if op > 0:
            self.item_qty.set("1")
            self.item_ctgy.set("")
            self.item_name.set("")
            self.item_prc.set("")
            self.delete_name.set("")
            self.display_m.set("")
            self.delete_m.set("")
            self.delete_d.set("")
            self.txtarea.delete('1.0',END)
        else:
            return

#================================================================================================================================  
        
    def header(self):
        width = 44
        self.txtarea.insert(END, f"{'=' * width}\n")
        self.txtarea.insert(END, f"{f'| Over All Expense List |'.center(width, '=')}\n")
        self.txtarea.insert(END, f"{'=' * width}\n")

#================================================================================================================================
        
    def header_month(self):
        month = self.display_m.get()
        category = self.display_c.get()
        width = 44
        self.txtarea.insert(END, f"{'=' * width}\n")
        self.txtarea.insert(END, f"{f'| {month} Expense List |'.center(width, '=')}\n")
        self.txtarea.insert(END, f"{'=' * width}\n")

#================================================================================================================================
        
    def header_ctgy(self):
        month = self.display_m.get()
        category = self.display_c.get()
        width = 44
        self.txtarea.insert(END, f"{'=' * width}\n")
        self.txtarea.insert(END, f"{f'| {month} Expense List |'.center(width, '=')}\n")
        self.txtarea.insert(END, f"{f' For {category} '.center(width, ' ')}\n")
        self.txtarea.insert(END, f"{'=' * width}\n")
    
#================================================================================================================================


global window
window = Tk()
window.geometry("800x600+200+80")
window.title("Expenses List v3.0")

#================================================================================================================================

def main():
    expense = Expense(window)
    window.mainloop()

if __name__ == "__main__":
    main()