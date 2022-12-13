from datetime import datetime, timedelta

from airflow import DAG

from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
	'owner':'emeli',
	'retries':2,
	'retry_delay':timedelta(minutes=2),
}

with DAG(
	dag_id='postgres_operator_dag',
	description='DAG with the connection to a Postgres DB',
	default_args=default_args,
	start_date=datetime(2022, 12, 12),
	schedule_interval='@daily',
	catchup=False,

	) as dag:
	    task1 = PostgresOperator(
	        task_id='create_table',
	        postgres_conn_id='postgres_localhost',
	        sql="""
	            create table if not exists dag_runs (
	                date date,
	                dag_id character varying,
	                primary key (date, dag_id)
	            )
	        """
	    )

	    task2 = PostgresOperator(
	        task_id='insert_into_table',
	        postgres_conn_id='postgres_localhost',
	        sql="""
	            insert into dag_runs (date, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
	        """
	    )
	
task1 >> task2
