# imports for requests to docker container
import os
import simplejson

import base64
import io
import json
import time

import requests


def container_predict(image_file_path, image_key):
    """Sends a prediction request to TFServing docker container REST API.

    Args:
        image_file_path: Path to a local image for the prediction request.
        image_key: Your chosen string key to identify the given image.
        port_number: The port number on your device to accept REST API calls.
    Returns:
        The response of the prediction request.
    """

    with io.open(image_file_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # The example here only shows prediction with one image. You can extend it
    # to predict with a batch of images indicated by different keys, which can
    # make sure that the responses corresponding to the given image.
    instances = {
            'instances': [
                    {'image_bytes': {'b64': str(encoded_image)},
                     'key': image_key}
            ]
    }

    # This example shows sending requests in the same server that you start
    # docker containers. If you would like to send requests to other servers,
    # please change localhost to IP of other servers.
    url = 'http://0.0.0.0:8601/v1/models/wear:predict'
    #url = 'http://localhost:{}/v1/models/wear:predict'.format(port_number)
    #url = 'http://192.168.2.13:{}/v1/models/wear:predict'.format(port_number)
    #url = 'https://cutterwear-jaikwcp3aq-uc.a.run.app:/v1/models/wear:predict'

    response = requests.post(url, data=json.dumps(instances))

    try:
        result = response.json()
    except simplejson.JSONDecodeError:
        time.sleep(5)
        response = requests.post(url, data=json.dumps(instances))
        result = response.json()

    return result


# enter the port number for server
#port_num = 8601

# get cutter wear
def cutter_wear(pic_path, key):
    pic = os.path.join(pic_path)

    # send image for inference
    #temp = container_predict(pic, key, port_num)
    temp = container_predict(pic, key)
    temp_pred = temp['predictions'][0]

    detect_classes = temp_pred['scores'].index(max(temp_pred['scores']))
    labels = temp_pred['labels'][detect_classes]
    return (temp_pred['key'], labels)
