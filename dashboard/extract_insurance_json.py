import os
import json
import pandas as pd

base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\insurance\india\state"
output_rows = []

for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)

        for q in ['1.json', '2.json', '3.json', '4.json']:
            file_path = os.path.join(year_path, q)
            if not os.path.exists(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    continue

            transactions = data.get("data", {}).get("transactionData", [])
            for txn in transactions:
                instruments = txn.get("paymentInstruments", [])
                for item in instruments:
                    if item["type"] == "TOTAL":
                        output_rows.append({
                            "state": state,
                            "district": "All Districts",  # No district data in these files
                            "year": int(year),
                            "quarter": int(q.split(".")[0]),
                            "count": item.get("count", 0),
                            "amount": item.get("amount", 0.0)
                        })

# Convert to DataFrame and save
df = pd.DataFrame(output_rows)
df.to_csv("insurance_district_fallback.csv", index=False)
print("✅ insurance_district_fallback.csv generated successfully.")
