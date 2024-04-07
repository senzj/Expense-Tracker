import datetime
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkinter import messagebox
import os
from tkcalendar import DateEntry
    
class Expense:

    #initialization
    def __init__(self, window):

        # Declarations
        self.window = window
        self.window.title("Expenses List v3.0")

        self.setup_grid()
        self.Static_GUI_Widget()

        #In progress..
        # self.Dynamic_GUI_Widget()

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
        self.days = [f"{i:02d}" for i in range(1, 32)]
        self.select_edate = datetime.today().strftime('%B %d, %Y')
        self.select_ddate = datetime.today().strftime('%B %d, %Y')
        
        
        #database things
        self.table_name = "expenses"
        # self.dbname = StringVar()
        self.conn = None
        self.cur = None
        # self.connect_to_db(self.dbname)

        print("Program Ready.")

#================================================================================================================================
    
    #dynanic widget and GUI display [in progress]
    def Dynamic_GUI_Widget(self):
        
        pass


#================================================================================================================================
    
    #dynanic widget and GUI display [done]
    def Static_GUI_Widget(self):

        dbutton_width = 12

        background = "sky blue"
        add_background = "sky blue"
        dis_background = "sky blue"
        del_background = "sky blue"

        add_frame_height = 200
        dis_frame_height = 140
        del_frame_height = 170
        out_frame_height1 = 600
        out_frame_height2 = 555

        add_frame_width = 345
        dis_frame_width = 345
        del_frame_width = 345
        out_frame_width1 = 450
        out_frame_width2 = 435

        # add_ = 
        # dis_ = 
        # del_ = 
        # out_ =


        self.setup_var()

#Adding Expense
        entries = LabelFrame(self.window, bd=10, relief=GROOVE, text="Add Expense", font=("times new roman", 20, "bold"), fg="black", bg="sky blue")
        entries.place(x=453, y=1, width=add_frame_width, height=add_frame_height)

        date_label = tk.Label(entries, text="Date ", bg=add_background).grid(row=1,column=0, pady=10, sticky="e")
        
        self.edate_cal = DateEntry(entries, width=12)  # Use self.window instead of entries
        self.edate_cal.grid(row=1, column=1, pady=10, sticky="w")
        self.edate_cal.set_date(datetime.today())  # Set date
        self.edate_cal.bind("<<DateEntrySelected>>", self.update_edate)  # Bind event

        qnty_label = tk.Label(entries, text="Item Quantity", bg=add_background).grid(row=2, column=0, sticky="e")
        qnty_entry = tk.Spinbox(entries, textvariable = self.item_qty,from_=1, to=9999, width=18, relief=SUNKEN).grid(row=2, column=1,pady=4)

        ctgy_label = tk.Label(entries, text="Payment Method", bg=add_background).grid(row=3,column=0, sticky="e")
        ctgy_entry = ttk.Combobox(entries, textvariable = self.item_ctgy, width=17, values=self.catgs)
        ctgy_entry.grid(row=3,column=1,pady=4)
        ctgy_entry.insert(0, "Cash")

        item_label = tk.Label(entries, text="Item Name", bg=add_background).grid(row=4,column=0, sticky="e")
        item_entry = tk.Entry(entries, textvariable = self.item_name, relief=SUNKEN).grid(row=4,column=1,pady=4)

        prc_label = tk.Label(entries, text="Item Price", bg=add_background).grid(row=5,column=0, sticky="e")
        prc_entry = tk.Entry(entries, textvariable = self.item_prc, relief=SUNKEN).grid(row=5, column=1)

        #add more items
        add_btn = tk.Button(entries, text="Add", command=self.add_item, width=11).grid(row=5,column=2, padx=13)


