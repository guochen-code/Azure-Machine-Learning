# submit to run
from azureml.core.experiment import Experiment
automl_experiment=Experiment(ws,'automl_experiment')
automl_run=automl_experiment.submit(automl_config)


# retrive the best model:
best_run, fitted_model=automl_run.get_output()
y_predict=fitted_model.predict(X_test.values)

best_run_metrics=best_run.get_metrics()
for metric_name in best_run_metrics:
  metric=best_run_metrics[metric_name]
  print(metric_name, metric)

# Exploring preprocessing steps. View those steps in the fitted_model obtaind from the best run:
for step in fitted_model.named_steps:
  print(step)
********************************************************************************************************************************* For Deployment Use
# Download the conda environment file
from azureml.automl.core.shared import constants
conda_env_file_name = 'conda_env.yml'
best_run.download_file(name="outputs/conda_env_v_1_0_0.yml", output_file_path=conda_env_file_name)
with open(conda_env_file_name, "r") as conda_file:
    conda_file_contents = conda_file.read()
    print(conda_file_contents)
    
# Download the model scoring file   
from azureml.automl.core.shared import constants
script_file_name = 'scoring_file.py'
best_run.download_file(name="outputs/scoring_file_v_1_0_0.py", output_file_path=script_file_name)
with open(script_file_name, "r") as scoring_file:
    scoring_file_contents = scoring_file.read()
    print(scoring_file_contents)  

# Deployment
myenv = Environment.from_conda_specification(name="myenv", file_path=conda_env_file_name)
inference_config = InferenceConfig(entry_script=script_file_name, environment=myenv)
