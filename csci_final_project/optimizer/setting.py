from itertools import product


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
