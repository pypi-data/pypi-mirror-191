import huble
from huble import Dataset
def run_experiment(experiment):
	model = huble.sklearn.decision_tree(parameters={'criterion': 'gini', 'splitter': 'best', 'max_depth': None, 'max_leaf_nodes': None, 'random_state': None})
	data = Dataset('https://ipfs.filebase.io/ipfs/QmRspeqXi9J2PVTmXYwMaBif9dYWVkNhM8EFomUAfajnT1').dataframe
	data = huble.sklearn.clean_data(data=data)
	training_dataset, test_dataset = huble.sklearn.train_test_split(data=data,parameters={'test_size': 0.2})
	Model, input_format, filename = huble.sklearn.train_model(data=training_dataset, model=model, column='Survived', task_type='classification')
	metrics = huble.sklearn.evaluate_model(model=Model, training_data=training_dataset, test_dataset=test_dataset, target_column= 'Survived', task_type='classification' )
	experiment.upload_metrics(metrics,input_format)
	print("Uploading model...")
	experiment.upload_model(filename)