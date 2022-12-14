# airflow_piplenes

## Airflow installation from scratch

To install airflow from scratch follow the airflow official [docs](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html) or instructions from [installation notes](installation_notes.md)

## To use airflow installation on Mac/Linux from this repo folow steps from below:

If you do not have Docker and Docker-compose install Docker and Docker Compose on your laptop https://docs.docker.com/engine/install/

1. [optional cause we use Docker!] Create & activate virtual env

```
python -m venv airflow
source airflow/bin/activate
```

2. Clone the repo

3. Go to the repo folder and initicalize airflow `docker compose up airflow-init`

4. Run airflow in docker
   `docker-compose up`
   ( or `docker-compose up -d` for detached mode)

5. Go to your browser
   http://0.0.0.0:8080/home

user & password: airflow/airflow

## To use airflow installation on Windows from this repo folow steps from below:

1. Make new directory

```
mkdir airflow_docker
```

2. Paste the installing command from the repo

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.0/docker-compose.yaml'
```

3. Open docker-composer file with any IDE

4. Delete selected paths:

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

5. Initialize db with this command

```
docker-compose up airflow-init
```

6. Run airflow in docker

```
docker-compose up
```

7. After all check in browser

```
localhost:8080
```

user & password: airflow/airflow
