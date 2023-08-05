import os
import shutil

from pureml.utils.constants import (
    API_IP_DOCKER,
    PATH_FASTAPI_FILE,
    PATH_PREDICT,
    PATH_PREDICT_DIR,
    PATH_PREDICT_REQUIREMENTS,
    PATH_PREDICT_REQUIREMENTS_USER,
    PATH_PREDICT_USER,
    PATH_USER_PROJECT,
    PORT_FASTAPI,
)
from pureml.utils.deploy import process_input, process_output


# def get_project_file():
#     os.makedirs(PATH_PREDICT_DIR, exist_ok=True)

#     project_dir_name = PATH_USER_PROJECT.split(os.path.sep)[-2]
#     predict_project_dir = os.path.join(PATH_PREDICT_DIR, project_dir_name)

#     os.makedirs(predict_project_dir, exist_ok=True)

#     project_file_name = PATH_USER_PROJECT.split(os.path.sep)[-1]
#     predict_project_file_name = os.path.join(predict_project_dir, project_file_name)

#     shutil.copy(PATH_USER_PROJECT, predict_project_file_name)


def get_predict_file(predict_path):

    os.makedirs(PATH_PREDICT_DIR, exist_ok=True)

    if predict_path is None:
        predict_path = PATH_PREDICT_USER
        print("Taking the default predict.py file path: ", predict_path)
    else:
        print("Taking the predict.py file path: ", predict_path)

    if os.path.exists(predict_path):
        shutil.copy(predict_path, PATH_PREDICT)
    else:
        raise Exception(predict_path, "doesnot exists!!!")


def get_requirements_file(requirements_path):

    os.makedirs(PATH_PREDICT_DIR, exist_ok=True)

    if requirements_path is None:
        requirements_path = PATH_PREDICT_REQUIREMENTS_USER
        print("Taking the default requirements.txt file path: ", requirements_path)
    else:
        print("Taking the requirements.txt file path: ", requirements_path)

    if os.path.exists(requirements_path):
        shutil.copy(requirements_path, PATH_PREDICT_REQUIREMENTS)
    else:
        raise Exception(requirements_path, "doesnot exists!!!")


def generate_file_upload_api(
    model_name, model_branch, model_version, input_type, input_shape, output_type, output_shape
):

    query = """
from fastapi import FastAPI, Depends, Request, UploadFile
import uvicorn
import pureml
from predict import model_predict
import os
from dotenv import load_dotenv
import json
import shutil
from pureml.utils.deploy import parse_input, parse_output
from typing import Union

load_dotenv()

org_id = os.getenv('ORG_ID')
access_token = os.getenv('ACCESS_TOKEN')

pureml.login(org_id=org_id, access_token=access_token)

model = pureml.model.fetch('{MODEL_NAME}', '{MODEL_BRANCH}', '{MODEL_VERSION}')

# Create the app
app = FastAPI()     

@app.post('/predict')
async def predict(file: Union[UploadFile, None] = None):
    input_type = '{INPUT_TYPE}'
    input_shape = '{INPUT_SHAPE}'
    output_type = '{OUTPUT_TYPE}'
    output_shape = '{OUTPUT_SHAPE}'

    if input_type == 'None':
        print('Rebuild the docker container with non null input_type')
        predictions = json.dumps(None)
        return predictions

    path = None

    if not file:
        print('No upload file sent')
        predictions = json.dumps(None)
        return predictions
    else:
        path = file.filename
        print(path)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    if path is None:
        print('Input imagepath is None')
        predictions = json.dumps(None)
        return predictions


    data = parse_input(data=path, input_type=input_type, input_shape=input_shape)

    if data is None:
        print('Error in data input format')
        predictions = json.dumps(None)
        return predictions


    predictions = model_predict(model, data)

    predictions = parse_output(data=predictions, output_type=output_type, output_shape=output_shape)


    return predictions


if __name__ == '__main__':
    uvicorn.run(app, host='{HOST}', port={PORT})""".format(
        HOST=API_IP_DOCKER,
        PORT=PORT_FASTAPI,
        MODEL_NAME=model_name,
        MODEL_BRANCH=model_branch,
        MODEL_VERSION=model_version,
        INPUT_TYPE=input_type,
        INPUT_SHAPE=input_shape,
        OUTPUT_TYPE=output_type,
        OUTPUT_SHAPE=output_shape,
    )

    return query


def generate_json_api(
    model_name, model_branch, model_version, input_type, input_shape, output_type, output_shape
):

    query = """
from fastapi import FastAPI, Depends, Request
import uvicorn
import pureml
from predict import model_predict
import os
from dotenv import load_dotenv
import pandas as pd
import json
import numpy as np
from pureml.utils.deploy import parse_input, parse_output

load_dotenv()

org_id = os.getenv('ORG_ID')
access_token = os.getenv('ACCESS_TOKEN')

pureml.login(org_id=org_id, access_token=access_token)

model = pureml.model.fetch('{MODEL_NAME}', '{MODEL_BRANCH}', '{MODEL_VERSION}')

# Create the app
app = FastAPI()     

@app.post('/predict')
async def predict(request: Request):
    input_type = '{INPUT_TYPE}'
    input_shape = '{INPUT_SHAPE}'
    output_type = '{OUTPUT_TYPE}'
    output_shape = '{OUTPUT_SHAPE}'

    if input_type == 'None':
        print('Rebuild the docker container with non null input_type')
        predictions = json.dumps(None)
        return predictions

    req_json = await request.json()

    data_json = req_json['test_data']


    data = parse_input(data=data_json, input_type=input_type, input_shape=input_shape)

    if data is None:
        print('Error in data input format')
        predictions = json.dumps(None)
        return predictions


    predictions = model_predict(model, data)

    predictions = parse_output(data=predictions, output_type=output_type, output_shape=output_shape)


    return predictions


if __name__ == '__main__':
    uvicorn.run(app, host='{HOST}', port={PORT})""".format(
        HOST=API_IP_DOCKER,
        PORT=PORT_FASTAPI,
        MODEL_NAME=model_name,
        MODEL_BRANCH=model_branch,
        MODEL_VERSION=model_version,
        INPUT_TYPE=input_type,
        INPUT_SHAPE=input_shape,
        OUTPUT_TYPE=output_type,
        OUTPUT_SHAPE=output_shape,
    )

    return query


def generate_api(input, output, model_name, model_branch, model_version):

    input_type, input_shape = process_input(input=input)
    output_type, output_shape = process_output(output=output)

    if input_type == "image":
        api = generate_file_upload_api(
            model_name=model_name, 
            model_branch=model_branch,
            model_version=model_version,
            input_type=input_type,
            input_shape=input_shape,
            output_type=output_type,
            output_shape=output_shape,
        )
    else:
        api = generate_json_api(
            model_name=model_name,
            model_branch=model_branch,
            model_version=model_version,
            input_type=input_type,
            input_shape=input_shape,
            output_type=output_type,
            output_shape=output_shape,
        )

    return api


def create_fastapi_file(
    model_name, model_branch, model_version, predict_path, requirements_path, input, output
):

    # get_project_file()

    get_predict_file(predict_path)

    get_requirements_file(requirements_path)

    api = generate_api(
        input=input, output=output, model_name=model_name, model_branch=model_branch, model_version=model_version
    )

    with open(PATH_FASTAPI_FILE, "w") as api_writer:
        api_writer.write(api)

    api_writer.close()

    print("FastAPI server files are created")


#     print("""
#           API sucessfully created. To run your API, please run the following command
# --> !python <api_name>
#           """)


def run_fastapi_server():
    pass
