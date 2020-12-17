from datetime import timedelta, datetime

from csci_final_project.dataloader import filehandler
from csci_final_project import cli
from csci_final_project.optimizer.ga import GeneticAlgorithm
from csci_final_project.optimizer.bf import Bruteforce
from csci_final_project.virtulization import graph_plotly
from csci_final_project.mockbacktest import backtest_output_producer

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "xt",
    "start_date": datetime(2020, 12, 7),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
# define dag parameters. no need to add scheduler
dag = DAG(
    "run_optimizer",
    default_args=default_args,
    description="consume the output from backtest and run optimizers. output optimized trades and draw graphs",
    schedule_interval=None,
)

filename = "sample.csv"
file_path = "/Users/xiaotan/Course/2020fa-csci_final_project-tanxiao64/data/"

# define tasks below
generate_mock_backtest_output = PythonOperator(
    task_id="generate_mock_backtest_output",
    python_callable=backtest_output_producer.generate_fake_output,
    op_kwargs={
        "signal_num": 5,
        "row_num": 7000,
        "filename": filename,
        "file_path": file_path,
        "use_salt": True,
    },
    dag=dag,
)

check_data_exist = PythonOperator(
    task_id="check_data_exist",
    python_callable=filehandler.file_exist,
    op_kwargs={"filename": filename, "file_path": file_path, "use_salt": True},
    dag=dag,
)

validate_data = PythonOperator(
    task_id="validate_data",
    python_callable=filehandler.validate,
    op_kwargs={"filename": filename, "file_path": file_path, "use_salt": True},
    dag=dag,
)

run_optimization_ga = PythonOperator(
    task_id="run_optimization_ga",
    python_callable=cli.main,
    op_kwargs={
        "optimizer": GeneticAlgorithm,
        "filename": filename,
        "file_path": file_path,
        "output_filename": "best_trades_ga.csv",
        "use_salt": True,
    },
    dag=dag,
)

run_optimization_bf = PythonOperator(
    task_id="run_optimization_bf",
    python_callable=cli.main,
    op_kwargs={
        "optimizer": Bruteforce,
        "filename": filename,
        "file_path": file_path,
        "output_filename": "best_trades_bf.csv",
        "use_salt": True,
    },
    dag=dag,
)


output_optimized_graphs_ga = PythonOperator(
    task_id="output_optimized_graphs_ga",
    python_callable=graph_plotly.read_csv_file_and_plot,
    op_kwargs={
        "filename": "best_trades_ga.csv",
        "file_path": file_path,
        "use_salt": True,
    },
    dag=dag,
)

output_optimized_graphs_bf = PythonOperator(
    task_id="output_optimized_graphs_bf",
    python_callable=graph_plotly.read_csv_file_and_plot,
    op_kwargs={
        "filename": "best_trades_bf.csv",
        "file_path": file_path,
        "use_salt": True,
    },
    dag=dag,
)

output_original_graphs = PythonOperator(
    task_id="output_original_graphs",
    python_callable=graph_plotly.read_csv_file_and_plot,
    op_kwargs={"filename": filename, "file_path": file_path, "use_salt": True},
    dag=dag,
)

# define the dependency graph
generate_mock_backtest_output >> check_data_exist >> validate_data >> run_optimization_ga >> output_optimized_graphs_ga
validate_data >> run_optimization_bf >> output_optimized_graphs_bf
validate_data >> output_original_graphs
