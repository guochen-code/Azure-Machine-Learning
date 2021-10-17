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

'''
# Syntax
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

