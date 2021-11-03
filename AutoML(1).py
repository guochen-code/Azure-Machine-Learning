import azureml.train.automl.utilities as automl_utils

for metric in automl_utils.get_primary_metrics('classification'):
    print(metric)
    
    
    
# Split the dataset into training and validation subsets
diabetes_ds = ws.datasets.get("diabetes dataset")
train_ds, test_ds = diabetes_ds.random_split(percentage=0.7, seed=123)
print("Data ready!")



from azureml.train.automl import AutoMLConfig

automl_config = AutoMLConfig(name='Automated ML Experiment',
                             task='classification',
                             compute_target=training_cluster,
                             training_data = train_ds,
                             validation_data = test_ds, # validation_size = 0.2/ n_cross_validations = 5/ n_cross_validations = 7 & validation_size = 0.2/
                             label_column_name='Diabetic',
                             iterations=4, ##The total number of different algorithm and parameter combinations to test during an automated ML experiment, default 1000 iterations.
                             primary_metric = 'AUC_weighted',
                             max_concurrent_iterations=2,
                             featurization='auto'
                             )

print("Ready for Auto ML run.")

****************************************************************************** !!! *********************************************************************************************
'''
ONLY connect to local data files or azure blob storage.
ONLY accepts azure ml TabularDatasets when working on a remote compute.
Train,validation, and test:
>20,000: 10%
<20,000:
  <1,000: 10 folds
  1,000-20,000: 3 folds

If you are using ONNX models, or have model-explanability enabled, stacking is disabled and ONLY voting is utilized.
'''
**************************************************************************** !!! ***********************************************************************************************
''' 
featurization = 'auto'/'off'/'FeaturizationConfig'

******************* auto
automatic featurization includes data guardrails and featurizatoin steps to be done automatically. This setting is the default.

featurization steps include:
1) drop high cardinality or no variance features (like IDs)
2) impute missing values (average value for numeric and most frequent value to categorical features)
3) Generate more features (for DateTime features: Year, Month, Day, Day of week, Day of year, Quarter, Week of year, Hour, Minute, Second)
4) Transform and encode (transform numeric features that have few unique values into categorical features; one-hot encoding for low cardinalty & one-hot-hash encoding for high cardinality)
5) word embeddings (a text featurizer coverts vectors of text tokens in to sentence vectors by using a pre-trained model)
6) cluster distance (trains a k-means clustering model on all numeric columns. Produce k new features that contain the distance of each sample to the centroid of each cluster, one new numeric feature per cluster)

data guardrails: help you identify potential issues with your data (missing values or class imbalance). They also help you take corrective actions for improved results.
data guardrails are applied:
for SDK experiments when the parameters 'featurizatoin':'auto' or validation = auto are specified in your AutoMLConfig object.
for studio experiments when automatic featurization is enabled.
1) missing feature values imputation:
  passed: no missing values detected.
  Done: detected and imputed.
2) high cardinality feature handling:
  passed: no high-cardinalty features detected.
  Done: detected and handled.
3) validation split handling:
  Done: <20,000 rows - cross-validation / >20,000 rows - train-validatoin-split
4) class balancing detection:
  passed: all classes are balanced.
  Alerted: imbalanced classes were detected. To fix model bias, fix the balancing problem.
  Done: Imbalanced classes were detected and the sweeping logic has determined to apply balancing.
5) memory issues detection:
  Passed: no potential out-of-memory issues detected.
  Done: analyzed and will potentially cause your experiment to run out of memory. The lag or rolling-window configurations have been turned off.
6) Frequency detection:
  Passed: time series was analyzed and all data points aligned with the detected frequency.
  Done: time series analyzed, data points do not aligh with detected frequency. These data points were removed from dataset.

*******************customize featurization
1) column purpose update (override the autodetected feature type for the specified column)
2) transformer parameter update (update parameters for specified transformer. supports imputer:mean/most frequent/median and HashOneHotEncoder.)
3) Drop columns (specifies columns to drip from being featurized. deprecated as of SDK version 1.19)
4) block transformers (specifies block transformer to be used in the featurizatoin process)'''

featurization_config = FeaturizationConfig()
featurization_config.blocked_transformers = ['LabelEncoder']
featurization_config.drop_columns = ['aspiration', 'stroke']
featurization_config.add_column_purpose('engine-size', 'Numeric')
featurization_config.add_column_purpose('body-style', 'CategoricalHash')
#default strategy mean, add transformer param for for 3 columns
featurization_config.add_transformer_params('Imputer', ['engine-size'], {"strategy": "median"})
featurization_config.add_transformer_params('Imputer', ['city-mpg'], {"strategy": "median"})
featurization_config.add_transformer_params('Imputer', ['bore'], {"strategy": "most_frequent"})
featurization_config.add_transformer_params('HashOneHotEncoder', [], {"number_of_bits": 3})
