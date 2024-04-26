import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkinter import messagebox
import os
from tkcalendar import DateEntry
from pprint import pprint
import calendar
    
class Expense:

    #initialization
    def __init__(self, window):

        icon = PhotoImage(file="icon.png")

        # Declarations
        self.window = window
        self.window.title("Expense Tracker v4")
        self.window.iconphoto(False, icon)


        self.setup_grid()
        self.GUI_Widget()

#================================================================================================================================
    #defining variables 
    def setup_var(self):
                #debugs
        print("Starting Program...")

        self.divide = 8
        self.date = datetime.today()

        self.item_date = StringVar()
        self.item_month = StringVar()
        self.item_day = StringVar()
        self.item_year = StringVar()
        self.item_qty = tk.IntVar()
        self.item_ctgy = tk.StringVar()
        self.item_name = tk.StringVar()
        self.item_prc = tk.StringVar()

        self.display_m = tk.StringVar()
        self.display_d = tk.StringVar()
        self.display_y = tk.StringVar()
        self.display_c = tk.StringVar()

        self.total_expenses = tk.DoubleVar()
        self.total_month_expenses = tk.DoubleVar()
        self.display_yr_entry = tk.StringVar()

        self.delete_ID = StringVar()
        self.delete_year = StringVar()

        self.edit_name = StringVar()
        self.edit_cost = StringVar()
        self.edit_qty = IntVar()
        self.edit_pay = StringVar()
        self.edit_ID = StringVar()
        self.edit_year = StringVar()

        self.catgs = [ 'Cash', 'GCash', 'Cheque', 'Others',]
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.days = [f"{i:02d}" for i in range(1, 32)]
        self.select_edate = datetime.today().strftime('%B %d, %Y')
        self.select_ddate = datetime.today().strftime('%B %d, %Y')
        self.select_eedate = ""
        
        
        #database things
        self.dbname = "expenses.db"
        self.conn = None
        self.cur = None

        print("Program Ready.")


#================================================================================================================================
    
    #dynanic widget and GUI display [done]
    def GUI_Widget(self):

        dbutton_width = 12

        background = "sky blue"
        add_background = "sky blue"
        dis_background = "sky blue"
        del_background = "sky blue"

        self.setup_var()

#display expense list

        display = LabelFrame(self.window, bd=5, relief=GROOVE)
        display.grid(row=0, column=0, sticky="nsew", rowspan=5)  # Add sticky="nsew"
        bill_title = Label(display, text="List of Expenses", font="arial 15 bold", bd=7, relief=GROOVE)
        bill_title.pack(fill=X)

        scrol_y = Scrollbar(display, orient=VERTICAL)
        self.txtarea = Text(display, yscrollcommand=scrol_y.set)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)


#Adding Expense
        add_expense = LabelFrame(self.window, bd=10, relief=GROOVE, text="Add Expense", font=("times new roman", 20, "bold"), fg="black", bg="sky blue")
        add_expense.grid(row=0, column=1, sticky="nsew")

        date_label = tk.Label(add_expense, text="Date ", bg=add_background).grid(row=0,column=0, pady=5, sticky="e")
        
        self.edate_cal = DateEntry(add_expense, width=12)  # Use self.window instead of entries
        self.edate_cal.grid(row=0, column=1, pady=10, sticky="w")
        self.edate_cal.set_date(datetime.today())  # Set date
        self.edate_cal.bind("<<DateEntrySelected>>", self.update_edate)  # Bind event

        qnty_label = tk.Label(add_expense, text="Expense Quantity", bg=add_background).grid(row=2, column=0, sticky="e")
        qnty_entry = tk.Spinbox(add_expense, textvariable = self.item_qty,from_=1, to=9999, width=18, relief=SUNKEN).grid(row=2, column=1,pady=4)

        ctgy_label = tk.Label(add_expense, text="Payment Method", bg=add_background).grid(row=3,column=0, sticky="e")
        ctgy_entry = ttk.Combobox(add_expense, textvariable = self.item_ctgy, width=17, values=self.catgs)
        ctgy_entry.grid(row=3,column=1,pady=4)
        ctgy_entry.insert(0, "Cash")

        item_label = tk.Label(add_expense, text="Exepnse Name", bg=add_background).grid(row=4,column=0, sticky="e")
        item_entry = tk.Entry(add_expense, textvariable = self.item_name, relief=SUNKEN).grid(row=4,column=1,pady=4)

        prc_label = tk.Label(add_expense, text="Expense Cost", bg=add_background).grid(row=5,column=0, sticky="e")
        prc_entry = tk.Entry(add_expense, textvariable = self.item_prc, relief=SUNKEN).grid(row=5, column=1)

        #add more items
        add_btn = tk.Button(add_expense, text="Add Expense", command=self.add_expense, width=11).grid(row=5,column=2, padx=13)


