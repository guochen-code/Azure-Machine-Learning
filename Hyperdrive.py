from azureml.core import Experiment, ScriptRunConfig, Environment
from azureml.train.hyperdrive import GridParameterSampling, HyperDriveConfig, PrimaryMetricGoal, choice
from azureml.widgets import RunDetails

# Create a Python environment for the experiment
hyper_env = Environment.from_conda_specification("experiment_env", experiment_folder + "/hyperdrive_env.yml")

# Get the training dataset
diabetes_ds = ws.datasets.get("diabetes dataset")

# Create a script config
script_config = ScriptRunConfig(source_directory=experiment_folder,
                                script='diabetes_training.py',
                                # Add non-hyperparameter arguments -in this case, the training dataset
                                arguments = ['--input-data', diabetes_ds.as_named_input('training_data')],
                                environment=hyper_env,
                                compute_target = training_cluster)

# Sample a range of parameter values
params = GridParameterSampling(
    {
        # Hyperdrive will try 6 combinations, adding these as script arguments
        '--learning_rate': choice(0.01, 0.1, 1.0),
        '--n_estimators' : choice(10, 100)
    }
)

# Configure hyperdrive settings
hyperdrive = HyperDriveConfig(run_config=script_config, 
                          hyperparameter_sampling=params, 
                          policy=None, # No early stopping policy
                          primary_metric_name='AUC', # Find the highest AUC metric
                          primary_metric_goal=PrimaryMetricGoal.MAXIMIZE, 
                          max_total_runs=6, # Restict the experiment to 6 iterations
                          max_concurrent_runs=2) # Run up to 2 iterations in parallel

# Run the experiment
experiment = Experiment(workspace=ws, name='mslearn-diabetes-hyperdrive')
run = experiment.submit(config=hyperdrive)

# Show the status in the notebook as the experiment runs
RunDetails(run).show()
run.wait_for_completion()

************************************************retrive the best model and related parameters + arguments************************************************
# Print all child runs, sorted by the primary metric
for child_run in run.get_children_sorted_by_primary_metric():
    print(child_run)

# Get the best run, and its metrics and arguments
best_run = run.get_best_run_by_primary_metric()
best_run_metrics = best_run.get_metrics()
script_arguments = best_run.get_details() ['runDefinition']['arguments']
print('Best Run Id: ', best_run.id)
print(' -AUC:', best_run_metrics['AUC'])
print(' -Accuracy:', best_run_metrics['Accuracy'])
print(' -Arguments:',script_arguments)

************************************************retrive the best model and related parameters + arguments************************************************
from azureml.core import Model

# Register model
best_run.register_model(model_path='outputs/diabetes_model.pkl', model_name='diabetes_model',
                        tags={'Training context':'Hyperdrive'},
                        properties={'AUC': best_run_metrics['AUC'], 'Accuracy': best_run_metrics['Accuracy']})

# List registered models
for model in Model.list(ws):
    print(model.name, 'version:', model.version)
    for tag_name in model.tags:
        tag = model.tags[tag_name]
        print ('\t',tag_name, ':', tag)
    for prop_name in model.properties:
        prop = model.properties[prop_name]
        print ('\t',prop_name, ':', prop)
    print('\n')
