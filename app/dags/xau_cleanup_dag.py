#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
# Runs every hour at minute 49
with DAG(
    'xau_cleanup_archiving',
    default_args=default_args,
    description='Archives XAU data into monthly zip files and cleans up old JSON files.',
    schedule='49 * * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['cleanup', 'xau', 'maintenance'],
) as dag:

    # Execute the central cleanup script which handles the zipping and unzipping validation
    run_cleanup = BashOperator(
        task_id='run_xau_cleanup',
        bash_command='bash /opt/airflow/XAU/clean_xau.sh /opt/airflow/XAU ',
    )

    run_cleanup
