import pandas as pd
import numpy as np
from csci_final_project.dataloader.filehandler import saveCSV


def generate_fake_output(signal_num, row_num, filename, file_path, init_start_date='1/1/2000', init_end_date='1/2/2000'):
    data = np.random.rand(row_num, signal_num)
    start_date = pd.date_range(start=init_start_date, periods=row_num).values
    end_date = pd.date_range(start=init_end_date, periods=row_num).values
    pnl = np.random.randint(-100, 100, row_num)
    df = pd.DataFrame(data, columns=['signal_' + str(i+1) for i in range(signal_num)])
    df['start_date'] = start_date
    df['end_date'] = end_date
    df['pnl'] = pnl
    saveCSV(df, filename, file_path)

# generate_fake_output(5, 7000, 'sample.csv', 'data/')
