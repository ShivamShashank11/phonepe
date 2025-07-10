# pages/components/line_chart_section.py
import pandas as pd
import streamlit as st
import plotly.express as px

def render_line_chart(engine, table_name, state, selected_type, cols, data_type):
    y_col = cols.get("amount") or cols.get("count")
    category_col = cols.get("category")
    category_filter = f"AND {category_col} = '{selected_type}'" if category_col and selected_type else ""

    query = f"""
        SELECT CONCAT(year, ' Q', quarter) AS period, SUM({y_col}) AS total
        FROM {table_name}
        WHERE state = '{state}' {category_filter}
        GROUP BY year, quarter
        ORDER BY year, quarter
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        st.warning("⚠️ No data available for time series chart.")
        return

    st.subheader(f"📈 {data_type} Growth in :orange[{state.title()}] Over Time")

    fig = px.line(
        df,
        x="period",
        y="total",
        title=f"{data_type} Trends | {state.title()}",
        markers=True,
        line_shape="spline",
        labels={"period": "Year - Quarter", "total": "Total Value"},
        color_discrete_sequence=["#FFA500"]
    )

    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#0f0f0f",
        font_color="#FFA500",
        title_font_color="#FFA500",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#444"),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
