import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# ------------------------ #
# Load trained model files #
# ------------------------ #
model_ref = joblib.load("Jupyter/Referee_Model/referee_model.pkl")
le_ref = joblib.load("Jupyter/Referee_Model/target_labelencoder.pkl")
scaler_ref = joblib.load("Jupyter/Referee_Model/scaler.pkl")
imputer_ref = joblib.load("Jupyter/Referee_Model/imputer.pkl")
train_columns_ref = joblib.load("Jupyter/Referee_Model/model_columns.pkl")

model_result = joblib.load("Jupyter/Result_Model/result_model.pkl")
le_result = joblib.load("Jupyter/Result_Model/target_labelencoder.pkl")
scaler_result = joblib.load("Jupyter/Result_Model/scaler.pkl")
imputer_result = joblib.load("Jupyter/Result_Model/imputer.pkl")
train_columns_result = joblib.load("Jupyter/Result_Model/model_columns.pkl")

# ----------------------------- #
# Load dataset dropdown options #
# ----------------------------- #
df = pd.read_excel("Jupyter/MasterDataset_ML.xlsx")

# Filter rare referees out #
counts = df['Referee'].value_counts()
rare_refs = counts[counts < 70].index
df = df[~df['Referee'].isin(rare_refs)]

# ----------- #
# The Main UI #
# ----------- #
st.title("Premier League Referee Predictor")
st.write("Select match details to predict the referee:")

# Categorical Dropdowns #
# --------------------- #
home_team = st.selectbox("Home Team", df['Home'].sort_values().unique())

away_options = sorted([team for team in df['Away'].unique() if team != home_team])
away_team = st.selectbox("Away Team", away_options)

stadium_city = st.selectbox("Stadium City", df['Stadium City'].sort_values().unique())
season_year = st.selectbox("Season Start Year", df['Season Start Year'].sort_values().unique())
uk_region = st.selectbox("Referee - UK Region of Birth", df['Referee - UK Region of Birth'].sort_values().unique())

# Numerical Features #
# ------------------ #
stadium_capacity = st.number_input("Stadium Capacity", min_value=0, value=int(df['Stadium Capacity'].mean()))
stadium_attendance = st.number_input("Stadium Attendance", min_value=0, value=int(df['Stadium Attendance'].mean()))

# Match Stats #
# ----------- #
h_ball_pos = st.slider("Home Ball Possession %", min_value=0, max_value=100, value=50)
a_ball_pos = 100 - h_ball_pos

h_free_kicks = st.number_input("Home Free Kicks", min_value=0, value=10)
a_free_kicks = st.number_input("Away Free Kicks", min_value=0, value=10)
h_corner_kicks = st.number_input("Home Corner Kicks", min_value=0, value=5)
a_corner_kicks = st.number_input("Away Corner Kicks", min_value=0, value=5)
h_fouls = st.number_input("Home Fouls", min_value=0, value=10)
a_fouls = st.number_input("Away Fouls", min_value=0, value=10)
h_yellow = st.number_input("Home Yellow Cards", min_value=0, value=1)
a_yellow = st.number_input("Away Yellow Cards", min_value=0, value=1)
h_red = st.number_input("Home Red Cards", min_value=0, value=0)
a_red = st.number_input("Away Red Cards", min_value=0, value=0)
penalties_awarded = st.number_input("Penalties Awarded", min_value=0, value=0)

