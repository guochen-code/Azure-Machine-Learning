****************************************************************************************************** versioning best practice
# When you load data from a dataset, the current data content referenced by the dataset is always loaded. 
# If you want to make sure that each dataset version is reproducible, we recommend that you not modify data content referenced by the dataset version. 
# When new data comes in, save new data files into a separate data folder and then create a new dataset version to include data from that new folder.

from azureml.core import Dataset

# get the default datastore of the workspace
datastore = workspace.get_default_datastore()

# create & register weather_ds version 1 pointing to all files in the folder of week 27
datastore_path1 = [(datastore, 'Weather/week 27')]
dataset1 = Dataset.File.from_files(path=datastore_path1)
dataset1.register(workspace = workspace,
                  name = 'weather_ds',
                  description = 'weather data in week 27',
                  create_new_version = True)

# create & register weather_ds version 2 pointing to all files in the folder of week 27 and 28
datastore_path2 = [(datastore, 'Weather/week 27'), (datastore, 'Weather/week 28')]
dataset2 = Dataset.File.from_files(path = datastore_path2)
dataset2.register(workspace = workspace,
                  name = 'weather_ds',
                  description = 'weather data in week 27, 28',
                  create_new_version = True)
*********************************************************************************************************** Version an ML pipeline output dataset
# ML pipelines populate the output of each step into a new folder every time the pipeline reruns. 
# This behavior allows the versioned output datasets to be reproducible.

from azureml.core import Dataset
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.core. runconfig import CondaDependencies, RunConfiguration

# get input dataset 
input_ds = Dataset.get_by_name(workspace, 'weather_ds')

# register pipeline output as dataset
output_ds = PipelineData('prepared_weather_ds', datastore=datastore).as_dataset()
output_ds = output_ds.register(name='prepared_weather_ds', create_new_version=True)

conda = CondaDependencies.create(
    pip_packages=['azureml-defaults', 'azureml-dataprep[fuse,pandas]'], 
    pin_sdk_version=False)

run_config = RunConfiguration()
run_config.environment.docker.enabled = True
run_config.environment.python.conda_dependencies = conda

# configure pipeline step to use dataset as the input and output
prep_step = PythonScriptStep(script_name="prepare.py",
                             inputs=[input_ds.as_named_input('weather_ds')],
                             outputs=[output_ds],
                             runconfig=run_config,
                             compute_target=compute_target,
                             source_directory=project_folder)

*********************************************************************************************************** Trace datasets in experiment runs
# For each Machine Learning experiment, you can easily trace the datasets used as input with the experiment Run object.
# The following code uses the get_details() method to track which input datasets were used with the experiment run:
# get input datasets
inputs = run.get_details()['inputDatasets']
input_dataset = inputs[0]['dataset']

# list the files referenced by input_dataset
input_dataset.to_path()
# You can also find the input_datasets from experiments by using the Azure Machine Learning studio.
# go to your Experiments pane and open the Properties tab for a specific run of your experiment.

*********************************************************************************************************** Register models with datasets
model = run.register_model(model_name='keras-mlp-mnist',
                           model_path=model_path,
                           datasets =[('training data',train_dataset)])
# After registration, you can see the list of models registered with the dataset by using Python or go to the studio.
# From the Datasets pane under Assets. Select the dataset and then select the Models tab for a list of the models that are registered with the dataset.
