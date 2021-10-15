# When sending a request to a service that is secured with a key or token, use the Authorization header to pass the key or token. 
# The key or token must be formatted as Bearer <key-or-token>, where <key-or-token> is your key or token value.

# KEY *******************************************************************************

# The primary difference between keys and tokens is that keys are static and can be regenerated manually, and tokens need to be refreshed upon expiration. 
# Key-based auth is supported for Azure Container Instance (disabled by default) and Azure Kubernetes Service deployed web-services (enabled by default),
# and token-based auth is only available for Azure Kubernetes Service deployments (disabled by default).

from azureml.core.webservice import AciWebservice

aci_config = AciWebservice.deploy_configuration(cpu_cores = 1,
                                                memory_gb = 1,
                                                auth_enabled=True)

# To fetch the auth keys, use aci_service.get_keys(). 
# To regenerate a key, use the regen_key() function and pass either Primary or Secondary.
aci_service.regen_key("Primary")
# or
aci_service.regen_key("Secondary")

# Token *******************************************************************************
# Token authentication is disabled by default when you deploy to Azure Kubernetes Service.
# Token authentication isn't supported when you deploy to Azure Container Instances.
# Token authentication can't be used at the same time as key-based authentication.
# To control token authentication, use the token_auth_enabled parameter when you create or update a deployment:
from azureml.core.webservice import AksWebservice
from azureml.core.model import Model, InferenceConfig

# Create the config
aks_config = AksWebservice.deploy_configuration()

#  Enable token auth and disable (key) auth on the webservice
aks_config = AksWebservice.deploy_configuration(token_auth_enabled=True, auth_enabled=False)

aks_service_name ='aks-service-1'

# deploy the model
aks_service = Model.deploy(workspace=ws,
                           name=aks_service_name,
                           models=[model],
                           inference_config=inference_config,
                           deployment_config=aks_config,
                           deployment_target=aks_target)

aks_service.wait_for_deployment(show_output = True)

# You'll need to request a new token after the token's refresh_by time.
# If token authentication is enabled, you can use the get_token method to retrieve a JSON Web Token (JWT) and that token's expiration time:
token, refresh_by = aks_service.get_token()
print(token)

