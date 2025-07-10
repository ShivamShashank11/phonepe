import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nicky@123",  # 🔁 Replace with your MySQL password
    database="phonepe_insights"
)

# ✅ SQL Query
query = """
SELECT state, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;
"""

# ✅ Fetch Data into DataFrame
df = pd.read_sql(query, conn)
conn.close()

# ✅ Plot using Seaborn
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='state', y='total_amount', palette='magma')
plt.xticks(rotation=45)
plt.title('Top 10 States by Transaction Amount (PhonePe)')
plt.xlabel('State')
plt.ylabel('Total Amount (₹)')
plt.tight_layout()
plt.show()
