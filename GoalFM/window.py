from .classes import *
import pygame

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
FPS = 60


def refresh():
    WIN.fill(Color.white)