#display list of items by month
        display_chng = LabelFrame(self.window, bd=10, relief=GROOVE, text="Display Expense", font=("times new roman", 20, "bold"), fg="black", bg="sky blue")
        display_chng.place(x=453, y=203, width=dis_frame_width, height=dis_frame_height)

        display_c_label = tk.Label(display_chng, text="Category(Optional)", bg=dis_background).grid(row=1, column=1, sticky=W)
        display_c_entry = ttk.Combobox(display_chng, textvariable = self.display_c, width=17, values = self.catgs).grid(row=1, column=2, sticky=E)
        
        display_m_label = tk.Label(display_chng, text="Month", bg=dis_background).grid(row=2, column=1, sticky=W)
        display_m_entry = ttk.Combobox(display_chng, textvariable = self.display_m, width=17, values = self.months)
        display_m_entry.grid(row=2, column=2, sticky=E)
        display_m_entry.insert(0, self.date.strftime('%B'))
        
        display_d_label = tk.Label(display_chng, text="Day (Optional)", bg=dis_background).grid(row=3, column=1, sticky=W)
        display_d_entry = ttk.Combobox(display_chng, textvariable = self.display_d, width=17, values = self.days)
        display_d_entry.grid(row=3, column=2, sticky=E)
        
        display_yr_label = tk.Label(display_chng, text="Year", bg=dis_background).grid(row=4, column=1, sticky=W)
        display_yr_entry = tk.Entry(display_chng, textvariable = self.display_y)
        display_yr_entry.grid(row=4, column=2, sticky=E)
        display_yr_entry.insert(0, self.date.strftime('%Y'))
        
        display_btn = tk.Button(display_chng, text="Show", command=self.display_specified, width=10).grid(row=3,column=3, sticky=E, padx=5)
        display_btn = tk.Button(display_chng, text="Display All", command=self.display_item, width=10).grid(row=4,column=3, sticky=E, padx=5)
        
        
#delete an item from database specified by name and date including month day year
        delete = LabelFrame(self.window, bd=10, relief=GROOVE, text="Delete Expense", font=("times new roman", 20,"bold"), fg="black", bg="sky blue")
        delete.place(x=453, y=345, width=del_frame_width, height=del_frame_height)

        delete_item_label = tk.Label(delete, text="Enter an Expense", bg=del_background).grid(row=2, column=1, sticky="e")
        delete_item_entry = tk.Entry(delete, textvariable=self.delete_name).grid(row=2, column=2, sticky="w", pady=5)
        
        date_label = tk.Label(delete, text="Date ", bg=del_background).grid(row=1,column=1, pady=5, sticky="e")
        self.ddate_cal = DateEntry(delete, width=12)  # Use self.window instead of entries
        self.ddate_cal.grid(row=1, column=2, pady=5, sticky="w")
        self.ddate_cal.set_date(datetime.today())  # Set date
        self.ddate_cal.bind("<<DateEntrySelected>>", self.update_ddate)  # Bind event
        
        
        display_btn = tk.Button(delete, text="Delete Item", command=self.delete_item, width=dbutton_width).grid(row=1,column=3, sticky=E, padx=5, pady=5)
        #clearing input field
        clr_btn = tk.Button(delete, text="Clear Entries", command=self.clear_item, width=dbutton_width).grid(row=2,column=3, sticky=E, padx=5, pady=5)
        #refresh
        display_btn = tk.Button(delete, text="Refresh List", command=self.display_specified, width=dbutton_width).grid(row=3,column=3, sticky=E, padx=5, pady=5)
    
    
#display items list area + by months and year
        #frame
        display = LabelFrame(self.window, bd=10, relief=GROOVE, text="Expenses List", font=("times new roman", 20,"bold"), fg="black", bg=background)
        display.place(x=3, y=1, width=out_frame_width1, height=out_frame_height1)
        
        #display
        display = LabelFrame(self.window, bd=10, relief=GROOVE)
        display.place(x=9, y=35, width=out_frame_width2, height=out_frame_height2)
        bill_title=Label(display, text="Your List of Expenses", font="arial 15 bold", bd=7, relief=GROOVE).pack(fill=X)


        scrol_y = Scrollbar(display, orient=VERTICAL) 
        self.txtarea = Text(display, yscrollcommand=scrol_y.set)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)

#================================================================================================================================
    
    def update_edate(self, event):
        # Get the selected date and store it in self.select_edate for add
        self.select_edate = event.widget.get_date().strftime('%B %d, %Y')

    def update_ddate(self, event):
        # Get the selected date and store it in self.select_ddate for delete
        self.select_ddate = event.widget.get_date().strftime('%B %d, %Y')