#display list of items by month
        display_chng = LabelFrame(self.window, bd=10, relief=GROOVE, text="Display Expense", font=("times new roman", 20, "bold"), fg="black", bg="sky blue")
        display_chng.grid(row=1, column=1, sticky="nsew")

        display_c_label = tk.Label(display_chng, text="Category (Optional)", bg=dis_background).grid(row=1, column=0, sticky=E)
        display_c_entry = ttk.Combobox(display_chng, textvariable = self.display_c, width=17, values = self.catgs).grid(row=1, column=1, sticky=E)
        
        display_m_label = tk.Label(display_chng, text="Month", bg=dis_background).grid(row=2, column=0, sticky=E)
        display_m_entry = ttk.Combobox(display_chng, textvariable = self.display_m, width=17, values = self.months)
        display_m_entry.grid(row=2, column=1, sticky=E)
        display_m_entry.insert(0, self.date.strftime('%B'))
        
        display_d_label = tk.Label(display_chng, text="Day (Optional)", bg=dis_background).grid(row=3, column=0, sticky=E)
        display_d_entry = ttk.Combobox(display_chng, textvariable = self.display_d, width=17, values = self.days)
        display_d_entry.grid(row=3, column=1, sticky=E)
        
        display_yr_label = tk.Label(display_chng, text="Year", bg=dis_background).grid(row=4, column=0, sticky=E)
        display_yr_entry = tk.Entry(display_chng, textvariable = self.display_y)
        display_yr_entry.grid(row=4, column=1, sticky=E)
        display_yr_entry.insert(0, self.date.strftime('%Y'))
        
        display_btn = tk.Button(display_chng, text="Get", command=self.display_categorized_expenses, width=10).grid(row=3,column=2, sticky=E, padx=5)
        display_btn = tk.Button(display_chng, text="Get All", command=self.display_expenses, width=10).grid(row=4,column=2, sticky=E, padx=5)
        
        
#delete an item from database specified by name and date including month day year
        delete = LabelFrame(self.window, bd=10, relief=GROOVE, text="Delete Expense", font=("times new roman", 20,"bold"), fg="black", bg="sky blue")
        delete.grid(row=4, column=1, sticky="nsew")

        delete_expense_label = tk.Label(delete, text="Enter an Expense by ID ", bg=del_background).grid(row=0, column=0, sticky="e")
        delete_expense_entry = tk.Entry(delete, textvariable=self.delete_ID).grid(row=0, column=1, sticky="w")

        delete_expense_label = tk.Label(delete, text="Enter Expense Year ", bg=del_background).grid(row=1, column=0, sticky="e")
        delete_expense_entry = tk.Entry(delete, textvariable=self.delete_year).grid(row=1, column=1, sticky="w")
        
        # date_label = tk.Label(delete, text="Date ", bg=del_background).grid(row=1,column=1, pady=5, sticky="e")
        # self.ddate_cal = DateEntry(delete, width=12)  # Use self.window instead of entries
        # self.ddate_cal.grid(row=1, column=2, pady=5, sticky="w")
        # self.ddate_cal.set_date(datetime.today())  # Set date
        # self.ddate_cal.bind("<<DateEntrySelected>>", self.update_ddate)  # Bind event
        
        
        display_btn = tk.Button(delete, text="Delete Item", command=self.delete_expense, width=dbutton_width).grid(row=1,column=2, sticky=E, padx=5, pady=5)


