import os
import json
import mysql.connector

# ✅ MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # update if needed
    database="phonepe_insights"
)
cursor = conn.cursor()

# ✅ Data path
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\top\insurance\country\india\state"

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
                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)

                            for category in ["districts", "pincodes"]:
                                records = data.get("data", {}).get(category, [])
                                if not records:
                                    continue

                                for item in records:
                                    name = item.get("entityName", "Unknown")
                                    metric = item.get("metric", {})

                                    m_type = metric.get("type", "TOTAL")
                                    count = int(metric.get("count", 0))
                                    amount = float(metric.get("amount", 0.0))

                                    cursor.execute("""
                                        INSERT INTO top_insurance (state, year, quarter, name, type, count, amount)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                                    """, (state, int(year), quarter, name, m_type, count, amount))
                                    conn.commit()
                                    inserted += 1

                        except Exception as e:
                            print(f"❌ Error in {file_path}: {e}")
                            skipped += 1

# ✅ Summary
cursor.execute("SELECT COUNT(*) FROM top_insurance")
total = cursor.fetchone()[0]

print("\n✅ Top Insurance Insertion Complete!")
print("➕ Rows inserted:", inserted)
print("⏭️ Rows skipped:", skipped)
print("📊 Total rows in top_insurance:", total)

cursor.close()
conn.close()

