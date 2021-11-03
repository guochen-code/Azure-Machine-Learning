from azureml.pipeline.steps import ParallelRunConfig, ParallelRunStep
from azureml.data import OutputFileDatasetConfig
from azureml.core.runconfig import DockerConfiguration

output_dir = OutputFileDatasetConfig(name='inferences')

parallel_run_config = ParallelRunConfig(
    source_directory=experiment_folder,
    entry_script="batch_diabetes.py",
    mini_batch_size="5",
    error_threshold=10,
    output_action="append_row",
    environment=batch_env,
    compute_target=inference_cluster,
    node_count=2)

parallelrun_step = ParallelRunStep(
    name='batch-score-diabetes',
    parallel_run_config=parallel_run_config,
    inputs=[batch_data_set.as_named_input('diabetes_batch')],
    output=output_dir,
    arguments=[],
    allow_reuse=True
)

print('Steps defined')

************************************************************************************************************************************************
from azureml.core import Experiment
from azureml.pipeline.core import Pipeline

pipeline = Pipeline(workspace=ws, steps=[parallelrun_step])
pipeline_run = Experiment(ws, 'mslearn-diabetes-batch').submit(pipeline)
pipeline_run.wait_for_completion(show_output=True)

************************************************************************************************************************************************
import pandas as pd
import shutil

# Remove the local results folder if left over from a previous run
shutil.rmtree('diabetes-results', ignore_errors=True)

# Get the run for the first step and download its output
prediction_run = next(pipeline_run.get_children())
prediction_output = prediction_run.get_output_data('inferences')
prediction_output.download(local_path='diabetes-results')

# Traverse the folder hierarchy and find the results file
for root, dirs, files in os.walk('diabetes-results'):
    for file in files:
        if file.endswith('parallel_run_step.txt'):
            result_file = os.path.join(root,file)

# cleanup output format
df = pd.read_csv(result_file, delimiter=":", header=None)
df.columns = ["File", "Prediction"]

# Display the first 20 results
df.head(20)