#edit items from the database by entering the expense ID
        edit = LabelFrame(self.window, bd=10, relief=GROOVE, text="Edit Expense", font=("times new roman", 20,"bold"), fg="black", bg="sky blue")
        edit.grid(row=3, column=1, sticky="nsew")

        edit_label = tk.Label(edit, text="Enter Expense by ID", bg=del_background).grid(row=0, column=0, sticky="e")
        edit_entry = tk.Entry(edit, textvariable=self.edit_ID).grid(row=0, column=1, sticky="w")

        edit_label = tk.Label(edit, text="Enter Expense Year", bg=del_background).grid(row=0, column=2, sticky="e")
        edit_entry = tk.Entry(edit, textvariable=self.edit_year, width=10).grid(row=0, column=3, sticky="w")

        display_btn = tk.Button(edit, text="Search Expense", command=self.search_edit_expense, width=dbutton_width).grid(row=0,column=5, sticky="e", padx=10)

        edit_label_name = tk.Label(edit, text="Expense", bg=del_background).grid(row=2, column=0, sticky="e", pady = 2)
        edit_entry_name = tk.Entry(edit, textvariable=self.edit_name).grid(row=2, column=1, sticky="w")

        date_label = Label(edit, text="Date ", background=del_background).grid(row=1,column=0, pady=5, sticky="e")
        self.select_eedate = DateEntry(edit)  # Use DateEntry instead of Entry
        self.select_eedate.grid(row=1, column=1, pady=5, sticky="w")
        self.select_eedate.delete(0, 'end')  # Clear the DateEntry when the program starts

        edit_label_cost = tk.Label(edit, text="Expense Cost", bg=del_background).grid(row=3, column=0, sticky="e", pady = 2)
        edit_entry_cost = tk.Entry(edit, textvariable=self.edit_cost).grid(row=3, column=1, sticky="w")

        edit_label_qnty = tk.Label(edit, text="Expense Quantity", bg=del_background).grid(row=4, column=0, sticky="e", pady = 2)
        edit_entry_qnty = tk.Spinbox(edit, textvariable = self.edit_qty,from_=0, to=9999, width=18, relief=SUNKEN).grid(row=4, column=1,pady=4)

        edit_label_pay = tk.Label(edit, text="Payment Method", bg=del_background).grid(row=5, column=0, sticky="e", pady = 2)
        edit_entry_pay = ttk.Combobox(edit, textvariable = self.edit_pay, width=17, values=self.catgs).grid(row=5,column=1,pady=4)

        confirm_edit_btn = tk.Button(edit, text="Edit Expense", command=self.edit_expense, width=dbutton_width).grid(row=5, column=2, sticky=E, padx=5)


#================================================================================================================================
    
    def update_edate(self, event):
        # Get the selected date and store it in self.select_edate for add
        self.select_edate = event.widget.get_date().strftime('%B %d, %Y')

    def update_ddate(self, event):
        # Get the selected date and store it in self.select_ddate for delete
        self.select_ddate = event.widget.get_date().strftime('%B %d, %Y')

    def update_eedate(self, event):
        # Get the selected date and store it in self.select_ddate for delete
        self.select_eedate = event.widget.get_date().strftime('%B %d, %Y')

#================================================================================================================================

    # creating or checking for existing db in the directory by year [done]
    def connect_to_db(self, tablename):
        if self.conn:
            self.conn.close()  # close previous connection if it exists

        db_name = self.dbname
        table_name = tablename

        # Check if the database file exists before connecting
        if not os.path.exists(db_name):
            print(f"The Database named \"{db_name}\" doesn't exist...\n")
            print(f"Creating Database \"{db_name}\"...\n")

        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

        # Create the table if not exists
        query = f'''CREATE TABLE IF NOT EXISTS "{table_name}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                quantity INTEGER,
                category TEXT,
                name TEXT,
                price REAL
                )'''

        # Execute the query
        print(f"Attempting to create table named \"{table_name}\"...\n")
        self.cur.execute(query)

        if not os.path.exists(db_name):
            print(f"Database \"{db_name}.db\" and Table \"{table_name}\" Created Successfully!")
        else:
            print(f"Database \"{db_name}\" and Table \"{table_name}\" already exist.")

#================================================================================================================================
    
    # adding item into the (year).db database. [done]
    def add_expense(self):
        date = self.select_edate
        date_object = datetime.strptime(date, '%B %d, %Y')
        print(date)

        #breaking the date into segments
        date_year = date_object.strftime('%Y')
        date_month = date_object.strftime('%B')
        date_day = date_object.strftime('%d')


        num = self.item_qty.get()
        ctgy = self.item_ctgy.get()
        name = self.item_name.get()
        prc = self.unformat_price(self.item_prc.get())
        dbname = self.dbname
        table_name = date_year


        if self.conn is None:
            self.connect_to_db(table_name)
            print(f"Connecting to database {dbname}...")

        
        if num == 0 or num < 0:
            messagebox.showerror("Invalid Quantity", "Please Enter a Valid Item Quantity.")
        # elif date == "" or date_month == "" or date_day == "" or date_year == "" or date == " " or date_month == " "  or date_day == " " or date_year == " ":
        #     messagebox.showerror("Invalid Date", "Please Enter a Valid Date")
        elif ctgy == "" or ctgy == " " or ctgy.isnumeric():
            messagebox.showerror("Invalid Category", "Please Enter a Valid Category")
        elif name == "" or name == " ":
            messagebox.showerror("Invalid Item", "Please Enter a Valid Expense.")
        elif prc == "0" or prc < "0" or prc == "" or prc == " " or prc.isalpha():
            messagebox.showerror("Invalid Price", "Please Enter a Valid Price.")
        else:
            #db data transfer debugging
            print("\nAdding the following expense details.")
            print(f"Date: {date}")
            print(f"Expense: {name}")
            print(f"Quantity: {num}")
            print(f"Price: {prc}")
            print(f"Payment Method: {ctgy}\n")
            
            query = "INSERT INTO \"{}\" (date, quantity, category, name, price) VALUES (?, ?, ?, ?, ?)".format(table_name)
            self.cur.execute(query, (date, num, ctgy ,name, prc))
            self.conn.commit()
            messagebox.showinfo('Success', 'Item added successfully!')
            print(f"Items Added Succesfully!")
            self.display_categorized_expenses()
            
        print(f"Process Completed Succesfully!")

        # self.fields_reset()
        self.item_qty.set("1")
        self.item_name.set("")
        self.item_prc.set("")

        self.edate_cal.set_date(datetime.today())

