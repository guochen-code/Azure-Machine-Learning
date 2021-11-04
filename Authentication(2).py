We strongly recommended that you do not insert the secret password to code. Instead, you can use environment variables to pass it to your code, 
for example through Azure Key Vault, or through secret build variables in Azure DevOps. 
For local testing, you can for example use following PowerShell command to set the environment variable.
$env:AZUREML_PASSWORD = "my-password"

*************************************************************** PART I - How to authenticate to your Azure ML Workspace ***************************************************************
'''
Interactive Login Authentication
Azure CLI Authentication
Managed Service Identity (MSI) Authentication
Service Principal Authentication
Token Authentication
The interactive authentication is suitable for local experimentation on your own computer. 
Azure CLI authentication is suitable if you are already using Azure CLI for managing Azure resources, and want to sign in only once. 
The MSI and Service Principal authentication are suitable for automated workflows, for example as part of Azure Devops build.

When setting up a machine learning workflow as an automated process, we recommend using Service Principal Authentication. 
This approach decouples the authentication from any specific user login, and allows managed access control.
Note that you must have administrator privileges over the Azure subscription to complete these steps.
'''
*************************************************************** Interactive authentication is the default mode when using Azure ML SDK.

# If you receive an error:
# AuthenticationException: You don't have access to xxxxxx-xxxx-xxx-xxx-xxxxxxxxxx subscription. All the subscriptions that you have access to = ...
**************solution: check that the you used correct login and entered the correct subscription ID.

# In some cases, you may see a version of the error message containing text: All the subscriptions that you have access to = []
**************solution: 
'''In such a case, you may have to specify the tenant ID of the Azure Active Directory you're using. 
An example would be accessing a subscription as a guest to a tenant that is not your default. 
You specify the tenant by explicitly instantiating InteractiveLoginAuthentication with Tenant ID as argument. 
The Tenant ID can be found, for example, from https://portal.azure.com under Azure Active Directory, Properties as Directory ID.'''

from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication(tenant_id="my-tenant-id")

ws = Workspace(subscription_id="my-subscription-id",
               resource_group="my-ml-rg",
               workspace_name="my-ml-workspace",
               auth=interactive_auth)

# Despite having access to the workspace, you may sometimes see the following error when retrieving it:
# You are currently logged-in to xxxxxxxx-xxx-xxxx-xxxx-xxxxxxxxxxxx tenant. You don't have access to xxxxxx-xxxx-xxx-xxx-xxxxxxxxxx subscription, 
# please check if it is in this tenant.
**************solution: 
'''This error sometimes occurs when you are trying to access a subscription to which you were recently added. 
In this case, you need to force authentication again to avoid using a cached authentication token that has not picked up the new permissions. 
You can do so by setting force=true on the InteractiveLoginAuthentication() object's constructor as follows:'''
forced_interactive_auth = InteractiveLoginAuthentication(tenant_id="my-tenant-id", force=True)

ws = Workspace(subscription_id="my-subscription-id",
               resource_group="my-ml-rg",
               workspace_name="my-ml-workspace",
               auth=forced_interactive_auth)

*************************************************************** Azure CLI Authentication
from azureml.core.authentication import AzureCliAuthentication

cli_auth = AzureCliAuthentication()

ws = Workspace(subscription_id="my-subscription-id",
               resource_group="my-ml-rg",
               workspace_name="my-ml-workspace",
               auth=cli_auth)

print("Found workspace {} at location {}".format(ws.name, ws.location))

*************************************************************** MSI authentication is supported only when using SDK from Azure Virtual Machine. 
*************************************************************** The code below will fail on local computer.
'''
When using Azure ML SDK on Azure Virtual Machine (VM), you can use Managed Service Identity (MSI) based authentication. 
This mode allows the VM connect to the Workspace without storing credentials in the Python code.

As a prerequisite, enable System-assigned Managed Identity for your VM as described in Configure managed identities for Azure resources on a VM using the Azure portal.

Then, assign the VM access to your Workspace. For example from Azure Portal, navigate to your workspace, 
select Access Control (IAM), Add Role Assignment, specify Virtual Machine for Assign Access To dropdown, and select your VM's identity.
'''
from azureml.core.authentication import MsiAuthentication

