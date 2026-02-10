import sqlite3

conn = sqlite3.connect("sqlite_database.db")
cursor = conn.cursor()

# RegisteredCases table
cursor.execute("ALTER TABLE registeredcases ADD COLUMN color TEXT")
cursor.execute("ALTER TABLE registeredcases ADD COLUMN height TEXT")

# PublicSubmissions table
cursor.execute("ALTER TABLE publicsubmissions ADD COLUMN color TEXT")
cursor.execute("ALTER TABLE publicsubmissions ADD COLUMN height TEXT")

conn.commit()
conn.close()

print("✅ Database updated successfully")