#================================================================================================================================

    # displaying all items from the current year from (year).db [done]
    def display_expenses(self):

        #variable declation
        sum = 0

        display_width = self.txtarea.winfo_width()
        num_dashes = display_width // self.divide
        dashed_line = "-" * num_dashes
        dbname = self.dbname
        table_name = self.display_y.get()

        os.system('cls' if os.name == 'nt' else 'clear') # clear the terminal
        print(f"Displaying all Expenses from the year {table_name}...\n")
        # print(display_width)
        # print(num_dashes)
        # print(dashed_line)
        print(f"database: {dbname}")
        print(f"table: {table_name}")


        #database actions
        if self.conn is None:
            self.connect_to_db(table_name)
            print(f"Connecting to database {dbname}...")

        self.cur.execute(f'SELECT * FROM "{table_name}"')
        expenses = self.cur.fetchall()

        self.cur.execute(f'SELECT date, SUM(price) FROM "{table_name}"')
        total_expenses = self.cur.fetchone()
        

        #display area
        self.txtarea.delete('1.0',END)
        self.header()

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

            self.txtarea.tag_config("bold", font=("Courier", 13, "bold"))
            self.txtarea.insert(END, f"{date}\n", "bold")

            for expense in expenses:
                # print(expense)
                total_item_price = expense[2] * expense[5]
                sum += total_item_price
                formatted_price = self.format_price(total_item_price)

                self.txtarea.insert(END, f"[ID: {expense[0]}][Type: {expense[3]}]\n>{expense[4]}\t\t\t~{expense[2]}x ₱{expense[5]}\t\t\t    = ₱{formatted_price}\n")

                self.txtarea.insert(END, f"\n")
            self.txtarea.insert(END, f"\n")

        # Insert total monthly expenses
        total_sum = self.format_price(sum)
        self.txtarea.insert(END, f"{dashed_line}\n")
        self.txtarea.insert(END, f"Overall Total Expenses for {table_name}\t\t\t\t\t\t    = ₱{total_sum}\n")

        #analysis
        # self.compare_month(table_name)
        self.compare_year(table_name)

        # total_expenses -> (date, sum)
        
        print("displaying all item...")
        print("Item retrieved.")
            
