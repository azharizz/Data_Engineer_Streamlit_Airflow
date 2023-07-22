from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

import os

os.chdir("/opt/airflow/plugins/")

from model_api.model_retrain import retrain_run

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 7, 11),
}

dag = DAG(
    "DAG_Python_Retrain_Model",
    default_args=default_args,
    description="DAG Retrain Model Credit Scoring",
    schedule_interval=None,
)


# Define the tasks using the PythonOperator
run_retrain_model = PythonOperator(
    task_id="run_plugin_python_file",
    python_callable=retrain_run,
    dag=dag,
)

# Set task dependencies
run_retrain_model
