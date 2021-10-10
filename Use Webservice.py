##################################### (1) use python SDK
import json

# This time our input is an array of two feature arrays
x_new = [[2,180,74,24,21,23.9091702,1.488172308,22],
         [0,148,58,11,179,39.19207553,0.160829008,45]]

# Convert the array or arrays to a serializable list in a JSON document
input_json = json.dumps({"data": x_new})

# Call the web service, passing the input data
predictions = service.run(input_data = input_json)

# Get the predicted classes.
predicted_classes = json.loads(predictions)
   
for i in range(len(x_new)):
    print ("Patient {}".format(x_new[i]), predicted_classes[i] )
    
########################################### (2) make HTTP requests
import requests
import json

x_new = [[2,180,74,24,21,23.9091702,1.488172308,22],
         [0,148,58,11,179,39.19207553,0.160829008,45]]

# Convert the array to a serializable list in a JSON document
input_json = json.dumps({"data": x_new})

# Set the content type
headers = { 'Content-Type':'application/json' }

predictions = requests.post(endpoint, input_json, headers = headers)
predicted_classes = json.loads(predictions.json())

for i in range(len(x_new)):
    print ("Patient {}".format(x_new[i]), predicted_classes[i] )
    
##################################### REST request to include Authorization header
import requests
import json
from azureml.core import Webservice

service = Webservice(workspace=ws, name="myservice")
scoring_uri = service.scoring_uri

# If the service is authenticated, set the key or token
key, _ = service.get_keys()

# Set the appropriate headers
headers = {"Content-Type": "application/json"}
headers["Authorization"] = f"Bearer {key}"

# Make the request and display the response and logs
data = {
    "query": "What color is the fox",
    "context": "The quick brown fox jumped over the lazy dog.",
}
data = json.dumps(data)
resp = requests.post(scoring_uri, data=data, headers=headers)
print(resp.text)
