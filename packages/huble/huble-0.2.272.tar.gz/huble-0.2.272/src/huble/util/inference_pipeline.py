def inference_pip(graph):
    id='0'
    for node in graph['nodes']:
        if node['data']['node_type']=='primary_dataset':
            node['data']['name']='Web API'
        elif node['data']['name']=='Train-Test Split':
            node['data']['name']='Predictions'
            node['data']['value']='Predictions' 
            node['data']['node_type']='predictions'
            node.pop('target')
            node['data'].pop('outputParameters')
        elif node['data']['name']=='Train Model':
            id = node['id']
        graph['edges'] = [edge for edge in graph['edges'] if edge['target'] not in ['998', id]]
        graph['nodes'] = [node for node in graph['nodes'] if node['data']['node_type'] in ['primary_dataset', 'preprocess', 'predictions']]

    return graph
