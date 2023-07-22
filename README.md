# STEP BY STEP FOR THIS PROJECT ON WINDOWS

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
7. Query to create table and insert 
