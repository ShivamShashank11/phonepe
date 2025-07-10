import os
import json
import mysql.connector

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",
    database="phonepe_insights"
)
cursor = conn.cursor()

# ✅ Path to top user data
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\top\user\country\india\state"

inserted = 0
skipped = 0
batch = []

for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith(".json"):
                        try:
                            quarter_str = file.replace(".json", "").strip().lower().replace("q", "")
                            quarter = int(quarter_str)
                            file_path = os.path.join(year_path, file)

                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)

                            pincode_data = data.get("data", {}).get("pincodes", [])
                            if not pincode_data:
                                skipped += 1
                                continue

                            for pin in pincode_data:
                                name = pin.get("name", "000000")
                                users = pin.get("registeredUsers", 0)

                                batch.append((state, int(year), quarter, name, users))
                                inserted += 1

                        except Exception as e:
                            print(f"❌ Error parsing file: {file} → {e}")
                            skipped += 1

# ✅ Insert batched rows
if batch:
    cursor.executemany("""
        INSERT INTO top_user (state, year, quarter, name, registered_users)
        VALUES (%s, %s, %s, %s, %s)
    """, batch)
    conn.commit()

# ✅ Summary
cursor.execute("SELECT COUNT(*) FROM top_user")
total = cursor.fetchone()[0]

print("\n✅ Top User Insertion Complete!")
print("➕ Rows inserted:", inserted)
print("⏭️ Rows skipped:", skipped)
print("📊 Total rows in top_user:", total)

cursor.close()
conn.close()
