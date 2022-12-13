# airflow_piplenes

## Airflow installation from scratch
To install airflow from scratch follow the airflow official [docs](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html) or instructions from [installation notes](installation_notes.md)

##  To use airflow installation from this repo folow steps from below:

If you do not have Docker and Docker-compose install Docker and Docker Compose on your laptop https://docs.docker.com/engine/install/ 

1. [optional cause we use Docker!] Create & activate virtual env
```
python -m venv airflow
source airflow/bin/activate
```

2. Clone the repo

3. Go to the repo folder and initicalize airflow ```docker compose up airflow-init```

4. Run airflow in docker
 ```docker-compose up```
( or ```docker-compose up -d``` for detached mode)

5. Go to your browser
http://0.0.0.0:8080/home

user & password: airflow/airflow

