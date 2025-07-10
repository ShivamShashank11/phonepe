import os
import json
import mysql.connector

# Set your base path
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\insurance\india\state"

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",
    database="phonepe_insights"
)
cursor = conn.cursor()

# Loop through states
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for file in os.listdir(year_path):
            if file.endswith(".json"):
                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_path, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                transaction_data = data.get("data", {}).get("transactionData", [])
                for entry in transaction_data:
                    instruments = entry.get("paymentInstruments", [])
                    for ins in instruments:
                        if ins["type"] == "TOTAL":
                            count = ins.get("count", 0)
                            amount = ins.get("amount", 0.0)
                            cursor.execute("""
                                INSERT INTO map_insurance (state, year, quarter, district, metric, amount)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """, (state, int(year), quarter, "All Districts", count, amount))
                            print(f"Inserted: {state} {year} Q{quarter}")

conn.commit()
cursor.close()
conn.close()
print("✅ Done inserting map_insurance data with 'All Districts'.")
