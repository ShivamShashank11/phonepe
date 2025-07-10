import os
import json
import mysql.connector
from datetime import datetime

# ✅ MySQL Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # 🔁 Your MySQL password
    database="phonepe_insights"
)
cursor = connection.cursor()

# ✅ Base path to your transaction data
base_path = r'C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\transaction\country\india\state'

inserted = 0

# ✅ Traverse: state > year > JSON
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

                                from_ts = data["data"]["from"]
                                to_ts = data["data"]["to"]

                                from_date = datetime.fromtimestamp(from_ts / 1000.0)
                                to_date = datetime.fromtimestamp(to_ts / 1000.0)

                                transaction_data = data.get("data", {}).get("transactionData", [])

                                for entry in transaction_data:
                                    trans_type = entry.get("name", "Unknown")
                                    instruments = entry.get("paymentInstruments", [])

                                    for instrument in instruments:
                                        count = instrument.get("count", 0)
                                        amount = instrument.get("amount", 0.0)

                                        insert_query = """
                                            INSERT INTO aggregated_transaction (
                                                state, year, quarter, from_date, to_date,
                                                transaction_type, transaction_count, transaction_amount
                                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                        """
                                        cursor.execute(insert_query, (
                                            state, int(year), quarter,
                                            from_date, to_date,
                                            trans_type, count, amount
                                        ))
                                        connection.commit()
                                        inserted += 1
                        except Exception as e:
                            print(f"❌ Error in {file_path}: {e}")

# ✅ Summary
cursor.execute("SELECT COUNT(*) FROM aggregated_transaction")
total = cursor.fetchone()[0]

print(f"\n✅ Inserted rows: {inserted}")
print(f"📊 Total rows now in aggregated_transaction table: {total}")

cursor.close()
connection.close()
