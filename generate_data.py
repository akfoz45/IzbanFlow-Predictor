import pandas as pd
import numpy as np
from datetime import timedelta

def generate_synthetic_data(start_date='2025-05-01', days=365):
    dates = pd.date_range(start=start_date, periods=days * 24, freq="h")
    df = pd.DataFrame({'date_hours': dates})

    df["time_of_day"] = df['date_hours'].dt.hour
    df["day_of_week"] = df['date_hours'].dt.dayofweek
    df["weekend"] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

    stations = ["Menemen", "Çiğli", "Egekent", "Nergiz", "Karşıyaka", "Bayraklı", "Halkapınar", "Alsancak"]
    df["station"] = np.random.choice(stations, size=len(df))

    df["heat"] = np.random.normal(loc=18, scale=7, size=len(df)).round(1)
    df["rains_mm"] = np.where(np.random.rand(len(df)) > 0.8, np.random.exponential(scale=3, size=len(df)), 0).round(1)

    is_peak = (
        ((df["time_of_day"] >= 7) & (df["time_of_day"] <= 9)) | 
        ((df["time_of_day"] >= 17) & (df["time_of_day"] <= 19))
    ) & (df["weekend"] == 0)

    base_crowd = 20
    crowd_score = (
        base_crowd +
        np.where(is_peak, 45, 0) +
        np.where(df["station"] == 'Halkapınar', 30, 0) +
        np.where(df["station"] == 'Alsancak', 15, 0) +
        np.where(df["station"] == 'Çiğli', 10, 0) +
        np.where(df['rains_mm'] > 0, 5, 0) +
        np.random.normal(0, 8, len(df))
    )

    df["density_class"] = pd.cut(crowd_score, bins=[-np.inf, 40, 75, np.inf], labels=["Sakin", "Normal", "Çok Yoğun"])

    return df

df_izban = generate_synthetic_data()
print(df_izban["density_class"].value_counts())