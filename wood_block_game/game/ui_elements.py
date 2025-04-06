# game/ui_elements.py
import pygame
from config import BUTTON_COLOR, BUTTON_SHADOW, BUTTON_HIGHLIGHT, TEXT_COLOR

class Button:
    def __init__(self, text, pos, font, action=None):
        self.text = text
        self.font = font
        self.action = action
        self.pos = pos
        self.width = 260
        self.height = 70
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = pos

    def draw(self, screen):
        # Sombra inferior externa (profundidade)
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(screen, BUTTON_SHADOW, shadow_rect, border_radius=18)

        # Corpo do botão
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect, border_radius=18)

        # Brilho interno (top highlight)
        highlight_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height // 2)
        pygame.draw.rect(screen, BUTTON_HIGHLIGHT, highlight_rect, border_top_left_radius=18, border_top_right_radius=18)

        # Texto centralizado
        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
