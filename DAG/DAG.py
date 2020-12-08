from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from csci_final_project.dataloader import filehandler
from csci_final_project import cli
from csci_final_project.optimizer.ga import GeneticAlgorithm
from csci_final_project.virtulization import graph_plotly
from csci_final_project.mockbacktest import backtest_output_producer

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
file_path = '/Users/xiaotan/Course/2020fa-csci_final_project-tanxiao64/data/'

generate_mock_backtest_output = PythonOperator(
    task_id='generate_mock_backtest_output',
    python_callable=backtest_output_producer.generate_fake_output,
    op_kwargs={'signal_num': 5, 'row_num': 7000, 'filename': filename, 'file_path': file_path},
    dag=dag,
)

check_data_exit = PythonOperator(
    task_id='check_data_exist',
    python_callable=filehandler.file_exist,
    op_kwargs={'filename': filename, 'file_path': file_path},
    dag=dag,
)

validate_data = PythonOperator(
    task_id='validate_data',
    python_callable=filehandler.validate,
    op_kwargs={'filename': filename, 'file_path': file_path},
    dag=dag,
)

run_optimization = PythonOperator(
    task_id='run_optimization',
    python_callable=cli.main,
    op_kwargs={'optimizer': GeneticAlgorithm, 'filename': filename, 'file_path': file_path},
    dag=dag,
)

output_optimized_graphs = PythonOperator(
    task_id='output_optimized_graphs',
    python_callable=graph_plotly.read_csv_file_and_plot,
    op_kwargs={'filename': 'best_trades.csv', 'file_path': file_path},
    dag=dag,
)

output_original_graphs = PythonOperator(
    task_id='output_original_graphs',
    python_callable=graph_plotly.read_csv_file_and_plot,
    op_kwargs={'filename': filename, 'file_path': file_path},
    dag=dag,
)


generate_mock_backtest_output >> check_data_exit >> validate_data >> run_optimization >> output_optimized_graphs
validate_data >> output_original_graphs