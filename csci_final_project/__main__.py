from csci_final_project.cli import main
from csci_final_project.optimizer.ga import GeneticAlgorithm

if __name__ == "__main__":  # pragma: no cover
    file_path = "../data/"
    main(
        GeneticAlgorithm,
        "sample.csv",
        file_path,
        target="pnl",
        output_filename="best_trades.csv",
    )
