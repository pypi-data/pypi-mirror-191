from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow operators.dummy_operator import DummyOperator
from pipeline_v2 import DataPipeline


cfg = {"pipeline":[

                    ],
        "dag_settings":{
            "dag_id":"kipling_cn",
            "schedule_interval":"@daily",
            "default_args":{"owner":"clement",
                            "retries":1,
                            "retry_delay":"1min",
                            "start_date":"2022-07-07"}
        }}

def build_dag(self, cfg, dag_settings):
    with DAG(
                dag_id = dag_settings["dag_id"],
                schedule_interval = dag_settings["schedule_interval"],
                default_args=dag_settings["default_args"],
                catchup=False) as dag:
        start = DummyOperator(task_id="start")

        end = DummyOperator(task_id="end")

        for tran_cfg  in cfg:
            