#================================================================================================================================

    # displaying all items with specified month, day (optional), along with year to know which database to open [done]
    def display_categorized_expenses(self):
        #variable declaration
        sum = 0
        month = self.display_m.get()
        year = self.display_y.get()
        day = self.display_d.get()
        category = self.display_c.get()

        display_width = self.txtarea.winfo_width()
        num_dashes = display_width // self.divide
        dashed_line = "-" * num_dashes

        db_name = self.dbname
        table_name = year

        os.system('cls' if os.name == 'nt' else 'clear') # clear the terminal
        print(f"Displaying Expenses from the year {year}...\n")
        print(f"\n\ndatabase: {db_name}")
        print(f"table: {table_name}")

        #database declaration
        if self.conn is None:
            self.connect_to_db(table_name)
            print(f"Connecting to database {db_name}...")


        #display prep
        self.txtarea.delete('1.0', END)
       
       #logic starts
        if month == "" or month == " ":
            messagebox.showerror("Invalid Month", "Please Enter a Valid Month.")
        elif year == "" or year == " ":
            messagebox.showerror("Invalid Year", "Please Enter a Valid Year.")
        else:
            if day == "" or day == " ":
                if category == "" or category == " ":
                    self.header_month()
                    self.cur.execute(f'SELECT * FROM "{table_name}" WHERE date LIKE ?', (f'%{month}%, {year}',))
                    expenses = self.cur.fetchall()

                    self.cur.execute(f'SELECT date, SUM(price) FROM "{table_name}" WHERE date LIKE ?', (f'%{month}%, {year}',))
                    self.total_expenses = self.cur.fetchone()
                else:
                    self.header_ctgy()
                    self.cur.execute(f'SELECT * FROM "{table_name}" WHERE date LIKE ? AND category = ?', (f'%{month}%, {year}', category))
                    expenses = self.cur.fetchall()

                    self.cur.execute(f'SELECT date, SUM(price) FROM "{table_name}" WHERE date LIKE ? AND category = ?', (f'%{month}%, {year}', category))
                    self.total_expenses = self.cur.fetchone()
            else:
                if category == "" or category == " ":
                    self.header_month()
                    self.cur.execute(f'SELECT * FROM "{table_name}" WHERE date LIKE ?', (f'%{month} {day}, {year}',))
                    expenses = self.cur.fetchall()

                    self.cur.execute(f'SELECT date, SUM(price) FROM "{table_name}" WHERE date LIKE ?', (f'%{month} {day}, {year}',))
                    self.total_expenses = self.cur.fetchone()
                else:
                    self.header_ctgy()
                    self.cur.execute(f'SELECT * FROM "{table_name}" WHERE date LIKE ? AND category = ?', (f'%{month} {day}, {year}', category))
                    expenses = self.cur.fetchall()

                    self.cur.execute(f'SELECT date, SUM(price) FROM "{table_name}" WHERE date LIKE ? AND category = ?', (f'%{month} {day}, {year}', category))
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

                self.txtarea.tag_config("bold", font=("Courier", 13, "bold"))
                self.txtarea.insert(END, f"{date}\n", "bold")

                
                for expense in expenses:
                    total_item_price = expense[2] * expense[5]
                    sum += total_item_price

                    formatted_price = self.format_price(total_item_price)

                    #expense[0] - expense ID
                    #expense[1] - date
                    #expense[2] - qty
                    #expense[3] - category
                    #expense[4] - item name
                    #expense[5] - price
                    self.txtarea.insert(END, f"[ID: {expense[0]}][Type: {expense[3]}]\n>{expense[4]}\t\t\t~{expense[2]}x ₱{expense[5]}\t\t\t    = ₱{formatted_price}\n")
                    self.txtarea.insert(END, f"\n")

                self.txtarea.insert(END, f"\n")
            self.txtarea.insert(END, f"\n{dashed_line}\n")

            formatted_total = self.format_price(sum)
            if day == "" or day == " ":
                self.txtarea.insert(END, f"Total Expenses as of {month}\t\t\t\t\t\t    = ₱{formatted_total}\n")
            else:
                self.txtarea.insert(END, f"Total Expenses as of {month} {day}\t\t\t\t\t\t    = ₱{formatted_total}\n")

            #analysis
            self.compare_month(table_name)
            # self.compare_year(table_name)
            # self.analysis(table_name)

        self.display_c.set("")

        #terminal log output
        if day == "":
            print(f"\nItems with the date of {month} {year}. Successfully Retrieved!")
        else:
            print(f"\nItems with the date of {month} {day}, {year}. Successfully Retrieved!")

#================================================================================================================================

    # deleting item from the selected year (year).db to delete the specified item with specified date. [done]
    def delete_expense(self):

        date = self.select_ddate
        date_object = datetime.strptime(date, '%B %d, %Y')

        #breaking the date into segments
        date_year = date_object.strftime('%Y')
        get_year = self.delete_year.get()

        eID = self.delete_ID.get()
        db_name = self.dbname

        #Strictly checking for year for validation
        if self.delete_year.get() == "" or self.delete_year.get() == " ": 
            messagebox.showerror("Invalid Year", "Please Enter a Valid Year.")
            return
        else:
            table_name = self.delete_year.get()

        # Setting the current year if year is empty
        # if get_year == "" or get_year == " ":
        #     table_name = date_year
        #     self.delete_year.set(date_year)
        # else:
        #     table_name = get_year

        if self.conn is None:
            self.connect_to_db(db_name)
            print(f"Connecting to database {db_name}")

        if eID == "" or eID == " ":
            messagebox.showerror("Invalid Expense ID", "Please Enter a Valid Expense ID.")
        else:
            #q = messagebox.askyesno('Deleting Expense', f'Are you sure do you want to DELETE this Expense Item? (This action cannot be undone)\n details:\nExpense ID: {eID}\nDate: {date}\nQuantity: {qty}\nCategory: {pay}\nItem: {name}\nPrice: {price}')
            q = messagebox.askyesno('Deleting Expense', f'\nAre you sure do you want to DELETE this Expense Item with the following details.\n(This action cannot be undone)\nExpense ID: {eID}\nDate: {date}\n')
            if q > 0:
                self.cur.execute(f'DELETE FROM "{table_name}" WHERE id = ?', (eID,))
                self.conn.commit()
                messagebox.showinfo('Success!', 'Expense has been Deleted Successfully!')

                self.delete_ID.set("")
                self.delete_year.set("")
                self.display_categorized_expenses()


                os.system('cls' if os.name == 'nt' else 'clear') # clear the terminal
                print(f"\nExpense \"{eID}\" from {date} has been Successfully Deleted!")

