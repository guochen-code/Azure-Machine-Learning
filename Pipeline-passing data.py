# a step in the pipeline can take data as input. 
# This data can be a data source that lives in one of the accessible data locations, 
# or intermediate data produced by a previous step in the pipeline.
Datasource ******************************************************************************************************************************* DataReference()
# Datasource is represented by DataReference object and points to data that lives in or is accessible from Datastore. 
# DataReference could be a pointer to a file or a directory.

# Reference the data uploaded to blob storage using DataReference
# Assign the datasource to blob_input_data variable

# DataReference(datastore, 
#               data_reference_name=None, 
#               path_on_datastore=None, 
#               mode='mount', 
#               path_on_compute=None, 
#               overwrite=False)

blob_input_data = DataReference(
    datastore=def_blob_store,
    data_reference_name="test_data",
    path_on_datastore="20newsgroups/20news.pkl")
print("DataReference object created")

Intermediate/Output Data **************************************************************************************************************** PipelineData()
# Intermediate data (or output of a Step) is represented by PipelineData object. 
# PipelineData can be produced by one step and consumed in another step by providing the PipelineData object as an output of one step and the input of one or more steps.

'''
Constructing PipelineData

name: [Required] Name of the data item within the pipeline graph
datastore_name: Name of the Datastore to write this output to
output_name: Name of the output
output_mode: Specifies "upload" or "mount" modes for producing output (default: mount)
output_path_on_compute: For "upload" mode, the path to which the module writes this output during execution
output_overwrite: Flag to overwrite pre-existing data
'''
# Define intermediate data using PipelineData
# Syntax

# PipelineData(name, 
#              datastore=None, 
#              output_name=None, 
#              output_mode='mount', 
#              output_path_on_compute=None, 
#              output_overwrite=None, 
#              data_type=None, 
#              is_directory=None)

# Naming the intermediate data as processed_data1 and assigning it to the variable processed_data1.
processed_data1 = PipelineData("processed_data1",datastore=def_blob_store)
print("PipelineData object created")

############## consumes the datasource (Datareference) in the previous step and produces processed_data1
trainStep = PythonScriptStep(
    script_name="train.py", 
    arguments=["--input_data", blob_input_data, "--output_train", processed_data1],
    inputs=[blob_input_data],
    outputs=[processed_data1],
    compute_target=aml_compute, 
    source_directory=source_directory,
    runconfig=run_config
)
print("trainStep created")

use output genereated from previous step & existing data in a datastore ************************************************************* PipleParameter() + DataPath()

# Reference the data uploaded to blob storage using a PipelineParameter and a DataPath
from azureml.pipeline.core import PipelineParameter
from azureml.data.datapath import DataPath, DataPathComputeBinding

datapath = DataPath(datastore=def_blob_store, path_on_datastore='20newsgroups/20news.pkl')
datapath_param = PipelineParameter(name="compare_data", default_value=datapath)
data_parameter1 = (datapath_param, DataPathComputeBinding(mode='mount'))
# Now define the compare step which takes two inputs and produces an output
processed_data3 = PipelineData("processed_data3", datastore=def_blob_store)
source_directory = "data_dependency_run_compare"

compareStep = PythonScriptStep(
    script_name="compare.py",
    arguments=["--compare_data1", data_parameter1, "--compare_data2", processed_data2, "--output_compare", processed_data3],
    inputs=[data_parameter1, processed_data2],
    outputs=[processed_data3],    
    compute_target=aml_compute, 
    source_directory=source_directory)
print("compareStep created")

pipeline1=Pipeline(workspace=ws,steps=[compareStep])
print('pipeline is built')
pipeline_run1=Experiment(ws,'name').submit(pipeline1)
RunDetails(pipeline_run1).show()
pipeline_run1.wait_for_completion(show_output=True)

see outputs *************************************************************
# See where outputs of each pipeline step are located on your datastore.
# Wait for pipeline run to complete, to make sure all the outputs are ready
# Get Steps
for step in pipeline_run1.get_steps():
    print("Outputs of step " + step.name)
    
    # Get a dictionary of StepRunOutputs with the output name as the key 
    output_dict = step.get_outputs()
    
    for name, output in output_dict.items():
        
        output_reference = output.get_port_data_reference() # Get output port data reference
        print("\tname: " + name)
        print("\tdatastore: " + output_reference.datastore_name)
        print("\tpath on datastore: " + output_reference.path_on_datastore)
        
# download ------------------------ Retrieve the step runs by name 'train.py'
train_step = pipeline_run1.find_step_run('train.py')

if train_step:
    train_step_obj = train_step[0] # since we have only one step by name 'train.py'
    train_step_obj.get_output_data('processed_data1').download("./outputs") # download the output to current directory
