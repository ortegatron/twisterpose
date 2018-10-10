# -*- coding: utf-8 -*-
import configparser
import cv2
import sys
import time
import numpy as np

import pygame
# Cargar OpenPose:
sys.path.append('/usr/local/python')
from openpose import *
# from utils import poses2boxes
# from pymongo import MongoClient
# import json

import Constants

class Input():
    def __init__(self, debug = False):
        # Cargar configuracion
        config = configparser.ConfigParser()
        config.read('config.ini')

        #from openpose import *
        params = dict()
        params["logging_level"] = 3
        params["output_resolution"] = "-1x-1"
        params["net_resolution"] = "176x160"
        params["model_pose"] = "BODY_25"
        params["alpha_pose"] = 0.6
        params["scale_gap"] = 0.3
        params["scale_number"] = 1
        params["render_threshold"] = 0.1
        params["num_gpu_start"] = 0
        params["disable_blending"] = False
        params["render_pose"] = 1

        #params["camera"] = 1
        # Ensure you point to the correct path where models are located
        params["default_model_folder"] = config['openpose']['path'] + "/models/"
        self.openpose = OpenPose(params)

        self.capture = cv2.VideoCapture(0)
        self.capture.set(3,Constants.SCREEN_WIDTH)
        self.capture.set(4,Constants.SCREEN_HEIGHT)
        if self.capture.isOpened():         # Checks the stream
            self.frameSize = (int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                               int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
        self.currentFrame = None
        self.keypoints = None

    def getCurrentFrameAsImage(self):
        frame = self.currentFrame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pgImg = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "RGB").convert()
        return pgImg

    def getCurrentFrame(self):
        return self.currentFrame

    def getCurrentPose(self):
        return self.keypoints

    def run(self):
        result, self.currentFrame = self.capture.read()
        self.currentFrame = cv2.flip(self.currentFrame,1)
        self.keypoints, self.currentFrame = self.openpose.forward(self.currentFrame, display = True)
        cv2.waitKey(1)
