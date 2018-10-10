# -*- coding: utf-8 -*-
import configparser
import cv2
import sys
import time
import numpy as np
from utils import poses2boxes
from pymongo import MongoClient
import json


# Cargar OpenPose:
sys.path.append('/usr/local/python')
#from openpose import *
params = dict()
params["logging_level"] = 3
params["output_resolution"] = "-1x-1"
params["net_resolution"] = "-1x736"
params["model_pose"] = "BODY_25"
params["alpha_pose"] = 0.6
params["scale_gap"] = 0.3
params["scale_number"] = 1
params["render_threshold"] = 0.05
params["num_gpu_start"] = 0
params["disable_blending"] = False
# Ensure you point to the correct path where models are located
params["default_model_folder"] = config['openpose']['path'] + "/models/"
# openpose = OpenPose(params)


model_filename = 'model_data/mars-small128.pb'
encoder = gdet.create_box_encoder(model_filename,batch_size=1)
metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
tracker = DeepTracker(metric, max_age = max_age,n_init= n_init)
