# 📁 File: pages/components/area_chart_section.py

import pandas as pd
import streamlit as st
import plotly.express as px

def render_area_chart(engine, table_name, state, selected_type, cols, data_type):
    y_col = cols.get("amount") or cols.get("count")
    category_col = cols.get("category")

    # SQL Filter: If category type exists (e.g. brand or transaction_type)
    category_filter = f"AND {category_col} = '{selected_type}'" if selected_type and category_col else ""

    query = f"""
        SELECT CONCAT(year, ' Q', quarter) AS period, SUM({y_col}) AS total
        FROM {table_name}
        WHERE state = '{state}' {category_filter}
        GROUP BY year, quarter
        ORDER BY year, quarter
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        st.warning("⚠️ No data available for area chart.")
        return

    st.subheader(f"🌊 {data_type} Area Chart in {state.title()} Over Time")

    fig = px.area(
        df,
        x="period",
        y="total",
        title=f"{data_type} Cumulative Trend by Quarter",
        labels={"period": "Year - Quarter", "total": "Total"},
        color_discrete_sequence=["#FF6F00"],
        markers=True
    )

    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#0f0f0f",
        font_color="#FFA500",
        xaxis=dict(showgrid=False, title="Quarter"),
        yaxis=dict(showgrid=True, gridcolor="#333", title="Total Value")
    )

    st.plotly_chart(fig, use_container_width=True)
