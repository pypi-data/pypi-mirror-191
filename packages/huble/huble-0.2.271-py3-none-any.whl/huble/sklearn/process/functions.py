import re
from re import sub
from sklearn import impute
from sklearn import preprocessing
import pandas as pd
from scipy import stats
import numpy as np
from datacleaner import autoclean
from ...error.decorators import function_error_handling

# @function_error_handling("remove_nan_values")
def remove_nan_values(**params):
    data = params["data"]
    data = data.dropna(**params["parameters"])
    return data


# @function_error_handling("replace_nan_values")
def replace_nan_values(**params):
    imputer = impute.SimpleImputer(**params["parameters"])
    data = params["data"]
    data[(params["column"])] = imputer.fit_transform(
        data[(params["column"])].values.reshape(-1, 1)
    )[:, 0]
    return data


# @function_error_handling("drop_rows_columns")
def drop_rows_columns(**params):
    data = params["data"]
    data = data.drop(**params["parameters"])
    return data


# @function_error_handling("remove_outliers")
def remove_outliers(**params):
    data = params["data"]
    for column in params["columns"]:
        data = data[(np.abs(stats.zscore(data[(column)])) < 3)]
    return data


# @function_error_handling("drop_duplicates")
def drop_duplicates(**params):
    data = params["data"]
    data = data.drop_duplicates()
    return data


# @function_error_handling("change_data_type")
def change_data_type(**params):
    data = params["data"]
    data[(params["column"])] = data[(params["column"])].astype(**params["parameters"])
    return data


# @function_error_handling("round_data")
def round_data(**params):
    data = params["data"]
    data = data.round(**params["parameters"])
    return data


# @function_error_handling("filter_dataframe")
def filter_dataframe(**params):
    data = params["data"]
    data = data.filter(**params["parameters"])
    return data


# @function_error_handling("truncate_dataframe")
def truncate_dataframe(**params):
    data = params["data"]
    data = data.truncate(**params["parameters"])
    return data


# @function_error_handling("sort_values")
def sort_values(**params):
    data = params["data"]
    data = data.sort_values(**params["parameters"])
    return data


# @function_error_handling("transpose")
def transpose(**params):
    data = params["data"]
    data = data.transpose()
    return data


# @function_error_handling("min_max_scale")
def min_max_scale(**params):
    data = params["data"]
    scaler = preprocessing.MinMaxScaler(**params["parameters"])
    data[(params["column"])] = scaler.fit_transform(
        data[(params["column"])].values.reshape(-1, 1)
    )[:, 0]
    return data


# @function_error_handling("max_abs_scale")
def max_abs_scale(**params):
    data = params["data"]
    scaler = preprocessing.MaxAbsScaler(**params["parameters"])
    data[(params["column"])] = scaler.fit_transform(
        data[(params["column"])].values.reshape(-1, 1)
    )[:, 0]
    return data


# @function_error_handling("robust_scale")
def robust_scale(**params):
    data = params["data"]
    scaler = preprocessing.RobustScaler(**params["parameters"])
    data[(params["column"])] = scaler.fit_transform(
        data[(params["column"])].values.reshape(-1, 1)
    )[:, 0]
    return data


# @function_error_handling("standard_scale")
def standard_scale(**params):
    data = params["data"]
    scaler = preprocessing.StandardScaler(**params["parameters"])
    data[(params["column"])] = scaler.fit_transform(
        data[(params["column"])].values.reshape(-1, 1)
    )[:, 0]
    return data


# @function_error_handling("normalize")
def normalize(**params):
    data = params["data"]
    for column in params["columns"]:
        params["X"] = column
        data = preprocessing.normalize(**params["parameters"])
    return data


# @function_error_handling("ordinal_encode")
def ordinal_encode(**params):
    data = params["data"]
    data_columns = params["columns"]
    enc = preprocessing.OrdinalEncoder(**params["parameters"])
    data[data_columns] = enc.fit_transform(data[data_columns])
    return data


# @function_error_handling("one_hot_encode")
def one_hot_encode(**params):
    data = params["data"]
    data_columns = params["columns"]
    le = preprocessing.LabelEncoder()
    data[data_columns] = data[data_columns].apply(lambda col: le.fit_transform(col))
    enc = preprocessing.OneHotEncoder(**params["parameters"])
    array_hot_encoded = enc.fit_transform(data[data_columns])
    data_hot_encoded = pd.DataFrame(array_hot_encoded, index=data.index)
    data_other_cols = data.drop(columns=data_columns)
    data_out = pd.concat([data_hot_encoded, data_other_cols], axis=1)
    return data_out


# @function_error_handling("remove_mismatch_data")
def remove_mismatch_data(**params):
    data = params["data"]
    exceptions = params["parameters"]["exceptions"]
    for col in data:
        if col in exceptions:
            continue
        data.reset_index(drop=True, inplace=True)
        s = [False] * len(data[col])
        for i, cell in enumerate(data[col]):
            try:
                n = int(cell)
            except:
                s[i] = True
        t = s.count(True)
        f = s.count(False)
        st = False
        if t > f:
            st = True
        remove = [i for i in range(len(data[col])) if s[i] != st]
        data.drop(remove, axis=0, inplace=True)
    return data


# @function_error_handling("merge")
def merge(**params):
    data = params["data"]
    df = data.merge(**params["parameters"])
    return df


# @function_error_handling("rename_columns")
def rename_columns(**params):
    data = params["data"]
    dict = params["dict"]
    axis = params["axis"]
    data = data.rename(dict, axis)
    return data


# @function_error_handling("select_columns")
def select_columns(**params):
    data = params["data"]
    df = data.select_dtypes(**params["parameters"])
    return df


# @function_error_handling("clean_column_names")
def clean_column_names(**params):
    data = params["data"]
    match = r"[\]\[\,\{\}\"\:]+"
    data.rename(columns=lambda x: re.sub(match, "", str(x)))
    return data


# @function_error_handling("clean_data")
def clean_data(**params):
    data = params["data"]
    df = autoclean(data)
    return df


# @function_error_handling("clip")
def clip(**params):
    data = params["data"]
    data = data.clip(**params["paramters"])
    return data


# @function_error_handling("split_data")
def split_data(**params):
    data = params["data"]
    df_shuffled = data.sample(frac=1)
    df_splits = np.array_split(df_shuffled, 2)
    return df_splits
