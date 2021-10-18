**********************************************************************Part-I Crediential-based authenticatoin**********************************************************************
'''
Authentication Type:

1) Account key or SAS token: Azure blob storage / Azure file share

2) Service Principal: Azure Data Lake Storage Gen 1 and Gen 2 / Azure SQL databse

3) SQL Authentication: Azure SQL databse / Azure PostgreSQL / Azure database for MySQL

4) No Authentication: Databricks file system
'''


# Azure blob container
blob_datastore_name='azblobsdk' # Name of the datastore to workspace
container_name=os.getenv("BLOB_CONTAINER", "<my-container-name>") # Name of Azure blob container
account_name=os.getenv("BLOB_ACCOUNTNAME", "<my-account-name>") # Storage account name
account_key=os.getenv("BLOB_ACCOUNT_KEY", "<my-account-key>") # Storage account access key

blob_datastore = Datastore.register_azure_blob_container(workspace=ws, 
                                                         datastore_name=blob_datastore_name, 
                                                         container_name=container_name, 
                                                         account_name=account_name,
                                                         account_key=account_key)

# Azure file share
file_datastore_name='azfilesharesdk' # Name of the datastore to workspace
file_share_name=os.getenv("FILE_SHARE_CONTAINER", "<my-fileshare-name>") # Name of Azure file share container
account_name=os.getenv("FILE_SHARE_ACCOUNTNAME", "<my-account-name>") # Storage account name
account_key=os.getenv("FILE_SHARE_ACCOUNT_KEY", "<my-account-key>") # Storage account access key

file_datastore = Datastore.register_azure_file_share(workspace=ws,
                                                     datastore_name=file_datastore_name, 
                                                     file_share_name=file_share_name, 
                                                     account_name=account_name,
                                                     account_key=account_key)


# Azure Data Lake Storage Generation 2
adlsgen2_datastore_name = 'adlsgen2datastore'

subscription_id=os.getenv("ADL_SUBSCRIPTION", "<my_subscription_id>") # subscription id of ADLS account
resource_group=os.getenv("ADL_RESOURCE_GROUP", "<my_resource_group>") # resource group of ADLS account

account_name=os.getenv("ADLSGEN2_ACCOUNTNAME", "<my_account_name>") # ADLS Gen2 account name
tenant_id=os.getenv("ADLSGEN2_TENANT", "<my_tenant_id>") # tenant id of service principal
client_id=os.getenv("ADLSGEN2_CLIENTID", "<my_client_id>") # client id of service principal
client_secret=os.getenv("ADLSGEN2_CLIENT_SECRET", "<my_client_secret>") # the secret of service principal

adlsgen2_datastore = Datastore.register_azure_data_lake_gen2(workspace=ws,
                                                             datastore_name=adlsgen2_datastore_name,
                                                             account_name=account_name, # ADLS Gen2 account name
                                                             filesystem='test', # ADLS Gen2 filesystem
                                                             tenant_id=tenant_id, # tenant id of service principal
                                                             client_id=client_id, # client id of service principal
                                                             client_secret=client_secret) # the secret of service principal


# Get datastores from your workspace
# Get a named datastore from the current workspace
datastore = Datastore.get(ws, datastore_name='your datastore name')
# or
datastore = Datastore(ws, datastore_name='your datastore name')

# List all datastores registered in the current workspace
datastores = ws.datastores
for name, datastore in datastores.items():
    print(name, datastore.datastore_type)


    
# get and change default datastore    
datastore = ws.get_default_datastore()
ws.set_default_datastore(new_default_datastore)


**********************************************************************Part-II Identity-based authenticatoin**********************************************************************
'''
Identity-based data access supports connections to only the following storage services:
1) Azure Blob Storage
2) Azure Data Lake Storage Gen1 and Gen2
3) Azure SQL Database
'''
# Create blob datastore without credentials.
blob_datastore = Datastore.register_azure_blob_container(workspace=ws,
                                                      datastore_name='credentialless_blob',
                                                      container_name='my_container_name',
                                                      account_name='my_account_name')

# Create Azure Data Lake Storage Gen1 datastore without credentials.
adls_dstore = Datastore.register_azure_data_lake(workspace = workspace,
                                                 datastore_name='credentialless_adls1',
                                                 store_name='adls_storage')

# Create Azure Data Lake Storage Gen2 datastore without credentials.
adls2_dstore = Datastore.register_azure_data_lake_gen2(workspace=ws, 
                                                       datastore_name='credentialless_adls2', 
                                                       filesystem='tabular', 
                                                       account_name='myadls2')

# Use data in storage
'''
To create datasets with identity-based data access, you have the following options. 
This type of dataset creation uses your Azure Active Directory token for data access authentication.
Reference paths from datastores that also use identity-based data access. 
In the following example, blob_datastore already exists and uses identity-based data access.
'''
blob_dataset = Dataset.Tabular.from_delimited_files(blob_datastore,'test.csv')

# Skip datastore creation and create datasets directly from storage URLs. 
# This functionality currently supports only Azure blobs and Azure Data Lake Storage Gen1 and Gen2.*******************
blob_dset = Dataset.File.from_files('https://myblob.blob.core.windows.net/may/keras-mnist-fashion/')
