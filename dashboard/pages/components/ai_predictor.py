# pages/components/ai_predictor.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_growth(df):
    try:
        if df.empty or 'total' not in df.columns:
            return 0

        df = df.copy()
        df["quarter_num"] = range(1, len(df)+1)

        X = df[["quarter_num"]].values
        y = df["total"].values

        model = LinearRegression()
        model.fit(X, y)

        next_quarter = np.array([[len(df)+1]])
        prediction = model.predict(next_quarter)[0]

        return max(0, round(prediction))
    except Exception:
        return 0
