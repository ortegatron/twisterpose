#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Input import Input
from Scene import Scene
from SplashScreen import SplashScreen
from Resource import Resource
from Gameplay import Gameplay
from GameBrain import GameBrain
from SceneEngine import Game, GameState
from ShowChallengeScore import ShowChallengeScore
from ShowFinalScore import ShowFinalScore
import sys
import getopt
import Constants
import pygame
import cv2
evento = None

class Twister():

    def __init__(self):
        self.input = Input()
        self.game_brain = GameBrain()
        self.resource = Resource()
        pygame.init()
        screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Twister!")

        states = {"SPLASH": SplashScreen(self.input, self.game_brain),
                       "GAMEPLAY": Gameplay(self.input, self.game_brain, self.resource),
                       "SHOW_CHALLENGE_SCORE": ShowChallengeScore(self.input, self.game_brain, self.resource),
                       "SHOW_FINAL_SCORE": ShowFinalScore(self.input, self.game_brain, self.resource)}
        game = Game(screen, states, "SPLASH")
        game.run()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    options, remainder = getopt.getopt(sys.argv[1:], 's:x:')
    for opt, arg in options:
        if opt in ('-s'):
            song = arg
        elif opt in ('-x'):
            speed = float(arg)
    game = Twister()
    game.run()
