from azureml.core import Datastore, Dataset
import pandas as pd
import os

# Set default data store
ws.set_default_datastore('workspaceblobstore')
default_ds = ws.get_default_datastore()

# Enumerate all datastores, indicating which is the default
for ds_name in ws.datastores:
    print(ds_name, "- Default =", ds_name == default_ds.name)

# Load the diabetes data
diabetes = pd.read_csv('data/diabetes2.csv')
# Get a 100-item sample of the feature columns (not the diabetic label)
sample = diabetes[['Pregnancies','PlasmaGlucose','DiastolicBloodPressure','TricepsThickness','SerumInsulin','BMI','DiabetesPedigree','Age']].sample(n=100).values

# Create a folder
batch_folder = './batch-data'
os.makedirs(batch_folder, exist_ok=True)
print("Folder created!")

# Save each sample as a separate file
print("Saving files...")
for i in range(100):
    fname = str(i+1) + '.csv'
    sample[i].tofile(os.path.join(batch_folder, fname), sep=",")
print("files saved!")

# Upload the files to the default datastore
print("Uploading files to datastore...")
default_ds = ws.get_default_datastore()
default_ds.upload(src_dir="batch-data", target_path="batch-data", overwrite=True, show_progress=True)

# Register a dataset for the input data
batch_data_set = Dataset.File.from_files(path=(default_ds, 'batch-data/'), validate=False)
try:
    batch_data_set = batch_data_set.register(workspace=ws, 
                                             name='batch-data',
                                             description='batch data',
                                             create_new_version=True)
except Exception as ex:
    print(ex)

print("Done!")
