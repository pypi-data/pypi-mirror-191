class EssentialsHandler:
    def __init__(self) -> None:
        pass

    def return_function(self, function_name: str, params: dict, task_type: str, target_column: str):

        essentials = {
            "Train-Test Split": self.__train_test_split,
            "Train Model": self.__train_model,
        }
        return essentials[function_name](params=params, task_type=task_type, target_column=target_column)

    def __train_test_split(self, params, target_column, **kwargs):
        parameters = {
            "test_size": params["test_size"],
        }
        return f"training_dataset, test_dataset, input_format = huble.sklearn.train_test_split(data=data,parameters={parameters}, target_column='{target_column}')"

    def __train_model(self, params, task_type, **kwargs):
        return f"Model, filename = huble.sklearn.train_model(data=training_dataset, model=model, column='{params['target_column']}', task_type='{task_type}')"
