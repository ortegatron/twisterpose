#!/usr/bin/env python
# -*- coding: cp1252 -*-
# -*- coding: 850 -*-
# -*- coding: utf-8 -*-

import sys
import pygame as pg
from SceneEngine import GameState
from GameBrain import GameBrain
import Constants

class SplashScreen(GameState):
    def __init__(self, input, game_brain):
        super(SplashScreen, self).__init__()
        self.title = self.font.render("Splash Screen", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"
        self.input = input
        self.playerName = ""
        self.game_brain = game_brain

    def startup(self, persistent):
        self.game_brain.start_game()
        self.playerName = ""

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.unicode.isalpha():
                self.playerName += event.unicode
            elif event.key == pg.K_BACKSPACE:
                self.playerName = self.playerName[:-1]
            elif event.key == pg.K_RETURN:
                if self.playerName != "":
                    self.game_brain.playerName = self.playerName
                    self.done = True

    def draw(self, surface):
        # Mostrar camara de fondo
        #surface.fill((168,218,220))
        surface.fill(pg.Color('grey'))
        frame = self.input.getCurrentFrameAsImage().convert()
        frame.set_alpha(80)
        surface.blit(frame, (0,0))

        # Mostrar texto de bienvenida
        font_name = Constants.FONT_NAME

        font = pg.font.SysFont(font_name, 72)
        text = font.render("Bienvenido a Twister! con OpenPose", True, (230, 57, 70))
        surface.blit(text,(Constants.SCREEN_WIDTH/2-(text.get_width()/2),100))

        font = pg.font.SysFont(font_name, 40)
        text = font.render('Intenta cubrir con tu pose los circulos que aparecen en pantalla', True, (29,53,87))
        surface.blit(text,(Constants.SCREEN_WIDTH/2-(text.get_width()/2),200))

        font = pg.font.SysFont(font_name, 32)
        text = font.render("Cuanto mas cerca del centro de cada circulo, mayor puntaje!", True, (29,53,87))
        surface.blit(text,(Constants.SCREEN_WIDTH/2-(text.get_width()/2),250))

        font = pg.font.SysFont(font_name, 32)
        text = font.render("Ingresa tu nombre para empezar a jugar:", True, (230, 57, 70))
        surface.blit(text,(Constants.SCREEN_WIDTH/2-(text.get_width()/2),330))

        # Mostrar nombre de jugador
        fontPlayerName = pg.font.SysFont(font_name, 72)
        showName = fontPlayerName.render(self.playerName, True, (241,250,238))
        surface.blit(showName, (Constants.SCREEN_WIDTH/2 - (showName.get_width()/2),Constants.SCREEN_HEIGHT/2+50))

    def update(self, dt):
        self.input.run()
