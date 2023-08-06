start_node = {
    "id": "999",
    "type": "custom",
    "position": {"x": 0, "y": 0},
    "data": {
        "name": "Raw Data",
        "value": "Raw Data",
        "color": "pink.400",
        "isInput": True,
        "parameters": {"Dataset": "Test"},
        "node_type": "preprocess",
    },
    "width": 400,
    "height": 76,
    "selected": False,
    "dragging": False,
    "target": "1",
}

node = {
    "id": "",
    "type": "custom",
    "position": {"x": 0, "y": 0},
    "data": {
        "name": "Remove NAN values",
        "value": "Remove NAN values",
        "parameters": {},
        "node_type": "preprocess",
    },
    "width": 400,
    "height": 76,
    "selected": False,
    "dragging": False,
    "source": "",
    "target": "",
}

end_node = {
    "id": "998",
    "type": "custom",
    "position": {"x": 0, "y": 0},
    "data": {
        "name": "Clean Data",
        "value": "Clean Data",
        "color": "green.400",
        "isOutput": True,
        "parameters": {"Dataset": "Test"},
        "node_type": "preprocess",
    },
    "width": 400,
    "height": 76,
    "selected": False,
    "dragging": False,
    "source": "",
}


start_edge = {
    "source": "999",
    "sourceHandle": None,
    "target": "1",
    "targetHandle": None,
    "type": "custom",
    "id": "999-1",
}


edge = {
    "source": "",
    "sourceHandle": None,
    "target": "",
    "targetHandle": None,
    "type": "custom",
    "id": "",
}


def convert_to_graph(json_data):
    # convert test JSON to same format as data graph
    node_arr = [start_node]
    edge_arr = [start_edge]
    count = 1
    for key, value in json_data.items():
        for key2, value2 in json_data[key].items():
            if len(value2) > 0:
                if key2 == "null_values" or key2 == "too_many_zeros":
                    node["data"]["name"] = "Replace NAN values"
                    node["data"]["value"] = "Replace NAN values"
                    node["data"]["parameters"] = {
                        "column": json_data["errors"]["null_values"].append(
                            json_data["warnings"]["too_many_zeros"]
                        )
                    }
                if key2 == "string_features":
                    node["data"]["name"] = "One Hot Encoding"
                    node["data"]["value"] = "One Hot Encoding"
                    node["data"]["parameters"] = {
                        "columns": json_data["errors"]["string_features"]
                    }
                if key2 == "outliers":
                    node["data"]["name"] = "Remove Outliers"
                    node["data"]["value"] = "Remove Outliers"
                    node["data"]["parameters"] = {
                        "columns": json_data["warnings"]["outliers"]
                    }
                if key2 == "data_normalization":
                    node["data"]["name"] = "Data normalization"
                    node["data"]["value"] = "Data normalization"
                    node["data"]["parameters"] = {
                        "column": json_data["warnings"]["data_normalization"]
                    }

                if count == 1:
                    node["id"] = str(count)
                    node["source"] = "999"
                else:
                    node["id"] = str(count)
                    node["source"] = str(count - 1)
                node["target"] = str(count + 1)
                node_arr.append(node)

                edge["source"] = str(count)
                edge["id"] = str(count) + "-" + str(count + 1)
                edge["target"] = str(count + 1)
                edge_arr.append(edge)

                count += 1
        node_arr.append(end_node)
        main_node = {"nodes": node_arr, "edges": edge_arr}
        return main_node
