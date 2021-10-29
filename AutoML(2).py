# retrive the best model:
best_run, fitted_model=automl_run.get_output()
y_predict=fitted_model.predict(X_test.values)

best_run_metrics=best_run.get_metrics()
for metric_name in best_run_metrics:
  metric=best_run_metrics[metric_name]
  print(metric_name, metric)

# Exploring preprocessing steps. View those steps in the fitted_model obtaind from the best run:
for step in fitted_model.named_steps:
  print(step)

# 
  
