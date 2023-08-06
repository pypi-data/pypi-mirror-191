class ModelHandler:
    def __init__(self) -> None:
        pass

    def return_function(self, function_name: str, params: dict):
        models = {
            "Logistic Regression": self.__logistic_regression,
            "SVM (SVC)": self.__svm_svc,
            "Gaussian Naive Bayes": self.__gaussian_naive_bayes,
            "Multinomial Naive Bayes": self.__multinomial_naive_bayes,
            "Stochastic Gradient Descent Classifier": self.__st_gradient_descent_classifier,
            "KNN": self.__knn,
            "Decision Tree Classifier": self.__decision_tree,
            "Random Forest Classifier": self.__random_forest,
            "Gradient Boosting Classifier": self.__gradient_boosting,
            "LGBM Classifier": self.__lgbm,
            "XGBoost Classifier": self.__xgboost,
            "Linear Regression": self.__linear_regression,
            "LGBM Regressor": self.__lgbm_regressor,
            "XGBoost Regressor": self.__xgboost_regressor,
            "CatBoost Regressor": self.__catboost_regressor,
            "Stochastic Gradient Descent Regression": self.__st_gradient_descent_regressor,
            "Kernel Ridge Regression": self.__kernel_ridge,
            "Elastic Net Regression": self.__elastic_net,
            "Bayesian Ridge Regression": self.__bayesian_ridge,
            "Gradient Boosting Regression": self.__gradient_boosting_reg,
            "SVM (SVR)": self.__svm_svr,
            "Mean Shift": self.__mean_shift,
            "KMeans": self.__kmeans,
            "Agglomerative Clustering": self.__agglomerative,
            "BIRCH": self.__birch,
            "Spectral Clustering": self.__spectral,
            "Affinity Propagation": self.__affinity_propogation,
            "OPTICS": self.__optics,
            "DBSCAN": self.__dbscan,
        }
        return models[function_name](params)

    def __logistic_regression(self, params):
        parameters = {
            "penalty": params["penalty"],
            "fit_intercept": params["fit_intercept"],
            "random_state": params["random_state"],
            "solver": params["solver"],
            "max_iter": params["max_iter"],
            "multi_class": params["multi_class"],
            "tol": params["tol"],
        }
        return f"model = huble.sklearn.logistic_regression(parameters={parameters})"

    def __svm_svc(self, params):
        parameters = {
            "C": params["C"],
            "kernel": params["kernel"],
            "probability": params["probability"],
            "random_state": params["random_state"],
            "max_iter": params["max_iter"],
            "decision_function_shape": params["decision_function_shape"],
            "tol": params["tol"],
        }
        return f"model = huble.sklearn.svm_svc(parameters={parameters})"

    def __gaussian_naive_bayes(self, params):
        parameters = {
            "priors": params["priors"],
            "var_smoothing": params["var_smoothing"],
        }
        return f"model = huble.sklearn.gaussian_naive_bayes(parameters={parameters})"

    def __multinomial_naive_bayes(self, params):
        parameters = {
            "class_prior": params["class_prior"],
            "alpha": params["alpha"],
            "fit_prior": params["fit_prior"],
        }
        return f"model = huble.sklearn.multinomial_naive_bayes(parameters={parameters})"

    def __st_gradient_descent_classifier(self, params):
        parameters = {
            "loss": params["loss"],
            "penalty": params["penalty"],
            "fit_intercept": params["fit_intercept"],
            "alpha": params["alpha"],
            "max_iter": params["max_iter"],
            "tol": params["tol"],
            "random_state": params["random_state"],
            "shuffle": params["shuffle"],
            "learning_rate": params["learning_rate"],
            "initial_learning_rate": params["initial_learning_rate"],
            "early_stopping": params["early_stopping"],
            "validation_fraction": params["validation_fraction"],
        }
        return f"model = huble.sklearn.st_gradient_descent_classifier(parameters={parameters})"

    def __knn(self, params):
        parameters = {
            "n_neighbors": params["n_neighbors"],
            "weights": params["weights"],
            "algorithm": params["algorithm"],
            "metric": params["metric"],
        }
        return f"model = huble.sklearn.knn(parameters={parameters})"

    def __decision_tree(self, params):
        parameters = {
            "criterion": params["criterion"],
            "splitter": params["splitter"],
            "max_depth": params["max_depth"],
            "max_leaf_nodes": params["max_leaf_nodes"],
            "random_state": params["random_state"],
        }
        return f"model = huble.sklearn.decision_tree(parameters={parameters})"

    def __random_forest(self, params):
        for param in params:
            if params[param] == "None":
                params[param] = None
        parameters = {
            "criterion": params["criterion"],
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "max_leaf_nodes": params["max_leaf_nodes"],
            "random_state": params["random_state"],
        }
        return f"model = huble.sklearn.random_forest(parameters={parameters})"

    def __gradient_boosting(self, params):
        parameters = {
            "criterion": params["criterion"],
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "max_leaf_nodes": params["max_leaf_nodes"],
            "random_state": params["random_state"],
            "loss": params["loss"],
            "learning_rate": params["learning_rate"],
            "subsample": params["subsample"],
            "tol": params["tol"],
        }
        return f"model = huble.sklearn.gradient_boosting(parameters={parameters})"

    def __lgbm(self, params):
        parameters = {
            "boosting_type": params["boosting_type"],
            "num_leaves": params["num_leaves"],
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "random_state": params["random_state"],
            "learning_rate": params["learning_rate"],
        }
        return f"model = huble.sklearn.lgbm(parameters={parameters})"

    def __xgboost(self, params):
        parameters = {
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "random_state": params["random_state"],
            "learning_rate": params["learning_rate"],
        }
        return f"model = huble.sklearn.xgboost(parameters={parameters})"

    # Regression

    def __linear_regression(self, params):
        parameters = {
            "fit_intercept": params["fit_intercept"],
            "normalize": params["normalize"],
            "copy_X": params["copy_X"],
            "positive": params["positive"],
        }
        return f"model = huble.sklearn.linear_regression(parameters={parameters})"

    def __lgbm_regressor(self, params):
        parameters = {
            "boosting_type": params["boosting_type"],
            "num_leaves": params["num_leaves"],
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "random_state": params["random_state"],
            "learning_rate": params["learning_rate"],
        }
        return f"model = huble.sklearn.lgbm_reg(parameters={parameters})"

    def __xgboost_regressor(self, params):
        parameters = {
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "random_state": params["random_state"],
            "learning_rate": params["learning_rate"],
        }
        return f"model = huble.sklearn.xgboost_reg(parameters={parameters})"

    def __catboost_regressor(self, params):
        parameters = {
            "iterations": params["iterations"],
            "learning_rate": params["learning_rate"],
        }
        return f"model = huble.sklearn.catboost_reg(parameters={parameters})"

    def __st_gradient_descent_regressor(self, params):
        parameters = {
            "loss": params["loss"],
            "penalty": params["penalty"],
            "fit_intercept": params["fit_intercept"],
            "alpha": params["alpha"],
            "max_iter": params["max_iter"],
            "tol": params["tol"],
            "random_state": params["random_state"],
            "shuffle": params["shuffle"],
            "learning_rate": params["learning_rate"],
            "early_stopping": params["early_stopping"],
        }
        return f"model = huble.sklearn.st_gradient_descent_reg(parameters={parameters})"

    def __kernel_ridge(self, params):
        parameters = {
            "alpha": params["alpha"],
        }
        return f"model = huble.sklearn.kernel_ridge_reg(parameters={parameters})"

    def __elastic_net(self, params):
        parameters = {
            "fit_intercept": params["fit_intercept"],
            "normalize": params["normalize"],
            "copy_X": params["copy_X"],
            "positive": params["positive"],
            "alpha": params["alpha"],
            "l1_ratio": params["l1_ratio"],
            "selection": params["selection"],
        }
        return f"model = huble.sklearn.elastic_net_reg(parameters={parameters})"

    def __bayesian_ridge(self, params):
        parameters = {
            "n_iter": params["n_iter"],
        }
        return f"model = huble.sklearn.bayesian_ridge_reg(parameters={parameters})"

    def __gradient_boosting_reg(self, params):
        parameters = {
            "criterion": params["criterion"],
            "n_estimators": params["n_estimators"],
            "max_depth": params["max_depth"],
            "max_leaf_nodes": params["max_leaf_nodes"],
            "random_state": params["random_state"],
            "loss": params["loss"],
            "learning_rate": params["learning_rate"],
            "subsample": params["subsample"],
            "tol": params["tol"],
        }
        return f"model = huble.sklearn.gradient_boosting_reg(parameters={parameters})"

    def __svm_svr(self, params):
        parameters = {
            "C": params["C"],
            "kernel": params["kernel"],
            "max_iter": params["max_iter"],
            "tol": params["tol"],
        }
        return f"model = huble.sklearn.svm_svr(parameters={parameters})"

    # Clustering

    def __mean_shift(self, params):
        parameters = {
            "bandwidth": params["bandwidth"],
            "bin_seeding": params["bin_seeding"],
            "min_bin_freq": params["min_bin_freq"],
            "cluster_all": params["cluster_all"],
            "max_iter": params["max_iter"],
        }
        return f"model = huble.sklearn.mean_shift(parameters={parameters})"

    def __kmeans(self, params):
        parameters = {
            "n_clusters": params["n_clusters"],
            "init": params["init"],
            "copy_X": params["copy_X"],
            "tol": params["tol"],
            "max_iter": params["max_iter"],
            "algorithm": params["algorithm"],
            "random_state": params["random_state"],
        }
        return f"model = huble.sklearn.kmeans(parameters={parameters})"

    def __agglomerative(self, params):
        parameters = {
            "n_clusters": params["n_clusters"],
            "linkage": params["linkage"],
        }
        return f"model = huble.sklearn.agglomerative(parameters={parameters})"

    def __birch(self, params):
        parameters = {
            "threshold": params["threshold"],
            "branching_factor": params["branching_factor"],
            "n_clusters": params["n_clusters"],
        }
        return f"model = huble.sklearn.birch(parameters={parameters})"

    def __spectral(self, params):
        parameters = {
            "n_clusters": params["n_clusters"],
            "eigen_solver": params["eigen_solver"],
            "n_init": params["n_init"],
            "assign_labels": params["assign_labels"],
        }
        return f"model = huble.sklearn.spectral(parameters={parameters})"

    def __affinity_propogation(self, params):
        parameters = {
            "damping": params["damping"],
            "max_iter": params["max_iter"],
            "convergence_iter": params["convergence_iter"],
            "affinity": params["affinity"],
        }
        return f"model = huble.sklearn.affinity_propogation(parameters={parameters})"

    def __optics(self, params):
        parameters = {
            "min_samples": params["min_samples"],
            "algorithm": params["algorithm"],
        }
        return f"model = huble.sklearn.optics(parameters={parameters})"

    def __dbscan(self, params):
        parameters = {
            "eps": params["eps"],
            "min_samples": params["min_samples"],
            "algorithm": params["algorithm"],
        }
        return f"model = huble.sklearn.dbscan(parameters={parameters})"
