# Run Configuration
from azureml.core.runconfig import CondaDependencies, RunConfiguration

# create a new RunConfig object
conda_run_config = RunConfiguration(framework="python")

# Set compute target to AmlCompute
conda_run_config.target = compute_target

conda_run_config.environment.docker.enabled = True

cd = CondaDependencies.create(pip_packages=['azureml-sdk[automl]', 'applicationinsights', 'azureml-opendatasets', 'azureml-defaults'], 
                              conda_packages=['numpy==1.16.2'], 
                              pin_sdk_version=False)
conda_run_config.environment.python.conda_dependencies = cd

print('run config is ready')

# Data Ingestion Pipeline
