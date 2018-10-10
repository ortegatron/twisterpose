#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import pygame as pg
from SceneEngine import GameState
from GameBrain import GameBrain
from pyhiero.pygamefont import PyGameHieroFont
import Constants
import gradients
import Point
import os

class Gameplay(GameState):

    def __init__(self, input, game_brain ,resource ):
        super(Gameplay, self).__init__()
        self.input = input
        self.game_brain = game_brain
        self.fontScore = PyGameHieroFont(resource.fileName("font", "font.fnt"))

    def startup(self, persistent):
        self.game_brain.start_challenge()

    def update(self, dt):
        self.input.run()
        timeout  = self.game_brain.tick_time(dt)
        if timeout:
            self.game_brain.end_challenge(self.input.getCurrentPose())
            self.next_state = "SHOW_CHALLENGE_SCORE"
            self.done = True

    def draw(self, surface):
        # Mostrar camara de fondo
        surface.fill(pg.Color("black"))
        frame = self.input.getCurrentFrameAsImage()
        surface.blit(frame, (0,0))

        #Mostrar tablero
        margin = self.game_brain.margin
        max_height = Constants.SCREEN_HEIGHT - margin
        max_width = Constants.SCREEN_WIDTH - margin
        board_size = self.game_brain.board_size

        for i in range(1,board_size):
            Point.draw_dashed_line(surface,(29,53,87), ((margin+(max_width-margin)*i/board_size),margin), ((margin+(max_width-margin)*i/board_size),max_height),3,20)
            Point.draw_dashed_line(surface,(29,53,87), (margin,margin+((max_height-margin)*i/board_size)), (max_width,margin+((max_height-margin)*i/board_size)),3,20)

        size_grid_x  =  (Constants.SCREEN_WIDTH - 2*margin) / board_size
        size_grid_y  =  (Constants.SCREEN_HEIGHT - 2*margin) / board_size
        for pos_x, pos_y in self.game_brain.get_target_coords():
            gradients.draw_circle(surface,(pos_x,pos_y),(pos_x+size_grid_x/5,pos_y+size_grid_y/5),(29,53,87,190),(241,250,238,190))

        font_name = Constants.FONT_NAME

        # Mostrar timer
        #self.game_brain.getTimeLeft() = 30

        clock_img = pg.image.load('clock.png').convert_alpha()
        clock_img = pg.transform.scale(clock_img,(100,100))
        surface.blit(clock_img,(Constants.SCREEN_WIDTH-230,self.game_brain.margin/2-clock_img.get_height()/2))

        fontPlayerName = pg.font.SysFont(font_name, 50)
        showName = fontPlayerName.render(str(round(self.game_brain.get_time_left()/1000,1)), True, (0, 0, 0))
        surface.blit(showName, (Constants.SCREEN_WIDTH-120,self.game_brain.margin/2 - showName.get_height()/2))

        # Mostrar nombre de jugador

        player_img = pg.image.load('player.png').convert_alpha()
        player_img = pg.transform.scale(player_img,(70,70))
        surface.blit(player_img,(90,self.game_brain.margin/2-player_img.get_height()/2))

        fontPlayerName = pg.font.SysFont(font_name, 50)
        showName = fontPlayerName.render(self.game_brain.playerName, True, (255, 255, 255))
        surface.blit(showName, (180,self.game_brain.margin/2 - showName.get_height()/2))

        #Mostrar puntaje
        scoreImage = self.fontScore.render(str(self.game_brain.score))
        surface.blit(scoreImage, (Constants.SCREEN_WIDTH/2 - scoreImage.get_width()/2, 20))

        #Si una pose está cerca de un objetivo, lo cambio de color
        #self.game_brain.score_pose(self.input.getCurrentPose(),self.game_brain.target)
