from airflow.providers.standard.operators.python import ExternalPythonOperator
from airflow.sdk import DAG
from airflow.models import Variable
from airflow.decorators import task
from datetime import timedelta

# path to python exec in venv
python_exec_path = Variable.get("MACHINEDATA_PROCESSING_PYTHON_EXEC_PATH")

# use date from airflow variable if present
date = Variable.get("MACHINEDATA_PROCESSING_DAG_DATE")

with DAG(
    "machinedata_processing_dag",
    default_args={
        "depends_on_past": False,
        "retries": 0,
        "retry_delay": timedelta(minutes=1)
    },
    description="Update machine events with stamping data",
    schedule="15 4 * * *"
) as dag:
    
    @task.external_python(python=python_exec_path, task_id="do_the_thing")
    def machinedata_processing_task(date=None):
        import os
        from tuova_machinedata_processing import process

        os.environ["TZ"] = "Europe/Helsinki"
        process.run(date=date, dry_run=True)
