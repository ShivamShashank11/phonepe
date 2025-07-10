import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---------- COMPONENTS ----------
from pages.components.pie_chart_section import render_pie_chart
from pages.components.line_chart_section import render_line_chart
from pages.components.bar_chart_section import render_bar_chart
from pages.components.area_chart_section import render_area_chart
from pages.components.ai_predictor import predict_growth
from pages.components.district_user_map import render_district_user_data

# ---------- AI Insight Function ----------
def generate_insight(df, data_type):
    latest = df.iloc[-1]['total']
    previous = df.iloc[-2]['total'] if len(df) > 1 else None
    if previous:
        growth = ((latest - previous) / previous) * 100
        if growth > 0:
            return f"{data_type} has increased by {growth:.2f}% compared to the last quarter."
        elif growth < 0:
            return f"{data_type} has decreased by {abs(growth):.2f}% compared to the last quarter."
        else:
            return f"{data_type} remained stable compared to the last quarter."
    return f"Latest {data_type} value is {latest:,}."

# ---------- PAGE CONFIG ----------
st.set_page_config(layout="wide", page_title="📱 PhonePe AI Dashboard")

# ---------- CUSTOM CSS ----------
css = '''
<style>
body, .stApp { background-color: #000000 !important; color: #FFA500 !important; }
[data-testid="stSidebar"] {
    background-color: #000000 !important;
    color: #FFA500 !important;
    border-right: 1px solid #FFA500;
}
[data-testid="stAppViewContainer"] > .main {
    background-color: #000000 !important;
    color: #FFA500 !important;
}
h1, h2, h3, h4, h5, h6, p, div, span {
    color: #FFA500 !important;
}
[data-testid="stMetricValue"] {
    color: #FFA500 !important;
}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# ---------- HEADER IMAGE ----------
image_path = os.path.join("assets", "img1.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("⚠️ Banner image not found.")

# ---------- TITLE ----------
st.title("📱 PhonePe AI Dashboard")

# ---------- INTRODUCTION ----------
with st.expander("📘 Project Introduction", expanded=True):
    st.markdown("""
### 📌 **Project Title:** PhonePe Transaction Insights  
#### 💼 **Domain:** Digital Payments & Financial Analytics  
#### 📊 **Tools Used:** Python, SQL, Streamlit, Plotly, MySQL

---

**📝 Problem Statement:**  
With the growing use of PhonePe and digital payments, analyzing transactions, user activity, and insurance data helps improve services and understand market trends. This dashboard enables interactive analysis and visualization of state/district-level data and top-performing zones.

**🔍 Business Use Cases:**
- **Customer Segmentation:** Classify users by behavior.
- **Fraud Detection:** Spot irregular transactions.
- **Geographical Insights:** Map user behavior across India.
- **Performance Metrics:** Measure transaction volumes/types.
- **User Engagement:** Track and improve retention.
- **Product Development:** Data-backed feature innovation.
- **Insurance Analytics:** Analyze digital insurance usage.
- **Marketing Optimization:** Improve targeting using trends.
- **Trend Analysis:** Spot rising/declining patterns.
- **Competitive Benchmarking:** Compare zones/state-wise growth.

**🛠️ Project Approach:**
- Data extracted from GitHub → structured in MySQL.
- Created tables: aggregated, map, top (for user, transaction, insurance).
- SQL queries written for analytical insights.
- Python + Pandas used for data wrangling.
- Visualizations built using Plotly + Streamlit (dark UI).

**✅ Skills Gained:**  
Data Extraction | SQL Proficiency | Streamlit UI | Analytical Thinking | Data Visualization | ETL Pipelines

**📂 Tech Stack:**  
Python | SQL | Streamlit | Pandas | Plotly | MySQL | GeoJSON

---
""")

# ---------- DB CONNECTION ----------
password = quote_plus("Nicky@123")
engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/phonepe_insights")

# ---------- GEOJSON ----------
geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
india_states = requests.get(geo_url).json()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("📜 Filters")
data_type = st.sidebar.selectbox("Select Data Type", ["Transaction", "User", "Insurance"])

# ✅ API KEY CHECK ----------
token_loaded = 'OPENAI_API_KEY' in st.secrets
st.sidebar.markdown(f"🔐 API Key Loaded: {token_loaded}")

# ---------- MAPPINGS ----------
table_map = {
    "Transaction": "aggregated_transaction",
    "User": "aggregated_user",
    "Insurance": "aggregated_insurance"
}
column_map = {
    "Transaction": {"count": "transaction_count", "amount": "transaction_amount", "category": "transaction_type"},
    "User": {"count": "registered_users", "amount": None, "percentage": "brand_percentage", "category": "brand"},
    "Insurance": {"count": "count", "amount": "amount", "category": None}
}
map_table_map = {
    "Transaction": "map_transaction",
    "User": "map_user",
    "Insurance": "map_insurance"
}

# ---------- FILTER VALUES ----------
table_name = table_map[data_type]
cols = column_map[data_type]
states = pd.read_sql(f"SELECT DISTINCT state FROM {table_name} ORDER BY state", engine)["state"].tolist()
selected_state = st.sidebar.selectbox("Select State", states)

if data_type == "User":
    years = pd.read_sql("SELECT DISTINCT year FROM top_user ORDER BY year", engine)["year"].tolist()
    quarters = pd.read_sql("SELECT DISTINCT quarter FROM top_user ORDER BY quarter", engine)["quarter"].tolist()
else:
    years = pd.read_sql(f"SELECT DISTINCT year FROM {table_name} ORDER BY year", engine)["year"].tolist()
    quarters = pd.read_sql(f"SELECT DISTINCT quarter FROM {table_name} ORDER BY quarter", engine)["quarter"].tolist()

selected_year = st.sidebar.selectbox("Select Year", years)
selected_quarter = st.sidebar.selectbox("Select Quarter", quarters)

if cols["category"]:
    categories = pd.read_sql(f"SELECT DISTINCT {cols['category']} AS category FROM {table_name} ORDER BY category", engine)["category"].tolist()
    selected_type = st.sidebar.selectbox("Select Type", categories)
else:
    selected_type = None

# ---------- METRICS ----------
metrics_query = f"SELECT SUM({cols['count']}) AS total_count"
if cols.get("amount"):
    metrics_query += f", SUM({cols['amount']}) AS total_amount"
if cols.get("percentage"):
    metrics_query += f", AVG({cols['percentage']}) AS avg_percentage"
metrics_query += f" FROM {table_name} WHERE year={selected_year} AND quarter={selected_quarter} AND state='{selected_state}'"
if selected_type:
    metrics_query += f" AND {cols['category']} = '{selected_type}'"

metrics = pd.read_sql(metrics_query, engine)
col1, col2, col3 = st.columns(3)
col1.metric("Total Count", f"{int(metrics['total_count'][0]):,}" if metrics['total_count'][0] else "N/A")
if data_type == "User" and metrics.get("avg_percentage")[0]:
    col2.metric("Avg. % Share", f"{metrics['avg_percentage'][0]:.2f}%")
elif metrics.get("total_amount") is not None and metrics["total_amount"][0]:
    col2.metric("Total Amount", f"₹{metrics['total_amount'][0]:,.2f}")

# ---------- AI FORECAST ----------
value_col = cols.get("amount") or cols.get("count")
trend_df = pd.read_sql(f"SELECT year, quarter, SUM({value_col}) as total FROM {table_name} WHERE state='{selected_state}' GROUP BY year, quarter ORDER BY year, quarter", engine)
if not trend_df.empty:
    prediction = predict_growth(trend_df)
    col3.metric("AI Forecast", f"₹{prediction:,.2f}" if cols.get("amount") else f"{int(prediction):,}")

# ---------- STATE MAP ----------
map_col = cols["amount"] if data_type != "User" else cols["count"]
query_map = f"""
SELECT state, ROUND(SUM({map_col})/10000000, 2) AS total_crores
FROM {table_name}
WHERE year = {selected_year} AND quarter = {selected_quarter}
{f"AND {cols['category']} = '{selected_type}'" if selected_type else ""}
GROUP BY state
"""
df_map = pd.read_sql(query_map, engine)
df_map["state"] = df_map["state"].str.replace("-", " ").str.title().replace({
    "Andaman & Nicobar Islands": "Andaman & Nicobar",
    "Nct Of Delhi": "Delhi",
    "Jammu & Kashmir": "Jammu & Kashmir"
})

st.subheader("🌐 State-Wise Map")
fig_map = px.choropleth(
    df_map,
    geojson=india_states,
    locations="state",
    featureidkey="properties.ST_NM",
    color="total_crores",
    hover_name="state",
    color_continuous_scale="inferno",
    title=f"{data_type} by State | Q{selected_quarter} {selected_year}",
    height=650
)
fig_map.update_geos(fitbounds="locations", visible=False, bgcolor='rgba(0,0,0,0)')
fig_map.update_layout(paper_bgcolor='#000000', font_color='#FFA500')
st.plotly_chart(fig_map, use_container_width=True)

# ---------- DISTRICT-WISE BAR ----------
map_table = map_table_map[data_type]
district_map_col = "registered_users" if data_type == "User" else "amount"
df_district = pd.read_sql(f"""
    SELECT district, SUM({district_map_col}) AS total
    FROM {map_table}
    WHERE year = {selected_year} AND quarter = {selected_quarter} AND state = '{selected_state}'
    GROUP BY district
    ORDER BY total DESC
    LIMIT 10
""", engine)

if not df_district.empty:
    st.subheader(f"🏩 Top Districts in {selected_state.title()} by {data_type}")
    fig_bar = go.Figure(data=go.Bar(
        x=df_district["total"],
        y=df_district["district"],
        orientation='h',
        marker=dict(color='orange')
    ))
    fig_bar.update_layout(
        yaxis=dict(autorange="reversed"),
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        font=dict(color='#FFA500'),
        height=450
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------- LOCAL JSON DISTRICT USER DATA ----------
if data_type == "User":
    render_district_user_data(selected_state, selected_year)

# ---------- CHARTS ----------
render_pie_chart(engine, table_name, selected_year, selected_quarter, selected_state, cols)
render_line_chart(engine, table_name, selected_state, selected_type, cols, data_type)
render_area_chart(engine, table_name, selected_state, selected_type, cols, data_type)
render_bar_chart(engine, table_name, selected_year, selected_quarter, value_col, cols.get("category"))

# ---------- AI INSIGHT ----------
insight_df = pd.read_sql(f"""
    SELECT year, quarter, SUM({value_col}) as total
    FROM {table_name}
    WHERE state='{selected_state}'
    GROUP BY year, quarter
    ORDER BY year, quarter
""", engine)
if not insight_df.empty:
    ai_insight = generate_insight(insight_df, data_type)
    st.markdown(f"**💡 AI Insight:** {ai_insight}")

st.caption("Data Source: PhonePe | Built by Shivam Shashank")
