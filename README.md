# CSCI Final Project

[![Build Status](https://travis-ci.com/tanxiao64/2020fa-csci_final_project-tanxiao64.svg?branch=master)](https://travis-ci.com/tanxiao64/2020fa-csci_final_project-tanxiao64)
[![Maintainability](https://api.codeclimate.com/v1/badges/d3b0cb677db44e613b26/maintainability)](https://codeclimate.com/github/tanxiao64/2020fa-csci_final_project-tanxiao64/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d3b0cb677db44e613b26/test_coverage)](https://codeclimate.com/github/tanxiao64/2020fa-csci_final_project-tanxiao64/test_coverage)

## Abstract

This repository displays the coding work for my final project. The goal of the project is to build the workflow to 
optimize output of the backtest results using Airflow with automatic optimizers.


## Background

In quantitative strategy development, people often need to repeat the same workflow to generate a model. 
This workflow is error-prone, especially when people have to go back and forth between “Run backtests” and 
“Optimize strategy” to tune their models. 

Also, the optimization step is often done by manually selecting/filtering of trading signals which is subjective and inefficient. 

In this project, I am building two components:  
1) the automated workflow from collecting data to generating results, 
2) the automated strategy optimizer to pick up the best combination of trading signals.


## Project Structure
* `data/` contains all input & output of the project, such as backtest output, optimized output, graphs etc.
* `DAG/` contains the Airflow dags to be deployed in the Airflow dag folder.
* `csci_final_project/optimizer` contains different classes of optimizers and related classes. They are used to run the 
optimization process.
* `csci_final_project/mockbacktest` contains the fake backtest generator which produces random backtest results but in a standard format.
* `csci_final_project/dataloader` handles data read & write. Can be extended to other file formats.
* `csci_final_project/utils` the general folder for utilities. It contains the salted graph util.
* `csci_final_project/virtulization` contains graphing tools. Currently only plotly is used.
* `csci_final_project/tests` pytest test cases.

## Workflow
The workflow is shown in the Airflow DAG below -
![alt text](https://github.com/tanxiao64/2020fa-csci_final_project-tanxiao64/blob/master/airflow_screenshot.png?raw=true)


To run the workflow, just trigger the dag. The full cycle of backtest optimization is run.


After the run, the user can go to the `data` folder and find the backtest sample file *sample.csv, the optimized backtest
file *best_trades_ga.csv(Genetic Algo) and *best_trades_bf.csv(Brute Force), the corresponding graphs *best_trades_ga_graph.html
and *best_trades_bf_graph.html.

To quickly setup Airflow, please reference https://airflow.apache.org/docs/apache-airflow/stable/start.html

## Topics from the Course
### How salt is added?
The salt is added in each input/output file generated. At the initial step, a hash code is generated by hashing the original
backtest file. The hash(salt) is then passed to the downstream via the "Variable" in Airflow. The user can easily determine which 
output is generated from which input by finding the same file prefix. 

In addition, the user can find the logs of each run in the Airflow UI. 
The parameters of each run are saved in the logs so no information of the optimization process is lost and 
all things are trackable.

### How Dask is used?
Dask is used in the core part of optimizers. Each optimizers has to repeatly evaluate the objective function. Dask is 
used to speed up the calculation of objective function. 

### Other topics
* I explored Airflow as the alternative of Luigi and found it more user friendly. Defining the workflow dependency 
is especially straightforward. 
* I used memorization in the optimizer to avoid repeat calculation. (use @lru_cache decorator) 
* I used OOP pattern to write optimizers so that it is easy to isolate results and modify the workflow. 
The user can also add or modify the optimizers without potentially breaking other parts.
* I used cookiecutter to build the structure of the project.

## Caveats
Airflow itself is in Python and has to run as a server to trigger/scheduler the DAGs. So it is hard to maintain a single 
pipenv environment for both Airflow and the project libraries. My current solution is to keep them separated. I have Airflow 
running in a dedicated conda env and install whatever I have in pipfile.lock to this env. Ideally, I can leverage 
`PythonVirtualenvOperator` provided by Airflow, which creates env at runtime.(But it only support requirements.txt with 
a list of dependencies, not pipfile) 


## Disclaimer
This project background is related to my work experience but the project does not content any of my actual work nor did I borrow any code from my work.  