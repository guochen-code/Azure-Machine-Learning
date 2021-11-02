# (1) baseline dataset

# (2) create target dataset
from azureml.core import Workspace, Dataset, Datastore

# get workspace object
ws = Workspace.from_config()

# get datastore object 
dstore = Datastore.get(ws, 'your datastore name')

# specify datastore paths
dstore_paths = [(dstore, 'weather/*/*/*/*/data.parquet')]

# specify partition format
partition_format = 'weather/{state}/{date:yyyy/MM/dd}/data.parquet'

# create the Tabular dataset with 'state' and 'date' as virtual columns 
dset = Dataset.Tabular.from_parquet_files(path=dstore_paths, partition_format=partition_format)

# assign the timestamp attribute to a real or virtual column in the dataset
dset = dset.with_timestamp_columns('date')

# register the dataset as the target dataset
dset = dset.register(ws, 'target')

# (3) create data drift monitor
from azureml.core import Workspace, Dataset
from azureml.datadrift import DataDriftDetector
from datetime import datetime

# get the workspace object
ws = Workspace.from_config()

# get the target dataset
target = Dataset.get_by_name(ws, 'target')

# set the baseline dataset
baseline = target.time_before(datetime(2019, 2, 1))

# set up feature list
features = ['latitude', 'longitude', 'elevation', 'windAngle', 'windSpeed', 'temperature', 'snowDepth', 'stationName', 'countryOrRegion']

# set up data drift detector
monitor = DataDriftDetector.create_from_datasets(ws, 'drift-monitor', baseline, target, 
                                                      compute_target='cpu-cluster', 
                                                      frequency='Week', 
                                                      feature_list=None, 
                                                      drift_threshold=.6, 
                                                      latency=24)

# get data drift detector by name
monitor = DataDriftDetector.get_by_name(ws, 'drift-monitor')

# update data drift detector
monitor = monitor.update(feature_list=features)

# run a backfill for January through May
backfill1 = monitor.backfill(datetime(2019, 1, 1), datetime(2019, 5, 1))

# run a backfill for May through today
backfill1 = monitor.backfill(datetime(2019, 5, 1), datetime.today())

# disable the pipeline schedule for the data drift detector
monitor = monitor.disable_schedule()

# enable the pipeline schedule for the data drift detector
monitor = monitor.enable_schedule()
***************************
from azureml.widgets import RunDetails

backfill = monitor.backfill(dt.datetime.now() - dt.timedelta(weeks=6), dt.datetime.now())

RunDetails(backfill).show()
backfill.wait_for_completion()

drift_metrics = backfill.get_metrics()
for metric in drift_metrics:
    print(metric, drift_metrics[metric])

**************************************************************************understanding data drift results******************************************************
# Metrics:
(1) Data drift magnitude
(2) Top drifting features: Shows the features from the dataset that have drifted the most and are therefore contributing the most to the Drift Magnitude metric.
  2.1 - Numeric features: Wasserstein distance/mean/min/max
  2.2 - Categorical features: Euclidian distance/Unique values
(3) Threshold: Data Drift magnitude beyond the set threshold will trigger alerts. This can be configured in the monitor settings.

*********************************************************************************Trouleshooting********************************************************************
# If the SDK backfill() function does not generate the expected output, it may be due to an authentication issue. 
# When you create the compute to pass into this function, do not use Run.get_context().experiment.workspace.compute_targets. 
# Instead, use ServicePrincipalAuthentication such as the following to create the compute that you pass into that backfill() function:
auth = ServicePrincipalAuthentication(
        tenant_id=tenant_id,
        service_principal_id=app_id,
        service_principal_password=client_secret
        )
ws = Workspace.get("xxx", auth=auth, subscription_id="xxx", resource_group="xxx")
compute = ws.compute_targets.get("xxx")
