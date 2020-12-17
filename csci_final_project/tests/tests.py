import os
from tempfile import TemporaryDirectory
from unittest import TestCase
import pandas as pd
from csci_final_project.dataloader.filehandler import (
    saveCSV,
    loadCSV,
    validate,
    file_exist,
)
from csci_final_project.mockbacktest.backtest_output_producer import (
    generate_fake_output,
)
from csci_final_project.virtulization.graph_plotly import read_csv_file_and_plot
from csci_final_project.optimizer.setting import OptimizationSetting
from csci_final_project.optimizer.ga import GeneticAlgorithm
from csci_final_project.optimizer.bf import Bruteforce
from datetime import datetime


class FilehandlerTest(TestCase):
    def test_filehandler(self):
        """
        Test file read and write functions
        """
        with TemporaryDirectory() as tmp:
            filename = "asdf.csv"
            file_path = tmp + "/"
            tmp_data = pd.DataFrame(
                [[1, 2, 3], [3, 4, 5]],
                index=[0, 1],
                columns=["start_date", "end_date", "pnl"],
            )

            saveCSV(tmp_data, filename, file_path)
            self.assertEqual(file_exist(filename, file_path), True)

            loaded_data = loadCSV(filename, file_path)
            self.assertEqual(len(loaded_data), 2)
            self.assertEqual(loaded_data.iloc[0, 0], 1)

            self.assertEqual(validate(filename, file_path), True)


class BacktestProducerTest(TestCase):
    def test_BacktestProducer(self):
        """
        Check if the backtest producer generate files in the correct format
        """
        with TemporaryDirectory() as tmp:
            filename = "asdf.csv"
            file_path = tmp
            generate_fake_output(
                signal_num=5, row_num=10, filename=filename, file_path=file_path
            )
            loaded_data = loadCSV(filename, file_path)
            self.assertEqual(len(loaded_data), 10)
            self.assertEqual("signal_5" in loaded_data.columns, True)

            self.assertEqual(validate(filename, file_path), True)


class GraphPlotlyTest(TestCase):
    def test_GraphPlotly(self):
        """
        Check if the graphing utilities works - plotly
        """
        with TemporaryDirectory() as tmp:
            filename = "asdf.csv"
            file_path = tmp
            generate_fake_output(
                signal_num=5, row_num=10, filename=filename, file_path=file_path
            )
            read_csv_file_and_plot(filename, file_path)

            self.assertEqual(os.path.exists(file_path + "asdf_graph.html"), True)


class OptimizationSettingsTest(TestCase):
    def testOptimizationSettings(self):
        """
        Test the optimizationSetting class. Check if it can produce correct search space
        """
        setting = OptimizationSetting()
        setting.set_target("pnl")
        setting.add_parameter("signal_1", start=0, end=1, step=0.1)
        setting.add_parameter("signal_2", start=0, end=1, step=0.2)
        self.assertEqual(len(setting.generate_setting_ga()), 50)
        self.assertEqual(len(setting.generate_setting_bf()), 50)


class OptimizerTest(TestCase):
    def testOptimizers(self):
        """Check if the implementation of optimizers work
        Compare if results are the same among optimizers
        """
        with TemporaryDirectory() as tmp:
            filename = "asdf.csv"
            file_path = tmp
            tmp_data = pd.DataFrame(
                [
                    [datetime(2020, 1, 2), datetime(2020, 1, 3), -1, 0.5, 0.4],
                    [datetime(2020, 1, 3), datetime(2020, 1, 4), 1, 0.6, 0.5],
                    [datetime(2020, 1, 4), datetime(2020, 1, 5), 2, 0.7, 0.6],
                    [datetime(2020, 1, 5), datetime(2020, 1, 6), 1, 0.8, 0.7],
                    [datetime(2020, 1, 6), datetime(2020, 1, 7), 3, 0.9, 0.8],
                ],
                index=[0, 1, 2, 3, 4],
                columns=["start_date", "end_date", "pnl", "signal_1", "signal_2"],
            )

            saveCSV(tmp_data, filename, file_path)

            setting = OptimizationSetting()
            setting.set_target("pnl")
            setting.add_parameter("signal_1", start=0, end=1, step=0.1)
            setting.add_parameter("signal_2", start=0, end=1, step=0.2)

            op = GeneticAlgorithm(filename=filename, filepath=file_path)
            res_ga = op.run_optimization(setting)

            self.assertEqual(res_ga[0][1][0], 3)  # optimized pnl
            op.output_data_best_signal("temp_output_ga.csv")
            loaded_data = loadCSV("temp_output_ga.csv", file_path)
            self.assertEqual(loaded_data["pnl"].sum(), 3)  # optimized pnl

            op = Bruteforce(filename=filename, filepath=file_path)
            res_bf = op.run_optimization(setting)
            self.assertEqual(res_bf[-1][1], 3)  # optimized pnl
            op.output_data_best_signal("temp_output_bf.csv")
            loaded_data = loadCSV("temp_output_bf.csv", file_path)
            self.assertEqual(loaded_data["pnl"].sum(), 3)  # optimized pnl
