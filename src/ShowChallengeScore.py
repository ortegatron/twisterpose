#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pygame as pg
from SceneEngine import GameState
from GameBrain import GameBrain
import cv2
import configparser
import Constants
import gradients

class ShowChallengeScore(GameState):
    def __init__(self, input, game_brain, resource ):
        super(ShowChallengeScore, self).__init__()
        self.title = self.font.render("Show Challege Score", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.game_brain = game_brain
        self.input = input
        self.resource = resource

    def startup(self, persistent):
        # GUARDA FOTO
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            frame = self.input.getCurrentFrame()
            cv2.imwrite(("%s/%s_%s.jpg") % (config['game']['screenshot_folder'], self.game_brain.playerName, self.game_brain.n_challenge), frame)
        except e:
            print(e)
            print("Error al guardar imagen")

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.game_brain.game_ended():
                    self.next_state = "SHOW_FINAL_SCORE"
                    self.done = True
                else:
                    self.next_state = "GAMEPLAY"
                    self.done = True

    def draw(self, surface):
        # Mostrar frame de input, quedó congelado en el último
        surface.fill(pg.Color("grey"))
        frame = self.input.getCurrentFrameAsImage().convert()
        frame.set_alpha(80)
        surface.blit(frame, (0,0))

        # Mostrar puntos obtenidos

        font_name = Constants.FONT_NAME
        fontPlayerName = pg.font.SysFont(font_name, 32)
        showScoreChallenge = fontPlayerName.render("Tu puntaje en este desafio fue:", True, (230, 57, 70))
        surface.blit(showScoreChallenge, (Constants.SCREEN_WIDTH/2-(showScoreChallenge.get_width()/2)-130,(self.game_brain.margin/2)-showScoreChallenge.get_height()/2))

        fontPlayerName = pg.font.SysFont(font_name, 60)
        showScoreChallenge = fontPlayerName.render(str(self.game_brain.get_challenge_score()), True, (230, 57, 70))
        surface.blit(showScoreChallenge, (Constants.SCREEN_WIDTH/2-(showScoreChallenge.get_width()/2)+130,(self.game_brain.margin/2)-showScoreChallenge.get_height()/2))

        # fontPlayerName = pg.font.Font(None, 30)
        # showScoreChallenge = fontPlayerName.render(str(self.game_brain.get_challenge_score()), True, pg.Color("dodgerblue"))
        # surface.blit(showScoreChallenge, showScoreChallenge.get_rect(center = (100,30)))

        # Mostrar targets
        margin = self.game_brain.margin
        board_size = self.game_brain.board_size
        size_grid_x  =  (Constants.SCREEN_WIDTH - 2*margin) / board_size
        size_grid_y  =  (Constants.SCREEN_HEIGHT - 2*margin) / board_size
        for fit in self.game_brain.best_fits_for_targets:
            target_x, target_y = fit['target']
            gradients.draw_circle(surface,(target_x,target_y),(target_x+size_grid_x/5,target_y+size_grid_y/5),(29,53,87,180),(241,250,238,180))
            pose_x, pose_y = fit['keypoint']
            gradients.draw_circle(surface,(pose_x,pose_y),(pose_x+size_grid_x/5,pose_y+size_grid_y/5),(241,250,238,180),(230,57,70,180))
            purple = (75, 0, 130)
            pg.draw.lines(surface, (29,53,87,180), True, ((pose_x,pose_y),(target_x,target_y)), 10)

        for fit in self.game_brain.best_fits_for_targets:
            keypoint = fit['keypoint']
            target = fit['target']
            print(keypoint)
            print(target)
    def update(self, dt):
        # Mover un timer para que se quede ne esta pantalla a lo sumo X SEGUNDOS
        pass
