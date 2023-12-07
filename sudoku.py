import pygame
from typing import Optional

from board import Board
from button import Button
from consts import *


WIN = pygame.display.set_mode((WIDTH, HEIGHT + MENU_HEIGHT))
pygame.display.set_caption('Sudoku')

middle_bottom = pygame.Rect((0, 0), SMALL_BTN_SIZE)
middle_bottom.center = (WIDTH / 2, HEIGHT + SMALL_BTN_SIZE[1]/2 + 5)
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

class Game:
    def __init__(self, difficulty: Difficulty) -> None:
        self.board = Board(removed=difficulty.value)
        self.state = State.ACTIVE
        self.clock = pygame.time.Clock()
    
    # def __init__(self) -> None:
    #     self.difficulty = None
    #     self.board = None
    #     self.state = State.START
    #     self.clock = pygame.time.Clock()

    def tick(self) -> bool:
        self.clock.tick(FPS)
        WIN.fill(WHITE)
        events = pygame.event.get()
        if pygame.QUIT in (event.type for event in events):
            return False
        match self.state:
            case State.START:
                loop = self.tick_start(events)
            case State.ACTIVE:
                loop = self.tick_active(events)
            case State.WON:
                loop = self.tick_won(events)
            case _:
                raise NotImplementedError
        pygame.display.update()
        return loop

    def tick_start(self, events: list[pygame.event.Event]) -> bool:
        raise NotImplementedError

    def tick_active(self, events: list[pygame.event.Event]) -> bool:
        self.board.draw(WIN)
        RESET_BTN.draw(WIN)
        RESTART_BTN.draw(WIN)
        EXIT_BTN.draw(WIN)
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

    def tick_won(self, events: list[pygame.event.Event]) -> bool:
        print('You Won!')
        return False  # not Implemented

    def run(self) -> None:
        while self.tick():
            pass


def main() -> None:
    Game(Difficulty.MEDIUM).run()


if __name__ == '__main__':
    main()
