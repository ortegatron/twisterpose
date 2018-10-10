#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pygame as pg
from SceneEngine import GameState
from GameBrain import GameBrain
import Constants
import Point


class ShowFinalScore(GameState):
    def __init__(self, input, game_brain, resource ):
        super(ShowFinalScore, self).__init__()
        self.title = self.font.render("Show Final Score", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.game_brain = game_brain
        self.input = input
        self.resource = resource

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.next_state = "SPLASH"
                self.done = True

    def startup(self, persistent):
        try:
            self.got_in_rank = self.game_brain.submit_game()
            self.ranking = self.game_brain.get_ranking()
        except:
            # Por si falla algo muestro todo en blanco pero que no se caiga el juego
            self.got_in_rank = False
            self.ranking = []

    def draw(self, surface):
        # Mostrar frame de input, quedó congelado en el último
        #surface.fill((215,67,34))
        surface.fill(pg.Color('grey'))
        frame = self.input.getCurrentFrameAsImage().convert()
        frame.set_alpha(80)
        surface.blit(frame, (0,0))

        # Mostrar puntos obtenidos
        font_name = Constants.FONT_NAME
        fontPlayerName = pg.font.SysFont(font_name, 40)
        showScoreTotal = fontPlayerName.render("Tu puntaje total fue:", True, (230, 57, 70))
        surface.blit(showScoreTotal, (Constants.SCREEN_WIDTH/2-(showScoreTotal.get_width()/2),50))
        fontPlayerName = pg.font.SysFont(font_name, 72)
        showScoreTotal = fontPlayerName.render(str(self.game_brain.get_score_total()), True, (230, 57, 70))
        surface.blit(showScoreTotal, (Constants.SCREEN_WIDTH/2-(showScoreTotal.get_width()/2),120))

        # Mostrar si quedo en ranking
        fontFinalMessage = pg.font.SysFont(font_name, 32)
        if self.got_in_rank:
            showCongratulations = fontFinalMessage.render("Bien ahi! Entraste al top 10!", True, (241,250,238))
            surface.blit(showCongratulations, (Constants.SCREEN_WIDTH/2-(showCongratulations.get_width()/2),200))
        else:
            showCongratulations = fontFinalMessage.render("Intenta de nuevo!", True, (241,250,238))
            surface.blit(showCongratulations, (Constants.SCREEN_WIDTH/2-(showCongratulations.get_width()/2),200))

        for i, toprank in enumerate(self.ranking):
            # Si esta en la lista lo resalto
            if self.game_brain.playerName == toprank['player'] and self.game_brain.get_score_total() == toprank['score']:
                fontColor = (230, 57, 70)
            else:
                fontColor = (29,53,87)
            fontPlayerName = pg.font.SysFont(font_name, 28)
            showRankName = fontPlayerName.render(str(i+1), True, fontColor)
            surface.blit(showRankName, (Constants.SCREEN_WIDTH/2-(showRankName.get_width()/2)-110,280+i*40))
            showRankName = fontPlayerName.render(str(toprank['player']), True, fontColor)
            surface.blit(showRankName, (Constants.SCREEN_WIDTH/2-(showRankName.get_width()/2)-0,280+i*40))
            showRankScore = fontPlayerName.render(str(toprank['score']), True, fontColor)
            surface.blit(showRankScore, (Constants.SCREEN_WIDTH/2-(showRankScore.get_width()/2)+110,280+i*40))

            Point.draw_dashed_line(surface,(241,250,238), (Constants.SCREEN_WIDTH/2-180,318+i*40), (Constants.SCREEN_WIDTH/2+180,318+i*40),3,1)


    def update(self, dt):
        # Mover un timer para que se quede ne esta pantalla a lo sumo X SEGUNDOS
        pass
