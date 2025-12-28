from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json


with DAG(
    dag_id='nasa_apod_postgres',
    start_date = days_ago(1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    ##step 1
    #create table is it doesn't exit
    @task
    def create_table():
        #initialize the postgres hook
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_db')
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS apod_data(
                id SERIAL PRIMARY KEY,
                title TEXT,
                explanation TEXT,
                url TEXT,
                date DATE,
                media_type VARCHAR(50)                
            );
        '''

        postgres_hook.run(create_table_query)


    #Step 2 Extract the NASA API data (APOD) Astronomy picture of the day
    #this step is the extract step of the ETL pipeline
    extract_apod = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method = 'GET',
        data={'api_key':'{{conn.nasa_api.extra_dejson.api_key}}'},
        response_filter=lambda response: response.json(),## convert json to response
    )
    #Step 3:
    #transform the data by picking the information we need to save

    @task
    def transform_apod_data(response):
        print('Enter transform appod data')
        apod_data = {
            'title':response.get('title',''),
            'explanation': response.get('explanation',''),
            'url': response.get('url',''),
            'date': response.get('date',''),
            'media_type': response.get('media_type','')
        }
        print(f'Exit with return_val {apod_data}')
        return apod_data

    #step 4:
    #load the data into PostGres DB
    @task
    def load_data_to_postgres(apod_data):
        print('Enter load data into load data into postgres')
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_db')
        insert_query = 'INSERT INTO APOD_DATA(title, explanation, url, date, media_type) ' \
        'VALUES (%s, %s, %s, %s, %s)'
        try:
            postgres_hook.run(insert_query, parameters = (
                apod_data['title'],
                apod_data['explanation'],
                apod_data['url'],
                apod_data['date'],
                apod_data['media_type'],
                )
            )
        except Exception as e:
            print(e)
        print('Enter load data into load data into postgres')

    #step 5 verify the data wiht DBViewer


    #step 6 define task dependencies
    create_table() >>  extract_apod
    api_response = extract_apod.output
    load_data_to_postgres(
        transform_apod_data(api_response)
    )