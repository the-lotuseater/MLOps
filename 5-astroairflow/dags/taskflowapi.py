'''
Docstring for 5-astroairflow.dags.taskflowapi
Airflow introduced the task flow API which allows you to create tasks using python decorators like @task

'''




from airflow import DAG
from airflow.decorators import task
from datetime import datetime


with DAG(
        dag_id='math_sequence_dag_with_airflow',
        start_date=datetime(2025,12,1),
        schedule='@once',
        catchup=False
    ) as dag:
    #TASK1 start with initial number
    @task
    def start_number():
        initial_value=10
        print(f'Starting number: {initial_value}')
        return initial_value
    
    @task
    def add_five(curr_val:int):
        new_val = curr_val+5
        print(f'Result after adding 5 {new_val}')
        return new_val

    @task
    def multiply_by_two(curr_val:int):
        new_val = curr_val*2
        print(f'Result after multiplying by 2{new_val}')
        return new_val

    
    @task 
    def subtract_three(curr_val:int):
        new_val = curr_val-3
        print(f'Result after subtract three {new_val}')
        return new_val

    @task
    def square_number(curr_val:int):
        new_val = curr_val**2
        print(f'New value after squaring is {new_val}')
        return new_val


    square_number(
        subtract_three(
            multiply_by_two(
                add_five(
                    start_number()
                )
            )
        )
    )

