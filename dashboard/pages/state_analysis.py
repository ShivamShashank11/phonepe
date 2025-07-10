# state_analysis.py
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---------- PAGE CONFIG ----------
st.set_page_config(layout="wide", page_title="📊 State-wise Analysis")
st.markdown("""
    <style>
    body, .stApp {
        background-color: #000000;
        color: #FFA500;
    }
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #FFA500;
    }
    h1, h2, h3, h4, h5, h6, div, span, p {
        color: #FFA500 !important;
    }
    .css-1v0mbdj, .css-ffhzg2 {
        color: #FFA500 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title(":bar_chart: :orange[State-wise District Analysis]")

# ---------- DB CONNECTION ----------
password = quote_plus("Nicky@123")
engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost:3306/phonepe_insights")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filter")
data_type = st.sidebar.selectbox("Select Data Type", ["Transaction", "Insurance"])

table_map = {
    "Transaction": "map_transaction",
    "Insurance": "map_insurance"
}

# Always pull filter options from "aggregated_transaction" table
years = pd.read_sql("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year", engine)["year"].tolist()
quarters = pd.read_sql("SELECT DISTINCT quarter FROM aggregated_transaction ORDER BY quarter", engine)["quarter"].tolist()
states = pd.read_sql("SELECT DISTINCT state FROM aggregated_transaction ORDER BY state", engine)["state"].tolist()

selected_year = st.sidebar.selectbox("Select Year", years)
selected_quarter = st.sidebar.selectbox("Select Quarter", quarters)
selected_state = st.sidebar.selectbox("Select State", states)

# ---------- QUERY DATA ----------
map_table = table_map[data_type]

df = pd.read_sql(f"""
    SELECT district, SUM(amount) AS amount
    FROM {map_table}
    WHERE state = '{selected_state}' AND year = {selected_year} AND quarter = {selected_quarter}
    GROUP BY district
    ORDER BY amount DESC
    LIMIT 10
""", engine)

# ---------- TITLE & LABEL ----------
chart_title = f"Top 10 Districts in {selected_state.title()} by {data_type} Volume (Q{selected_quarter} {selected_year})"
y_label = f"{data_type} Amount"

# ---------- CHART ----------
if df.empty:
    st.warning("⚠️ No data available for selected filters.")
else:
    fig = px.bar(
        df,
        x="district",
        y="amount",
        color="amount",
        color_continuous_scale="inferno",
        labels={"district": "District", "amount": y_label},
        title=chart_title
    )
    fig.update_layout(
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="#FFA500",
        title_font_color="#FFA500",
        xaxis_title="District",
        yaxis_title=y_label
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- FOOTER ----------
st.caption("📊 Data Source: PhonePe | Theme: Ultra Black + Orange | Built by Shivam Shashank")