#================================================================================================================================

    # creating or checking for existing db in the directory by year [done]
    def connect_to_db(self, dbname):
        if self.conn:
            self.conn.close()  # close previous connection if it exists

        db_name = f"{dbname}.db"

        # Check if the database file exists before connecting
        if not os.path.exists(db_name):
            print(f"The Database named {db_name} does not exist..")
            print(f"Creating Database named {db_name} now...")
            print(f"Creating table named {self.table_name}...")

            self.conn = sqlite3.connect(db_name)
            self.cur = self.conn.cursor()

            # Create the table
            
            query = f'''CREATE TABLE IF NOT EXISTS "{self.table_name}" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    quantity INTEGER,
                    category TEXT,
                    name TEXT,
                    price REAL
                    )'''

            # Execute the query
            self.cur.execute(query)
            
            print(f"Database {db_name} and Table {self.table_name} Created Successfully!")

        else:
            print(f"Database {db_name} already exist")
            print(f"The table {self.table_name} already exists.")

        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

#================================================================================================================================
    
    # adding item into the (year).db database. [done]
    def add_item(self):
        date = self.select_edate
        date_object = datetime.strptime(date, '%B %d, %Y')

        #breaking the date into segments
        date_year = date_object.strftime('%Y')
        date_month = date_object.strftime('%B')
        date_day = date_object.strftime('%d')


        num = self.item_qty.get()
        ctgy = self.item_ctgy.get()
        name = self.item_name.get()
        prc = self.item_prc.get()
        table_name = self.table_name

        if self.conn is None:
            self.connect_to_db(date_year)
            print(f"Connecting to database {date_year}...")
        else:
            print(f"Already Connected to {date_year}.db")
        
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
            print(f"Payment Method: {ctgy}\n")
            
            query = f'INSERT INTO "{table_name}" (date, quantity, category, name, price) VALUES (?, ?, ?, ?, ?)'
            self.cur.execute(query, (date, num, ctgy ,name, prc))
            self.conn.commit()
            messagebox.showinfo('Success', 'Item added successfully!')
            print(f"Items Added Succesfully!")
            self.display_specified()
            
        print(f"Process Completed Succesfully!")

        # self.fields_reset()
        self.item_qty.set("1")
        self.item_name.set("")
        self.item_prc.set("")

        self.edate_cal.set_date(datetime.today())

#================================================================================================================================

    # displaying all items from the current year from (year).db [done]
    def display_item(self):

        #variable declation
        sum = 0
        date_year = f"{self.item_year.get()}"

        display_width = self.txtarea.winfo_width()
        num_dashes = display_width // self.divide
        dashed_line = "-" * num_dashes
        # print(display_width)
        # print(num_dashes)
        # print(dashed_line)


        #database actions
        if self.conn is None:
            self.connect_to_db(date_year)
            print(f"Connecting to database {date_year}...")
        else:
            print(f"Already Connected to {date_year}.db")

        self.cur.execute("""SELECT * FROM expenses""")
        expenses = self.cur.fetchall()

        self.cur.execute("""SELECT date, SUM(price) FROM expenses""")
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
                total_item_price = expense[2] * expense[5]
                sum += total_item_price

                self.txtarea.insert(END, f"[{expense[3]}]\n>{expense[4]}\t\t\t~{expense[2]}x ₱{expense[5]}\t\t= ₱{total_item_price}\n")

                self.txtarea.insert(END, f"\n")
            self.txtarea.insert(END, f"\n")

        # Insert total monthly expenses
        self.txtarea.insert(END, f"{dashed_line}\n")
        self.txtarea.insert(END, f"Overall Total Expenses \t\t\t\t\t= ₱{sum}\n")

        #make a analysis like
        # this month you spent mostly on (item with the highest total_item_price)
        # You spent (less/more) than previous month (march, if current month is april)

            

        # total_expenses -> (date, sum)
        
        print("displaying all item...")
        print("Item retrieved.")
            
