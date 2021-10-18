# (1) track local runs
pip install azureml-mlflow

import mlflow
from azureml.core import Workspace
ws = Workspace.from_config()
mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())

experiment_name='experiment_with_mlflow'
mlflow.set_experiment(experiment_name)
with mlflow.start_run():
  mlflow.log_metric('alpha',0.03)
  
# (2) track remote runs
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core import ScriptRunConfig
exp = Experiment(workspace='my_workspace',name='my_experiment')
mlflow_env=Environment(name='mlflow-env')
cd=CondaDependencies.create(pip_packages=['mlflow','azureml-mlflow'])
mlflow_env.python.conda_dependencies=cd
src=ScriptRunConfig=(source_directory='./my_script_location', script='my_script.py')
src.run_config.target='my-remote-compute'
src.run_config.environment=mlflow_env

import mlflow
with mlflow.start_run():
  mlflow.log_metric('example',1.23)
run=exp.submit(src)
