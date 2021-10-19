# transfer from azure data lake storage to azure blob storage


******************************************************************************************************************blob_data_ref 
from azureml.exceptions import UserErrorException

blob_datastore_name='MyBlobDatastore'
account_name=os.getenv("BLOB_ACCOUNTNAME_62", "<my-account-name>") # Storage account name
container_name=os.getenv("BLOB_CONTAINER_62", "<my-container-name>") # Name of Azure blob container
account_key=os.getenv("BLOB_ACCOUNT_KEY_62", "<my-account-key>") # Storage account key

try:
    blob_datastore = Datastore.get(ws, blob_datastore_name)
    print("Found Blob Datastore with name: %s" % blob_datastore_name)
except UserErrorException:
    blob_datastore = Datastore.register_azure_blob_container(
        workspace=ws,
        datastore_name=blob_datastore_name,
        account_name=account_name, # Storage account name
        container_name=container_name, # Name of Azure blob container
        account_key=account_key) # Storage account key
    print("Registered blob datastore with name: %s" % blob_datastore_name)

blob_data_ref = DataReference(
    datastore=blob_datastore,
    data_reference_name="blob_test_data",
    path_on_datastore="testdata")
******************************************************************************************************************adls_data_ref        
datastore_name='MyAdlsDatastore'
subscription_id=os.getenv("ADL_SUBSCRIPTION_62", "<my-subscription-id>") # subscription id of ADLS account
resource_group=os.getenv("ADL_RESOURCE_GROUP_62", "<my-resource-group>") # resource group of ADLS account
store_name=os.getenv("ADL_STORENAME_62", "<my-datastore-name>") # ADLS account name
tenant_id=os.getenv("ADL_TENANT_62", "<my-tenant-id>") # tenant id of service principal
client_id=os.getenv("ADL_CLIENTID_62", "<my-client-id>") # client id of service principal
client_secret=os.getenv("ADL_CLIENT_SECRET_62", "<my-client-secret>") # the secret of service principal

try:
    adls_datastore = Datastore.get(ws, datastore_name)
    print("Found datastore with name: %s" % datastore_name)
except UserErrorException:
    adls_datastore = Datastore.register_azure_data_lake(
        workspace=ws,
        datastore_name=datastore_name,
        subscription_id=subscription_id, # subscription id of ADLS account
        resource_group=resource_group, # resource group of ADLS account
        store_name=store_name, # ADLS account name
        tenant_id=tenant_id, # tenant id of service principal
        client_id=client_id, # client id of service principal
        client_secret=client_secret) # the secret of service principal
    print("Registered datastore with name: %s" % datastore_name)

adls_data_ref = DataReference(
    datastore=adls_datastore,
    data_reference_name="adls_test_data",
    path_on_datastore="testdata")

******************************************************************************************************************DataFactoryCompute
data_factory_name = 'adftest'

def get_or_create_data_factory(workspace, factory_name):
    try:
        return DataFactoryCompute(workspace, factory_name)
    except ComputeTargetException as e:
        if 'ComputeTargetNotFound' in e.message:
            print('Data factory not found, creating...')
            provisioning_config = DataFactoryCompute.provisioning_configuration()
            data_factory = ComputeTarget.create(workspace, factory_name, provisioning_config)
            data_factory.wait_for_completion()
            return data_factory
        else:
            raise e
            
data_factory_compute = get_or_create_data_factory(ws, data_factory_name)

print("Setup Azure Data Factory account complete")     
******************************************************************************************************************DataTransferStep()
transfer_adls_to_blob = DataTransferStep(
    name="transfer_adls_to_blob",
    source_data_reference=adls_data_ref,
    destination_data_reference=blob_data_ref,
    compute_target=data_factory_compute)

print("Data transfer step created")

pipeline_01 = Pipeline(
    description="data_transfer_01",
    workspace=ws,
    steps=[transfer_adls_to_blob])

pipeline_run_01 = Experiment(ws, "Data_Transfer_example_01").submit(pipeline_01)
pipeline_run_01.wait_for_completion()

from azureml.widgets import RunDetails
RunDetails(pipeline_run_01).show()
