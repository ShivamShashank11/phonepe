import os
import json
import mysql.connector
from datetime import datetime

# ✅ MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # ← Apna password
    database="phonepe_insights"
)
cursor = conn.cursor()

# ✅ Base path to all transaction data
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\transaction\country\india\state"

inserted = 0
skipped = 0

# ✅ Loop over state/year/quarter-wise JSON files
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

                            from_ts = data.get("data", {}).get("from")
                            to_ts = data.get("data", {}).get("to")
                            transactions = data.get("data", {}).get("transactionData", [])

                            if not (from_ts and to_ts and transactions):
                                skipped += 1
                                continue

                            from_date = datetime.fromtimestamp(from_ts / 1000)
                            to_date = datetime.fromtimestamp(to_ts / 1000)

                            for tx in transactions:
                                tx_type = tx.get("name")
                                instruments = tx.get("paymentInstruments", [])
                                for instrument in instruments:
                                    count = int(instrument.get("count", 0))
                                    amount = float(instrument.get("amount", 0.0))

                                    cursor.execute("""
                                        INSERT INTO aggregated_transaction (
                                            state, year, quarter, from_date, to_date,
                                            transaction_type, transaction_count, transaction_amount
                                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (
                                        state, int(year), quarter,
                                        from_date, to_date,
                                        tx_type, count, amount
                                    ))
                                    conn.commit()
                                    inserted += 1

                        except Exception as e:
                            print(f"❌ Error in {file_path}: {e}")
                            skipped += 1

# ✅ Final Summary
cursor.execute("SELECT COUNT(*) FROM aggregated_transaction")
total = cursor.fetchone()[0]

print("\n✅ Insertion complete!")
print("➕ Rows inserted:", inserted)
print("⏭️ Rows skipped:", skipped)
print("📊 Total rows in DB:", total)

cursor.close()
conn.close()
