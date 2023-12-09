import pygame

from button import Button
from consts import *

WELCOME = TITLE_FONT.render('Welcome to Sudoku', True, BLACK)
WELCOME_RECT = WELCOME.get_rect()
WELCOME_RECT.center = (WIDTH/2, 100)

WON = TITLE_FONT.render('You Won!', True, BLACK)
WON_RECT = WON.get_rect()
WON_RECT.center = (WIDTH/2, 100)

DIFFICULTY_LABLE = HEADER_FONT.render('Select a Difficulty:', True, BLACK)
DIFFICULTY_LABLE_RECT = DIFFICULTY_LABLE.get_rect()
DIFFICULTY_LABLE_RECT.center = (WIDTH/2, HEIGHT/2 + 50)

medium_rect = pygame.Rect((0, 0), BIG_BTN_SIZE)
medium_rect.center = (WIDTH/2, HEIGHT/2 + 150)
MEDIUM_BTN = Button(
    rect=medium_rect,
    text='MEDIUM',
    bg_color=ORANGE,
    text_color=WHITE,
    font=BIG_BTN_FONT,
)

easy_rect = medium_rect.copy()
easy_rect.x -= BIG_BTN_SIZE[0] + 5
EASY_BTN = Button(
    rect=easy_rect,
    text='EASY',
    bg_color=ORANGE,
    text_color=WHITE,
    font=BIG_BTN_FONT,
)

hard_rect = medium_rect.copy()
hard_rect.x += BIG_BTN_SIZE[0] + 5
HARD_BTN = Button(
    rect=hard_rect,
    text='HARD',
    bg_color=ORANGE,
    text_color=WHITE,
    font=BIG_BTN_FONT,
)

middle_bottom = pygame.Rect((0, 0), SMALL_BTN_SIZE)
middle_bottom.center = (WIDTH/2, HEIGHT + SMALL_BTN_SIZE[1]/2 + 5)
RESTART_BTN = Button(
    rect=middle_bottom,
    text='RESTART',
    bg_color=ORANGE,
    text_color=WHITE,
    font=SMALL_BTN_FONT,
)

reset_rect = middle_bottom.copy()
reset_rect.x -= SMALL_BTN_SIZE[0] + 5
RESET_BTN = Button(
    rect=reset_rect,
    text='RESET',
    bg_color=ORANGE,
    text_color=WHITE,
    font=SMALL_BTN_FONT,
)

exit_rect = middle_bottom.copy()
exit_rect.x += SMALL_BTN_SIZE[0] + 5
EXIT_BTN = Button(
    rect=exit_rect,
    text='EXIT',
    bg_color=ORANGE,
    text_color=WHITE,
    font=SMALL_BTN_FONT,
)

final_exit_rect = pygame.Rect((0, 0), BIG_BTN_SIZE)
final_exit_rect.center = (WIDTH/2, HEIGHT/2)
FINAL_EXIT_BTN = Button(
    rect=final_exit_rect,
    text='EXIT',
    bg_color=ORANGE,
    text_color=WHITE,
    font=BIG_BTN_FONT,
)
