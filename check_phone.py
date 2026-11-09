
from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT patient_id, name, phone FROM patients")

records = cursor.fetchall()

print("\n===== STORED PHONE NUMBERS =====")

for record in records:
    print(record)

conn.close()

