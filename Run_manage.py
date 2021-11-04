run.get_status()
run.get_details()
run.get_details_with_logs()

# properties ---- immutable
run.add_properties({"author":"azureml-user"})
print(run.get_properties())

# tags ---- mutable
local_script_run.tag("quality", "great run")
print(run.get_tags())
# You can also add a simple string tag. It appears in the tag dictionary with value of None
list(exp.get_runs(properties={"author":"azureml-user"},tags="worth another look"))

# Query properties and tags
list(exp.get_runs(properties={"author":"azureml-user"},tags={"quality":"fantastic run"}))
list(exp.get_runs(properties={"author":"azureml-user"},tags="worth another look"))

# You can also mark an unsuccessful run as failed.
local_script_run = exp.submit(run_config)
local_script_run.fail()
print(local_script_run.get_status())

# Reproduce a run

# When updating or troubleshooting on a model deployed to production, you sometimes need to revisit the original training run that produced the model. 
# To help you with this, Azure ML service by default creates snapshots of your scripts a the time of run submission:

# You can use restore_snapshot to obtain a zip package of the latest snapshot of the script folder.
local_script_run.restore_snapshot(path="snapshots")
# You can then extract the zip package, examine the code, and submit your run again.
