############################################# Part I - Running a few steps in parallel #############################################

'''
Azure Machine Learning Pipelines provides the following built-in Steps:
PythonScriptStep: Adds a step to run a Python script in a Pipeline.
AdlaStep: Adds a step to run U-SQL script using Azure Data Lake Analytics.
DataTransferStep: Transfers data between Azure Blob and Data Lake accounts.
DatabricksStep: Adds a DataBricks notebook as a step in a Pipeline.
HyperDriveStep: Creates a Hyper Drive step for Hyper Parameter Tuning in a Pipeline.
AzureBatchStep: Creates a step for submitting jobs to Azure Batch
EstimatorStep: Adds a step to run Estimator in a Pipeline.
MpiStep: Adds a step to run a MPI job in a Pipeline.
AutoMLStep: Creates a AutoML step in a Pipeline.

The best practice is to use separate folders for scripts and its dependent files for each step and specify that folder as the source_directory for the step. 
This helps reduce the size of the snapshot created for the step (only the specific folder is snapshotted). 
Since changes in any files in the source_directory would trigger a re-upload of the snapshot, 
this helps keep the reuse of the step when there are no changes in the source_directory of the step.
'''
******************************************************************************************************** seprate folder + PythonScriptStep()
# For this step, we use a different source_directory
source_directory = './compare'
print('Source directory for the step is {}.'.format(os.path.realpath(source_directory)))

'''
# PythonScriptStep(
#     script_name, 
#     name=None, 
#     arguments=None, 
#     compute_target=None, 
#     runconfig=None, 
#     inputs=None, 
#     outputs=None, 
#     params=None, 
#     source_directory=None, 
#     allow_reuse=True, 
#     version=None, 
#     hash_paths=None)
# This returns a Step
'''
******************************************************************************************************** list of steps to run

# list of steps to run
steps = [step1, step2, step3]
print("Step lists created")

******************************************************************************************************** Pipeline()
'''
# Syntax
# Pipeline(workspace, 
#          steps, 
#          description=None, 
#          default_datastore_name=None, 
#          default_source_directory=None, 
#          resolve_closure=True, 
#          _workflow_provider=None, 
#          _service_endpoint=None)
'''
pipeline1 = Pipeline(workspace=ws, steps=steps)
print ("Pipeline is built")

******************************************************************************************************** Validate the pipeline
'''
You have the option to validate the pipeline prior to submitting for run. 
The platform runs validation steps such as checking for circular dependencies and parameter checks etc. 
even if you do not explicitly call validate method.
'''
pipeline1.validate()
print("Pipeline validation complete")

******************************************************************************************************** submit pipeline
'''
# Submit syntax
# submit(experiment_name, 
#        pipeline_parameters=None, 
#        continue_on_step_failure=False, 
#        regenerate_outputs=False)
'''
pipeline_run1 = Experiment(ws, 'Hello_World1').submit(pipeline1, regenerate_outputs=False)
print("Pipeline is submitted for execution")
# Note: If regenerate_outputs is set to True, a new submit will always force generation of all step outputs, 
# and disallow data reuse for any step of this run. Once this run is complete, however, subsequent runs may reuse the results of this run.
 
******************************************************************************************************** Examine pipeline run
RunDetails(pipeline_run1).show()

# You can cycle through the node_run objects and examine job logs, stdout, and stderr of each of the steps.
step_runs = pipeline_run1.get_children()
for step_run in step_runs:
    status = step_run.get_status()
    print('Script:', step_run.name, 'status:', status)
    
    # Change this if you want to see details even if the Step has succeeded.
    if status == "Failed":
        joblog = step_run.get_job_log()
        print('job log:', joblog)

# If you wait until the pipeline_run is finished, you may be able to get additional details on the run.
pipeline_run1.wait_for_completion()
for step_run in pipeline_run1.get_children():
   print("{}: {}".format(step_run.name, step_run.get_metrics()))
    
****************************************************************************************************************************************************************************************************************
****************************************************************************************************************************************************************************************************************
****************************************************************************************************************************************************************************************************************

############################################# Part II - Running a few steps in sequence #############################################

step2.run_after(step1)
step3.run_after(step2)

# Try a loop
#step2.run_after(step3)

# Now, construct the pipeline using the steps.

# We can specify the "final step" in the chain, 
# Pipeline will take care of "transitive closure" and 
# figure out the implicit or explicit dependencies
# https://www.geeksforgeeks.org/transitive-closure-of-a-graph/
pipeline2 = Pipeline(workspace=ws, steps=[step3])
print ("Pipeline is built")

pipeline2.validate()
print("Simple validation complete")
pipeline_run2 = Experiment(ws, 'Hello_World2').submit(pipeline2)
print("Pipeline is submitted for execution")
RunDetails(pipeline_run2).show()
