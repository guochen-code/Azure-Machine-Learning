# a step in the pipeline can take data as input. 
# This data can be a data source that lives in one of the accessible data locations, 
# or intermediate data produced by a previous step in the pipeline.
Datasource ******************************************************************************************************************************************** DataReference()
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

Intermediate/Output Data ***************************************************************************************************************************** PipelineData()
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

