import sqlite3
import os
from datetime import datetime

date = datetime.today()
year = date.strftime('%Y')

# Create a db file that is based on the current year. like 2024.db
db_name = f"{year}.db"
# db_name = f"2023.db"

# Check if the database file exists before creating it
if not os.path.exists(db_name):
    print(f"Creating database {db_name}...")
else:
    print(f"Database {db_name} already exists.")

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect(db_name)
cur = conn.cursor()

# Define the table name and the CREATE TABLE query
table_name = "expenses"
query = f'''CREATE TABLE IF NOT EXISTS "{table_name}" (
            date TEXT,
            quantity INTEGER,
            category TEXT,
            name TEXT,
            price REAL
            )'''

# Execute the query
cur.execute(query)
conn.commit()
print("Creating databse completed.")

# Close the connection
conn.close()
