************************************************************************************Experiment URL****************************************************************
# Get the latest run of the experiment
run = list(experiment.get_runs())[0]

# Get logged metrics
print("\nMetrics:")
metrics = run.get_metrics()
for key in metrics.keys():
        print(key, metrics.get(key))
    
# Get a link to the experiment in Azure ML studio   
experiment_url = experiment.get_portal_url()
print('See details at', experiment_url)


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ not running with a script @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
experiment=Experiment(workspace=ws,name='name')
run=experiment.start_logging()
.
.
.
.
run.wait_for_completion()

# logging metrics
run.log('name',x) # record a single named value
run.log_list # record a named list of values
run.log_row # record a row with multiple columns
run.log_table # record a dictionary as a table
run.log_image # record an image file or plot

##################################################################### retrieve and view logs #####################################################################
RunDetails(run).show()
# or
metrics=run.get_metrics()
print(json.dump(metrics,indent=2))

##################################################################### experiment output files #####################################################################
# you can upload local files to the run's outputs folder
run.upload_file(name='outputs/sample.csv',path_or_stream='./sample.csv')
# when running an experiment in a remote compute context, any files written to the outputs folder in the compute context are 
# automatically uploaded to the run's outputs folder when the run completes
files=run.get_file_names()
print(json.dump(files,indent=2))
***************************************************************************
import os
download_folder = 'downloaded-files'
# Download files in the "outputs" folder
run.download_files(prefix='outputs', output_directory=download_folder)
# Verify the files have been downloaded
for root, directories, filenames in os.walk(download_folder): 
    for filename in filenames:  
        print (os.path.join(root,filename))

***************************************************************************
# If you need to troubleshoot the experiment run, you can use the get_details method to retrieve basic details about the run, 
# or you can use the get_details_with_logs method to retrieve the run details as well as the contents of log files generated during the run:
run.get_details_with_logs()
# Note that this time, the run generated some log files. You can view these (metrics + files) in the widget, <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# or you can use the get_details_with_logs method like we did before, only this time the output will include the log data.
run.get_details_with_logs()

***************************************************************************
# Although you can view the log details in the output above, it's usually easier to download the log files and view them in a text editor.
import os
log_folder = 'downloaded-logs'
# Download all files
run.get_all_logs(destination=log_folder)
# Verify the files have been downloaded
for root, directories, filenames in os.walk(log_folder): 
    for filename in filenames:  
        print (os.path.join(root,filename))

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ running with a script @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# to access the experiment run context, which is needed to log metrics, the script must import azureml.core.Run class and call its get_context method
run = Run.get_context()

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ View experiment run history @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Now that you've run the same experiment multiple times, you can view the history in Azure Machine Learning studio and explore each logged run. 
# Or you can retrieve an experiment by name from the workspace and iterate through its runs using the SDK:
from azureml.core import Experiment, Run

diabetes_experiment = ws.experiments['mslearn-diabetes']
for logged_run in diabetes_experiment.get_runs():
    print('Run ID:', logged_run.id)
    metrics = logged_run.get_metrics()
    for key in metrics.keys():
        print('-', key, metrics.get(key))
