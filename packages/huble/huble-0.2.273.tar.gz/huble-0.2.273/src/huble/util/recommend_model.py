def recommend_model(dataset, target):
    """Recommend which models to use for training"""
    THRESHOLD = 0.01

    if isinstance(dataset["target"], str):
        return {"recommended_model": "classification"}

    else:
        num_unique_values = len(dataset[target].unique())
        num_rows = len(dataset[target])

        if num_unique_values / num_rows < THRESHOLD:
            return {"recommended_model": "classification"}
        else:
            return {"recommended_model": "regression"}
