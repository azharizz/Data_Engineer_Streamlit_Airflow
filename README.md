# STEP BY STEP FOR THIS PROJECT ON WINDOWS

## INSTALL WSL Ubuntu 20.0 Version on microsoft store 
## Also in this section i will guide to python installation

1. Enter username ubuntu, password ubuntu
2. To open where is directory ubuntu at on explorer run the command below:
   '''
   explorer.exe .
   '''
3. Run Code Next Step :
   '''
   sudo -i
   '''
4. Insert password 'ubuntu'
5. Run Code Next Step :
   '''
   cd /home/ubuntu/
   mkdir airflow
   sudo apt update
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt-get install python3.9
   '''

6. Run and copy output:
   '''
   which python3.9
   '''
