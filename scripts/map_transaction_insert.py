import os, json, mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="Nicky@123", database="phonepe_insights"
)
cursor = conn.cursor()

base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\map\transaction\country\india\state"
inserted = 0

# ✅ Insert map_transaction
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
                        metric = district.get("metric", 0)
                        amount = district.get("amount", 0.0)

                        cursor.execute("""
                            INSERT INTO map_transaction (state, year, quarter, district, metric, amount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (state, int(year), quarter, name, metric, amount))
                        inserted += 1
                conn.commit()

print(f"✅ map_transaction insertion complete. Rows inserted: {inserted}")
cursor.close()
conn.close()
