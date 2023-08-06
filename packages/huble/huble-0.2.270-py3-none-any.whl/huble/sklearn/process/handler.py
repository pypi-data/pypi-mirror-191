class PreprocessHandler:
    def __init__(self) -> None:
        pass

    def return_function(self, function_name: str, params: dict):
        operations = {
            "Remove NAN values": self.__remove_nan_values,
            "Replace NAN values": self.__replace_nan_values,
            "Dropping rows or columns": self.__drop_rows_columns,
            "Remove Outliers": self.__remove_outliers,
            "Drop Duplicates": self.__drop_duplicates,
            "Change Data Type": self.__change_data_type,
            "Round Data": self.__round_data,
            "Filter DataFrame": self.__filter_dataframe,
            "Truncate DataFrame": self.__truncate_dataframe,
            "Sort Values": self.__sort_values,
            "Transpose DataFrame": self.__transpose,
            "Min Max Scaler": self.__min_max_scale,
            "Max Abs Scaler": self.__max_abs_scale,
            "Robust Scaler": self.__robust_scale,
            "Standard Scaler": self.__standard_scale,
            "Normalization": self.__normalize,
            "Ordinal Encoding": self.__ordinal_encode,
            "One Hot Encoding": self.__one_hot_encode,
            "Remove Mismatch Data": self.__remove_mismatch_data,
            "Rename Columns": self.__rename_columns,
            "Select Columns": self.__select_columns,
            "Clean Column Names": self.__clean_column_names,
            "Clip": self.__clip,
            "Merge Datasets": self.__merge,
            "Clean Dataset": self.__clean_data,
            "Split Datasets": self.__split,
        }
        return operations[function_name](params)

    def __remove_nan_values(self, params):
        subset = []
        for i in range(len(params["subset"])):
            subset.append(params["subset"][i]["value"])
        parameters = {
            "axis": params["axis"],
            "how": params["how"],
            "inplace": params["inplace"],
            "subset": subset,
        }
        return (
            f"data = huble.sklearn.remove_nan_values(data=data,parameters={parameters})"
        )

    def __replace_nan_values(self, params):
        parameters = {
            "missing_values": params["missing_values"],
            "strategy": params["strategy"],
            "fill_value": params["fill_value"],
        }
        return f"data = huble.sklearn.replace_nan_values(data=data, column='{params['column']}', parameters={parameters})"

    def __drop_rows_columns(self, params):
        labels = []
        for i in range(len(params["labels"])):
            labels.append(params["labels"][i]["value"])

        parameters = {
            "labels": labels,
            "axis": params["axis"],
            "inplace": params["inplace"],
            "errors": params["errors"],
        }
        return (
            f"data = huble.sklearn.drop_rows_columns(data=data,parameters={parameters})"
        )

    def __remove_outliers(self, params):
        columns = []
        for i in range(len(params["columns"])):
            columns.append(params["columns"][i]["value"])
        return f"data = huble.sklearn.remove_outliers(data=data,columns={columns})"

    def __drop_duplicates(self, params):
        subset = []
        if len(params["subset"]) != 0:
            for i in range(len(params["subset"])):
                subset.append(params["subset"][i]["value"])
        parameters = {
            "subset": subset,
            "keep": params["keep"],
            "inplace": params["inplace"],
            "ignore_index": params["ignore_index"],
        }
        return (
            f"data = huble.sklearn.drop_duplicates(data=data,parameters={parameters})"
        )

    def __change_data_type(self, params):
        parameters = {
            "dtype": params["data type"],
            "copy": params["copy"],
            "errors": params["errors"],
        }
        return f"data = huble.sklearn.change_data_type(data=data,column={params['column']}, parameters={parameters})"

    def __round_data(self, params):
        parameters = {
            "decimals": params["decimals"],
        }
        return f"data = huble.sklearn.round_data(data=data, parameters={parameters})"

    def __filter_dataframe(self, params):
        items = []
        for i in range(len(params["items"])):
            items.append(params["items"][i]["value"])
        parameters = {
            "items": items,
            "like": params["like"],
            "axis": params["axis"],
        }
        return (
            f"data = huble.sklearn.filter_dataframe(data=data, parameters={parameters})"
        )

    def __truncate_dataframe(self, params):
        parameters = {
            "before": params["before"],
            "after": params["after"],
            "copy": params["copy"],
            "axis": params["axis"],
        }
        return f"data = huble.sklearn.truncate_datfarame(data=data, parameters={parameters})"

    def __sort_values(self, params):
        by = []
        for i in range(len(params["by"])):
            by.append(params["by"][i]["value"])
        parameters = {
            "by": by,
            "axis": params["axis"],
            "ascending": params["ascending"],
            "inplace": params["inplace"],
            "kind": params["kind"],
            "na_position": params["na_position"],
            "ignore_index": params["ignore_index"],
        }
        return f"data = huble.sklearn.sort_values(data=data, parameters={parameters})"

    def __transpose(self):
        return f"data = huble.sklearn.transpose(data=data)"

    def __min_max_scale(self, params):
        parameters = {
            "feature_range": params["feature_range"],
            "copy": params["copy"],
            "clip": params["clip"],
        }
        return f"data = huble.sklearn.min_max_scalar(data=data, columns={params['columns']}, parameters={parameters})"

    def __max_abs_scale(self, params):
        parameters = {
            "copy": params["copy"],
        }
        return f"data = huble.sklearn.max_abs_scalar(data=data, columns={params['columns']}, parameters={parameters})"

    def __robust_scale(self, params):
        columns = []
        for i in range(len(params["column"])):
            columns.append(params["column"][i]["value"])
        parameters = {
            "with_centering": params["with_centering"],
            "with_scaling": params["with_scaling"],
            "copy": params["copy"],
            "unit_variance": params["unit_variance"],
            "quantile_range": params["quantile_range"],
        }
        return f"data = huble.sklearn.robust_scalar(data=data, column={columns}, parameters={parameters})"

    def __standard_scale(self, params):
        parameters = {
            "copy": params["copy"],
            "with_mean": params["with_mean"],
            "with_std": params["with_std"],
        }
        return f"data = huble.sklearn.standard_scalar(data=data, column={params['column']}, parameters={parameters})"

    def __normalize(self, params):
        columns = params["columns"]
        parameters = {
            "norm": params["norm"],
            "copy": params["copy"],
        }
        return f"data = huble.sklearn.normalize(data=data, columns={columns}, parameters={parameters})"

    def __ordinal_encode(self, params):
        columns = []
        for i in range(len(params["columns"])):
            columns.append(params["columns"][i]["value"])
        parameters = {
            "categories": params["categories"],
            "dtype": params["dtype"],
            "handle_unknown": params["handle_unknown"],
            "unknown_value": params["unknown_value"],
            "encoded_missing_value": params["encoded_missing_value"],
        }
        return f"data = huble.sklearn.ordinal_encode(data=data, columns={columns}, parameters={parameters})"

    def __one_hot_encode(self, params):
        columns = []
        for i in range(len(params["columns"])):
            columns.append(params["columns"][i]["value"])
        parameters = {
            "categories": params["categories"],
            "dtype": params["dtype"],
            "handle_unknown": params["handle_unknown"],
            "sparse": params["sparse"],
            "min_frequency": params["min_frequency"],
            "max_categories": params["max_categories"],
        }
        return f"data = huble.sklearn.one_hot_encode(data=data, columns={columns}, parameters={parameters})"

    def __remove_mismatch_data(self, params):
        parameters = {
            "exceptions": params["exceptions"],
        }
        return f"data = huble.sklearn.remove_mismatch_data(data=data, parameters={parameters})"

    def __rename_columns(self, params):
        parameters = {
            "mapper": params["mapper"],
            "axis": params["axis"],
            "errors": params["errors"],
        }
        return (
            f"data = huble.sklearn.rename_columns(data=data, parameters={parameters})"
        )

    def __select_columns(self, params):
        parameters = {
            "include": params["include"],
            "exclude": params["exclude"],
        }
        return (
            f"data = huble.sklearn.select_columns(data=data, parameters={parameters})"
        )

    def __clean_column_names(self, params):
        return f"data = huble.sklearn.clean_column_names(data=data)"

    def __clip(self, params):
        parameters = {
            "lower": params["lower"],
            "upper": params["upper"],
            "axis": params["axis"],
        }
        return f"data = huble.sklearn.clip(data=data, parameters={parameters})"

    def __merge(self, params):
        parameters = {
            "right": params["right"],
            "how": params["how"],
            "on": params["on"],
            "left_on": params["left_on"],
            "right_on": params["right_on"],
            "sort": params["sort"],
        }
        return f"data = huble.sklearn.merge(data=data, parameters={parameters})"

    def __clean_data(self, params):
        return f"data = huble.sklearn.clean_data(data=data)"

    def __split(self, params):
        return f"data = huble.sklearn.split(data=data)"
