# 📄 dashboard/load_insurance_map_data.py

import os
import json
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ✅ MySQL Connection
password = quote_plus("Nicky@123")
engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/phonepe_insights")

# ✅ Base path to your JSON files
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\insurance\india\state"

# ✅ Collect all rows
rows = []

# ✅ Traverse each state folder
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for quarter_file in ['1.json', '2.json', '3.json', '4.json']:
            file_path = os.path.join(year_path, quarter_file)
            if not os.path.exists(file_path):
                print(f"❌ Missing: {file_path}")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"⚠️ Error parsing {file_path}: {e}")
                continue

            transactions = data.get("data", {}).get("transactionData", [])
            for txn in transactions:
                instruments = txn.get("paymentInstruments", [])
                for item in instruments:
                    rows.append({
                        "state": state,
                        "year": int(year),
                        "quarter": int(quarter_file.split(".")[0]),
                        "district": "All Districts",  # Since no district data
                        "metric": item.get("count", 0),
                        "amount": item.get("amount", 0.0)
                    })

# ✅ Save to DataFrame
df = pd.DataFrame(rows)

# ✅ Preview
print(df.head())
print(f"✅ Total records: {len(df)}")

# ✅ Insert to MySQL
if not df.empty:
    df.to_sql("map_insurance", con=engine, if_exists="append", index=False)
    print("✅ Inserted data into map_insurance table.")
else:
    print("⚠️ No data available to insert.")
