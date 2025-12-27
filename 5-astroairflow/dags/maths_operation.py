'''
Define a DAG where the tasks are as follows:

Task 0: Start with an initial number
Task 1: Add 5 to the number.
Task 2: Multiply the result by 2
Task 3: Subtract 3 from the result.
Task 4: Compute the square of the result.
'''

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

##Define function for each task
def start_number(**context):
    context['ti'].xcom_push(key='current_value',value=10)
    print('Starting number is 10')

    
def add_five(**context):
    current_val=context['ti'].xcom_pull(key='current_value', task_ids='start_task')
    print(f'Result after before 5{current_val}')
    new_value = current_val+5
    print(f'Result after adding 5{new_value}')
    context['ti'].xcom_push(key='current_value',value=new_value)


def multiply_by_two(**context):
    current_val=context['ti'].xcom_pull(key='current_value', task_ids='add_five_task')
    print(f'Value before multiplying by 2 {current_val}')
    new_val = current_val*2
    context['ti'].xcom_push(key='current_value',value=new_val)
    print(f'Value after multiplying by two {new_val}')


def subtract_three(**context):
    current_val=context['ti'].xcom_pull(key='current_value', task_ids='multiply_by_2_task')
    print(f'Value before subtracting 3 {current_val}')
    new_val = current_val-3
    context['ti'].xcom_push(key='current_value',value=new_val)
    print(f'Result after subtracting by 3{current_val}-3 = {new_val}')


def square_number(**context):
    current_val=context['ti'].xcom_pull(key='current_value', task_ids='subtract_3_task')
    print(f'Result before squaring number {current_val}')
    new_val = current_val**2
    context['ti'].xcom_push(key='current_value',value=new_val)
    print(f'Result after squaring number {new_val}')

with DAG(dag_id='math_sequence_dag',
        start_date=datetime(2025,12,26),
        schedule='@once',
        catchup=False) as dag:
    ##define the task
    start_task = PythonOperator(task_id='start_task',
                                python_callable=start_number)

    add_five_task = PythonOperator(task_id='add_five_task',
                                python_callable=add_five)
    
    multiply_by_two_task = PythonOperator(task_id='multiply_by_2_task',
                                python_callable=multiply_by_two)
    
    subtract_three_task = PythonOperator(task_id='subtract_3_task',
                                python_callable=subtract_three)

    square_number_task = PythonOperator(task_id='square_number_task',
                                python_callable=square_number)


    ##dependencies
    start_task >> add_five_task >> multiply_by_two_task >> subtract_three_task >> square_number_task
