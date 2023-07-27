import streamlit as st
import requests
import pandas as pd
import joblib

st.set_page_config(page_title="Credit Scoring Prediction", page_icon="📊")
st.sidebar.header("📊 Credit Scoring Prediction")


# Streamlit app
def main():
    # Create a connection to the database

    # Streamlit layout
    st.title("Credit Scoring")

    st.markdown(
        """
    Ini adalah contoh dari penggunaan credit scoring dengan menggunakan model machine learning. Mohon input nilai pada sidebar halaman ini.
    """
    )

    ######################################################

    # Side Bar

    age = st.sidebar.slider(label="Umur", min_value=18, max_value=100, value=49)

    MonthlyIncome = st.sidebar.number_input(label="Penghasilan perbulan", value=63588.0)

    NumberOfDependents = st.sidebar.number_input(
        label="Jumlah Tanggungan keluarga", value=0.0
    )

    DebtRatio = st.sidebar.number_input(label="Rasio perhutangan", value=0.024926)

    RevolvingUtilizationOfUnsecuredLines = st.sidebar.number_input(
        label="Total saldo pada kartu kredit setelah pengurangan", value=0.907239
    )

    NumberOfOpenCreditLinesAndLoans = st.sidebar.number_input(
        label="Jumlah pinjaman yang sedang dilakukan", value=7
    )

    NumberRealEstateLoansOrLines = st.sidebar.number_input(
        label="Jumlah pinjaman rumah", value=1
    )
    DaysPastDueNotWorse_30_59 = st.sidebar.number_input(
        label="Peminjaman jatuh tempo lebih 30 - 59 hari", value=1
    )
    DaysPastDueNotWorse_60_89 = st.sidebar.number_input(
        label="Peminjaman jatuh tempo lebih 60 - 89 hari", value=0
    )
    NumberOfTimes90DaysLate = st.sidebar.number_input(
        label="Peminjaman jatuh tempo lebih dari 90 hari", value=0
    )

    # Execute the query and display results
    # if st.sidebar.button("Predict"):
    #     input_data = {
    #         "RevolvingUtilizationOfUnsecuredLines": RevolvingUtilizationOfUnsecuredLines,
    #         "age": age,
    #         "DaysPastDueNotWorse_30_59": DaysPastDueNotWorse_30_59,
    #         "DebtRatio": DebtRatio,
    #         "MonthlyIncome": MonthlyIncome,
    #         "NumberOfOpenCreditLinesAndLoans": NumberOfOpenCreditLinesAndLoans,
    #         "NumberOfTimes90DaysLate": NumberOfTimes90DaysLate,
    #         "NumberRealEstateLoansOrLines": NumberRealEstateLoansOrLines,
    #         "DaysPastDueNotWorse_60_89": DaysPastDueNotWorse_60_89,
    #         "NumberOfDependents": NumberOfDependents,
    #     }

    #     response = requests.post("http://<YOUR-IP-ADDRESS>:8000/predict/", json=input_data)
    #     # print(response.json())

    #     prediction = response.json()["prediction"] * 100

    #     st.success(f"Successfully Predict! (Good Score Percentage : {prediction}) %")
        
        
    if st.sidebar.button("Predict"):
        input_data = {
        "RevolvingUtilizationOfUnsecuredLines": [RevolvingUtilizationOfUnsecuredLines],
        "age": [age],
        "DaysPastDueNotWorse_30_59": [DaysPastDueNotWorse_30_59],
        "DebtRatio": [DebtRatio],
        "MonthlyIncome": [MonthlyIncome],
        "NumberOfOpenCreditLinesAndLoans": [NumberOfOpenCreditLinesAndLoans],
        "NumberOfTimes90DaysLate": [NumberOfTimes90DaysLate],
        "NumberRealEstateLoansOrLines": [NumberRealEstateLoansOrLines],
        "DaysPastDueNotWorse_60_89": [DaysPastDueNotWorse_60_89],
        "NumberOfDependents": [NumberOfDependents],
    }
    
        df = pd.DataFrame.from_dict(input_data)

        print(df)

        model = joblib.load("/mount/src/data_engineer_streamlit_airflow/airflow/plugins/project_streamlit/pages/best_model.pkl")
        scaler = joblib.load("/mount/src/data_engineer_streamlit_airflow/airflow/plugins/project_streamlit/pages/std_scaler.pkl")

        print('SUCCESS LOAD MODEL')

        X = scaler.transform([df.iloc[0]])

        prediction_list = model.predict_proba(X).tolist()
        prediction = prediction_list[0][0] * 100


        st.success(f"Successfully Predict! (Good Score Percentage : {prediction}) %")


# Run the app
if __name__ == "__main__":
    main()
