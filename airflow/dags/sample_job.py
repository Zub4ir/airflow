# %%
import datetime, time

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.param import Param
from airflow.utils.dates import days_ago

# %%

# dag meta
default_args = {
    'owner': 'Jordan Petersen',
    'retries': 0,
    'retry_delay': datetime.timedelta(seconds=30),
    'email': ['jordan.perterson@gmail.co.za'],
    'email_on_retry': False,
    'email_on_failure': True,
    }

# dag params
dag_sample_job = DAG(
    dag_id='sample-job',
    concurrency=2,
    max_active_runs=2,
    is_paused_upon_creation=False,
    default_args=default_args,
    schedule=None,
    start_date=days_ago(1),
    dagrun_timeout=datetime.timedelta(minutes=1),
    description='Sample AirFlow Dag',
    params={'data': Param(default='', type='string')}
)

# %%

def lets_wait():

    print('---> lets wait for 5 seconds')
    time.sleep(5)

def lets_print(**context):

    print('---> lets print')
    print(context['params'])
    print(context['params']['data'])

# %%

run1 = PythonOperator(python_callable=lets_wait, task_id="lets-wait", dag=dag_sample_job)

run2 = PythonOperator(python_callable=lets_print, task_id="lets-print", dag=dag_sample_job)

# %%

run1 >> run2

# %%

if __name__ == "__main__":
    dag_sample_job.cli()
