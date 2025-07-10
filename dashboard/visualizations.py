import plotly.express as px

def draw_choropleth(df, geojson, col, year, quarter, data_type):
    fig = px.choropleth(
        df, geojson=geojson, locations="state", featureidkey="properties.ST_NM",
        color=col, hover_name="state",
        title=f"🗺️ {data_type} Volume by State | Q{quarter} {year}",
        color_continuous_scale="Viridis"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
    return fig

def draw_bar(df, x, y, title):
    return px.bar(df, x=x, y=y, title=title, text_auto=True)

def draw_line(df, x_idx, y, year_col, quarter_col, state, data_type):
    fig = px.line(df, x=x_idx, y=y, title=f"{data_type} Trend Over Time in {state}")
    fig.update_layout(xaxis=dict(
        tickmode='array',
        tickvals=df.index,
        ticktext=[f"Y{y} Q{q}" for y, q in zip(df[year_col], df[quarter_col])]
    ))
    return fig
