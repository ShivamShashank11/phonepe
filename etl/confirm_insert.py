import mysql.connector
from datetime import datetime

# ✅ Step 1: MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # 🔁 ← Apna MySQL password
    database="phonepe_insights"  # ✅ ← Yehi DB banaya tha
)
cursor = conn.cursor()

# ✅ Step 2: Confirm Connected Database
cursor.execute("SELECT DATABASE();")
db_name = cursor.fetchone()[0]
print("📍 Connected to:", db_name)

# ✅ Step 3: Insert one test row manually
cursor.execute("""
    INSERT INTO aggregated_transaction (
        state, year, quarter, from_date, to_date,
        transaction_type, transaction_count, transaction_amount
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (
    "bihar", 2020, 1,
    datetime(2020, 1, 1), datetime(2020, 3, 31),
    "Recharge & bill payments", 1323, 983274.0
))

conn.commit()
print("✅ 1 row inserted successfully.")

# ✅ Step 4: Check total rows in table
cursor.execute("SELECT COUNT(*) FROM aggregated_transaction")
count = cursor.fetchone()[0]
print("📊 Total rows in aggregated_transaction:", count)

# ✅ Step 5: Close connection
cursor.close()
conn.close()
