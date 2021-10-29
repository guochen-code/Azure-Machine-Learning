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

  
  

