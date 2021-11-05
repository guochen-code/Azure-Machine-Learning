# Generate feature importance values via remote runs
# The following example shows how you can use the ExplanationClient class to enable model interpretability for remote runs. 
# It is conceptually similar to the local process, except you:
# Use the ExplanationClient in the remote run to upload the interpretability context.
# Download the context later in a local environment.
pip install azureml-interpret

from azureml.interpret import ExplanationClient
from azureml.core.run import Run
from interpret.ext.blackbox import TabularExplainer

run = Run.get_context()
client = ExplanationClient.from_run(run)

# write code to get and split your data into train and test sets here
.......
.......
# write code to train your model here 
......
......

# explain predictions on your local machine
# "features" and "classes" fields are optional
explainer = TabularExplainer(model, 
                             x_train, 
                             features=feature_names, 
                             classes=classes)

# explain overall model predictions (global explanation)
global_explanation = explainer.explain_global(x_test)

# uploading global model explanation data for storage or visualization in webUX
# the explanation can then be downloaded on any compute
# multiple explanations can be uploaded
client.upload_model_explanation(global_explanation, comment='global explanation: all features')
# or you can only upload the explanation object with the top k feature info
#client.upload_model_explanation(global_explanation, top_k=2, comment='global explanation: Only top 2 features')


# Download the explanation in your local Jupyter Notebook.
from azureml.interpret import ExplanationClient

client = ExplanationClient.from_run(run)

# get model explanation data
explanation = client.download_model_explanation()
# or only get the top k (e.g., 4) most important features with their importance values
explanation = client.download_model_explanation(top_k=4)

global_importance_values = explanation.get_ranked_global_values()
global_importance_names = explanation.get_ranked_global_names()
print('global importance values: {}'.format(global_importance_values))
print('global importance names: {}'.format(global_importance_names))
