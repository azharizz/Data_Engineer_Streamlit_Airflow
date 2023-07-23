import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import roc_auc_score
from imblearn.under_sampling import RandomUnderSampler

import joblib


def get_best_model(list_of_model, list_of_param, train_X, train_y, test_X, test_y):
    best_model_obj = None
    best_model_name = None
    best_score = 0

    for model_dict in list_of_model:
        print(model_dict)

        model_obj = model_dict["model_object"]
        model_param = list_of_param[model_dict["model_name"]]

        model = RandomizedSearchCV(
            estimator=model_obj,
            param_distributions=model_param,
            n_iter=5,
            cv=5,
            random_state=123,
            n_jobs=1,
            verbose=10,
            scoring="roc_auc",
        )

        model.fit(train_X, train_y)

        y_pred_proba = model.predict_proba(test_X)[:, 1]

        print("predict is success")
        score_now = roc_auc_score(test_y, y_pred_proba)

        if score_now > best_score:
            best_score = score_now
            best_model_obj = model
            best_model_name = model_dict["model_name"]

    print(
        f"""
          ==============================
          BEST MODEL        : {best_model_name}
          BEST SCORE        : {best_score}
          BEST MODEL OBJ    : {best_model_obj}
          ==============================
          """
    )

    # save your model or results
    joblib.dump(best_model_obj, "/opt/airflow/plugins/model_api/model/best_model.pkl")

    print("Model saved !")


def retrain_run():
    df = pd.read_csv("/opt/airflow/plugins/model_api/data.csv")
    df = df.drop(["Unnamed: 0"], axis=1)

    X = df.drop(["SeriousDlqin2yrs"], axis=1)
    y = df["SeriousDlqin2yrs"]

    # Train test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Fill missing value
    median_imputer_train = SimpleImputer(missing_values=np.nan, strategy="median")

    median_imputer_train.fit(X_train[["MonthlyIncome"]])

    median_imputer_test = SimpleImputer(missing_values=np.nan, strategy="median")

    median_imputer_test.fit(X_test[["MonthlyIncome"]])

    X_train["MonthlyIncome"] = median_imputer_train.transform(
        X_train[["MonthlyIncome"]]
    )

    X_test["MonthlyIncome"] = median_imputer_test.transform(X_test[["MonthlyIncome"]])

    X_train.loc[X_train["NumberOfDependents"].isnull(), "NumberOfDependents"] = 0.0
    X_test.loc[X_test["NumberOfDependents"].isnull(), "NumberOfDependents"] = 0.0

    # Scaling
    scaler = StandardScaler()

    scaler.fit(X_train)

    X_train_std = scaler.transform(X_train)
    X_test_std = scaler.transform(X_test)

    joblib.dump(scaler, "/opt/airflow/plugins/model_api/model/std_scaler.pkl")

    # Undersampling
    ros = RandomUnderSampler(random_state=42)

    #X_resample, y_resample = ros.fit_resample(X_train_std, y_train)
    X_resample = X_train_std
    y_resample = y_train

    # Modeling
    knn = KNeighborsClassifier()
    lgr = LogisticRegression(solver="liblinear")
    xgb = XGBClassifier()
    rf = RandomForestClassifier()

    # Create list of model
    list_of_model = [
        {"model_name": knn.__class__.__name__, "model_object": knn},
        {"model_name": lgr.__class__.__name__, "model_object": lgr},
        {"model_name": xgb.__class__.__name__, "model_object": xgb},
        {"model_name": rf.__class__.__name__, "model_object": rf},
    ]

    # 'n_neighbors': [50, 100, 200]
    knn_params = {
        "n_neighbors": [50, 100, 200],
    }

    # 'penalty': ['l1', 'l2'],
    # 'C': [0.01, 0.1],
    # 'max_iter': [100, 300, 500]
    lgr_params = {"penalty": ["l2"], "C": [0.01], "max_iter": [300]}

    # 'n_estimators': [5, 10, 25, 50]
    xgb_params = {"n_estimators": [5, 10, 25, 50]}

    # 'n_estimators': [5, 10, 25, 50]
    rf_params = {"n_estimators": [5, 10, 25, 50]}

    # Create model params
    list_of_param = {
        "KNeighborsClassifier": knn_params,
        "LogisticRegression": lgr_params,
        "XGBClassifier": xgb_params,
        "RandomForestClassifier": rf_params,
    }

    print("Trying to get best M")

    get_best_model(
        list_of_model, list_of_param, X_resample, y_resample, X_test_std, y_test
    )
