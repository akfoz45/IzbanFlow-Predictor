import pandas as pd
import pickle
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'izban_model.pkl')

try:
    with open(MODEL_PATH, 'rb') as file:
        model_data = pickle.load(file)

    gb_model = model_data['model']
    le_target = model_data['le_target']
    model_columns = model_data['model_columns']
    print("The Machine Learning Model has been successfully uploaded!")

except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    gb_model, le_target, model_columns = None, None, None

def get_density_prediction(time_of_day, day_of_week, weekend, heat, rains_mm, station):
    if gb_model is None:
        return "Model could not be loaded"
    
    df_input = pd.DataFrame(columns=model_columns)
    df_input.loc[0] = 0

    df_input["time_of_day"] = int(time_of_day)
    df_input["day_of_week"] = int(day_of_week)
    df_input["weekend"] = int(weekend)
    df_input["heat"] = int(heat)
    df_input["rains_mm"] = int(rains_mm)

    station_col = f"station_{station}"

    if station_col in df_input.columns:
        df_input[station_col] = 1

    prediction_encoded = gb_model.predict(df_input)[0]

    prediction_label = le_target.inverse_transform([prediction_encoded])[0]

    return prediction_label