#================================================================================================================================

    def search_edit_expense(self):
        table_name = self.edit_year.get()
        dbname = self.dbname
        eID = self.edit_ID.get()

        date = self.select_ddate
        date_object = datetime.strptime(date, '%B %d, %Y')

        # breaking the date into segments
        date_year = date_object.strftime('%Y')
        get_year = self.delete_year.get()

        # retrieving ID and year
        if self.edit_ID.get() == "" or self.edit_ID.get() == " ":
            messagebox.showerror("Invalid Expense ID", "Please Enter a Valid Expense ID.")
            return

        # Strictly checking for year for validation
        elif self.edit_year.get() == "" or self.edit_year.get() == " ":
            messagebox.showerror("Invalid Year", "Please Enter a Valid Year.")
            return
        else:
            eID = self.edit_ID.get()
            table_name = self.edit_year.get()

        # database declaration
        if self.conn is None:
            self.connect_to_db(table_name)
            print(f"Connecting to database {dbname}...")

        # debugs
        os.system('cls' if os.name == 'nt' else 'clear')  # clear the terminal
        print(f"\nSearching for Expense ID: {eID} in table \"{table_name}\"...\n")

        # retrieving data from the database with eID and table_name
        self.cur.execute(f'SELECT * FROM "{table_name}" WHERE id = ?', (eID,))
        expense = self.cur.fetchone()

        # if eID not in table_name: then return error message "Expense ID not found in the database."
        if expense is None:
            print(f"Expense ID: {eID} not found in the the table \"{table_name}\".")
            messagebox.showerror("Expense ID not found", f"Expense ID not found in the database with the year {table_name}.")
            return
        else:
            print(f"Search Success! Expense ID: {eID} found in the table \"{table_name}\".\n")
            name = expense[4]
            price = expense[5]
            qty = expense[2]
            pay = expense[3]
            date = expense[1]

            formatted_price = self.format_price(price)
            print(formatted_price)

            print(f"Expense ID: {eID}")
            print(f"Date: {date}")
            print(f"Expense Name: {name}")
            print(f"Expense Price: {formatted_price}")
            print(f"Expense Quantity: {qty}")
            print(f"Payment Method: {pay}")

            # displaying the data into the edit fields
            self.edit_name.set(name)
            self.edit_cost.set(formatted_price)
            self.edit_qty.set(qty)
            self.edit_pay.set(pay)
            self.select_eedate.delete(0, 'end')  # Clear the DateEntry before setting the date
        self.select_eedate.insert(0, datetime.strptime(date, '%B %d, %Y').strftime('%m/%d/%Y'))

