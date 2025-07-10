import streamlit as st
import pandas as pd
import plotly.express as px

def render_pie_chart(engine, table_name, year, quarter, state, cols):
    category_col = cols.get("category")
    value_col = cols.get("amount") or cols.get("count")

    if not category_col:
        return  # Skip if no category column

    query = f"""
        SELECT {category_col} AS category, SUM({value_col}) AS total
        FROM {table_name}
        WHERE year = {year} AND quarter = {quarter} AND state = '{state}'
        GROUP BY {category_col}
        ORDER BY total DESC
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return

    st.subheader("📊 Category-Wise Distribution")

    fig = px.pie(
        df,
        names="category",
        values="total",
        color_discrete_sequence=px.colors.sequential.Inferno
    )

    fig.update_layout(
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        font_color='#FFA500',
        title_font_color='#FFA500',
        legend_font_color='#FFA500'
    )

    st.plotly_chart(fig, use_container_width=True)
