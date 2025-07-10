# 📁 File: pages/components/bar_chart_section.py

import pandas as pd
import streamlit as st
import plotly.express as px

def render_bar_chart(engine, table_name, year, quarter, value_col, category_col=None):
    filter_clause = f"WHERE year = {year} AND quarter = {quarter}"

    if category_col:
        query = f"""
            SELECT {category_col} AS category, SUM({value_col}) AS total
            FROM {table_name}
            {filter_clause}
            GROUP BY category
            ORDER BY total DESC
        """
        label = category_col.replace('_', ' ').title()
    else:
        query = f"""
            SELECT state AS category, SUM({value_col}) AS total
            FROM {table_name}
            {filter_clause}
            GROUP BY category
            ORDER BY total DESC
        """
        label = "State"

    df = pd.read_sql(query, engine)

    if df.empty:
        st.warning("⚠️ No data available for the selected filters.")
        return

    st.subheader(f"📊 Bar Chart: {label}-wise Distribution (Q{quarter} {year})")

    fig = px.bar(
        df,
        x="category",
        y="total",
        text="total",
        color="total",
        color_continuous_scale="inferno",
        labels={"category": label, "total": "Total Value"},
        height=500
    )

    fig.update_traces(
        texttemplate='%{text:.2s}',
        textposition='outside'
    )
    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#0f0f0f",
        font_color="#FFA500",
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis_tickangle=-30
    )

    st.plotly_chart(fig, use_container_width=True)