#================================================================================================================================

    def edit_expense(self):
        table_name = self.edit_year.get()
        dbname = self.dbname
        eID = self.edit_ID.get()


        date_str = self.select_eedate.get()
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')

        date = date_obj.strftime('%B %d, %Y')
        name = self.edit_name.get()
        price = self.edit_cost.get().replace(", ", "").replace(" ", "")
        qty = self.edit_qty.get()
        pay = self.edit_pay.get()

        os.system('cls' if os.name == 'nt' else 'clear')  # clear the terminal
        print(f"database: {dbname}")
        print(f"table: {table_name}")
        print(f"Expense ID: {eID}")
        print(f"Date: {date}")
        print(f"Expense Name: {name}")
        print(f"Expense Price: {price}")
        print(f"Expense Quantity: {qty}")
        print(f"Payment Method: {pay}")

        unformat = self.unformat_price(price)

        print(unformat)
        

        #connecting to database
        if self.conn is None:
            self.connect_to_db(table_name)
            print(f"Connecting to database {dbname}...")
        else:
            print(f"Already Connected to {dbname}.db")

        os.system('cls' if os.name == 'nt' else 'clear') # clear the terminal
        #Editing/updating the data from the database
        if name == "" or name == " ":
            messagebox.showerror("Invalid Expense Name", "Please Enter a Valid Expense Name.")
        elif price == "0" or price < "0" or price == "" or price == " ":
            messagebox.showerror("Invalid Expense Price", "Please Enter a Valid Expense Price.")
        elif qty == 0 or qty < 0 or qty == "" or qty == " ":
            messagebox.showerror("Invalid Expense Quantity", "Please Enter a Valid Expense Quantity.")
        elif pay == "" or pay == " ":
            messagebox.showerror("Invalid Payment Method", "Please Enter a Valid Payment Method.")
        else:
            print(f"Editing Expense ID: {eID} in table \"{table_name}\"...\n")
            self.cur.execute(f'UPDATE "{table_name}" SET name = ?, price = ?, quantity = ?, category = ?, date = ? WHERE id = ?', (name, price, qty, pay, date, eID))
            self.conn.commit()
            messagebox.showinfo('Success!', f'Expense with Expense ID: {eID} has been Edited Successfully!')
            self.display_categorized_expenses()

        self.edit_ID.set("")
        self.edit_year.set("")
        self.select_eedate.delete(0, 'end')
        self.edit_name.set("")
        self.edit_cost.set("")
        self.edit_qty.set("")
        self.edit_pay.set("")
        print(f"Expense ID: {eID} has been Successfully Edited!")

#================================================================================================================================

    def compare_month(self, table_name):
        dbname = self.dbname

        os.system('cls' if os.name == 'nt' else 'clear') # clear the terminal
        print(f"database: {dbname}")
        print(f"table: {table_name}")

        #Database declaration
        if self.conn is None:
            self.connect_to_db(table_name)
            print(f"Connecting to database {dbname}...")

        #database actions
        self.cur.execute(f'SELECT date, quantity, price FROM "{table_name}" ')
        montly_expense = self.cur.fetchall()

        # Sort dates in ascending order
        sort_month = sorted(montly_expense, key=lambda x: datetime.strptime(x[0].strip(), '%B %d, %Y'))

        #grouping the expenses by month
        expenses_by_month = {}
        for expense in sort_month:
            date = expense[0]
            month = date.split(" ")[0]
            if month not in expenses_by_month:
                expenses_by_month[month] = []
            expenses_by_month[month].append(expense)

        # sum of monthly of expenses
        month_sum = {}
        for month, expenses in expenses_by_month.items():
            total = 0
            for expense in expenses:
                total += expense[1] * expense[2]
            month_sum[month] = total

        # comparison logic
        highest = max(month_sum, key=month_sum.get)
        lowest = min(month_sum, key=month_sum.get)

        highest_spent = month_sum[highest]
        lowest_spent = month_sum[lowest]

        formatted_highest = self.format_price(highest_spent)
        formatted_lowest = self.format_price(lowest_spent)

        print(f"Month with the Highest Expense is \"{highest}\" with the total of \"₱{formatted_highest}\".")
        print(f"Month with the Lowest Expense is \"{lowest}\" with the total of \"₱{formatted_lowest}\".\n")

        # statement for the comparison
        # if month_sum[highest] == month_sum[lowest]:
        #     print(f"You spent the same amount in {highest} as in the previous month, {lowest}.")
        # elif month_sum[highest] > month_sum[lowest]:
        #     print(f"You spent more in {highest} with ₱{month_sum[highest]} than in the month {lowest} with ₱{month_sum[lowest]}.")
        # else:
        #     print(f"You spent less in {highest} with ₱{month_sum[highest]} than in the month {lowest} with ₱{month_sum[lowest]}.")

        self.txtarea.insert(END, f"\nMost Expense Month: \"{highest}\" with the total of: \"₱{formatted_highest}\".\n")
        self.txtarea.insert(END, f"Least Expense Month: \"{lowest}\" with the total of: \"₱{formatted_lowest}\".\n")

        #analysis of which item is the most expensive from that month
        #sample output: "You spent mostly on (item) this (month)."

        #make a analysis like
        # this month you spent mostly on (item with the highest total_item_price)
        # You spent (less/more) than previous (month/day) (march, if current month is april)

