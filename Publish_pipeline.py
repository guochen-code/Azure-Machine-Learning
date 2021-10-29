(1) after you have created a pipeline, you can publish it and run it on demand.
published_pipeline=pipeline.publish(name='pipeline_name',description='description',version='1.0')

(2) publish pipeline from a submitted PipelineRun
# get the most recent run of the pipeline
experiment_name='name',
pipeline_experiment=ws.experiment.get(experiment_name)
pipeline_run=list(pipeline_experiment.get_runs())[0]
published_pipeline=pipeline_run.publish_pipeline(name='name',description='description',version='1.0')

rest_endpoint = published_pipeline.endpoint
print(rest_endpoint)

# get all published pipeline
all_pub_pipelines = PublishPipeline.get_all(ws)

# get a published pipeline via id
from azureml.pipeline.core import PublishedPipeline
pipeline_id=published_pipeline.id
published_pipeline = PublishedPipeline.get(ws, pipeline_id)

******************************************************************** Schedule ********************************************************************
rom azureml.pipeline.core import ScheduleRecurrence, Schedule

# Submit the Pipeline every Monday at 00:00 UTC
recurrence = ScheduleRecurrence(frequency="Week", interval=1, week_days=["Monday"], time_of_day="00:00")
weekly_schedule = Schedule.create(ws, name="weekly-diabetes-training", 
                                  description="Based on time",
                                  pipeline_id=published_pipeline.id, 
                                  experiment_name='mslearn-diabetes-pipeline', 
                                  recurrence=recurrence)
print('Pipeline scheduled.')
******************************************************************** Triggering a pipeline run on data changes ************************************************
you can monitor a specified path on a datastore. This will become a trigger for a new run.

from azureml.core import Datastore
from azureml.pipeline.core import schedule

training_datastore=Datastore(workspace=ws,name='blob_data')
pipeline_schedule=Schedule.create(ws, name='Reactive Training', 
                                  description='trains model on data change',
                                  pipeline_id=published_pipeline_id,
                                  experiment_name='Training_Pipeline',
                                  datastore=training_datastore,
                                  path_on_datastore='data/training')
                                  
                             
