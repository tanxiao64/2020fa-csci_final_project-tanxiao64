from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from csci_final_project.dataloader import filehandler
from csci_final_project import cli
from csci_final_project.optimizer import ga
from csci_final_project.virtulization import graphPlotly

default_args = {
    'owner': 'xt',
    'start_date': datetime(2020, 12, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    'run_ga_optimizer',
    default_args=default_args,
    description='consume the output from backtest and run ga optimizer. output optimized trades and draw graphs',
    schedule_interval=None,
)

filename = 'sample.csv'
check_data_exit = PythonOperator(
    task_id='check_data_exist',
    python_callable=filehandler.file_exist,
    op_kwargs={'filename': filename},
    dag=dag,
)

validate_data = PythonOperator(
    task_id='validate_data',
    python_callable=filehandler.validate,
    op_kwargs={'filename': filename},
    dag=dag,
)

run_optimization = PythonOperator(
    task_id='run_optimization',
    python_callable=cli.main,
    op_kwargs={'optimizer': ga, 'filename': filename},
    dag=dag,
)

output_optimized_graphs = PythonOperator(
    task_id='output_graphs',
    python_callable=graphPlotly.read_csv_file_and_plot,
    op_kwargs={},
    dag=dag,
)


check_data_exit >> validate_data >> run_optimization >> output_optimized_graphs
