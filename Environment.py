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
