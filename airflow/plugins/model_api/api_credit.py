from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import json
from fastapi.encoders import jsonable_encoder


app = FastAPI()

# Load your pre-trained machine learning model


# Define the input data schema using Pydantic
class InputData(BaseModel):
    # Define your input data fields here, adjust accordingly to your model requirements
    RevolvingUtilizationOfUnsecuredLines: float
    age: float
    DaysPastDueNotWorse_30_59: float
    DebtRatio: float
    MonthlyIncome: float
    NumberOfOpenCreditLinesAndLoans: float
    NumberOfTimes90DaysLate: float
    NumberRealEstateLoansOrLines: float
    DaysPastDueNotWorse_60_89: float
    NumberOfDependents: float


# Define the prediction route
@app.post("/predict/")
def predict(data: InputData):
    try:
        print(jsonable_encoder(data))

        df = pd.DataFrame([jsonable_encoder(data)])

        print(df)

        model = joblib.load("/home/model/best_model.pkl")
        scaler = joblib.load("/home/model/std_scaler.pkl")

        print('SUCCESS LOAD MODEL')

        X = scaler.transform([df.iloc[0]])

        prediction_list = model.predict_proba(X).tolist()
        prediction = prediction_list[0][0]

        print("Prediction list success", prediction_list)
        print("Prediction success", prediction)

        # Return the prediction as a JSON response
        return {
            "prediction": prediction
        }  # Assuming your model outputs a single prediction

    except Exception as e:
        #raise HTTPException(status_code=500, detail=str(e))
        raise e


if __name__ == "__main__":
    # To run the API locally for testing

    uvicorn.run(app, host="0.0.0.0", port=8000)
