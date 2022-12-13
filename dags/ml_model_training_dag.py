from datetime import datetime, timedelta
import csv

from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from sklearn.datasets import load_iris
import pandas as pd


default_args = {
	'owner':'emeli',
	'retries':2,
	'retry_delay':timedelta(minutes=2),
}

def dump_iris_data_to_csv(train_path, val_path):
	iris_data = load_iris(as_frame='auto')
	iris = iris_data.frame

	iris_train = iris.sample(n=150, replace=False)
	iris_validation = iris.sample(n=150, replace=False)

	iris_train.to_csv(train_path, sep='\t', index=True, header=False)
	iris_validation.to_csv(val_path, sep='\t', index=True, header=False)

def generate_predictions():
	pass

def load_data_into_db(table_name, file_path):
	postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
	postgres_hook.bulk_load(table_name, file_path)

with DAG(
	dag_id='ml_iris_dag',
	description='DAG with an ml model over iris data',
	default_args=default_args,
	start_date=datetime(2022, 12, 12),
	schedule_interval='@daily',
	catchup=False,

	) as dag:
		
		task1 = PythonOperator(
			task_id = 'dump_iris_data_to_csv',
			python_callable=dump_iris_data_to_csv,
			op_kwargs={'train_path':'reports/iris_train.tsv',
				'val_path':'reports/iris_val.tsv'
				}
			)

		task2 = PostgresOperator(
	        task_id='create_table',
	        postgres_conn_id='postgres_localhost',
	        sql="""
	            create table if not exists iris_data (
	                id int,
	                sepal_length float,
	                sepal_width  float,
	                petal_length float,
	                petal_width  float,
	                target int,
	                primary key (id)
	            )
	        """
	    )

#	    task3 load datasets from files, train model, write predictions to a file

		task4 = PythonOperator(
			task_id='file_to_db',
			python_callable=load_data_into_db,
			op_kwargs={'table_name':'iris_data',
				'file_path':'reports/iris_val.tsv'
				})
	    
		[task1, task2] >> task4
	

