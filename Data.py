1) to access a pth in a datastore in an experiment script, you must create a data reference and pass it to the script as a parameter. 
The script can then read data from the data reference parameter just like a local file path.
2) to access a dataset in an experiment, pass the dataset as a named input to the ScriptRunConfig.
************************************************************************************************************************************
from azureml.core import Dataset

default_ds = ws.get_default_datastore()

if 'diabetes dataset' not in ws.datasets:
    default_ds.upload_files(files=['./data/diabetes.csv', './data/diabetes2.csv'], # Upload the diabetes csv files in /data
                        target_path='diabetes-data/', # Put it in a folder path in the datastore
                        overwrite=True, # Replace existing files of the same name
                        show_progress=True)

    #Create a tabular dataset from the path on the datastore (this may take a short while)
    tab_data_set = Dataset.Tabular.from_delimited_files(path=(default_ds, 'diabetes-data/*.csv'))

    # Register the tabular dataset
    try:
        tab_data_set = tab_data_set.register(workspace=ws, 
                                name='diabetes dataset',
                                description='diabetes data',
                                tags = {'format':'CSV'},
                                create_new_version=True)
        print('Dataset registered.')
    except Exception as ex:
        print(ex)
else:
    print('Dataset already registered.')

    
******************************************************************
img_paths=[(blob_ds,'data/files/images/*.jpg),(blob_ds,'data/files/images/*.png)]
file_ds=Dataset.File.from_files(path=img_paths)
file_ds=file_ds.register(workspace=ws, name='img_files', create_new_version=True)

img_ds=Dataset.get_by_name(workspace=ws, name='img_files', version=2)

************************************************************************************************************************************
for file_path in files_ds.to_path():
    print(file_path)
    
************************************************************************************************************************************
when passing file dataset, you must specify the acces mode:
estimator=Estimator(...,
                    inputs=[img_ds.as_named_input('img_data').as_download(path_on_compute='data')],
                    ....)
            
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Train a model from a file dataset
# When you're using a file dataset, the dataset argument passed to the script represents a mount point containing file paths. 
# How you read the data from these files depends on the kind of data in the files and what you want to do with it. 
# In the case of the diabetes CSV files, you can use the Python glob module to create a list of files in the virtual mount point defined by the dataset, 
# and read them all into Pandas dataframes that are concatenated into a single dataframe.

# Get script arguments (rgularization rate and file dataset mount point)
parser = argparse.ArgumentParser()
parser.add_argument('--regularization', type=float, dest='reg_rate', default=0.01, help='regularization rate')
parser.add_argument('--input-data', type=str, dest='dataset_folder', help='data mount point')
args = parser.parse_args()

# Set regularization hyperparameter (passed as an argument to the script)
reg = args.reg_rate

data_path = run.input_datasets['training_files'] # Get the training data path from the input
# (You could also just use args.dataset_folder if you don't want to rely on a hard-coded friendly name) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Read the files
all_files = glob.glob(data_path + "/*.csv")
diabetes = pd.concat((pd.read_csv(f) for f in all_files), sort=False)

# Just as with tabular datasets, you can retrieve a file dataset from the input_datasets collection by using its friendly name. 
# You can also retrieve it from the script argument, which in the case of a file dataset contains a mount path to the files 
# (rather than the dataset ID passed for a tabular dataset).

# Next we need to change the way we pass the dataset to the script - it needs to define a path from which the script can read the files. 
# You can use either the as_download or as_mount method to do this. 
# Using as_download causes the files in the file dataset to be downloaded to a temporary location on the compute where the script is being run, 
# while as_mount creates a mount point from which the files can be streamed directly from the datastore.

# You can combine the access method with the as_named_input method to include the dataset in the input_datasets collection in the experiment run 
# (if you omit this, for example by setting the argument to diabetes_ds.as_mount(), !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# the script will be able to access the dataset mount point from the script arguments, but not from the input_datasets collection). !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from azureml.core import Experiment
from azureml.widgets import RunDetails


# Get the training dataset
diabetes_ds = ws.datasets.get("diabetes file dataset")

# Create a script config
script_config = ScriptRunConfig(source_directory=experiment_folder,
                                script='diabetes_training.py',
                                arguments = ['--regularization', 0.1, # Regularizaton rate parameter
                                             '--input-data', diabetes_ds.as_named_input('training_files').as_download()], # Reference to dataset location
                                environment=env) # Use the environment created previously

# submit the experiment
experiment_name = 'mslearn-train-diabetes'
experiment = Experiment(workspace=ws, name=experiment_name)
run = experiment.submit(config=script_config)
RunDetails(run).show()
run.wait_for_completion()
