import sqlite3

conn = sqlite3.connect('court_data.db')
c = conn.cursor()

c.execute("SELECT * FROM queries ORDER BY timestamp DESC")
rows = c.fetchall()

for row in rows:
    print(f"\nID: {row[0]}")
    print(f"Case Type: {row[1]}")
    print(f"Case Number: {row[2]}")
    print(f"Year: {row[3]}")
    print(f"Timestamp: {row[4]}")
    print(f"Raw Response:\n{row[5][:500]}...")  # Only showing first 500 chars
