import csv
import sqlite3

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

#query = "INSERT INTO sys_command VALUES(null,'Video1', 'C:\\Users\\Dell\\OneDrive\\Videos\\Video1.exe')"
#cursor.execute(query)
#conn.commit()

query = "INSERT INTO web_command VALUES(null,'Youtube', 'https://www.youtube.com/')"
cursor.execute(query)
conn.commit()

#query = "DELETE FROM web_command WHERE name='Chatgpt'"
#cursor.execute(query)
#conn.commit()

#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name VARCHAR(200), Phone VARCHAR(255), email VARCHAR(255) NULL)''') 
#    # Multi-Contacts
#desired_columns_indices = [0, 17]
#
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'Phone') VALUES (null, ?,? );''', tuple(selected_data))
# # Commit changes and close connection
#conn.commit()
#conn.close()
#print("Data inserted successfully") 
#      # Single Contact
#query = "INSERT INTO contacts VALUES (null,'raj', '1234567890', 'null')" cursor.execute(query)
#conn.commit() 
#
#
#   # Find Number
#
#query = 'Ankit'
#query = query.strip().lower()  # Added parentheses to call the method      
#cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
#               ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])


# Delete old contact data
#cursor.execute("DELETE FROM contacts")

# Read CSV
#with open("contacts.csv", "r", encoding="utf-8", newline="") as csvfile:
#
#    csvreader = csv.reader(csvfile)
#
#    # Skip CSV header
#    next(csvreader, None)
#
#    for row in csvreader:
#
#        # CSV contains 19 columns: 0 to 18
#        if len(row) < 19:
#            print("Skipping invalid row")
#            continue
#
#        # Correct columns
#        name = row[0].strip()
#        phone = row[18].strip()
#
#        # Skip empty contacts
#        if not name or not phone:
#            continue
#
#        # Insert contact
#        cursor.execute("""
#            INSERT INTO contacts (name, Phone)
#            VALUES (?, ?)
#        """, (name, phone))
#
## Save changes
#conn.commit()
#
## Close database
#conn.close()
#
#print("Old contact data deleted.")
#print("New contact data inserted successfully!")