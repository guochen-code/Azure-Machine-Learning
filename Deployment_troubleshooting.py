# get deployed serivce
from azureml.core.webservice import AksWebservice
service = AksWebservice(name='name',workspace=ws)

# check its state
print(service.state) # to view the state of a service, must use compute-specific service type (AksWebservice) instead of a generic Webservice object.

# service logs
print(service.get_logs()) # if you need to make a change and redeploy, you may need to delete unhealthy service.

# delete service
try:
  service.delete()
except Exception as ex:
  print(ex)

# Enable Application Insights
service.update(enable_app_insights=True)
print('Appinsights enabled!')

# display services in ws:
for webservice_name in ws.webservices:
  print(webservice_name)

# check on runtime errors by deploying to a local container
from azureml.core.webservice import LocalWebservice
deployment_config=LocalWebservice.deploy_configration(port=8890)
service=Model.deploy(ws,service_name,[model],inference_config,deployment_config)
# you can test the locally deployed service using the SDK:
service.run(input_data=json_data)
# and troubleshoot runtime issues by making changes to the scoring file and reloading the service without redeploying (this can ONLY be done with a local service)
service.reload()
print(service.run(input_data=json_data))

  
************************************************************************************************************************
# After successfully training your ML model, you have successfully deployed it as a real-time service to an AKS inference environment. 
# During the live operation, you experience an error and your service crashes when you post data to the scoring endpoint.

# Solution: in your **DEV** environment, add an error catching statement to your run() function so that it returns a detailed error message.

# Including statements to return error messages from the run() function should only be used for debugging purposes. 
# For security and performance reasons, this should be avoided in a production environment. Try debugging errors in a local container environment.

def run(input_data):
    try:
        data = json.loads(input_data)['data']
        data = np.array(data)
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        # return error message back to the client
        return json.dumps({"error": result})
#
# Note: Returning error messages from the run(input_data) call should be done for debugging purpose only. 
# For security reasons, you should not return error messages this way in a production environment.
