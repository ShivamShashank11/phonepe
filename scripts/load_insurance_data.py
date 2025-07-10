import os
import json
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ------------------------------
# Database connection setup
# ------------------------------
password = quote_plus("Nicky@123")
engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/phonepe_insights")

# ------------------------------
# Folder path to state-wise JSON files
# ------------------------------
base_path = r"C:\Users\Shivam Shashank\Desktop\phonepe\data\aggregated\insurance\india\state"

# ------------------------------
# Process all JSON files
# ------------------------------
records = []

for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                if file.endswith(".json"):
                    quarter = int(file.replace(".json", ""))
                    with open(os.path.join(year_path, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data.get("data") and "transactionData" in data["data"]:
                            for txn in data["data"]["transactionData"]:
                                for instrument in txn.get("paymentInstruments", []):
                                    records.append({
                                        "state": state,
                                        "year": int(year),
                                        "quarter": quarter,
                                        "count": instrument.get("count", 0),
                                        "amount": instrument.get("amount", 0.0)
                                    })

# ------------------------------
# Load into DataFrame and Database
# ------------------------------
df = pd.DataFrame(records)

# Optional: clean state names
df["state"] = df["state"].str.replace("&", "and").str.replace("-", " ").str.title()

# Load into database (append mode)
df.to_sql("aggregated_insurance", con=engine, if_exists="append", index=False)

print("✅ Data inserted successfully:", df.shape)
