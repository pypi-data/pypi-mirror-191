from .process.handler import PreprocessHandler
from .train.handler import ModelHandler
from .essentials.handler import EssentialsHandler
from .graph import Graph
from ..util import get_typed_params


def generate_file(graph, target_column, task_type, colab=False):
    g = Graph(len(graph["nodes"]))
    graph_dict = {}
    for i in graph["nodes"]:
        graph_dict[(i["data"]["name"])] = i
    map = {}
    j = 0
    while j < (len(graph["nodes"])):
        for i in graph["nodes"]:
            map[(i["id"])] = j
            j += 1
    map2 = {y: x for x, y in map.items()}
    for i in graph["edges"]:
        g.addEdge(map[i["source"]], map[i["target"]])
    res = g.topologicalSort()
    steps = []
    for i in res:
        steps.append(map2[i])
    steps_list = {}
    for i in steps:
        for j in range(len(graph["nodes"])):
            if i == graph["nodes"][j]["id"]:
                steps_list[(graph["nodes"][j]["data"]["name"])] = graph["nodes"][j][
                    "data"
                ]["node_type"]
    if colab:
        output_file = "/content/output.py"
    else:
        output_file = "output.py"
    preprocess_handler = PreprocessHandler()
    train_handler = ModelHandler()
    essentials_handler = EssentialsHandler()
    with open(output_file, "w") as f:
        f.write("import huble\n")
        f.write("from huble import Dataset\n")
        f.write("def run_experiment(experiment):\n")
        for i in steps_list:
            node = graph_dict[i]
            params = get_typed_params(node["data"]["parameters"])
            if steps_list[i] == "preprocess":
                f.write(
                    "\t"
                    + preprocess_handler.return_function(
                        function_name=node["data"]["name"], params=params
                    )
                )
                f.write("\n")
            elif (
                steps_list[i] == "classification_model"
                or steps_list[i] == "regression_model"
                or steps_list[i] == "clustering_model"
                or steps_list[i] == "model"
            ):
                f.write(
                    "\t"
                    + train_handler.return_function(
                        function_name=node["data"]["name"], params=params
                    )
                )
                f.write("\n")
            elif steps_list[i] == "essential":
                f.write(
                    "\t"
                    + essentials_handler.return_function(
                        function_name=node["data"]["name"], params=params, task_type=task_type, target_column= target_column
                    )
                )
                f.write("\n")
            elif steps_list[i] == "evaluate_model":
                f.write(
                    # TODO: make changes for clustering
                    f"\tmetrics = huble.sklearn.evaluate_model(model=Model, training_data=training_dataset, test_dataset=test_dataset, target_column= '{target_column}', task_type='{task_type}' )"
                )
                f.write("\n")
            elif steps_list[i] == "primary_dataset":
                # TODO: Add support for other datasets
                f.write(f"\tdata = Dataset('{node['data']['url']}').dataframe\n")
        f.write("\texperiment.upload_metrics(metrics,input_format)")
        f.write("\n\tprint(\"Uploading model...\")")
        f.write("\n\texperiment.upload_model(filename)")
