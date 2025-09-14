import sqlite3
import pandas as pd

# Load CSV
df = pd.read_csv('swiggy.csv')

## Connectt to SQlite
connection=sqlite3.connect("swiggy.db")

# Write dataframe to a SQL table
df.to_sql("swiggy", connection, if_exists="replace", index=False)

# Query the database
cursor=connection.cursor()
data=cursor.execute('''Select * from swiggy LIMIT 5''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()
