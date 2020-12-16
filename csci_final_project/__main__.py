from csci_final_project.cli import main
from csci_final_project.mockbacktest.backtest_output_producer import (
    generate_fake_output,
)
from csci_final_project.virtulization.graph_plotly import read_csv_file_and_plot
from csci_final_project.optimizer.ga import GeneticAlgorithm
from csci_final_project.optimizer.bf import Bruteforce

if __name__ == "__main__":  # pragma: no cover
    file_path = "data/"
    filename = "sample.csv"
    generate_fake_output(
        signal_num=5, row_num=7000, filename=filename, file_path=file_path
    )

    main(
        GeneticAlgorithm,
        filename,
        file_path,
        target="pnl",
        output_filename="best_trades_ga.csv",
    )
    read_csv_file_and_plot("best_trades_ga.csv", file_path)

    main(
        Bruteforce,
        filename,
        file_path,
        target="pnl",
        output_filename="best_trades_bf.csv",
    )
    read_csv_file_and_plot("best_trades_bf.csv", file_path)
