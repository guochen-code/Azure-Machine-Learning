pass compute_target into ScriptRunStep:
(1) using name: compute_target = compute_name
(2) using ComputeTarget Object: compute_target = training_cluster

********************************************************************************* Part I *********************************************************************************
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

cluster_name = "your-compute-cluster"

try:
    # Check for existing compute target
    training_cluster = ComputeTarget(workspace=ws, name=cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    # If it doesn't already exist, create it
    try:
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2', min_nodes=0,max_nodes=2, 
                                                               vm_priority='dedicaetd/low priority', idle_seconds_before_scaledown=1800)
        training_cluster = ComputeTarget.create(ws, cluster_name, compute_config)
        training_cluster.wait_for_completion(show_output=True)
    except Exception as ex:
        print(ex)

  *********************************************************************************
# For a more detailed view of current Azure Machine Learning Compute status, use get_status()
training_cluster.get_status().serialize()

********************************************************************************* Part II *********************************************************************************
from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, DatabricksCompute
ws=Workspace.from_config()
compute_name='db_cluster
db_workspace_name='db_workspace'
db_resource_group='db_resource_group'
db_access_token='1234-abc-5678-defg-90...'
db_config=DatabricksCompute.attach_configuration(resource_group=db_resource_group,
                                                 workspace_name=db_workspace_name,
                                                 access_token=db_access_token)
databricks_compute=ComputeTarget.attach(ws,compute_name,db_config)
databricks_compute.wait_for_completion(True)
