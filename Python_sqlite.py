import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object to interact with the database
cur = conn.cursor()

# Create a table
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Insert some data
cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))
cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Charlie', 40))

# Save (commit) the changes
conn.commit()

# Query the database
cur.execute("SELECT * FROM users")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
