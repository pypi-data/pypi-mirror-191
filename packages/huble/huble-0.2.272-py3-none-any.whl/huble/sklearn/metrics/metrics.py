from sklearn import metrics
import evalml
import pandas as pd
from evalml.problem_types import detect_problem_type

def regression_metrics(y_true, y_pred):
    max_error = metrics.max_error(y_true, y_pred)
    mean_absolute_error = metrics.mean_absolute_error(y_true, y_pred)
    mean_squared_error = metrics.mean_squared_error(y_true, y_pred)
    mean_squared_log_error = metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error = metrics.median_absolute_error(y_true, y_pred)
    r2_score = metrics.r2_score(y_true, y_pred)
    mean_poisson_deviance = metrics.mean_poisson_deviance(y_true, y_pred)
    mean_gamma_deviance = metrics.mean_gamma_deviance(y_true, y_pred)
    mean_tweedie_deviance = metrics.mean_tweedie_deviance(y_true, y_pred)
    # create dictionary of metrics
    metrics_dict = {
        "max_error": max_error,
        "mean_absolute_error": mean_absolute_error,
        "mean_squared_error": mean_squared_error,
        "mean_squared_log_error": mean_squared_log_error,
        "median_absolute_error": median_absolute_error,
        "r2_score": r2_score,
        "mean_poisson_deviance": mean_poisson_deviance,
        "mean_gamma_deviance": mean_gamma_deviance,
        "mean_tweedie_deviance": mean_tweedie_deviance,
    }
    return metrics_dict


def classification_metrics(y_true, y_pred):
    accuracy_score = metrics.accuracy_score(y_true, y_pred)
    balanced_accuracy_score = metrics.balanced_accuracy_score(y_true, y_pred)
    cohen_kappa_score = metrics.cohen_kappa_score(y_true, y_pred)
    f1_score = metrics.f1_score(y_true, y_pred)
    fbeta_score = metrics.fbeta_score(y_true, y_pred, beta=0.5)
    hamming_loss = metrics.hamming_loss(y_true, y_pred)
    jaccard_score = metrics.jaccard_score(y_true, y_pred)
    log_loss = metrics.log_loss(y_true, y_pred)
    matthews_corrcoef = metrics.matthews_corrcoef(y_true, y_pred)
    precision_score = metrics.precision_score(y_true, y_pred)
    recall_score = metrics.recall_score(y_true, y_pred)
    zero_one_loss = metrics.zero_one_loss(y_true, y_pred)
    roc_auc_score = metrics.roc_auc_score(y_true, y_pred)
    metrics_dict={}
    y_task = pd.Series(y_true)
    task=(detect_problem_type(y_task))
    task_str = str(task)
    if task_str == 'binary':
        metrics_dict = {
            "accuracy_score": accuracy_score,
            "balanced_accuracy_score": balanced_accuracy_score,
            "precision_score": precision_score,
            "recall_score": recall_score,
            "f1_score": f1_score,
            "roc_auc_score": roc_auc_score,
            "log_loss": log_loss,
            "matthews_corrcoef": matthews_corrcoef,
        }
    elif task == 'multiclass':
        metrics_dict = {
            "accuracy_score": accuracy_score,
            "balanced_accuracy_score": balanced_accuracy_score,
            "precision_score": precision_score,
            "recall_score": recall_score,
            "hamming_loss": hamming_loss,
            "jaccard_score": jaccard_score,
            "log_loss": log_loss,
            "cohen_kappa_score": cohen_kappa_score,
            "f1_score": f1_score,           
            "zero_one_loss": zero_one_loss,
        }
    return metrics_dict


def clustering_metrics(X, labels):
    silhouette_score = metrics.silhouette_score(X, labels)
    calinski_harabasz_score = metrics.calinski_harabasz_score(X, labels)
    davies_bouldin_score = metrics.davies_bouldin_score(X, labels)
    
    # create dictionary of metrics
    metrics_dict = {
        "silhouette_score": silhouette_score,
        "calinski_harabasz_score": calinski_harabasz_score,
        "davies_bouldin_score": davies_bouldin_score,
    }
    return metrics_dict


def log_metrics(y_true, y_pred, task, X, labels):
    if task == "regression":
        metrics_dict = regression_metrics(y_true, y_pred)
        return metrics_dict
    elif task == "classification":
        metrics_dict = classification_metrics(y_true, y_pred)
        return metrics_dict
    elif task == "clustering":
        metrics_dict = clustering_metrics(X, labels)
        return metrics_dict
