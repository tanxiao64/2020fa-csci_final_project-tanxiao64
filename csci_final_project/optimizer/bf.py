from functools import lru_cache
import os
import logging
import dask.dataframe as dd
from csci_final_project.dataloader import filehandler


class Bruteforce:
    """
    The Brute Force optimizer
    """

    def __init__(self, filename, filepath, target_name="pnl"):
        self.data = filehandler.loadCSV(filename, filepath)
        self.target_name = target_name
        self.results = []
        self.filename = filename
        self.filepath = filepath

    def _calculate_metrics(self, data):
        """The objective function metrics"""
        if len(data) > 0:
            return data[self.target_name].sum().compute()
        return 0

    @lru_cache(maxsize=100000)
    def _bf_optimize(self, parameter_values: tuple):
        """
        Here I use lru cache to memorize the parameter combinations that have searched before
        """
        ind = dict(parameter_values)
        data_filtered = dd.from_pandas(
            self.data, npartitions=max(1, os.cpu_count() - 1)
        )
        for col, val in ind.items():
            lower = val[0]
            upper = val[1]
            data_filtered = data_filtered.loc[
                (data_filtered[col] > lower) & (data_filtered[col] <= upper)
            ]

        return self._calculate_metrics(data_filtered)

    def _evaluate(self, parameter_values: list):
        return self._bf_optimize(tuple(parameter_values))

    def run_optimization(self, optimization_setting, max_iteration=100000000):
        """
        The entry point to run optimization
        """
        # Get optimization setting and target
        settings = optimization_setting.generate_setting_ga()
        self.target_name = optimization_setting.target_name

        total_size = len(settings)

        # Run ga optimization
        logging.info(f"total search space size：{total_size}")
        score = dict()
        counter = 0
        for combination in settings:
            score[self._evaluate(combination)] = combination
            counter += 1
            if counter > max_iteration:
                logging.warning("Max number of iteration reached. Search stopped.. ")
                break

        results = []
        for key in sorted(score.keys()):
            results.append((score[key], key))

        # Return result list

        self.results = results
        logging.info(f"Best signal combination {results[-1]} ")
        return results

    def output_data_best_signal(self, output_filename):
        data_filtered = self.data.copy()
        for col, val in self.results[-1][0]:
            lower = val[0]
            upper = val[1]
            data_filtered = data_filtered.loc[
                (data_filtered[col] > lower) & (data_filtered[col] <= upper)
            ]
        filehandler.saveCSV(data_filtered, output_filename, self.filepath)


# from csci_final_project.optimizer.setting import OptimizationSetting
# setting = OptimizationSetting()
# setting.set_target('pnl')
# setting.add_parameter('signal_1', start=0, end=1, step=0.4)
# setting.add_parameter('signal_2', start=0, end=1, step=0.5)
#
# b = Bruteforce(filename='sample.csv', filepath='/Users/xiaotan/Course/2020fa-csci_final_project-tanxiao64/data/')
# print(b.run_optimization(setting))
# b.output_data_best_signal('best.csv')
