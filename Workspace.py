# get workspace configuration
# use azure sdk to output the configuration given a workspace reference ws:
ws.write_config(path='./file_path', filename='config.json')

# Connection to Workspace
import azureml.core
from azureml.core import workspace
ws=Workspace.from_config()
print('Ready to use azure ml {} to work with {}'.format(azureml.core.VERSION,ws.name)

# connection to workspace
from azureml.core import Workspace
ws=Workspace(subscription_id='<subscription_id>',
             resource_group='<resource_group>',
             workspace_name='<workspace_name>')
