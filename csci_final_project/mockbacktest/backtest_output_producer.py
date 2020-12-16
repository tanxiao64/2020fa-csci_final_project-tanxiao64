import shutil

import pandas as pd
import numpy as np
from csci_final_project.dataloader.filehandler import saveCSV
from csci_final_project.utils.salted import get_salt
from airflow.models import Variable


def generate_fake_output(
    signal_num,
    row_num,
    filename,
    file_path,
    init_start_date="1/1/2000",
    init_end_date="1/2/2000",
    use_salt=False
):
    """
    Generate fake backtest output csv files. Attach 'salt' to the file name.
    I use Airflow Variable to store the global variable salt which is consumed by the downstream processes
    """
    data = np.random.rand(row_num, signal_num)
    start_date = pd.date_range(start=init_start_date, periods=row_num).values
    end_date = pd.date_range(start=init_end_date, periods=row_num).values
    pnl = np.random.randint(-100, 100, row_num)
    df = pd.DataFrame(data, columns=["signal_" + str(i + 1) for i in range(signal_num)])
    df["start_date"] = start_date
    df["end_date"] = end_date
    df["pnl"] = pnl

    saveCSV(df, filename, file_path)
    # generate salt and copy the file with a salted filename
    if use_salt:
        salt = get_salt(file_path + filename)
        salted_file = file_path + salt + filename
        shutil.copy(file_path + filename, salted_file)

        Variable.set("salt", salt)
