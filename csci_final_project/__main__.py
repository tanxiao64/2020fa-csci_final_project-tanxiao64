from csci_final_project.cli import main
from csci_final_project.optimizer.ga import GeneticAlgorithm

if __name__ == "__main__":
    file_path = '/Users/xiaotan/Course/2020fa-csci_final_project-tanxiao64/data/'
    main(GeneticAlgorithm, 'sample.csv', file_path, target='pnl', output_filename='best_trades.csv')
