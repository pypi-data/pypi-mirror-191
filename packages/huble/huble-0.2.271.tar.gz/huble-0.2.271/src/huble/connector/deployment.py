import requests
from .experiment import Experiment

class Deployment:

    def generate_code(self, experiment_id: str):
        experiment = Experiment(experiment_id=experiment_id)
        with open("deployment.py", "w") as f:
            f.write("import requests")
            f.write("\nimport os")
            f.write("\nimport pandas as pd")
            f.write("\nfrom pydantic import BaseModel")
            f.write("\nfrom huble import Experiment")
            f.write("\nfrom typing import Union")
            f.write("\nimport joblib")
            f.write("\nexperiment_id = os.getenv(\"EXPERIMENT_ID\")")
            f.write(f"\nexperiment = Experiment(experiment_id)")
            f.write("\n")
            f.write("\nclass RequestBody(BaseModel):")
            for column in experiment.input_format["columns"]:
              if(column['name'] != "index"):
                f.write(f"\n\t{column['name']}: Union[int, float]")
            f.write("\n")
            f.write(f"\nmodel_url = experiment.modelURL")
            f.write('\nmodel_content = requests.get(f"https://ipfs.filebase.io/ipfs/{model_url}")')
            f.write("\nopen('model.joblib', 'wb').write(model_content.content)")
            f.write("\nmodel = joblib.load('model.joblib')")
            f.write("\n")
            f.write("\n")
            f.write("\ndef predict(request_body: RequestBody):")
            f.write("\n\trequest_body = request_body.dict()")
            f.write("\n\tX = pd.DataFrame(request_body, index=[0])")
            f.write("\n\treturn model.predict(X)")



