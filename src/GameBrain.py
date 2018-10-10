#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Constants
import random
import configparser
import sys
import numpy as np
from pymongo import MongoClient

class GameBrain():
    def __init__(self):
        self.playerName = ""
        self.score = 0
        self.challenge_score = 0
        self.best_fits_for_targets = []
        self.board_size = 4
        self.margin = 100
        self.time_challenge = 0
        self.n_challenge = 0
        self.target = []

        # Cargar configuracion
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        mongodb_uri = self.config['database']['uri']
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[self.config['database']['database']]
        self.score_collection = self.db[self.config['database']['scores_collection']]

    def score_keypoint_to_target(self, keypoint, target):
        distancia =  np.linalg.norm(np.array(keypoint[0:2])-np.array(target))
        score =  (1000 / distancia) * 100
        return int(score)

    def get_target_coords(self):
        target_coords = []
        for target in self.target:
            size_grid_x  =  (Constants.SCREEN_WIDTH - 2*self.margin) / self.board_size
            size_grid_y  =  (Constants.SCREEN_HEIGHT - 2*self.margin) / self.board_size
            center_x = self.margin + (size_grid_x * target[0]) + size_grid_x / 2
            center_y = self.margin + (size_grid_y * target[1]) + size_grid_y / 2
            target_coords.append([center_x,center_y])
        return target_coords

    """
        Calcula el score de una pose con respecto a una serie de targets
        Devuelve score, best_fits_for_targets
        Donde score es el total de puntos que logra la pose,
        y best_fits_for_targets es la asociación entre que keypoints de la pose logran los targets y con cuantos puntos
    """
    def score_pose(self, people_poses, targets):
        best_fits_for_targets = []
        for target_center in self.get_target_coords():
            best_score = 0
            best_keypoint = None
            for pose in people_poses:
                for keypoint in pose:
                    # Si el keypoint es una deteccion, es decir si no es solo [0,0]
                    if any(keypoint):
                        score = self.score_keypoint_to_target(keypoint,target_center)
                        if (score > best_score):
                            best_score = score
                            best_keypoint = keypoint
            best_fits_for_targets.append({
                'target':target_center,
                'keypoint':best_keypoint[0:2],
                'score':best_score,
            })
        sum_score = sum([fit['score'] for fit in best_fits_for_targets])
        return sum_score, best_fits_for_targets

    def start_game(self):
        self.playerName = ""
        self.score = 0
        self.challenge_score = 0
        self.n_challenge = 0

    def start_challenge(self):
        self.time_challenge = 0
        self.target = [[random.randint(0,self.board_size-1),random.randint(0,self.board_size-1)] for _ in range(Constants.N_TARGETS)]

    # returns True if time has endeed
    def tick_time(self, dt):
        if (self.time_challenge + dt >  Constants.TIME_PER_CHALLENGE):
            self.time_challenge = Constants.TIME_PER_CHALLENGE
        else: self.time_challenge += dt
        return self.time_challenge >=  Constants.TIME_PER_CHALLENGE

    def end_challenge(self, pose):
        self.challenge_score, self.best_fits_for_targets = self.score_pose(pose, self.target)
        self.challenge_pose = pose
        self.score += self.challenge_score
        self.n_challenge += 1

    def game_ended(self):
        return self.n_challenge >= Constants.CHALLENGE_PER_GAME

    def get_time_left(self):
        return int(Constants.TIME_PER_CHALLENGE - self.time_challenge)

    def get_challenge_score(self):
        return self.challenge_score

    def get_score_total(self):
        return self.score

    # Manda el score del juego actual a labase y devuelve true si se entro en el ranking
    def submit_game(self):
        game = {
            'player': self.playerName,
            'score': self.score
        }
        self.score_collection.insert_one(game)
        ranking = self.get_ranking()
        return any([True for score in ranking if score['player'] == self.playerName])

    def get_ranking(self):
        all_scores = list(self.score_collection.find())
        all_scores.sort(key= lambda s: s['score'], reverse = True)
        return all_scores[:10]
