# components/ai_insight_generator.py

import openai
import streamlit as st

# ✅ Securely fetch the OpenAI API key
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OpenAI API key is missing. Please add it in .streamlit/secrets.toml")

# ✅ Set the key for API usage
openai.api_key = api_key

def generate_insight(df, data_type):
    if df.empty:
        return "⚠️ No data available to generate insights."

    # Create a clean markdown prompt with the DataFrame
    prompt = f"""
You are a skilled data analyst. Analyze the following table of {data_type} data and summarize the key insights:

{df.to_markdown(index=False)}

Return your analysis in **2-3 concise sentences**, highlighting trends, anomalies, or patterns.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert data analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=250
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ Error generating insight: {e}"
