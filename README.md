# airflow_piplenes

## Airflow installation from scratch

More info on Airflow installation can be found in the official [docs](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html) or  [installation notes](installation_notes.md)

## Airflow docker installation
1. Install Docker and Docker Compose on your laptop https://docs.docker.com/engine/install/ 
For Mac OS and Windows install Docker Desktop (it includes both).
Switch it on.

Check docker and docker-compose version in terminal
```
docker --version
```

2. Create priject directory and go there
```
mkdir airflow_docker
```
and go to this directory

3. [optional cause we use Docker!] Create & activate virtual env
```
python -m venv airflow
source airflow/bin/activate
```

4. Load docker compose file 
Before running the following command make sure, that you use the likn with airflow version you want to install. 
If you prefer to install the other version of airflow update the link.
```
 curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.0/docker-compose.yaml'
```

5. Update docker-compose.yaml 
Open docker-compose.yaml file with any IDE or text editor

**Note:** Celery Executor is needed for scaling (scale out the number of workers)
Flower is needed for monitoring.
We are not going to use either of them.

5.1 Instead of Celery we are going to use airflow locally.
Update: ```AIRFLOW__CORE__EXECUTOR: CeleryExecutor``` with ```AIRFLOW__CORE__EXECUTOR: LocalExecutor```

5.2 Delete or comment the following file parts:
```
AIRFLOW**CELERY**RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
AIRFLOW**CELERY**BROKER_URL: redis://:@redis:6379/0

redis:
condition: service_healthy

redis:
image: redis:latest
expose: - 6379
healthcheck:
test: ["CMD", "redis-cli", "ping"]
interval: 5s
timeout: 30s
retries: 50
restart: always

airflow-worker:
<<: *airflow-common
command: celery worker
healthcheck:
test: - "CMD-SHELL" - 'celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
interval: 10s
timeout: 10s
retries: 5
environment:
<<: *airflow-common-env # Required to handle warm shutdown of the celery workers properly # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
DUMB_INIT_SETSID: "0"
restart: always
depends_on:
<<: \*airflow-common-depends-on
airflow-init:
condition: service_completed_successfully
```

5.3 Add an aditional volume for reports
```
  volumes:
    - ./reports:/opt/airflow/reports
```

6. Create folders for dags, logs, plugins and reports
```
mkdir -p ./dags ./logs ./plugins ./reports
```

7. initialize db
```
docker-compose up airflow-init
```
It downloads all docker containers with airflow username and password

Result should look somewhat like:
```
airflow_docker-airflow-init-1  | 2.5.0
airflow_docker-airflow-init-1 exited with code 0
```

8. Run airflow in docker
```
 docker-compose up
(docker-compose up -d for detached mode)
```

To see what is running: 
```
docker ps
```

9. Check airflow dashboard in your browser
http://0.0.0.0:8080/home
user/password: airflow/airflow

**Note from the official docs:** The docker-compose environment we have prepared is a “quick-start” one. It was not designed to be used in production and it has a number of caveats - one of them being that the best way to recover from any problem is to clean it up and restart from scratch.
The best way to do this is to:
- Run docker-compose down --volumes --remove-orphans command in the directory you downloaded the docker-compose.yaml file
- Remove the entire directory where you downloaded the docker-compose.yaml file rm -rf '<DIRECTORY>'
- Run through this guide from the very beginning, starting by re-downloading the docker-compose.yaml file

## Removing Airflow default DAG examples

1. In the docker-compose.yaml set
```AIRFLOW__CORE__LOAD_EXAMPLES: 'false' ```

2. Then shut down docker and delete all volumes:
```
docker-compose down -v
```

3. Then init airflow again:  
```
docker-compose up airflow-init
```

4. And run the docker: 
```
docker-compose up -d
```