# -------------------- #
# Single Row Dataframe #
# -------------------- #
input_dict_ref = {
    "Home": [home_team],
    "Away": [away_team],
    "Stadium City": [stadium_city],
    "Season Start Year": [season_year],
    "Referee - UK Region of Birth": [uk_region],
    "Stadium Capacity": [stadium_capacity],
    "Stadium Attendance": [stadium_attendance],
    "H_Ball_Possession": [h_ball_pos],
    "A_Ball_Possession": [a_ball_pos],
    "H_Free_Kicks": [h_free_kicks],
    "A_Free_Kicks": [a_free_kicks],
    "H_Corner_Kicks": [h_corner_kicks],
    "A_Corner_Kicks": [a_corner_kicks],
    "H_Fouls": [h_fouls],
    "A_Fouls": [a_fouls],
    "H_Yellow_Cards": [h_yellow],
    "A_Yellow_Cards": [a_yellow],
    "H_Red_Cards": [h_red],
    "A_Red_Cards": [a_red],
    "PenaltiesAwarded": [penalties_awarded]
}
input_dict_result = {
    "Home": [home_team],
    "Away": [away_team],
    "Stadium City": [stadium_city],
    "Season Start Year": [season_year],
    "Referee - UK Region of Birth": [uk_region],
    "Stadium Capacity": [stadium_capacity],
    "Stadium Attendance": [stadium_attendance],
    "H_Ball_Possession": [h_ball_pos],
    "A_Ball_Possession": [a_ball_pos],
    "H_Free_Kicks": [h_free_kicks],
    "A_Free_Kicks": [a_free_kicks],
    "H_Corner_Kicks": [h_corner_kicks],
    "A_Corner_Kicks": [a_corner_kicks],
    "H_Fouls": [h_fouls],
    "A_Fouls": [a_fouls],
    "H_Yellow_Cards": [h_yellow],
    "A_Yellow_Cards": [a_yellow],
    "H_Red_Cards": [h_red],
    "A_Red_Cards": [a_red],
    "PenaltiesAwarded": [penalties_awarded]
}

input_df_ref = pd.DataFrame(input_dict_ref)
input_df_result = pd.DataFrame(input_dict_result)

# -------------------------------------------------- #
# Preprocessing - Dummy Encoded Categorical Features #
# -------------------------------------------------- #
categorical_cols_ref = ["Home", "Away", "Stadium City", "Referee - UK Region of Birth", "Season Start Year"]
input_encoded_ref = pd.get_dummies(input_df_ref, columns = categorical_cols_ref, drop_first=True)

for col in train_columns_ref:
    if col not in input_encoded_ref.columns:
        input_encoded_ref[col] = 0
input_encoded_ref = input_encoded_ref[train_columns_ref]

input_imputed_ref = imputer_ref.transform(input_encoded_ref)
input_scaled_ref = scaler_ref.transform(input_imputed_ref)

# -------------------------------------------------- #
# Preprocessing - Dummy Encoded Categorical Features #
# -------------------------------------------------- #
categorical_cols_result = ["Home", "Away", "Stadium City", "Referee - UK Region of Birth", "Season Start Year"]
input_encoded_result = pd.get_dummies(input_df_result, columns = categorical_cols_result, drop_first=True)

for col in train_columns_result:
    if col not in input_encoded_result.columns:
        input_encoded_result[col] = 0
input_encoded_result = input_encoded_result[train_columns_result]

input_imputed_result = imputer_result.transform(input_encoded_result)
input_scaled_result = scaler_result.transform(input_imputed_result)

# ----------------- #
# Predict Referee ! #
# ----------------- #
if st.button("Predict Referee"):
    pred_encoded_ref = model_ref.predict(input_scaled_ref)
    pred_referee = le_ref.inverse_transform(pred_encoded_ref)
    
    pred_probability_ref = model_ref.predict_proba(input_scaled_ref)
    confidence_ref = pred_probability_ref[0][pred_encoded_ref[0]] * 100

    st.success(f"Predicted Referee: {pred_referee[0]}")
    st.info(f"Model Confidence: {confidence_ref:.2f}%")

# -------------------------- #
# Predict Match Win/Loss/Tie #
# -------------------------- #
if st.button("Predict Match Result"):
    pred_encoded_result = model_result.predict(input_scaled_result)
    pred_result = le_result.inverse_transform(pred_encoded_result)

    pred_probability_result = model_result.predict_proba(input_scaled_result)
    confidence_result = pred_probability_result[0][pred_encoded_result[0]] * 100

    st.success(f"Predicted Match Result: {pred_result[0]}")
    st.info(f"Model Confidence: {confidence_result:.2f}%")