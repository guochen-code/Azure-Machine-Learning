'''
1. Remove all nonessential code : Removing nonessential code will also make the code more maintainable. 
2. Refactor code into functions: Refactoring code into functions makes unit testing easier and makes the code more maintainable. 
3. Combine related functions in Python files: related functions need to be merged into Python files to better help code reuse.
4. Create unit tests for each Python file: Unit tests protect code against functional regressions and make it easier to maintain. 
  A unit test usually contains three main actions:
    Arrange object - creating and setting up necessary objects
    Act on an object
    Assert what is expected
 '''
import numpy as np
from code.training.train import train_model


def test_train_model():
    # Arrange
    X_train = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
    y_train = np.array([10, 9, 8, 8, 6, 5])
    data = {"train": {"X": X_train, "y": y_train}}

    # Act
    reg_model = train_model(data, {"alpha": 1.2})

    # Assert
    preds = reg_model.predict([[1], [2]])
    np.testing.assert_almost_equal(preds, [9.93939393939394, 9.03030303030303])
    

# At this stage, there should be no code remaining in the notebook that isn't in a function, other than import statements in the first cell.
# Add a statement that calls the main function.
# After refactoring, experimentation/Diabetes Ridge Regression Training.ipynb should look like the following code without the markdown:

from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib


# Split the dataframe into test and train data
def split_data(df):
    X = df.drop('Y', axis=1).values
    y = df['Y'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0)
    data = {"train": {"X": X_train, "y": y_train},
            "test": {"X": X_test, "y": y_test}}
    return data


# Train the model, return the model
def train_model(data, args):
    reg_model = Ridge(**args)
    reg_model.fit(data["train"]["X"], data["train"]["y"])
    return reg_model


# Evaluate the metrics for the model
def get_model_metrics(reg_model, data):
    preds = reg_model.predict(data["test"]["X"])
    mse = mean_squared_error(preds, data["test"]["y"])
    metrics = {"mse": mse}
    return metrics


def main():
    # Load Data
    sample_data = load_diabetes()

    df = pd.DataFrame(
        data=sample_data.data,
        columns=sample_data.feature_names)
    df['Y'] = sample_data.target

    # Split Data into Training and Validation Sets
    data = split_data(df)

    # Train Model on Training Set
    args = {
        "alpha": 0.5
    }
    reg = train_model(data, args)

    # Validate Model on Validation Set
    metrics = get_model_metrics(reg, data)

    # Save Model
    model_name = "sklearn_regression_model.pkl"

    joblib.dump(value=reg, filename=model_name)

main()

***************************************************************
# After refactoring, experimentation/Diabetes Ridge Regression Scoring.ipynb should look like the following code without the markdown:
import json
import numpy
from azureml.core.model import Model
import joblib

def init():
    model_path = Model.get_model_path(
        model_name="sklearn_regression_model.pkl")
    model = joblib.load(model_path)

def run(raw_data, request_headers):
    data = json.loads(raw_data)["data"]
    data = numpy.array(data)
    result = model.predict(data)

    return {"result": result.tolist()}

init()
test_row = '{"data":[[1,2,3,4,5,6,7,8,9,10],[10,9,8,7,6,5,4,3,2,1]]}'
request_header = {}
prediction = run(test_row, {})
print("Test result: ", prediction)

********************************************* Combine related functions in Python files *********************************************
# Convert your notebook to an executable script by running the following statement in a command prompt, 
# which uses the nbconvert package and the path of experimentation/Diabetes Ridge Regression Training.ipynb:
jupyter nbconvert "Diabetes Ridge Regression Training.ipynb" --to script --output train

# Once the notebook has been converted to train.py, remove any unwanted comments. 
# Replace the call to main() at the end of the file with a conditional invocation like the following code:
if __name__ == '__main__':
    main()
# train.py can now be invoked from a terminal by running python train.py. The functions from train.py can also be called from other files.

#convert for scoring
jupyter nbconvert "Diabetes Ridge Regression Scoring.ipynb" --to script --output score
# The model variable needs to be global so that it's visible throughout the script. Add the following statement at the beginning of the init function:
def init():
    global model

    # load the model from file into a global object
    model_path = Model.get_model_path(
        model_name="sklearn_regression_model.pkl")
    model = joblib.load(model_path)
#
