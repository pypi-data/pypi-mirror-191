from .sklearn import generate_file
from .connector import Experiment


def generate_experiment(experiment_id: str, auth_key=""):
    # TODO: Implement auth keys
    experiment = Experiment(experiment_id=experiment_id)
    print(experiment.target_column)
    generate_file(
        graph=experiment.graph,
        task_type=experiment.task_type,
        target_column=experiment.target_column,
    )
    return experiment