#================================================================================================================================

    # displaying all items with specified month, day (optional), along with year to know which database to open [done]
    def display_specified(self):

        #variable declaration
        sum = 0
        month = self.display_m.get()
        year = self.display_y.get()
        day = self.display_d.get()
        category = self.display_c.get()

        display_width = self.txtarea.winfo_width()
        num_dashes = display_width // self.divide
        dashed_line = "-" * num_dashes
        # print(display_width)
        # print(num_dashes)
        # print(dashed_line)


        #database declaration
        date_year = f"{year}"
        if self.conn is None:
            self.connect_to_db(date_year)
            print(f"Connecting to database {date_year}...")
        else:
            print(f"Already Connected to {date_year}.db")
        

        #display prep
        self.txtarea.delete('1.0', END)
       
        #logic starts
        if month == "" or month == " ":
            messagebox.showerror("Invalid Month", "Please Enter a Valid Month (E.G. June, July).")
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

                self.txtarea.tag_config("bold", font=("Courier", 13, "bold"))
                self.txtarea.insert(END, f"{date}\n", "bold")

                
                for expense in expenses:
                    total_item_price = expense[2] * expense[5]
                    sum += total_item_price

                    # print(expense)

                    #expense[0] - key ID
                    #expense[1] - date
                    #expense[2] - qty
                    #expense[3] - category
                    #expense[4] - item name
                    #expense[5] - price
                    self.txtarea.insert(END, f"[{expense[3]}]\n>{expense[4]}\t\t~{expense[2]}x ₱{expense[5]}\t\t\t= ₱{total_item_price}\n")
                    self.txtarea.insert(END, f"\n")

                self.txtarea.insert(END, f"\n")
            self.txtarea.insert(END, f"\n{dashed_line}\n")

            if day == "" or day == " ":
                self.txtarea.insert(END, f"Total Expenses for {month}\t\t\t\t    = ₱{sum}\n")
            else:
                self.txtarea.insert(END, f"Total Expenses for {month} {day}\t\t\t\t    = ₱{sum}\n")

            #make a analysis like
            # this month you spent mostly on (item with the highest total_item_price)
            # You spent (less/more) than previous (month/day) (march, if current month is april)

        self.display_c.set("")

        #terminal log output
        if day == "":
            print(f"\nItems with the date of {month} {year}. Successfully Retrieved!")
        else:
            print(f"\nItems with the date of {month} {day}, {year}. Successfully Retrieved!")

#================================================================================================================================

    # deleting item from the selected year (year).db to delete the specified item with specified date. [done]
    def delete_item(self):

        date = self.select_ddate
        date_object = datetime.strptime(date, '%B %d, %Y')

        #breaking the date into segments
        date_year = date_object.strftime('%Y')
        date_month = date_object.strftime('%B')
        date_day = date_object.strftime('%d')

        name = self.delete_name.get()
        today_delete = datetime.today()
        ddate = f"{date_month} {date_day}, {date_year}"

        if self.conn is None:
            self.connect_to_db(date_year)
            print(f"Connecting to database {date_year}...")
        else:
            print(f"Already Connected to {date_year}.db")

        if name == "" or name == " ":
            alertm = messagebox.showerror("Invalid Item", "Kindly Enter a Valid Item.")
        elif date_month == "" or date_month == " ":
            alertm = messagebox.showerror("Invalid Month", "Kindly Enter a Valid Month.")
        elif date_day == "" or date_day == " ":
            alertd = messagebox.showerror("Invalid Date","Kindly Enter a Valid Day.")
        elif date_year == "" or date_year == " ":
            alerty = messagebox.showerror("Invalid Year", "Kindly Enter a Valid Year.")
        else:
            q = messagebox.askyesno("Deleting an Item...", "Do you want to Delete This Item?")
            if q > 0:
                self.cur.execute('DELETE FROM expenses WHERE name = ? AND date = ?', (name, date))
                self.conn.commit()
                messagebox.showinfo('Success', 'Item deleted successfully!')
                self.delete_name.set("")
                self.delete_d.set(today_delete.strftime('%d'))
                self.delete_m.set(today_delete.strftime('%B'))
                self.delete_y.set(today_delete.year)
                self.display_specified()

                print(f"\nItem {name}, from {date}, Successfully Removed.")
                # print(f"\nItem {name}, from {date}, with the ID of  Successfully Removed.")

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
        width = self.txtarea.winfo_width()

        display_width = self.txtarea.winfo_width()
        text = f"| Expense List for {month} |"

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

    # def fields_reset(self):
    #     self.item_qty.set("1")
    #     self.item_name.set("")
    #     self.item_prc.set("")

    #     today_date = datetime.today()
    #     self.resetdate.set_date(datetime.today())


#================================================================================================================================

# Declare so GUI wont close
def main():
    # expense = Expense(window)
    # window.mainloop()

    window = Tk()  # Creating the Tkinter window instance here
    window.geometry("800x600+200+80")
    app = Expense(window)
    window.mainloop()

#================================================================================================================================
# loop
if __name__ == "__main__":
    main()