The following data can(/NOT) be collected:
(1) Model input data from web services deployed in an AKS cluster. Voice audio, images, and video are NOT collected.
(2) Model predictions using production input data.
# The output is saved in Blob storage. Because the data is added to Blob storage, you can choose your favorite tool to run the analysis.
***************************************************************Enable data collection***************************************************************
# 1. Open the scoring file.
# 2. Add the following code at the top of the file:
from azureml.monitoring import ModelDataCollector
# 3. Declare your data collection variables in your init function:
global inputs_dc, prediction_dc
inputs_dc = ModelDataCollector("best_model", designation="inputs", feature_names=["feat1", "feat2", "feat3", "feat4", "feat5", "feat6"])
prediction_dc = ModelDataCollector("best_model", designation="predictions", feature_names=["prediction1", "prediction2"])

# 4. Add the following lines of code to the run(input_df) function:
data = np.array(data)
result = model.predict(data)
inputs_dc.collect(data) #this call is saving our input data into Azure Blob
prediction_dc.collect(result) #this call is saving our prediction data into Azure Blob

# 5. Data collection is not automatically set to true when you deploy a service in AKS. Update your configuration file, as in the following example:
aks_config = AksWebservice.deploy_configuration(collect_model_data=True)
aks_config = AksWebservice.deploy_configuration(collect_model_data=True, enable_app_insights=True)

# 6. Add the 'Azure-Monitoring' pip package to the conda-dependencies of the web service environment:
env = Environment('webserviceenv')
env.python.conda_dependencies = CondaDependencies.create(conda_packages=['numpy'],pip_packages=['azureml-defaults','azureml-monitoring','inference-schema[numpy-support]'])

# 7. You can stop collecting data at any time. Use Python code to disable data collection.
## replace <service_name> with the name of the web service
<service_name>.update(collect_model_data=False)
