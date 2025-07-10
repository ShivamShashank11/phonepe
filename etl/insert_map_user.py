import os
import json
import mysql.connector

# ✅ MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # 🔁 Change if needed
    database="phonepe_insights"
)
cursor = conn.cursor()

# ✅ Base path to map user data
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\map\user\hover\country\india\state"

inserted = 0
skipped = 0

# ✅ Loop through state → year → json
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith(".json"):
                        quarter = int(file.replace(".json", ""))
                        file_path = os.path.join(year_path, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)

                            hover_data = data.get("data", {}).get("hoverData", {})

                            if not hover_data:
                                skipped += 1
                                continue

                            for district, details in hover_data.items():
                                reg_users = details.get("registeredUsers", 0)
                                app_opens = details.get("appOpens", 0)

                                cursor.execute("""
                                    INSERT INTO map_user (state, year, quarter, district, registered_users, app_opens)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """, (state, int(year), quarter, district, reg_users, app_opens))
                                conn.commit()
                                inserted += 1

                        except Exception as e:
                            print(f"❌ Error in {file_path}: {e}")
                            skipped += 1

# ✅ Summary
cursor.execute("SELECT COUNT(*) FROM map_user")
total = cursor.fetchone()[0]

print("\n✅ Map User Insertion Complete!")
print("➕ Rows inserted:", inserted)
print("⏭️ Rows skipped:", skipped)
print("📊 Total rows in map_user:", total)

cursor.close()
conn.close()
