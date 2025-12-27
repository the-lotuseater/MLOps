from airflow import DAG
from airflow.providers.http.operators.http import HTTPOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostGresHook
from airflow.utils.dates import days_ago
import json


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='nasa_apod_postgres',
    start_date = days_ago(1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    ##step 1
    #create table is it doesn't exit

    #Step 2 Extract the NASA API data (APOD) Astronomy picture of the day
    #this step is the extract step of the ETL pipeline

    #Step 3:
    #transform the data by picking the information we need to save

    #step 4:
    #load the data into PostGres DB

    #step 5 verify the data wiht DBViewer

    #step 6 define task dependencies
    pass