#================================================================================================================================

    def compare_year(self, table_name):
        dbname = self.dbname

        # os.system('cls' if os.name == 'nt' else 'clear') # clear the terminal

        # database declaration
        if self.conn is None:
            self.connect_to_db()
            print(f"Connecting to database {dbname}...")

        # Get all non-system table names
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = self.cur.fetchall()

        yearly_expense = []
        for table in tables:
            # Check if the table has the 'date', 'quantity', and 'price' columns
            self.cur.execute(f"PRAGMA table_info('{table[0]}')")
            columns = [column[1] for column in self.cur.fetchall()]
            if all(column in columns for column in ['date', 'quantity', 'price']):
                #database actions
                self.cur.execute(f'SELECT date, quantity, price FROM "{table[0]}"')
                yearly_expense += self.cur.fetchall()
            else:
                print(f"Table '{table[0]}' does not have 'date', 'quantity', or 'price' column.")

        # Sort year in ascending order
        sort_year = sorted(yearly_expense, key=lambda x: datetime.strptime(x[0].strip(), '%B %d, %Y'))

        #grouping the expenses by year
        expenses_by_year = {}
        for expense in sort_year:
            date = expense[0]
            year = date.split(" ")[2]
            if year not in expenses_by_year:
                expenses_by_year[year] = []
            expenses_by_year[year].append(expense)

        # sum of yearly of expenses
        year_sum = {}
        for year, expenses in expenses_by_year.items():
            total = 0
            for expense in expenses:
                total += expense[1] * expense[2]
            year_sum[year] = total

        #comparison logic
        highest = max(year_sum, key=year_sum.get)
        lowest = min(year_sum, key=year_sum.get)

        formatted_highest = self.format_price(year_sum[highest])
        formatted_lowest = self.format_price(year_sum[lowest])

        print(f"\nYear with the Highest Expense is \"{highest}\" with the total of \"₱{formatted_highest}\".")
        print(f"Year with the Lowest Expense is \"{lowest}\" with the total of \"₱{formatted_lowest}\".\n")

        self.txtarea.insert(END, f"\nMost Expense Year: \"{highest}\" with the Total of: \"₱{formatted_highest}\".\n")
        self.txtarea.insert(END, f"Least Expense Year: \"{lowest}\" with the Total of: \"₱{formatted_lowest}\".\n\n")

#================================================================================================================================
    
    def format_price(self, price):
        formatted_price = "{:,}".format(price).replace(",", ", ")
        return formatted_price
    
    def unformat_price(self, formatted_price):
        unformatted_price = formatted_price.replace(", ", "").replace(" ", "").replace(",", "")
        return unformatted_price

#================================================================================================================================

    # setting all entries into blank
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

    # header for the database display   
    def header(self):
        year = self.display_y.get()

        display_width = self.txtarea.winfo_width()
        text = f"| Expense List for {year} |"

        num_dashes = display_width // self.divide
        header_dashes = "=" * num_dashes


        self.txtarea.insert(END, f"{header_dashes}\n")
        self.txtarea.insert(END, f"{f'{text}'.center(num_dashes, '=')}\n")
        self.txtarea.insert(END, f"{header_dashes}\n")

#================================================================================================================================
    
    # header for the database display   
    def header_month(self):
        month = self.display_m.get()
        year = self.display_y.get()
        width = self.txtarea.winfo_width()

        display_width = self.txtarea.winfo_width()
        text = f"| Expense List for {month} {year}|"

        num_dashes = display_width // self.divide
        header_dashes = "=" * num_dashes

        self.txtarea.insert(END, f"{header_dashes}\n")
        self.txtarea.insert(END, f"{f'{text}'.center(num_dashes, '=')}\n")
        self.txtarea.insert(END, f"{header_dashes}\n")

#================================================================================================================================
    
    # header for the database display   
    def header_ctgy(self):
        month = self.display_m.get()
        category = self.display_c.get()

        display_width = self.txtarea.winfo_width()
        text = f"| Expense List for {month} by {category} |"

        num_dashes = display_width // self.divide
        header_dashes = "=" * num_dashes


        self.txtarea.insert(END, f"{header_dashes}\n")
        self.txtarea.insert(END, f"{f'{text}'.center(num_dashes, '=')}\n")
        self.txtarea.insert(END, f"{header_dashes}\n")
    
#================================================================================================================================
    
    #dynamic layout for the screen
    def setup_grid(self):
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

#================================================================================================================================

# Declare so GUI wont close
def main():
    window = Tk()  # Creating the Tkinter window instance here
    window.geometry("1180x640+200+80")
    app = Expense(window)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    #window.resizable(True, True)
    window.mainloop()

#================================================================================================================================
# loop
if __name__ == "__main__":
    main()