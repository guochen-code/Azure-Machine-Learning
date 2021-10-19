This schedule will run when additions or modifications are made to Blobs in the Datastore. 
By default, the Datastore container is monitored for changes. 
Use the path_on_datastore parameter to instead specify a path on the Datastore to monitor for changes. 
Note: the path_on_datastore will be under the container for the datastore, so the actual path monitored will be container/path_on_datastore. 
Changes made to subfolders in the container/path will not trigger the schedule. 
Note: Only Blob Datastores are supported. Note: Not supported for CMK workspaces. 
Please review these instructions in order to setup a blob trigger submission schedule with CMK enabled. 
Also see those instructions to bring your own LogicApp to avoid the schedule triggers per month limit.

from azureml.core.datastore import Datastore

datastore = Datastore(workspace=ws, name="workspaceblobstore")

schedule = Schedule.create(workspace=ws, name="My_Schedule",
                           pipeline_id=pub_pipeline_id, 
                           experiment_name='Schedule-run-sample',
                           datastore=datastore,
                           wait_for_provisioning=True,
                           description="Schedule Run")
                          #polling_interval=5, use polling_interval to specify how often to poll for blob additions/modifications. Default value is 5 minutes.
                          #path_on_datastore="file/path") use path_on_datastore to specify a specific folder to monitor for changes.

# You may want to make sure that the schedule is provisioned properly
# before making any further changes to the schedule

print("Created schedule with id: {}".format(schedule.id))


# Set the wait_for_provisioning flag to False if you do not want to wait  
# for the call to provision the schedule in the backend.
schedule.disable(wait_for_provisioning=True)
schedule = Schedule.get(ws, schedule_id)
print("Disabled schedule {}. New status is: {}".format(schedule.id, schedule.status))
