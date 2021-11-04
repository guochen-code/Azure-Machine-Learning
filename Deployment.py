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

******************************** Model Profiling ****************************************************************
Model Profiling

# Profile your model to understand how much CPU and memory the service, created as a result of its deployment, will need. 
# Profiling returns information such as CPU usage, memory usage, and response latency. 
# It also provides a CPU and memory recommendation based on the resource usage. 
# You can profile your model (or more precisely the service built based on your model) on any CPU and/or memory combination 
# where 0.1 <= CPU <= 3.5 and 0.1GB <= memory <= 15GB. If you do not provide a CPU and/or memory requirement, 
# we will test it on the default configuration of 3.5 CPU and 15GB memory.

# In order to profile your model you will need:

(1) a registered model
(2) an entry script
(3) an inference configuration
(4) a single column tabular dataset, where each row contains a string representing sample request data sent to the service.
# Please, note that profiling is a long running operation and can take up to 25 minutes depending on the size of the dataset.

# At this point we only support profiling of services that expect their request data to be a string, for example: string serialized json, text, string serialized image, etc. 
# The content of each row of the dataset (string) will be put into the body of the HTTP request and sent to the service encapsulating the model for scoring.

# Below is an example of how you can construct an input dataset to profile a service which expects its incoming requests to contain serialized json. 
# In this case we created a dataset based one hundred instances of the same request data. In real world scenarios however, 
# we suggest that you use larger datasets with various inputs, especially if your model resource usage/behavior is input dependent.

# You may want to register datasets using the register() method to your workspace so they can be shared with others, reused and referred to by name in your script. 
# You can try get the dataset first to see if it's already registered.
profile = Model.profile(ws, "profilename", [model], inference_config, test_sample)
profile.wait_for_profiling(True)
profiling_results = profile.get_results()
print(profiling_results)


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Example
from azureml.core import Datastore
from azureml.core.dataset import Dataset
from azureml.data import dataset_type_definitions

dataset_name='diabetes_sample_request_data'

dataset_registered = False
try:
    sample_request_data = Dataset.get_by_name(workspace = ws, name = dataset_name)
    dataset_registered = True
except:
    print("The dataset {} is not registered in workspace yet.".format(dataset_name))

if not dataset_registered:
    # create a string that can be utf-8 encoded and
    # put in the body of the request
    serialized_input_json = json.dumps({
        'data': [
            [ 0.03807591,  0.05068012,  0.06169621, 0.02187235, -0.0442235,
            -0.03482076, -0.04340085, -0.00259226, 0.01990842, -0.01764613]
        ]
    })
    dataset_content = []
    for i in range(100):
        dataset_content.append(serialized_input_json)
    dataset_content = '\n'.join(dataset_content)
    file_name = "{}.txt".format(dataset_name)
    f = open(file_name, 'w')
    f.write(dataset_content)
    f.close()

    # upload the txt file created above to the Datastore and create a dataset from it
    data_store = Datastore.get_default(ws)
    data_store.upload_files(['./' + file_name], target_path='sample_request_data')
    datastore_path = [(data_store, 'sample_request_data' +'/' + file_name)]
    sample_request_data = Dataset.Tabular.from_delimited_files(
        datastore_path,
        separator='\n',
        infer_column_types=True,
        header=dataset_type_definitions.PromoteHeadersBehavior.NO_HEADERS)
    sample_request_data = sample_request_data.register(workspace=ws,
                                                    name=dataset_name,
                                                    create_new_version=True)
    
# Now that we have an input dataset we are ready to go ahead with profiling. 
# In this case we are testing the previously introduced sklearn regression model on 1 CPU and 0.5 GB memory. 
# The memory usage and recommendation presented in the result is measured in Gigabytes. The CPU usage and recommendation is measured in CPU cores.    
from datetime import datetime
environment = Environment('my-sklearn-environment')
environment.python.conda_dependencies = CondaDependencies.create(pip_packages=[
    'azureml-defaults',
    'inference-schema[numpy-support]',
    'joblib',
    'numpy',
    'scikit-learn=={}'.format(sklearn.__version__)
])
inference_config = InferenceConfig(entry_script='score.py', environment=environment)
# if cpu and memory_in_gb parameters are not provided
# the model will be profiled on default configuration of
# 3.5CPU and 15GB memory
profile = Model.profile(ws,
            'rgrsn-%s' % datetime.now().strftime('%m%d%Y-%H%M%S'),
            [model],
            inference_config,
            input_dataset=sample_request_data,
            cpu=1.0,
            memory_in_gb=0.5)

# profiling is a long running operation and may take up to 25 min
profile.wait_for_completion(True)
details = profile.get_details()
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

******************************** Model packaging ****************************************************************

# If you want to build a Docker image that encapsulates your model and its dependencies, you can use the model packaging option. 
# The output image will be pushed to your workspace's ACR.

# You must include an Environment object in your inference configuration to use Model.package().

package = Model.package(ws, [model], inference_config)
package.wait_for_creation(show_output=True)  # Or show_output=False to hide the Docker build logs.
package.pull()

# Instead of a fully-built image, you can also generate a Dockerfile and download all the assets needed to build an image on top of your Environment.

package = Model.package(ws, [model], inference_config, generate_dockerfile=True)
package.wait_for_creation(show_output=True)
package.save("./local_context_dir")
