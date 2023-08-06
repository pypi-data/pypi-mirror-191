import lightgbm as lgb
import xgboost as xgb
import catboost as cb
from sklearn import (
    ensemble,
    linear_model,
    svm,
    naive_bayes,
    neighbors,
    tree,
    cluster,
    kernel_ridge,
)
from ...error.decorators import function_error_handling


# @function_error_handling("logistic_regression")
def logistic_regression(**params):
    model = linear_model.LogisticRegression(**params["parameters"])
    return model


# @function_error_handling("svm_svc")
def svm_svc(**params):
    model = svm.SVC(**params["parameters"])
    return model


# @function_error_handling("gaussian_naive_bayes")
def gaussian_naive_bayes(**params):
    model = naive_bayes.GaussianNB(**params["parameters"])
    return model


# @function_error_handling("multinomial_naive_bayes")
def multinomial_naive_bayes(**params):
    model = naive_bayes.MultinomialNB(**params["parameters"])
    return model


# @function_error_handling("st_gradient_descent_classifier")
def st_gradient_descent_classifier(**params):
    model = linear_model.SGDClassifier(**params["parameters"])
    return model


# @function_error_handling("knn")
def knn(**params):
    model = neighbors.KNeighborsClassifier(**params["parameters"])
    return model


# @function_error_handling("decision_tree")
def decision_tree(**params):
    model = tree.DecisionTreeClassifier(**params["parameters"])
    return model


# @function_error_handling("random_forest")
def random_forest(**params):
    model = ensemble.RandomForestClassifier(**params["parameters"])
    return model


# @function_error_handling("gradient_boosting")
def gradient_boosting(**params):
    model = ensemble.GradientBoostingClassifier(**params["parameters"])
    return model


# @function_error_handling("lgbm")
def lgbm(**params):
    model = lgb.LGBMClassifier(**params["parameters"])
    return model


# @function_error_handling("xgboost")
def xgboost(**params):
    model = xgb.XGBClassifier(**params["parameters"])
    return model


# Regression

# @function_error_handling("linear_regression")
def linear_regression(**params):
    model = linear_model.LinearRegression(**params["parameters"])
    return model


# @function_error_handling("lgbm_reg")
def lgbm_reg(**params):
    model = lgb.LGBMRegressor(**params["parameters"])
    return model


# @function_error_handling("xgboost_reg")
def xgboost_reg(**params):
    model = xgb.XGBRegressor(**params["parameters"])
    return model


# @function_error_handling("catboost_reg")
def catboost_reg(**params):
    model = cb.CatBoostRegressor(**params["parameters"])
    return model


# @function_error_handling("st_gradient_descent_reg")
def st_gradient_descent_reg(**params):
    model = linear_model.SGDRegressor(**params["parameters"])
    return model


# @function_error_handling("kernel_ridge_reg")
def kernel_ridge_reg(**params):
    model = kernel_ridge.KernelRidge(**params["parameters"])
    return model


# @function_error_handling("elastic_net_reg")
def elastic_net_reg(**params):
    model = linear_model.ElasticNet(**params["parameters"])
    return model


# @function_error_handling("bayesian_ridge_reg")
def bayesian_ridge_reg(**params):
    model = linear_model.BayesianRidge(**params["parameters"])
    return model


# @function_error_handling("gradient_boosting_reg")
def gradient_boosting_reg(**params):
    model = ensemble.GradientBoostingRegressor(**params["parameters"])
    return model


# @function_error_handling("svm_svr")
def svm_svr(**params):
    model = svm.SVR(**params["parameters"])
    return model


# Clustering

# @function_error_handling("mean_shift")
def mean_shift(**params):
    model = cluster.MeanShift(**params["parameters"])
    return model


# @function_error_handling("kmeans")
def kmeans(**params):
    model = cluster.KMeans(**params["parameters"])
    return model


# @function_error_handling("agglomerative")
def agglomerative(**params):
    model = cluster.AgglomerativeClustering(**params["parameters"])
    return model


# @function_error_handling("birch")
def birch(**params):
    model = cluster.Birch(**params["parameters"])
    return model


# @function_error_handling("spectral")
def spectral(**params):
    model = cluster.SpectralClustering(**params["parameters"])
    return model


# @function_error_handling("affinity_propogation")
def affinity_propogation(**params):
    model = cluster.AffinityPropagation(**params["parameters"])
    return model


# @function_error_handling("optics")
def optics(**params):
    model = cluster.OPTICS(**params["parameters"])
    return model


# @function_error_handling("dbscan")
def dbscan(**params):
    model = cluster.DBSCAN(**params["parameters"])
    return model
