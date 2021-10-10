# register a model from a local file
import urllib.request
from azureml.core.model import Model
urllib.request.urlretrive('https://....','model.onnx')
model=Model.register(ws,model_name='model_name',model_path='./model_name') ### model_path refers to local path

# register a model from run
# save model, automatically uploaded
os.makedirs('outputs',exist_ok=True)
joblib.dump(value=model,filename='outputs/model_name.pkl')
# register model
run.register_model(model_path='outputs/model_name.pkl',  ### model_path refers to the cloud location of the model
                   model_name='model_name',
                   tags={'Training Contect':'Tabular dataset'},
                   properties={'AUC':run.get_metrics()['AUC'],'Accuracy':run.get_metrics()['Accuracy']})
# display registered model
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

