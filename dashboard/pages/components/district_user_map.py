# 📁 File: pages/components/district_user_map.py

import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px

def render_district_user_data(selected_state, selected_year):
    base_dir = "C:/Users/Shivam Shashank/Desktop/phonepe/data/map/user/hover/country/india/state"
    state_folder = selected_state.lower().replace(" ", "-")
    folder_path = os.path.join(base_dir, state_folder, str(selected_year))

    district_data = []

    if not os.path.exists(folder_path):
        st.error(f"❌ Folder not found: {folder_path}")
        return

    files = sorted([f for f in os.listdir(folder_path) if f.endswith(".json")])
    if not files:
        st.warning(f"⚠️ No JSON files found in: {folder_path}")
        return

    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                hover_data = data.get("data", {}).get("hoverData", {})
                for district, info in hover_data.items():
                    district_data.append({
                        "district": district.title(),
                        "registered_users": info.get("registeredUsers", 0)
                    })
        except Exception as e:
            st.error(f"❌ Error reading {file}: {e}")

    if not district_data:
        st.warning("⚠️ No district data extracted from JSON files.")
        return

    df = pd.DataFrame(district_data)
    df = df.sort_values(by="registered_users", ascending=False)

    st.subheader(f"🏙️ District-Wise User Data | {selected_state.title()} | {selected_year}")
    st.dataframe(df, use_container_width=True)

    fig = px.bar(
        df.head(10),
        x="registered_users",
        y="district",
        orientation="h",
        color="registered_users",
        title=f"Top 10 Districts by Registered Users ({selected_state.title()} - {selected_year})",
        color_continuous_scale="sunset"
    )
    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font_color="#FFA500",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
