import pygame


class Button:
    def __init__(
        self,
        *,
        rect: pygame.Rect,
        bg_color: tuple[int, int, int],
        text: str,
        text_color: tuple[int, int, int],
        font: pygame.font.Font,
    ) -> None:
        self.rect = rect
        self.bg_color = bg_color
        self.text = text
        self.text_color = text_color
        self.font = font
    
    def draw(self, window: pygame.Surface) -> None:
        text = self.font.render(self.text, True,
                                self.text_color,
                                self.bg_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center

        pygame.draw.rect(window, self.bg_color, self.rect)
        window.blit(text, text_rect)
    
    def click(self, x: float, y: float) -> bool:
        return self.rect.collidepoint(x, y)
