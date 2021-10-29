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
                     
