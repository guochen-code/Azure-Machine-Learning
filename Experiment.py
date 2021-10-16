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
Rundetails(run).show
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


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ running with a script @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# to access the experiment run context, which is needed to log metrics, the script must import azureml.core.Run class and call its get_context method
run = Run.get_context()
