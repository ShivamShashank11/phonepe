import os
import json
import mysql.connector

# ✅ Safe extractor
def extract_number(val):
    try:
        if isinstance(val, list):
            return float(val[0]) if val else 0.0
        elif isinstance(val, (int, float)):
            return float(val)
    except:
        pass
    return 0.0

# ✅ MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # change if needed
    database="phonepe_insights"
)
cursor = conn.cursor()

base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\map\insurance\hover\country\india\state"

inserted = 0
skipped = 0

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

                            insurance_data = data.get("data", {}).get("hoverDataList", [])

                            if not insurance_data:
                                skipped += 1
                                continue

                            for item in insurance_data:
                                district = item.get("name", "Unknown")
                                metric = int(extract_number(item.get("metric", 0)))
                                amount = float(extract_number(item.get("amount", 0.0)))

                                cursor.execute("""
                                    INSERT INTO map_insurance (state, year, quarter, district, metric, amount)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """, (state, int(year), quarter, district, metric, amount))
                                conn.commit()
                                inserted += 1

                        except Exception as e:
                            print(f"❌ Error in {file_path}: {e}")
                            skipped += 1

cursor.execute("SELECT COUNT(*) FROM map_insurance")
total = cursor.fetchone()[0]

print("\n✅ Map Insurance Insertion Complete!")
print("➕ Rows inserted:", inserted)
print("⏭️ Rows skipped:", skipped)
print("📊 Total rows in map_insurance:", total)

cursor.close()
conn.close()
