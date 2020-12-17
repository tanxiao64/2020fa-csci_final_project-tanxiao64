from csci_final_project.optimizer.setting import OptimizationSetting
import logging
from airflow.models import Variable


def main(
    optimizer,
    filename,
    file_path,
    target="pnl",
    output_filename="best_trades.csv",
    use_salt=False,
):  # pragma: no cover
    """
    Create settings and run optimization based on the passed in optimizer
    """
    setting = OptimizationSetting()
    setting.set_target(target)
    setting.add_parameter("signal_1", start=0, end=1, step=0.1)
    setting.add_parameter("signal_2", start=0, end=1, step=0.1)

    if use_salt:
        filename = Variable.get("salt") + filename
        output_filename = Variable.get("salt") + output_filename
    op = optimizer(filename=filename, filepath=file_path)
    logging.info(op.run_optimization(setting))
    op.output_data_best_signal(output_filename)
