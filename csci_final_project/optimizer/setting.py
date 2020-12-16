from itertools import product


class OptimizationSetting:
    """
    OptimizationSetting class is used to generate the search space for the optimizers
    """

    def __init__(self):
        """"""
        self.params = {}
        self.target_name = ""

    def add_parameter(
        self, name: str, start: float, end: float = None, step: float = None
    ):
        """
        Add searching parameters
        """

        value = start
        value_list = []

        while value + step <= end:
            value_list.append((value, value + step))
            value += step

        self.params[name] = value_list

    def set_target(self, target_name: str):
        """
        Objective function's column
        """
        self.target_name = target_name

    def generate_setting_ga(self):
        """
        Generate settings for genetic algorithm
        """
        settings_ga = []
        keys = self.params.keys()
        values = self.params.values()
        products = list(product(*values))

        for p in products:
            setting = dict(zip(keys, p))
            param = [tuple(i) for i in setting.items()]
            settings_ga.append(param)

        return settings_ga

    def generate_setting_bf(self):
        """
        Generate settings for brute force
        """
        settings_bf = []
        keys = self.params.keys()
        values = self.params.values()
        products = list(product(*values))

        for p in products:
            setting = dict(zip(keys, p))
            settings_bf.append(setting)

        return settings_bf
