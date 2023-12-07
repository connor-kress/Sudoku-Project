from enum import Enum, auto
import pygame
import os

pygame.font.init()

ARIAL_PATH = os.path.join('fonts', 'arial.ttf')
NUMBER_FONT = pygame.font.Font(ARIAL_PATH, 32)
BIG_BTN_FONT = pygame.font.Font(ARIAL_PATH, 25)
SMALL_BTN_FONT = pygame.font.Font(ARIAL_PATH, 15)

WIDTH, HEIGHT = 450, 450
MENU_HEIGHT = 50

FPS = 60

LINE_THICKNESS = 2

BIG_BTN_SIZE = (125, 67)
SMALL_BTN_SIZE = (75, 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

VALID_NUMS = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

class State(Enum):
    START = auto()
    ACTIVE = auto()
    WON = auto()

class Difficulty(Enum):
    EASY = 30
    MEDIUM = 40
    HARD = 50
