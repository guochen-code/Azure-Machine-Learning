################################### register a model from a local file
import urllib.request
from azureml.core.model import Model
urllib.request.urlretrive('https://....','model.onnx')
model=Model.register(ws,model_name='model_name',model_path='./model_name') ### model_path refers to local path

#################################### register a model from run
#                         (1) Register a model from an azureml.core.Run object:
# save model, automatically uploaded
os.makedirs('outputs',exist_ok=True)
joblib.dump(value=model,filename='outputs/model_name.pkl')
# register model
run.register_model(model_path='outputs/model_name.pkl',  ### model_path refers to the cloud location of the model
                   model_name='model_name',
                   tags={'Training Contect':'Tabular dataset'},
                   properties={'AUC':run.get_metrics()['AUC'],'Accuracy':run.get_metrics()['Accuracy']})

print(model.name, model.id, model.version, sep='\t')

#                        (2) Register a model from an azureml.train.automl.run.AutoMLRun object:
description = 'My AutoML Model'
model = run.register_model(description = description,
                               tags={'area': 'qna'})

print(run.model_id)
# In this example, the metric and iteration parameters aren't specified, so the iteration with the best primary metric will be registered. 
# The model_id value returned from the run is used instead of a model name.

###################################### display registered model
from azureml.core import Model
for model in Model.list(ws):
  print(model.name,'version',model.version)
  for tag_name in model.tags:
    tag=model.tags[tag_name]
    print('\t',tag_name,':',tag)
  for prop_name in model.properties:
    prop=model.properties[prop_name]
    print('\t',prop_name,':',prop)
  print('\n')

################################ By defauly, if we specify a name, the lastest version will be returned:
model=ws.model['specific_model_name']
print(model.name,'version',model.version)
