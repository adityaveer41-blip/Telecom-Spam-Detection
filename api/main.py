from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import shap

# INIT APP
app = FastAPI()

# LOAD MODEL
model = joblib.load("models/fraud_model.pkl")

# SHAP explainer 
explainer = shap.TreeExplainer(model)

# INPUT SCHEMA
class InputData(BaseModel):
    account_length: int
    vmail_message: int
    day_mins: float
    day_calls: int
    eve_mins: float
    eve_calls: int
    night_mins: float
    night_calls: int
    intl_mins: float
    intl_calls: int
    custserv_calls: int

# HEALTH CHECK
@app.get("/")
def home():
    return {"message": "API is running"}

# PREDICTION API
@app.post("/predict")
def predict(data: InputData):

    input_df = pd.DataFrame([{
        "Account Length": data.account_length,
        "VMail Message": data.vmail_message,
        "Day Mins": data.day_mins,
        "Day Calls": data.day_calls,
        "Eve Mins": data.eve_mins,
        "Eve Calls": data.eve_calls,
        "Night Mins": data.night_mins,
        "Night Calls": data.night_calls,
        "Intl Mins": data.intl_mins,
        "Intl Calls": data.intl_calls,
        "CustServ Calls": data.custserv_calls
    }])

    # MODEL PREDICTION
    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    # SHAP EXPLANATION
    shap_values = explainer.shap_values(input_df)

    if isinstance(shap_values, list):
        shap_array= shap_values[1]
    else:
        shap_array= shap_values

    shap_array= shap_array[0]    


    shap_df = pd.DataFrame({
        "feature": input_df.columns,
        "impact": shap_array
    })

    # sort by importance (absolute value)
    shap_df = shap_df.sort_values(by="impact", key=abs, ascending=False)

    # top 5 features
    top_features = shap_df.head(5).to_dict(orient="records")

    # RESPONSE
    return {
        "Prediction": int(pred),
        "Probability": float(prob),
        "Top_Features": top_features
    }


        




