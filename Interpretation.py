************************************************ Part I - generate explanations for models trained outside of Azure Machine Learning **************************************
from interpret.ext.blackbox import TabularExplainer

###################### "features" and "classes" fields are optional
tab_explainer = TabularExplainer(model,
                             X_train, 
                             features=features, 
                             classes=labels)
print(tab_explainer, "ready!")

************************************************************************************************ global importance
# you can use the training data or the test data here
global_tab_explanation = tab_explainer.explain_global(X_train)

# Get the top features by importance
global_tab_feature_importance = global_tab_explanation.get_feature_importance_dict()
for feature, importance in global_tab_feature_importance.items():
    print(feature,":", importance)
# The feature importance is ranked, with the most important feature listed first.

************************************************************************************************ local importance
# Get the observations we want to explain (the first two)
X_explain = X_test[0:2]

# Get predictions
predictions = model.predict(X_explain)

# Get local explanations
local_tab_explanation = tab_explainer.explain_local(X_explain)

# Get feature names and importance for each possible label
local_tab_features = local_tab_explanation.get_ranked_local_names()
local_tab_importance = local_tab_explanation.get_ranked_local_values()

for l in range(len(local_tab_features)):
    print('Support for', labels[l])
    label = local_tab_features[l]
    for o in range(len(label)):
        print("\tObservation", o + 1)
        feature_list = label[o]
        total_support = 0
        for f in range(len(feature_list)):
            print("\t\t", feature_list[f], ':', local_tab_importance[l][o][f])
            total_support += local_tab_importance[l][o][f]
        print("\t\t ----------\n\t\t Total:", total_support, "Prediction:", labels[predictions[o]])
        
****************************************************** Part II - Adding explainability to a model training experiment ********************************************
%%writefile $experiment_folder/diabetes_training.py
.....
.....
# calculate AUC
y_scores = model.predict_proba(X_test)
auc = roc_auc_score(y_test,y_scores[:,1])
run.log('AUC', np.float(auc))

os.makedirs('outputs', exist_ok=True)
# note file saved in the outputs folder is automatically uploaded into experiment record
joblib.dump(value=model, filename='outputs/diabetes.pkl')

# Get explanation
explainer = TabularExplainer(model, X_train, features=features, classes=labels)
explanation = explainer.explain_global(X_test)

# Get an Explanation Client and upload the explanation
explain_client = ExplanationClient.from_run(run)
explain_client.upload_model_explanation(explanation, comment='Tabular Explanation')

# Complete the run
run.complete()

# Now you can run the experiment. Note that the azureml-interpret library is included in the training environment 
# so the script can create a TabularExplainer and use the ExplainerClient class.

******************************************************************************** Part III - Retrieve the feature importance values ****************************************
from azureml.interpret import ExplanationClient

# Get the feature explanations
client = ExplanationClient.from_run(run)
engineered_explanations = client.download_model_explanation()
feature_importances = engineered_explanations.get_feature_importance_dict()

# Overall feature importance
print('Feature\tImportance')
for key, value in feature_importances.items():
    print(key, '\t', value)
    

