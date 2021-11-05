# log_row vs log_list:
# log_row:
Log a row with 2 numerical columns repeatedly 
- run.log_row(name='Cosine Wave', angle=angle, cos=np.cos(angle)) sines['angle'].append(angle) sines['sine'].append(np.sin(angle))
- Two-variable line chart
    
# log_list:    
Log an array of numeric values 
- run.log_list(name='Fibonacci', value=[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]) 
- single-variable line chart
    

********************************************************************************************************************************************************
# Create an Azure ML experiment in your workspace
experiment = Experiment(workspace=ws, name="mslearn-diabetes")

# Start logging data from the experiment, obtaining a reference to the experiment run
run = experiment.start_logging()
print("Starting experiment:", experiment.name)

# load the data from a local file
data = pd.read_csv('data/diabetes.csv')

# Count the rows and log the result
row_count = (len(data))
run.log('observations', row_count)
print('Analyzing {} rows of data'.format(row_count))

# Plot and log the count of diabetic vs non-diabetic patients
diabetic_counts = data['Diabetic'].value_counts()
fig = plt.figure(figsize=(6,6))
ax = fig.gca()    
diabetic_counts.plot.bar(ax = ax) 
ax.set_title('Patients with Diabetes') 
ax.set_xlabel('Diagnosis') 
ax.set_ylabel('Patients')
plt.show()
run.log_image(name='label distribution', plot=fig)

# log distinct pregnancy counts
pregnancies = data.Pregnancies.unique()
run.log_list('pregnancy categories', pregnancies)

# Log summary statistics for numeric columns
med_columns = ['PlasmaGlucose', 'DiastolicBloodPressure', 'TricepsThickness', 'SerumInsulin', 'BMI']
summary_stats = data[med_columns].describe().to_dict()
for col in summary_stats:
    keys = list(summary_stats[col].keys())
    values = list(summary_stats[col].values())
    for index in range(len(keys)):
        run.log_row(col, stat=keys[index], value = values[index])

# Save a sample of the data and upload it to the experiment output
data.sample(100).to_csv('sample.csv', index=False, header=True)
run.upload_file(name='outputs/sample.csv', path_or_stream='./sample.csv')

# Complete the run
run.complete()        

************************************************************************************
logging vectors: log_list or repeatly log value
logging tables: log_table from a dictionary of lists where each list represents a column in the table or repeatly log log_row
# Vectors are good for recording information such as loss curves. You can log a vector by creating a list of numbers, calling log_list() and supplying a name and the list, 
# or by repeatedly logging a value using the same name.
************************************************************************************ log file
# Note: vectors logged into the run are expected to be relatively small. Logging very large vectors into Azure ML can result in reduced performance. 
# If you need to store large amounts of data associated with the run, you can write the data to file that will be uploaded.
# Note: tables logged into the run are expected to be relatively small. Logging very large tables into Azure ML can result in reduced performance. 
# If you need to store large amounts of data associated with the run, you can write the data to file that will be uploaded.
import os
directory = 'logging-api'

if not os.path.exists(directory):
    os.mkdir(directory)

file_name = os.path.join(directory, "myfile.txt")

with open(file_name, "w") as f:
    f.write('This is an output file that will be uploaded.\n')

# Upload the file explicitly into artifacts 
run.upload_file(name = file_name, path_or_stream = file_name)
************************************************************************************ Analyze results
# You can refresh the run in the Azure portal to see all of your results. 
# In many cases you will want to analyze runs that were performed previously to inspect the contents or compare results. 
# Runs can be fetched from their parent Experiment object using the Run() constructor or the experiment.get_runs() method.
fetched_run = Run(experiment, run_id)
fetched_run

# Call run.get_metrics() to retrieve all the metrics from a run.
# Call run.get_metrics(name = <metric name>) to retrieve a metric value by name. Retrieving a single metric can be faster, especially if the run contains many metrics.
# See the files uploaded for this run by calling run.get_file_names()
# Once you know the file names in a run, you can download the files using the run.download_file() method
import os
os.makedirs('files', exist_ok=True)

for f in run.get_file_names():
    dest = os.path.join('files', f.split('/')[-1])
    print('Downloading file {} to {}...'.format(f, dest))
    fetched_run.download_file(f, dest)   
#
# Often when you analyze the results of a run, you may need to tag that run with important personal or external information. 
# You can add a tag to a run using the run.tag() method. AzureML supports valueless and valued tags.
fetched_run.tag("My Favorite Run")
fetched_run.tag("Competition Rank", 1)

fetched_run.get_tags()
