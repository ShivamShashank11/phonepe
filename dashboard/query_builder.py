def build_metric_query(table_name, cols, year, quarter, state, selected_type=None):
    parts = []
    if cols.get("count"):
        parts.append(f"SUM({cols['count']}) AS total_count")
    if cols.get("amount"):
        parts.append(f"SUM({cols['amount']}) AS total_amount")
    if cols.get("percentage"):
        parts.append(f"AVG({cols['percentage']}) AS avg_percentage")

    condition = f"""
        WHERE year = {year}
        AND quarter = {quarter}
        AND state = '{state}'
    """
    if selected_type and cols.get("category"):
        condition += f" AND {cols['category']} = '{selected_type}'"

    return f"SELECT {', '.join(parts)} FROM {table_name} {condition}"

def build_map_query(table_name, map_col, year, quarter, category_col=None, selected_type=None):
    where_clause = f"WHERE year = {year} AND quarter = {quarter}"
    if category_col and selected_type:
        where_clause += f" AND {category_col} = '{selected_type}'"

    return f"""
        SELECT state, ROUND(SUM({map_col})/10000000, 2) AS total_crores
        FROM {table_name}
        {where_clause}
        GROUP BY state
    """

def build_district_query(table, col, state, year, quarter):
    return f"""
        SELECT district, SUM({col}) AS total_value
        FROM {table}
        WHERE state = '{state}' AND year = {year} AND quarter = {quarter}
        GROUP BY district ORDER BY total_value DESC LIMIT 15
    """

def build_top_states_query(table_name, map_col, year, quarter):
    return f"""
        SELECT state, SUM({map_col}) AS total_value
        FROM {table_name}
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY state ORDER BY total_value DESC LIMIT 10
    """

def build_time_trend_query(table_name, map_col, state):
    return f"""
        SELECT year, quarter, SUM({map_col}) AS total_value
        FROM {table_name}
        WHERE state = '{state}'
        GROUP BY year, quarter ORDER BY year, quarter
    """