msi_auth = MsiAuthentication()

ws = Workspace(subscription_id="my-subscription-id",
               resource_group="my-ml-rg",
               workspace_name="my-ml-workspace",
               auth=msi_auth)

print("Found workspace {} at location {}".format(ws.name, ws.location))

*************************************************************** Service Principal
'''
Note that you must have administrator privileges over the Azure subscription to complete these steps.

(1) register a new service principal: 
go to Azure Portal, select Azure Active Directory and App Registrations. 
Then select +New application, give your service principal a name, for example my-svc-principal. You can leave other parameters as is. 
Then click Register.

(2) save your client ID and tenant ID
From the page for your newly created service principal
Copy your client ID and tenant ID
Select Certificates & secrets, and +New client secret write a description for your key, and select duration. 
Then click Add, and copy the value of client secret to a secure location.

(3) give the service principal permissions to access your workspace
Navigate to Resource Groups, to the resource group for your Machine Learning Workspace.
Then select Access Control (IAM) and Add a role assignment. 
For Role, specify which level of access you need to grant, for example Contributor. 
Start entering your service principal name and once it is found, select it, and click Save.
'''
import os
from azureml.core.authentication import ServicePrincipalAuthentication

svc_pr_password = os.environ.get("AZUREML_PASSWORD")

svc_pr = ServicePrincipalAuthentication(
    tenant_id="my-tenant-id",
    service_principal_id="my-application-id",
    service_principal_password=svc_pr_password)


ws = Workspace(
    subscription_id="my-subscription-id",
    resource_group="my-ml-rg",
    workspace_name="my-ml-workspace",
    auth=svc_pr
    )

print("Found workspace {} at location {}".format(ws.name, ws.location))

*************************************************************** Part II - Use secrets in remote runs ***************************************************************
'''
Sometimes, you may have to pass a secret to a remote run, for example username and password to authenticate against external data source.

Azure ML SDK enables this use case through Key Vault associated with your workspace. The workflow for adding a secret is following.

On local computer:

1. Read in a local secret, for example from environment variable or user input. To keep them secret, do not insert secret values into code as hard-coded strings.
2. Obtain a reference to the keyvault
3. Add the secret name-value pair in the key vault.
'''
import uuid
local_secret = os.environ.get("LOCAL_SECRET", default = str(uuid.uuid4())) # Use random UUID as a substitute for real secret.
keyvault = ws.get_default_keyvault()
keyvault.set_secret(name="secret-name", value = local_secret)

keyvault.list_secrets() # ou can list secret names you've added. This method doesn't return the values of the secrets.

########## Note: This method returns the secret value. Take care not to write the the secret value to output.
retrieved_secret = keyvault.get_secret(name="secret-name")
local_secret==retrieved_secret

# In submitted runs on local and remote compute, you can use the get_secret method of Run instance to get the secret value from Key Vault.
#The method gives you a simple shortcut: the Run instance is aware of its Workspace and Keyvault, 
# so it can directly obtain the secret without you having to instantiate the Workspace and Keyvault within remote run.
########## Note: This method returns the secret value. Take care not to write the the secret value to output.
%%writefile get_secret.py
from azureml.core import Run
run = Run.get_context()
secret_value = run.get_secret(name="secret-name")
print("Got secret value {} , but don't write it out!".format(len(secret_value) * "*"))

# Then, submit the script as a regular script run, and find the obfuscated secret value in run output. 
#You can use the same approach to other kinds of runs, such as Estimator ones.
from azureml.core import Experiment
from azureml.core.script_run_config import ScriptRunConfig
exp = Experiment(workspace = ws, name="try-secret")
src = ScriptRunConfig(source_directory=".", script="get_secret.py")
run = exp.submit(src)
run.wait_for_completion(show_output=True)
