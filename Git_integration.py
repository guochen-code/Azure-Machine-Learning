# Clone Git repositories into your workspace file system
# create a compute instance & open a terminal.
git clone https://github.com/Azure/MachineLearningNotebooks.git

# Authenticate your Git Account with SSH
************************* I. Generate a new SSH key
# (1) Open the terminal window in the Azure Machine Learning Notebook Tab.
# (2) Paste the text below, substituting in your email address.
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# This creates a new ssh key, using the provided email as a label.
> Generating public/private rsa key pair.
# (3) When you're prompted to "Enter a file in which to save the key" press Enter. This accepts the default file location.
# (4) Verify that the default location is '/home/azureuser/.ssh' and press enter. Otherwise specify the location '/home/azureuser/.ssh'
> Enter a file in which to save the key (/home/azureuser/.ssh/id_rsa): [Press enter]
# (5) At the prompt, type a secure passphrase. We recommend you add a passphrase to your SSH key for added security 
> Enter passphrase (empty for no passphrase): [Type a passphrase]
> Enter same passphrase again: [Type passphrase again]
*************************** II. Add the public key to Git Account
# (1) In your terminal window, copy the contents of your public key file. If you renamed the key, replace id_rsa.pub with the public key file name.
cat ~/.ssh/id_rsa.pub

********************************************************************************************************************************************************************
# Clone the Git repository with SSH
# (1) Copy the SSH Git clone URL from the Git repo.
# (2) Paste the url into the git clone command below, to use your SSH Git repo URL. This will look something like:
git clone git@example.com:GitUser/azureml-example.git
Cloning into 'azureml-example'...


********************************************************************************************************************************************************************
# Track code that comes from Git repositories
"properties": {
    "_azureml.ComputeTargetType": "batchai",
    "ContentSnapshotId": "5ca66406-cbac-4d7d-bc95-f5a51dd3e57e",
    "azureml.git.repository_uri": "git@github.com:azure/machinelearningnotebooks",
    "mlflow.source.git.repoURL": "git@github.com:azure/machinelearningnotebooks",
    "azureml.git.branch": "master",
    "mlflow.source.git.branch": "master",
    "azureml.git.commit": "4d2b93784676893f8e346d5f0b9fb894a9cf0742",
    "mlflow.source.git.commit": "4d2b93784676893f8e346d5f0b9fb894a9cf0742",
    "azureml.git.dirty": "True",
    "AzureML.DerivedImageName": "azureml/azureml_9d3568242c6bfef9631879915768deaf",
    "ProcessInfoFile": "azureml-logs/process_info.json",
    "ProcessStatusFile": "azureml-logs/process_status.json"
}
  
# the following code retrieves the commit hash:
run.properties['azureml.git.commit']
