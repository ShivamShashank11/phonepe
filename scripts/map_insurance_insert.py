import os, json, mysql.connector

# ✅ MySQL connection
conn = mysql.connector.connect(
    host="localhost", user="root", password="Nicky@123", database="phonepe_insights"
)
cursor = conn.cursor()

# ✅ Data path
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\map\user\country\india\state"
inserted = 0

# ✅ Insert map_user
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        for file in os.listdir(year_path):
            if file.endswith(".json"):
                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for district in data["data"]["districts"]:
                        name = district["name"]
                        reg_users = district.get("registeredUsers", 0)
                        app_opens = district.get("appOpens", 0)

                        cursor.execute("""
                            INSERT INTO map_user (state, year, quarter, district, registered_users, app_opens)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (state, int(year), quarter, name, reg_users, app_opens))
                        inserted += 1
                conn.commit()

print(f"✅ map_user insertion complete. Rows inserted: {inserted}")
cursor.close()
conn.close()
