import os
import json
import pandas as pd

base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\map\insurance\india\state"

records = []

for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for file in os.listdir(year_path):
            if not file.endswith(".json"):
                continue

            quarter = int(file.replace(".json", ""))
            file_path = os.path.join(year_path, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    hover_data = data.get("data", {}).get("hoverData", {})
                    for district, values in hover_data.items():
                        metric = values.get("metric", 0)
                        amount = values.get("amount", 0.0)

                        records.append({
                            "state": state,
                            "year": int(year),
                            "quarter": quarter,
                            "district": district,
                            "metric": metric,
                            "amount": amount
                        })

            except Exception as e:
                print(f"Error parsing {file_path}: {e}")

# Convert to DataFrame
df = pd.DataFrame(records)

# Save to CSV
csv_path = r"C:\Users\Shivam Shashank\Desktop\phonepay\dashboard\parsed_map_insurance.csv"
df.to_csv(csv_path, index=False)

print("✅ Parsing complete. CSV saved at:", csv_path)
