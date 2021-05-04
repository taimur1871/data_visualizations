# imports for running the image operations
import os
from PIL import Image
import pandas as pd
from utils import iou
from utils import anomaly_CBLOF

import base64
import io
import json

import requests

#CON_PORT = os.environ.get('CON_PORT')

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
    url = 'http://0.0.0.0:8815/v1/models/cutter_detect:predict'
    #url = 'http://localhost:{}/v1/models/cutter_detect:predict'.format(port_number)
    #url = 'http://192.168.2.13:{}/v1/models/cutter_detect:predict'.format(port_number)
    #url = 'https://cuttercrop-jaikwcp3aq-uc.a.run.app:/v1/models/cutter_detect:predict'

    response = requests.post(url, data=json.dumps(instances))

    return response.json()

# folder to save pictures
target_folder = './crop_save'

# enter the port number for server
#port_num_obj = 8815

# main function to process blades
def cutter_crop(pic_folder, conf_thresh):
    # get list of files
    file_list = os.listdir(pic_folder)

    # dict to save final cutter data
    cutter_data = {}

    # dict to save processing data
    #process_data = {}

    # process individual paths from the list of pics
    for fn in file_list:

        # get picture path
        pic_path = os.path.join('./upload', fn)

        # send image for inference
        temp = container_predict(pic_path, fn)
    
        # fix prediction key error
        try:
            temp_pred = temp['predictions'][0]
            detect_multiclass_score = temp_pred['detection_multiclass_scores']
            detect_boxs = temp_pred['detection_boxes']
        except KeyError:
            continue

        # list to check for duplicates
        box_list = []

        for bbox, conf in zip(detect_boxs, detect_multiclass_score):
            if conf[2]>conf_thresh:
                box_list.append(bbox)
                box_list = iou(box_list)
            else:
                continue
        
        # store boxes in cutter data
        for i, box in enumerate(box_list):
            top = box[0]
            left = box[1]
            bottom = box[2]
            right = box[3]
        
            cutter_data[str(i)+fn] = [fn, top+(top-bottom)/2, left+(right-left)/2, box]
       
    cutter_data_df = check_anomaly(cutter_data)
    crop_cleaned(cutter_data_df)

    return target_folder, cutter_data

def check_anomaly(cutter_dict):
    df = pd.DataFrame(cutter_dict)
    df.rename({0:'filename', 1:'x_coord', 2:'y_coord', 3:'b_box'})
    df_clean = anomaly_CBLOF(df)
    return df_clean

# finally crop cutters
def crop_cleaned(df):
    for i in df:
        # open image
        pic_path = os.path.join('./upload', i[0])
        im = Image.open(pic_path)
        wd = im.width
        ht = im.height

        # crop the cutters
        box = i[3]
        top = box[0]*ht
        left = box[1]*wd
        bottom = box[2]*ht
        right = box[3]*wd

        temp = im.crop((left,top, right, bottom))
        try:
            temp.save(target_folder + '/'+str(i[1])+i[0], format='jpeg')
        except OSError:
            temp = temp.convert('RGB')
            temp.save(target_folder + '/'+str(i[1])+i[0], format='jpeg')