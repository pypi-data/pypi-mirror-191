from huble.sklearn.metrics import log_metrics


def evaluate_model(model, training_dataset, test_dataset, target_column, task_type):
    if task_type=="classification" or task_type=="regression":
        y_test = test_dataset[target_column]
        X_test = test_dataset.drop([target_column], axis=1)
        y_pred = model.predict(X_test)
        metrics = log_metrics(y_true=y_test, y_pred=y_pred, task=task_type, X=None, labels=None)
        return metrics
    elif task_type=="clustering":
        labels = model.labels_
        metrics = log_metrics(y_true=None, y_pred=None, task=task_type, X=training_dataset, labels=labels)
        return metrics

