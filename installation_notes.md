# Airflow 2.x
## Airflow local installation
Run Airflow in Python Env
Go to the official github REPO, navigate to installing from pypi
https://github.com/apache/airflow#installing-from-pypi 

Check out YOUR python version:
"""
python --version 
"""

 create virtual env
"""
python -m venv airflow
"""

Activate it: """
source airflow/bin/activate
"""

Copy the installing command from the repo (the first one)
"""
pip install 'apache-airflow==2.5.0' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.8.txt"
"""

Update command with your python version! And run.

4. Initialize DB for Airflow
Indicate Airflow home directory
"""
export AIRFLOW_HOME=.
(fro me worked full path: export AIRFLOW_HOME=/Users/emelidral/Dev/airflow2_tutorial/airflow)
"""

Initialize db with command: 
"""
airflow db init
"""

Results:
Creation of DB DB: sqlite:///./airflow.db Note! Here is no encryption (values will not be stored encrypted)
Creation of log folder “logs”
Creation of some configuration scripts

5.  Start Airflow webserver:
"""
airflow webserver -p 8080
"""

This runs Airflow, but to access it we need to create a user 

6. Create Airflow user:
Some help:
"""
Airflow user create — help
"""
And the command:
"""
airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.com
"""
 
7. Start Airflow webserver:
"""
airflow webserver -p 8080
"""

And go to the browser: http://localhost:8080/

8. Open up a second tab in your terminal.
Activate env:  """
source airflow/bin/activate
"""

Set the AIRFLOW_HOME: 
"""
export AIRFLOW_HOME=/Users/emelidral/Dev/airflow2_tutorial/airflow
"""

Run the scheduler: 
"""
airflow scheduler
"""

You will see some examples.
To test installation trigger  """example_bash_operator"""
## Airflow docker installation
1. Install Docker and Docker Compose on your laptop https://docs.docker.com/engine/install/ 
For Mac OS and Windows install Docker Desktop (it includes both).
Switch it on.

Check docker and docker-compose version in terminal
"""
docker --version
docker-compose --version
"""

2. go to the airflow docs in https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html 

3. Create directory 
"""
mkdir airflow_docekr
"""
and go to this directory

4. Load docker compose file 
"""
 curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.0/docker-compose.yaml'
"""

Update docker-compose:

4.1 Instead of Celery we are going to use airflow locally, so we change  
AIRFLOW__CORE__EXECUTOR: CeleryExecutor -> LocalExecutor

Note: Celery Executor is needed for scaling (scale out the number of workers)
Flower is needed for monitoring
We are not going to use either of them.

4.2 We comment  or delete
    # AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    # AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0

4.3 Redis in necessary for Celery, we do not need it (delete or comment)
"""
    redis:
      condition: service_healthy
"""

 And comment/delete its definition
"""
  redis:
    image: redis:latest
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 30s
      retries: 50
    restart: always
"""
 
We do not need celery in airflow-worker (delete or comment)
"""
  airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 10s
      timeout: 10s
      retries: 5
    environment:
      <<: *airflow-common-env
      # Required to handle warm shutdown of the celery workers properly
      # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
      DUMB_INIT_SETSID: "0"
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully
"""

We do not need flower (delete or comment)
"""
  flower:
    <<: *airflow-common
    command: celery flower
    profiles:
      - flower
    ports:
      - 5555:5555
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully
"""

5. Create folders for dags, logs and plugins
"""
mkdir -p ./dags ./logs ./plugins
"""
I will also need a folder for reports, so I create ./reports as well

6. initialize db
"""
docker compose up airflow-init
"""
It downloads all docker containers with airflow username and password

Result:
"""
airflow_docker-airflow-init-1  | 2.5.0
airflow_docker-airflow-init-1 exited with code 0
"""


7. Run airflow in docker
"""
 docker-compose up
(docker-compose up -d for detached mode)
"""

To see what is running: 
"""
docker ps
"""

8. go to your browser
http://0.0.0.0:8080/home
user & password: airflow/airflow

Note from the official docs: The docker-compose environment we have prepared is a “quick-start” one. It was not designed to be used in production and it has a number of caveats - one of them being that the best way to recover from any problem is to clean it up and restart from scratch.
The best way to do this is to:
Run docker-compose down --volumes --remove-orphans command in the directory you downloaded the docker-compose.yaml file
Remove the entire directory where you downloaded the docker-compose.yaml file rm -rf '<DIRECTORY>'
Run through this guide from the very beginning, starting by re-downloading the docker-compose.yaml file
Removing DAG examples
Disable examples:
In the docker-compose.yaml set
AIRFLOW__CORE__LOAD_EXAMPLES: 'false' 

Then shut down docker and delete all volumes:
"""
docker-compose down -v
"""

Then init airflow again:  
"""
docker-compose up airflow-init
"""

And run docker: 
"""
docker-compose up -d
"""

