import os
import json
import mysql.connector

# ✅ Safely extract count and amount
def extract_values(metric_list):
    try:
        if isinstance(metric_list, list) and metric_list:
            metric_item = metric_list[0]
            count = int(metric_item.get("count", 0))
            amount = float(metric_item.get("amount", 0.0))
            return count, amount
    except:
        pass
    return 0, 0.0

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",
    database="phonepe_insights"
)
cursor = conn.cursor()

# ✅ Set base folder
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\map\transaction\hover\country\india\state"

inserted = 0
skipped = 0
batch_data = []

# ✅ Loop over all folders
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

                            districts = data.get("data", {}).get("hoverDataList", [])

                            if not districts:
                                skipped += 1
                                continue

                            for dist in districts:
                                district = dist.get("name", "Unknown")
                                metric_list = dist.get("metric", [])
                                metric, amount = extract_values(metric_list)

                                if metric == 0 and amount == 0.0:
                                    continue

                                batch_data.append((state, int(year), quarter, district, metric, amount))
                                inserted += 1

                        except Exception as e:
                            print(f"❌ Error in file {file_path}: {e}")
                            skipped += 1

# ✅ Insert into database
if batch_data:
    cursor.executemany("""
        INSERT INTO map_transaction (state, year, quarter, district, metric, amount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, batch_data)
    conn.commit()

# ✅ Show summary
cursor.execute("SELECT COUNT(*) FROM map_transaction")
total = cursor.fetchone()[0]

print("\n✅ Insertion complete")
print("➕ Rows inserted:", inserted)
print("⏭️ Skipped:", skipped)
print("📊 Total in DB:", total)

cursor.close()
conn.close()

