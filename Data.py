from azureml.core import Dataset

default_ds = ws.get_default_datastore()

if 'diabetes dataset' not in ws.datasets:
    default_ds.upload_files(files=['./data/diabetes.csv', './data/diabetes2.csv'], # Upload the diabetes csv files in /data
                        target_path='diabetes-data/', # Put it in a folder path in the datastore
                        overwrite=True, # Replace existing files of the same name
                        show_progress=True)

    #Create a tabular dataset from the path on the datastore (this may take a short while)
    tab_data_set = Dataset.Tabular.from_delimited_files(path=(default_ds, 'diabetes-data/*.csv'))

    # Register the tabular dataset
    try:
        tab_data_set = tab_data_set.register(workspace=ws, 
                                name='diabetes dataset',
                                description='diabetes data',
                                tags = {'format':'CSV'},
                                create_new_version=True)
        print('Dataset registered.')
    except Exception as ex:
        print(ex)
else:
    print('Dataset already registered.')

    
******************************************************************
img_paths=[(blob_ds,'data/files/images/*.jpg),(blob_ds,'data/file/images/*.png)]
file_ds=Dataset.File.from_files(path=img_paths)
file_ds=file_ds.register(workspace=ws, name='img_files', create_new_version=True)

img_ds=Dataset.get_by_name(workspace=ws, name='img_files', version=2)

************************************************************************************************************************************
for file_path in files_ds.to_path():
    print(file_path)
    
************************************************************************************************************************************
when passing file dataset, you must specify the acces mode:
estimator=Estimator(...,
                    inputs=[img_ds.as_named_input('img_data').as_download(path_on_compute='data')],
                    ....)
            
