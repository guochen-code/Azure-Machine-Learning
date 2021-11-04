Compute Targets for Inference:
(1) AKS: real-time/high-scale production/ ONLY use UI to change nodes
(2) AML Compute Clusters: Batch-inference/ NOT support for real-time
(3) ACI: real-time/ for dev/test purposes/ low-scale & cpu-based < 48GB RAM
(4) Local: limited testing and debugging
  
******************************************************************************************
# Deploy model as web service
# (1) create deployment folder
# (2) write entry/scoring script in the folder
# (3) InferenceConfig()
# (4) web service container: AciWebservice.deploy_configuration()
# (5) deploy the model as a service

************* if deploy to AKS, create the compute target before deploy
cluster_name='aks-cluster'
compute_config=AksCompute.provisioning_configuration(location='eastus')
production_cluster=ComputeTarget.create(ws,cluster_name,compute_config)
production_cluster.wait_for_completion(show_output=True)

from azureml.core.webservice import AksWebservice
classifier_deploy_config = AksWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

azureml.core.webservice.AciWebservice: no need to explicitly create an ACI compute target.
azureml.core.webservice.LocalWebservice: configure a local Docker-based service.

# deploy the model
from azureml.core.model import Model
model = ws.models['model_name']
service=Model.deploy(workspace=ws,
                     name='service_name',
                     models=[model],
                     inference_config=inference_config,
                     deployment_config=deployment_config,
                     deployment_target=production_cluseter)
service.wait_for_completion(show_output=True)

# for ACI or local services, you can omit the deployment_target parameter (or set it to None).
                     
*************CLI
az ml model deploy --ct myaks -m mymodel:1 -n myservice --ic inferenceconfig.json --dc deploymentconfig.json

********************************************************************************************
# Reload Service

# You can update your score.py file and then call reload() to quickly restart the service. 
# This will only reload your execution script and dependency files, it will not rebuild the underlying Docker image. 
# As a result, reload() is fast, but if you do need to rebuild the image -- to add a new Conda or pip package, for instance -- you will have to call update()
local_service.reload()

# If you want to change your model(s), Conda dependencies or deployment configuration, call update() to rebuild the Docker image.
# Update Service
local_service.update(models=[model],
                     inference_config=inference_config,
                     deployment_config=deployment_config)


******************************** Deploy model to AKS cluster based on the LocalWebservice's configuration ****************************************************************
# This is a one time setup for AKS Cluster. You can reuse this cluster for multiple deployments after it has been created. 
# If you delete the cluster or the resource group that contains it, then you would have to recreate it.
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.compute_target import ComputeTargetException

# Choose a name for your AKS cluster
aks_name = 'my-aks-9' 

# Verify the cluster does not exist already
try:
    aks_target = ComputeTarget(workspace=ws, name=aks_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    # Use the default configuration (can also provide parameters to customize)
    prov_config = AksCompute.provisioning_configuration()

    # Create the cluster
    aks_target = ComputeTarget.create(workspace = ws, 
                                      name = aks_name, 
                                      provisioning_configuration = prov_config)

if aks_target.get_status() != "Succeeded":
    aks_target.wait_for_completion(show_output=True)


from azureml.core.webservice import AksWebservice
# Set the web service configuration (using default here)
aks_config = AksWebservice.deploy_configuration()

# # Enable token auth and disable (key) auth on the webservice
# aks_config = AksWebservice.deploy_configuration(token_auth_enabled=True, auth_enabled=False)

%%time
aks_service_name ='aks-service-1'

aks_service = local_service.deploy_to_cloud(name=aks_service_name,
                                            deployment_config=aks_config,
                                            deployment_target=aks_target)

aks_service.wait_for_deployment(show_output = True)
print(aks_service.state)

# Test aks service

sample_input = json.dumps({
    'data': dataset_x[0:2].tolist()
})

aks_service.run(sample_input)

# Delete the service if not needed.
aks_service.delete()
