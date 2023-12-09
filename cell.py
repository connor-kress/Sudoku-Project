import pygame

from consts import (
    WIDTH, HEIGHT,
    WHITE, BLACK, RED,
    LIGHT_GRAY, DARK_GRAY,
    LINE_THICKNESS,
    NUMBER_FONT,
)


class Cell:
    def __init__(self, value: int, pos: tuple[int, int],
                 dims: tuple[int, int], editable: bool = True) -> None:
        row, col = pos
        rows, cols = dims
        width, height = WIDTH/cols, HEIGHT/rows
        self.value = value
        self.pos = pos
        self.string = str(value) if value else ''
        self.outer = pygame.Rect(width*col, height*row, width, height)
        self.inner = pygame.Rect(width*col + LINE_THICKNESS,
                                 height*row + LINE_THICKNESS,
                                 width - 2*LINE_THICKNESS,
                                 height - 2*LINE_THICKNESS)
        self.selected = False
        self.editable = editable
    
    def __repr__(self) -> str:
        """Cannot be used to recreate the `Cell` instance (just for debugging)."""
        return f'Cell(value={self.value}, pos={self.pos}, editable={self.editable})'
    
    def set_(self, __value: int) -> bool:
        if not self.editable:
            return False
        self.value = __value
        self.string = str(__value) if __value else ''
        return True
    
    # def clear(self) -> None:
    #     self.value = 0
    #     self.string = ''
    
    def draw(self, window: pygame.Surface) -> None:
        border_color = RED if self.selected else LIGHT_GRAY
        pygame.draw.rect(window, border_color, self.outer)
        pygame.draw.rect(window, WHITE, self.inner)

        text_color = RED if self.selected else\
            (DARK_GRAY if self.editable else BLACK)
        text = NUMBER_FONT.render(self.string, True, text_color, WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.inner.center
        window.blit(text, text_rect)
