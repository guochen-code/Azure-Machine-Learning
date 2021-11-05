'''summary:
  (1) Use MLflow with an inline experiment: 
    To use MLflow to track metrics for an inline experiment, you must set the MLflow tracking URI to the workspace where the experiment is being run. 
    This enables you to use mlflow tracking methods to log data to the experiment run.
  (2) Use MLflow in an experiment script:
    When you use MLflow tracking in an Azure ML experiment script, the MLflow tracking URI is set automatically when you start the experiment run. 
    However, the environment in which the script is to be run must include the required mlflow packages.'''
*********************************************************************************************************************************************
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

******************************************************** Register Model !!! sklearn !!! *********************************************************

# register model
mlflow.sklearn.log_model(model, artifact_path = "trained_model", 
                         registered_model_name = 'my_trained_model')

******************************************************** log_artifact *********************************************************
 # Plot actuals vs predictions and save the plot within the run
    fig = plt.figure(1)
    idx = np.argsort(data['test']['y'])
    plt.plot(data['test']['y'][idx],preds[idx])
    fig.savefig("actuals_vs_predictions.png")
    mlflow.log_artifact("actuals_vs_predictions.png") 

# Log numpy metrics or PIL image objects: 
mlflow.log_image(img, 'figure.png')

# Log matlotlib plot or image file: 
mlflow.log_figure(fig, "figure.png")
********************************************************Retrieve*********************************************************
# After the run completes, you can retrieve it using the MlFlowClient().
from mlflow.tracking import MlflowClient

# Use MlFlow to retrieve the run that was just completed
client = MlflowClient()
finished_mlflow_run = MlflowClient().get_run(mlflow_run.info.run_id)

# You can view the metrics, parameters, and tags for the run in the data field of the run object.
metrics = finished_mlflow_run.data.metrics
tags = finished_mlflow_run.data.tags
params = finished_mlflow_run.data.params

# Note: The metrics dictionary under mlflow.entities.Run.data.metrics only returns the most recently logged value for a given metric name. 
# For example, if you log, in order, 1, then 2, then 3, then 4 to a metric called sample_metric, only 4 is present in the metrics dictionary for sample_metric.
# To get all metrics logged for a particular metric name, you can use 
MlFlowClient.get_metric_history().
