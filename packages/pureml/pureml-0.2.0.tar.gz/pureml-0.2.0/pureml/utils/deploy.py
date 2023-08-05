import pandas as pd
import numpy as np
from PIL import Image
import json


def process_input(input):

    input_type = ''
    input_shape = None


    if input is not None:
        input_keys = input.keys()

        if 'type' in input_keys:
            input_type = input['type']
        if 'shape' in input_keys:
            input_shape = input['shape']
    
    return input_type, input_shape



def process_output(output):

    output_type = ''
    output_shape = None


    if output is not None:
        output_keys = output.keys()

        if 'type' in output_keys:
            output_type = output['type']
        if 'shape' in output_keys:
            output_shape = output['shape']
    
    return output_type, output_shape



def parse_input(data, input_type, input_shape):
    # if input_type == 'json':
    #     data = data

    if input_type == 'numpy ndarray':
        if type(data) == str:
            data = json.loads(data)
        data = np.array(data)
        data = data.reshape(input_shape)
    elif input_type == 'pandas dataframe':
        if type(data) == str:
            data = json.loads(data)
        data =  pd.DataFrame.from_dict(data)
    elif input_type == 'text':
        data = json.loads(data)
    elif input_type == 'image':
        data = Image.open(data)
        data = np.array(data)
        print(data.shape)
    else:
        data = None

    print(type(data))
    # print(data)

    return data

def parse_output(data, output_type, output_shape):
    # if input_type == 'json':
    #     data = data


    if output_type == 'numpy ndarray':
        data = data.tolist()
        data = json.dumps(data)
    elif output_type == 'pandas dataframe':
        data = data.to_dict()
        data = json.dumps(data)
    elif output_type == 'text':
        data = json.dumps(data)
    else:
        data = json.dumps(data)



    return data

