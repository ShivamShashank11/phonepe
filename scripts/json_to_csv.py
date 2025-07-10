import json
import pandas as pd
import os

# JSON data string (replace this with file reading for real use)
data_json = '''{
  "success": true,
  "code": "SUCCESS",
  "data": {
    "meta": {
      "dataLevel": "STATE",
      "gridLevel": 11,
      "percentiles": {
        "10.0": 1,
        "20.0": 1,
        "40.0": 2,
        "80.0": 4,
        "90.0": 7,
        "99.5": 82,
        "50.0": 2,
        "30.0": 1,
        "60.0": 2
      }
    },
    "data": {
      "columns": ["lat", "lng", "metric", "label"],
      "data": [
        [25.588703810097638, 85.15312162928252, 492.0, "patna district"],
        [25.587327268291588, 85.11162636754604, 471.0, "patna district"]
      ]
    }
  }
}'''

# Parse JSON
parsed_data = json.loads(data_json)

# Extract and convert to DataFrame
columns = parsed_data['data']['data']['columns']
rows = parsed_data['data']['data']['data']
df = pd.DataFrame(rows, columns=columns)

# Create output folder if it doesn't exist
output_folder = os.path.join(os.path.dirname(__file__), '../data/processed')
os.makedirs(output_folder, exist_ok=True)

# Save to CSV
output_path = os.path.join(output_folder, 'district_metrics.csv')
df.to_csv(output_path, index=False)

print("✅ CSV file saved to:", output_path)
print(df.head())
