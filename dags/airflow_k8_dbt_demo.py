from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
        'airflow_k8_dbt_demo',
        # These args will get passed on to each operator
        # You can override them on a per-task basis during operator initialization
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='A simple tutorial DAG',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2022, 1, 1),
        catchup=False,
        tags=['example']
) as dag:
    dbt_run = KubernetesPodOperator(
        namespace="k8-executor",  # the new namespace you've created in the Workload Identity creation process
        service_account_name="composer", # the new k8 service account you've created in the Workload Identity creation process
        image="eu.gcr.io/rocketech-de-pgcp-sandbox/airflow-k8-dbt-demo:1.0.1",
        cmds=["bash", "-cx"],
        arguments=["dbt run --project-dir dbt_k8_demo"],
        labels={"foo": "bar"},
        name="dbt-run-k8",
        task_id="run_dbt_job_on_k8_demo",
        image_pull_policy="Always",
        get_logs=True,
        dag=dag
    )

    dbt_run.dry_run()
