import os
import json
import mysql.connector
import pandas as pd
from datetime import datetime

# ✅ MySQL Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # 🔁 CHANGE THIS to your MySQL password
    database="phonepe_insights"
)
cursor = connection.cursor()

# ✅ Correct path to your insurance data folder
# 🔁 Update path
base_path = r'C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\insurance\country\india\state'


inserted = 0  # counter for inserted rows

# ✅ Loop through each state folder
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
                            print(f"📂 Processing: {state} | {year} | Q{quarter} | File: {file}")

                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                trans_data = data.get("data", {}).get("transactionData", [])

                                if trans_data:
                                    payment_info = trans_data[0].get("paymentInstruments", [])[0]
                                    from_ts = data["data"]["from"]
                                    to_ts = data["data"]["to"]

                                    # Convert timestamps to MySQL datetime
                                    from_date = datetime.fromtimestamp(from_ts / 1000)
                                    to_date = datetime.fromtimestamp(to_ts / 1000)

                                    count = payment_info.get("count", 0)
                                    amount = payment_info.get("amount", 0.0)

                                    # ✅ Insert into MySQL
                                    insert_query = """
                                        INSERT INTO aggregated_insurance (state, year, quarter, from_date, to_date, count, amount)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                                    """
                                    cursor.execute(insert_query, (
                                        state, int(year), quarter, from_date, to_date, count, amount
                                    ))
                                    connection.commit()
                                    inserted += 1
                                else:
                                    print(f"⚠️ No transaction data in: {file_path}")

                        except Exception as e:
                            print(f"❌ Error processing {file_path}: {e}")

# ✅ Final Status
print(f"\n✅ Data Insertion Complete. Total Rows Inserted: {inserted}")
cursor.close()
connection.close()
