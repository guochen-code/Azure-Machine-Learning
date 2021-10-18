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
# the get_mlflow_tracking_uri() method assigns a unique tracking URI address to the workspace, ws, 
# and set_tracking_uri() points the MLflow tracking URI to that address.
# The tracking URI is valid up to an hour or less. 
# If you restart your script after some idle time, use the get_mlflow_tracking_uri API to get a new URI.

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
