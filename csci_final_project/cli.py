from csci_final_project.optimizer.ga import OptimizationSetting, GeneticAlgorithm


def main(optimizer, filename, **kwargs):
    setting = OptimizationSetting()
    setting.set_target('pnl')
    setting.add_parameter('signal_1', start=0, end=1, step=0.5)
    setting.add_parameter('signal_2', start=0, end=1, step=0.5)

    ga = GeneticAlgorithm(filename='sample.csv', filepath='/Users/xiaotan/Course/2020fa-csci_final_project-tanxiao64/data/')
    print(ga.run_optimization(setting))
    ga.output_data_best_signal('best.csv')



