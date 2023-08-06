import pickle
import os, glob

import pandas as pd
from sklearn.preprocessing import (MinMaxScaler,
                                   StandardScaler,
                                   QuantileTransformer)
from simba.enums import Options


def read_pickle(data_path: str) -> dict:
    if os.path.isdir(data_path):
        data = {}
        files_found = glob.glob(data_path + '/*.pickle')
        if len(files_found) == 0:
            print(f'SIMBA ERROR: Zero pickle files found in {data_path}.')
            raise ValueError
        for file_cnt, file_path in enumerate(files_found):
            with open(file_path, 'rb') as f:
                data[file_cnt] = pickle.load(f)
    if os.path.isfile(data_path):
        with open(data_path, 'rb') as f:
            data = pickle.load(f)

    return data

def check_that_directory_is_empty(directory: str) -> None:
    try:
        all_files_in_folder = [f for f in next(os.walk(directory))[2] if not f[0] == '.']
    except StopIteration:
        return 0
    else:
        if len(all_files_in_folder) > 0:
            print('''ssss''')
            print(f'SIMBA ERROR: The {directory} is not empty and contains {str(len(all_files_in_folder))} files. Use a directory that is empty.')
            raise ValueError()


def check_directory_exists(directory: str) -> None:
    if not os.path.isdir(directory):
        print(f'SIMBA ERROR: {directory} is not a valid directory.')
        raise NotADirectoryError
    else:
        pass

def define_scaler(scaler_name: str):
    if scaler_name not in Options.SCALER_NAMES.value:
        print('SIMBA ERROR: {} is not a valid scaler option (VALID OPTIONS: {}'.format(scaler_name, Options.SCALER_NAMES.value))
        raise ValueError()
    if scaler_name == 'MIN-MAX':
        return MinMaxScaler()
    elif scaler_name == 'STANDARD':
        return StandardScaler()
    elif scaler_name == 'QUANTILE':
        return QuantileTransformer()

def drop_low_variance_fields(data: pd.DataFrame, fields: list):
    return data.drop(columns=fields)


def scaler_transform(data: pd.DataFrame, scaler: object):
    return pd.DataFrame(scaler.transform(data), columns=data.columns)

def find_embedding(embeddings: dict, hash: str):
    for k, v in embeddings.items():
        if v['HASH'] == hash:
            return v
    print(f'SIMBA ERROR: {hash} embedder could not be found in the embedding directory.')
    raise FileNotFoundError()

