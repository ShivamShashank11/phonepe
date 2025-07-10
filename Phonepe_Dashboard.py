# ----------------------
# Export Final Summary CSVs (All States & Districts)
# ----------------------
st.subheader("📁 Download Final Summary CSVs")

# ✅ State-Level Summary
query_state = """
SELECT 
    t.state,
    t.year,
    t.quarter,
    SUM(t.transaction_count) AS total_transactions,
    ROUND(SUM(t.transaction_amount)/10000000, 2) AS total_amount_cr,
    COALESCE(SUM(u.registered_users), 0) AS total_users,
    ROUND(COALESCE(SUM(i.amount), 0)/10000000, 2) AS insurance_amount_cr
FROM aggregated_transaction t
LEFT JOIN aggregated_user u ON t.state = u.state AND t.year = u.year AND t.quarter = u.quarter
LEFT JOIN aggregated_insurance i ON t.state = i.state AND t.year = i.year AND t.quarter = i.quarter
GROUP BY t.state, t.year, t.quarter
ORDER BY t.year, t.quarter, t.state
"""
df_state_summary = pd.read_sql(query_state, engine)
st.download_button("📄 Download State-Level Summary", data=df_state_summary.to_csv(index=False), file_name="State_Level_Summary.csv")

# ✅ District-Level Summary
query_district = """
SELECT 
    state,
    district,
    year,
    quarter,
    SUM(amount) AS total_transaction_amount
FROM map_transaction
GROUP BY state, district, year, quarter
ORDER BY year, quarter, total_transaction_amount DESC
"""
df_district_summary = pd.read_sql(query_district, engine)
df_district_summary["total_transaction_amount"] = (df_district_summary["total_transaction_amount"] / 10000000).round(2)
st.download_button("🏙️ Download District-Level Summary", data=df_district_summary.to_csv(index=False), file_name="District_Level_Summary.csv")
