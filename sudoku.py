import pygame
from pygame.event import Event
from typing import Optional

from board import Board
from button import Button
from consts import *
from assets import *


WIN = pygame.display.set_mode((WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption('Sudoku')


class Game:
    def __init__(self) -> None:
        """Instantiates the `Game` in the starting state."""
        self.difficulty = None
        self.board = None
        self.state = State.START
        self.clock = pygame.time.Clock()

    def tick(self) -> bool:
        """Performs the drawing and logic for one game tick.
        Returns a boolean representing if the game loop should continue.
        """
        self.clock.tick(FPS)
        WIN.fill(WHITE)
        events = pygame.event.get()
        if pygame.QUIT in (event.type for event in events):
            return False
        loop = True
        match self.state:
            case State.START:  # starting menu/screen
                self.tick_start_screen(events)
            case State.ACTIVE:  # active game screen
                loop = self.tick_active_screen(events)
            case State.WON:  # game completed screen
                loop = self.tick_game_over_screen(events)
            case _:
                raise Exception(f'Invalid state: {self.state!r}')
        pygame.display.update()
        return loop

    def draw_start_screen(self) -> None:
        WIN.blit(WELCOME, WELCOME_RECT)
        WIN.blit(DIFFICULTY_LABLE, DIFFICULTY_LABLE_RECT)
        EASY_BTN.draw(WIN)
        MEDIUM_BTN.draw(WIN)
        HARD_BTN.draw(WIN)

    def tick_start_screen(self, events: list[Event]) -> None:
        self.draw_start_screen()
        difficulty = None
        for event in events:
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue
            x, y = event.dict['pos']
            if EASY_BTN.click(x, y):
                difficulty = Difficulty.EASY
            if MEDIUM_BTN.click(x, y):
                difficulty = Difficulty.MEDIUM
            if HARD_BTN.click(x, y):
                difficulty = Difficulty.HARD
        if difficulty is not None:
            self.state = State.ACTIVE
            self.board = Board(removed=difficulty.value)

    def draw_active_screen(self) -> None:
        self.board.draw(WIN)
        RESET_BTN.draw(WIN)
        RESTART_BTN.draw(WIN)
        EXIT_BTN.draw(WIN)

    def tick_active_screen(self, events: list[Event]) -> bool:
        self.draw_active_screen()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.dict['pos']
                if EXIT_BTN.click(x, y):
                    return False
                if RESET_BTN.click(x, y):
                    self.board.reset_to_original()
                if RESTART_BTN.click(x, y):
                    self.state = State.START
                idx = self.board.click(x, y)
                if idx is None:
                    continue
                self.board.select(*idx)
            elif event.type == pygame.KEYDOWN:
                key = event.dict['unicode']
                if key in VALID_NUMS and self.board.selection is not None:
                    row, col = self.board.selection
                    if self.board.initial_state[row][col] == 0:
                        self.board.set_current(int(key))
                        if self.board.is_solved():
                            self.state = State.WON
        return True
    
    def draw_game_over_screen(self) -> None:
        WIN.blit(WON, WON_RECT)
        FINAL_EXIT_BTN.draw(WIN)

    def tick_game_over_screen(self, events: list[Event]) -> bool:
        self.draw_game_over_screen()
        for event in events:
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue
            x, y = event.dict['pos']
            if FINAL_EXIT_BTN.click(x, y):
                return False
        return True

    def run(self) -> None:
        while self.tick():
            pass


def main() -> None:
    Game().run()


if __name__ == '__main__':
    main()
