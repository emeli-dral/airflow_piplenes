from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
	'owner':'emeli',
	'retries':2,
	'retry_delay':timedelta(minutes=2)

}

def get_iris_name():
	return 'iris'

def get_dataset_name(name):
	return name

def print_dataset_name(ti):
	dataset_name = ti.xcom_pull(task_ids='get_name')
	print(f'Dataset name is: {dataset_name}')

def get_dataset_names(ti):
	ti.xcom_push(key='train_dataset', value='iris_train')
	ti.xcom_push(key='validation_dataset', value='iris_validation')

def print_dataset_names(ti):
	train_name = ti.xcom_pull(task_ids='get_dataset_names', key='train_dataset')
	validation_name = ti.xcom_pull(task_ids='get_dataset_names', key='validation_dataset')
	source_name = ti.xcom_pull(task_ids='get_iris_name')
	print(f'Datasource name is: {source_name}')
	print(f'Dataset names are: train:{train_name}, validation:{validation_name}')

with DAG(
	dag_id='xcoms_dag',
	description='This is a dag with xcoms!',
	default_args=default_args,
	start_date=datetime(2022,12,9,9),
	schedule_interval='@daily',

	) as dag:
		task1 = PythonOperator(
			task_id='get_dataset_names',
			python_callable=get_dataset_names,
			#op_kwargs={'name':'iris'}
			)

		task2 = PythonOperator(
			task_id='print_dataset_names',
			python_callable=print_dataset_names,
			)

		task3 = PythonOperator(
			task_id='get_iris_name',
			python_callable=get_iris_name,
			)


		[task1, task3] >> task2