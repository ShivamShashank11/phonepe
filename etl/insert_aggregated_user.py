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

# ✅ Path to your data
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\user\country\india\state"

inserted = 0
skipped = 0

# ✅ Loop through states
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith(".json"):
                        try:
                            quarter = int(file.replace(".json", ""))
                            file_path = os.path.join(year_path, file)

                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)

                            aggregated = data.get("data", {}).get("aggregated", {})
                            registered_users = aggregated.get("registeredUsers", 0)
                            app_opens = aggregated.get("appOpens", 0)

                            devices = data.get("data", {}).get("usersByDevice", [])

                            if not devices:
                                # Insert without brand
                                cursor.execute("""
                                    INSERT INTO aggregated_user 
                                    (state, year, quarter, registered_users, app_opens)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (state, int(year), quarter, registered_users, app_opens))
                                inserted += 1
                            else:
                                for device in devices:
                                    brand = device.get("brand", "Unknown")
                                    brand_count = device.get("count", 0)
                                    brand_percentage = device.get("percentage", 0.0)

                                    cursor.execute("""
                                        INSERT INTO aggregated_user 
                                        (state, year, quarter, registered_users, app_opens, brand, brand_count, brand_percentage)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (
                                        state, int(year), quarter,
                                        registered_users, app_opens,
                                        brand, brand_count, brand_percentage
                                    ))
                                    inserted += 1
                            conn.commit()

                        except Exception as e:
                            print(f"❌ Error in {file_path}: {e}")
                            skipped += 1

# ✅ Summary
cursor.execute("SELECT COUNT(*) FROM aggregated_user")
print("\n✅ Aggregated User Brand Insertion Complete!")
print("➕ Rows inserted:", inserted)
print("⏭️ Skipped:", skipped)
print("📊 Total rows:", cursor.fetchone()[0])

cursor.close()
conn.close()
