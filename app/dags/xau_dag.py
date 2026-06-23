#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the tasks
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# DAG 1: Retrieve Gold Price
dag_get = DAG(
    'xau_get_gold_price',
    default_args=default_args,
    description='Retrieves gold price from the Spuerkeess API',
    schedule_interval='22,52 * * * *',
    catchup=False,
)

get_task = BashOperator(
    task_id='get_gold_price',
    bash_command='cd /opt/airflow/XAU && python get_gold_price.py',
    dag=dag_get,
)

# DAG 2: Load Gold Price to Database
dag_load = DAG(
    'xau_load_price',
    default_args=default_args,
    description='Loads the retrieved gold price into the MySQL database',
    schedule_interval='25,55 * * * *',
    catchup=False,
)

load_task = BashOperator(
    task_id='load_xau',
    bash_command='cd /opt/airflow/XAU && python load_xau.py',
    dag=dag_load,
)
