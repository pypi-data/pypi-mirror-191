from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS


def feature_selection(X, y, model):
    efs = EFS(
        estimator=model,
        min_features=1,
        max_features=len(X.columns),
        scoring="accuracy",
        cv=5,
    )
    efs = efs.fit(X, y)
    features = []
    for feature in efs.best_feature_names_:
        features.append(feature)
    return features
