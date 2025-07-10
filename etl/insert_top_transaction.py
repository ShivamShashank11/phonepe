import os
import json
import mysql.connector

# ✅ MySQL Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # 🔁 Replace with your MySQL password
    database="phonepe_insights"
)
cursor = connection.cursor()

# ✅ Path to top transaction data
base_path = r'C:\Users\Shivam Shashank\Desktop\phonepe\data\top\transaction\country\india\state'

inserted = 0

# ✅ Traverse state → year → files
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    if file.endswith('.json'):
                        try:
                            quarter = int(file.replace('.json', ''))
                            file_path = os.path.join(year_path, file)
                            print(f"📂 Processing: {state} | {year} | Q{quarter} | File: {file}")

                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)

                                for category in ["districts", "pincodes"]:
                                    items = data.get("data", {}).get(category, [])
                                    for item in items:
                                        name = item.get("entityName", "Unknown")
                                        metric_data = item.get("metric", {})
                                        data_type = metric_data.get("type", category[:-1])
                                        count = metric_data.get("count", 0)
                                        amount = metric_data.get("amount", 0.0)

                                        insert_query = """
                                            INSERT INTO top_transaction
                                            (state, year, quarter, name, type, count, amount)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                                        """
                                        cursor.execute(insert_query, (
                                            state, int(year), quarter, name, data_type, count, amount
                                        ))
                                        connection.commit()
                                        inserted += 1

                        except Exception as e:
                            print(f"❌ Error processing {file_path}: {e}")

# ✅ Count check
cursor.execute("SELECT COUNT(*) FROM top_transaction")
count = cursor.fetchone()[0]
print(f"\n✅ Top Transaction Insertion Complete. Rows Inserted: {inserted}")
print(f"🔢 Total rows now in table: {count}")

cursor.close()
connection.close()
