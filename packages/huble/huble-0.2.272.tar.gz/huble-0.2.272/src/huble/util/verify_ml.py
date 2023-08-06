import numpy as np
import pandas as pd
from scipy import stats
import evalml
from evalml.problem_types import detect_problem_type
from evalml.data_checks import (
    DataChecks,
    NullDataCheck,
    InvalidTargetDataCheck,
    NoVarianceDataCheck,
    ClassImbalanceDataCheck,
    TargetLeakageDataCheck,
    NoVarianceDataCheck,
    IDColumnsDataCheck,
    OutliersDataCheck,
    MulticollinearityDataCheck
)
from evalml.problem_types import ProblemTypes

def verify_ml_dataset(dataset, target):
    y_task = pd.Series(dataset[target])
    task=(detect_problem_type(y_task))
    task_str = str(task)
    if task_str=="regression":
        data_check_params={
            "InvalidTargetDataCheck": {
                "problem_type": ProblemTypes.REGRESSION,
                "objective": "R2",
            }
        }
    elif task_str=="binary":
        data_check_params={
            "InvalidTargetDataCheck": {
                "problem_type": ProblemTypes.BINARY,
                "objective": "log loss binary",
            }
        }

    elif task_str=="multiclass":
        data_check_params={
            "InvalidTargetDataCheck": {
                "problem_type": ProblemTypes.MULTICLASS,
                "objective": "log loss multiclass",
            }
        }
    else:
        data_check_params={}

    custom_data_checks = DataChecks(
        data_checks=[
            NullDataCheck,
            InvalidTargetDataCheck,
            NoVarianceDataCheck,
            ClassImbalanceDataCheck,
            TargetLeakageDataCheck,
            NoVarianceDataCheck,
            IDColumnsDataCheck,
            OutliersDataCheck,
            MulticollinearityDataCheck
        ],

        data_check_params=data_check_params
    )

    X = dataset.drop([target], axis=1)
    y = dataset[target]
    data_checks = custom_data_checks
    messages = data_checks.validate(X, y)
    return messages























    # # check for null values in pandas dataframe
    # DATA_IMBALANCE_THRESHOLD = 0.1
    # TOO_MANY_ZEROES_THRESHOLD = 0.1
    # FEATURE_IMPORTANCE_THRESHOLD = 0.01
    # dict_main = {}
    # dict_main["errors"] = {"null_values": [], "string_features": []}
    # dict_main["warnings"] = {
    #     "too_many_zeros": [],
    #     "outliers": [],
    #     "data_imbalance": [],
    #     "data_normalization": [],
    # }
    # dict_main["success"] = {
    #     "null_values": [],
    #     "string_features": [],
    #     "too_many_zeros": [],
    #     "outliers": [],
    #     "data_imbalance": [],
    #     "data_normalization": [],
    # }
    # dict_main["status"] = "ok"

    # for column in dataset.columns:

    #     # check for null values in pandas dataframe
    #     if dataset[column].isnull().values.any():
    #         dict_main["errors"]["null_values"].append(column)
    #         dict_main["status"] = "error"
    #     else:
    #         dict_main["success"]["null_values"].append(column)

    #     # check for string columns in pandas dataframe
    #     if (dataset[column].dtypes == object) == False:
    #         dict_main["errors"]["string_features"].append(column)
    #         dict_main["status"] = "error"
    #     else:
    #         dict_main["success"]["string_features"].append(column)

    #     # check for too many zeroes in pandas dataframe
    #     count = 0
    #     column_name = dataset[column]
    #     count += (column_name == 0).sum()
    #     if count > len(dataset[column]) * TOO_MANY_ZEROES_THRESHOLD:
    #         dict_main["warnings"]["too_many_zeros"].append(column)
    #         break

    #     # Check for outliers
    #     if column in dict_main["success"]["string_features"]:
    #         z_scores = stats.zscore(dataset[column])
    #         abs_z_scores = np.abs(z_scores)
    #         # Select data points with a z-scores above or below 3
    #         # filtered_entries = (abs_z_scores < 3)
    #         # print(filtered_entries)
    #         if (abs_z_scores < 3).all():
    #             dict_main["warnings"]["outliers"].append(column)
    #         else:
    #             dict_main["success"]["outliers"].append(column)

    #     # Data normalization
    #     if column in dict_main["success"]["string_features"]:
    #         if dataset[column].min() < -1 or dataset[column].max() > 1:
    #             dict_main["warnings"]["data_normalization"].append(column)
    #             break
    #         else:
    #             dict_main["success"]["data_normalization"].append(column)

    # values = dataset[target].value_counts()
    # if (
    #     values[0] * DATA_IMBALANCE_THRESHOLD > values[1]
    #     or values[1] * DATA_IMBALANCE_THRESHOLD > values[0]
    # ):
    #     dict_main["warnings"]["data_imbalance"].append("data_imbalance")
    # else:
    #     dict_main["success"]["data_imbalance"].append("data_imbalance")

    # return dict_main.popitem()

