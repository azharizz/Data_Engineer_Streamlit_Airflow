# STEP BY STEP FOR THIS PROJECT ON WINDOWS


### NOTE : PLEASE CHECK THIS FOR DOCKER IF CANNOT BE ACCESSABLE
   If running 'docker ps' cannot be accesable you should run :
   ```
   sudo service docker start
   ```


## INSTALL WSL Ubuntu 20.0 Version on microsoft store 
## Also in this section i will guide to python installation

1. Enter username ubuntu, password ubuntu
2. To open where is directory ubuntu at on explorer run the command below:
   ```
   explorer.exe .
   ```
3. Run Code Next Step :
   ```
   sudo -i
   ```
4. Insert password 'ubuntu'
5. Run Code Next Step :
   ```
   cd /home/ubuntu/
   mkdir airflow
   sudo apt update
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt-get install python3.9
   ```

6. Run and copy output:
   ```
   which python3.9
   ```
7. Run Code Next Step :
   ```
   nano ~/.bashrc
   ```

   Add in end of line with step no 6 directory (Paling bawah tambah 1 enter) :
   ```
   alias python=/usr/bin/python3.9
   ```

8. Run Code Next Step :
   ```
   source ~/.bashrc
   apt-get install pip
   ```

## 1. Docker Installation
1. Run Code Next Step :
   ```
   source ~/.bashrc
   apt-get install pip
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   ```

2. Run Code Next Step :
   ```
   echo \
   "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
   "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
3. Run Code Next Step :
   ```
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   sudo service docker start
   sudo docker run hello-world
   ```

   
## 2. Install Postgres and PGAdmin4
1. Run Code & Copy Output for your IP address :
   ```
   hostname -I | awk '{print $1}'
   ```
2. Run Code Next Step :
   ```
   docker run --name postgresql-container -p 5433:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret -d postgres
   ```
4. Run Code Next Step :
   ```
   docker run --name pgadmin -p 80:80 \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="secret" \
    -d dpage/pgadmin4
   ```
5. Open on website 127.0.0.1:80 and input email is "admin@admin.com" password is "secret"
6. Make connection with hostname is your ip address on step number 1, Database = postgres, username = postgres, password = secret
7. Query to create table and insert on table_postgres.txt in this repository


## 3. Install Streamlit
1. Run Code  Next Step :
   ```
   nano ~/.bashrc
   ```
   
   Add in end of line with (Paling bawah tambah 1 enter) :
   ```
   alias pip='python -m pip'
   ```
2. Run Code Next Step :
   ```
   source ~/.bashrc
   pip install streamlit
   pip install psycopg2-binary
   pip install scikit-learn
   pip install matplotlib
   ```
3. Copy code + directory on this repository airflow/plugins/project_streamlit
4. Run Code Next Step :
   ```
   streamlit run Hello.py
   ```
5. Change directory to file located for Hello.py :
   ```
   docker build -t streamlit-app .
   docker run -p 8501:8501 streamlit-app
   ```

## 4. Install Airflow
1. Run Code  Next Step :
   ```
   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml'
   ```

2. Run Code  Next Step :
   ```
   nano Dockerfile 
   ```
   Input this or you can copy from this repository airflow/Dockerfile:
   ```
   FROM apache/airflow:2.6.3
   USER root
   USER airflow
   COPY requirements.txt /
   RUN pip install -r /requirements.txt
   ```
3. Please copy the requirements.txt on airflow/requirements.txt
4. Run Code Next Step :
   ```
   docker build -t airflow_custom .
   ```
5. Run Code  Next Step :
   ```
   nano docker-compose.yaml 
   ```
   Find and replace or you can copy all from airflow/docker-compose.yml:
   ```
   version: '3.8'
   x-airflow-common:
     &airflow-common
     # In order to add custom dependencies or upgrade provider packages you can use your extended image.
     # Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
     # and uncomment the "build" line below, Then run `docker-compose build` to build the images.
     image: ${AIRFLOW_IMAGE_NAME:-airflow_custom} <------------------ REPLACE THIS !!!

   
   ```
6. Run Code  Next Step :
   ```
   mkdir -p ./dags ./logs ./plugins ./config
   echo -e "AIRFLOW_UID=$50000\nAIRFLOW_GID=0" > .env
   ```
7. Run Code  Next Step :
   ```
   docker compose up
   ```
8. Open on WEB : http://127.0.0.1:8080/
9. Copy all files on airflow/dags in this repository into the airflow directory
9. Login with username is "airflow" and password is "airflow"


## 5. Making API for Model :
1. change directory to airflow/plugins/model_api and copy all files and folder there
2. Run Code  Next Step :
   ```
   docker build -t fast_api_model .
   docker compose up
   ```





# **Project Output** :

You can visit this project : https://dataengineer-azhar-test.streamlit.app/

![image](https://github.com/azharizz/Data_Engineer_Streamlit_Airflow/assets/45253059/0821471e-f97b-4f6e-8c5a-e737da0f3efd)

![image](https://github.com/azharizz/Data_Engineer_Streamlit_Airflow/assets/45253059/88660637-442f-4255-8e0c-169cdb2780aa)

![image](https://github.com/azharizz/Data_Engineer_Streamlit_Airflow/assets/45253059/6e23a37b-cfd9-4fc5-8de9-2f0f99e39e9b)




Note:

Docker : Pembungkus tiap tools aplikasi pada project dalam bentuk container, memungkinkan untuk menjalan banyak aplikasi menggunakan os linux.

Postgres : Sebagai database yang akan kita tarik data nya untuk visualisasi dari Streamlit (Bisa juga sebagai proses ETL, Data pada model retrain)

PgAdmin : UI dari postgres dan memudahkan kita untuk melakukan Data Modeling pada Postgres

Streamlit : Sebagai framework / tools yang tujuannya itu memvisualisasikan data, mengintegrasi Machine Learning, dan mempublikasikan hasil project ke publik dengan streamlit share.

Airflow : Sebagai orchestrator / tools scheduler untuk menjalankan suatu job yang dimana itu proses retrain model.

FastAPI : Framework yang tujuannya dijadikan API untuk ML Model yang berfungsi sebagai prediksi kredit scoring

ML Model : Machine Learning menggunakan Scikit-learn dan juga RandomizedSearchCV untuk mencari parameter terbaik
