import pandas as pd
import os


def loadCSV(filename, file_path=None, **kwargs):
    if file_path is None:
        file_path = 'data/'
    trades = pd.read_csv(file_path + filename)
    return trades

def saveCSV(data, filename, file_path=None, **kwargs):
    if file_path is None:
        file_path = 'data/'
    data.to_csv(file_path + filename)


def file_exist(filename, file_path=None, **kwargs):
    if file_path is None:
        file_path = 'data/'
    if not os.path.exists(file_path + filename):
        raise FileNotFoundError()


def validate(filename, file_path=None, **kwargs):
    if file_path is None:
        file_path = 'data/'

    trades = pd.read_csv(file_path + filename)
    if not ('start_date' in trades.columns and 'end_date' in trades.columns and 'pnl' in trades.columns):
        raise Exception('Csv trade file does not have expected column')
