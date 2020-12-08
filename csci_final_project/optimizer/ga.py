from functools import lru_cache
from itertools import product
from deap import creator, base, tools, algorithms
import random
import numpy as np

import logging

from csci_final_project.dataloader import filehandler

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

class OptimizationSetting:
    """
    Setting class.
    """

    def __init__(self):
        """"""
        self.params = {}
        self.target_name = ""


    def add_parameter(
        self, name: str, start: float, end: float = None, step: float = None
    ):
        """"""

        value = start
        value_list = []

        while value+step <= end:
            value_list.append((value, value+step))
            value += step

        self.params[name] = value_list

    def set_target(self, target_name: str):
        """"""
        self.target_name = target_name

    def generate_setting_ga(self):
        """"""
        settings_ga = []
        keys = self.params.keys()
        values = self.params.values()
        products = list(product(*values))

        for p in products:
            setting = dict(zip(keys, p))
            param = [tuple(i) for i in setting.items()]
            settings_ga.append(param)

        return settings_ga


class GeneticAlgorithm:

    def __init__(self, filename, filepath):
        self.data = filehandler.loadCSV(filename, filepath)
        self.target_name = 'pnl'
        self.results = []
        self.filename = filename
        self.filepath = filepath

    def _calculate_metrix(self, data):
        if len(data) > 0:
            return data[self.target_name].sum()
        return 0

    @lru_cache(maxsize=100000)
    def _ga_optimize(self, parameter_values: tuple):
        """"""
        ind = dict(parameter_values)
        data_filtered = self.data.copy()
        for col, val in ind.items():
            lower = val[0]
            upper = val[1]
            data_filtered = data_filtered.loc[(data_filtered[col]> lower)&(data_filtered[col]<= upper)]

        return (self._calculate_metrix(data_filtered),)

    def _evaluate(self, parameter_values: list):
        """"""
        return self._ga_optimize(tuple(parameter_values))

    def run_optimization(self, optimization_setting, population_size=100, ngen_size=30):
        """"""
        # Get optimization setting and target
        settings = optimization_setting.generate_setting_ga()
        self.target_name = optimization_setting.target_name

        # Define parameter generation function
        def generate_parameter():
            """"""
            return random.choice(settings)

        def mutate_individual(individual, indpb):
            """"""
            size = len(individual)
            paramlist = generate_parameter()
            for i in range(size):
                if random.random() < indpb:
                    individual[i] = paramlist[i]
            return individual,


        # Set up genetic algorithem
        toolbox = base.Toolbox()
        toolbox.register("individual", tools.initIterate, creator.Individual, generate_parameter)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", mutate_individual, indpb=1)
        toolbox.register("evaluate", self._evaluate)
        toolbox.register("select", tools.selNSGA2)

        total_size = len(settings)
        pop_size = population_size  # number of individuals in each generation
        lambda_ = pop_size  # number of children to produce at each generation
        mu = int(pop_size * 0.8)  # number of individuals to select for the next generation

        cxpb = 0.95
        mutpb = 1 - cxpb
        ngen = ngen_size

        pop = toolbox.population(pop_size)
        hof = tools.ParetoFront()

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        # np.set_printoptions(suppress=True)
        stats.register("mean", np.mean, axis=0)
        stats.register("std", np.std, axis=0)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

        # Run ga optimization
        logging.info(f"total size：{total_size}")
        logging.info(f"population size：{pop_size}")
        logging.info(f"individuals for the next generation：{mu}")
        logging.info(f"number of generation：{ngen}")
        logging.info(f"probability of mating two individuals：{cxpb:.0%}")
        logging.info(f"probability of mutating an individual：{mutpb:.0%}")


        algorithms.eaMuPlusLambda(
            pop,
            toolbox,
            mu,
            lambda_,
            cxpb,
            mutpb,
            ngen,
            stats,
            halloffame=hof
        )

        # Return result list
        results = []

        for parameter_values in hof:
            setting = dict(parameter_values)
            target_value = self._evaluate(parameter_values)
            results.append((setting, target_value, {}))

        self.results = results
        logging.info(f"Best signal combination {results[0]} ")
        return results

    def output_data_best_signal(self, output_filename):
        data_filtered = self.data.copy()
        for col, val in self.results[0][0].items():
            lower = val[0]
            upper = val[1]
            data_filtered = data_filtered.loc[(data_filtered[col]> lower)&(data_filtered[col]<= upper)]
        filehandler.saveCSV(data_filtered, output_filename, self.filepath)


# setting = OptimizationSetting()
# setting.set_target('pnl')
# setting.add_parameter('signal_1', start=0, end=1, step=0.5)
# setting.add_parameter('signal_2', start=0, end=1, step=0.5)
#
# ga = GeneticAlgorithm(filename='sample.csv', filepath='/Users/xiaotan/Course/2020fa-csci_final_project-tanxiao64/data/')
# print(ga.run_optimization(setting))
# ga.output_data_best_signal('best.csv')

