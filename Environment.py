# (1) create from a .yml file
env=Environment.from_conda_specification('experiment_env','environment.yml')

# register environment
env.register(workspace=ws)
# get resigstered environment
registered_env=Environment.get(ws,'experiment_env)
# display registered environment
envs=Environment.List(workspace=ws)
for env in envs:
  print('Name',env)
                              
# (2) via python packages
service_env=Environment(name='service_env')
python_packages=['scikit-learn','azureml-defaults','azure-ml-api-sdk']
for package in packages:
  service_env.python.conda_dependencies.add_pip_package(package)
                         
                               
******************************************************************* Specify conda dependencies and a base docker image through a RunConfiguration
# Use a RunConfiguration to specify some additional requirements for this step.
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE

# create a new runconfig object
run_config = RunConfiguration()

# enable Docker 
run_config.environment.docker.enabled = True

# set Docker base image to the default CPU-based image
run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE

# use conda_dependencies.yml to create a conda environment in the Docker image for execution
run_config.environment.python.user_managed_dependencies = False

# specify CondaDependencies obj
run_config.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['scikit-learn'])

# For this step, we use yet another source_directory
source_directory = './extract'
print('Source directory for the step is {}.'.format(os.path.realpath(source_directory)))

step = PythonScriptStep(name="extract_step",
                         script_name="extract.py", 
                         compute_target=aml_compute, 
                         source_directory=source_directory,
                         runconfig=run_config)
