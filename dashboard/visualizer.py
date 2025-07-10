import plotly.express as px
import streamlit as st

def plot_choropleth(df_map, india_states, data_type, selected_quarter, selected_year):
    fig = px.choropleth(
        df_map,
        geojson=india_states,
        locations="state",
        featureidkey="properties.ST_NM",
        color="total_crores",
        hover_name="state",
        title=f"🗺️ {data_type} Volume by State | Q{selected_quarter} {selected_year}",
        color_continuous_scale="Viridis"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

def plot_bar(df, x_col, y_col, title):
    fig = px.bar(df, x=x_col, y=y_col, title=title, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_line(df_time, state, data_type):
    fig_line = px.line(df_time, x=df_time.index, y="total_value", title="Time Trend")
    fig_line.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=df_time.index,
            ticktext=[f"Y{y} Q{q}" for y, q in zip(df_time['year'], df_time['quarter'])]
        )
    )
    st.subheader(f"📈 {data_type} Trend Over Time in {state.title()}")
    st.plotly_chart(fig_line, use_container_width=True)
