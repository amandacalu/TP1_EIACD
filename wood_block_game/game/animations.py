# game/animations.py
import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def show_victory(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial Black", 48)
    button_font = pygame.font.SysFont("Arial", 28)

    # Textos
    title = font.render("VITÓRIA!", True, (255, 100, 200))
    button_text = button_font.render("JOGAR DE NOVO", True, (50, 50, 80))

    # Cálculo de posicionamento vertical central
    total_height = title.get_height() + 40 + 60  # texto + espaço + botão
    start_y = (SCREEN_HEIGHT - total_height) // 2

    # Botão centralizado
    button_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 130,
        start_y + title.get_height() + 40,
        260, 60
    )

    # Confetes
    confetes = [{"x": random.randint(0, SCREEN_WIDTH),
                 "y": random.randint(-500, 0),
                 "color": [random.randint(100, 255) for _ in range(3)]}
                for _ in range(100)]

    running = True
    while running:
        # Fundo gradiente frutiger-aero
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            color = (
                210 + y // 20,
                230 + y // 25,
                255
            )
            pygame.draw.line(gradient, color, (0, y), (SCREEN_WIDTH, y))
        screen.blit(gradient, (0, 0))

        # Texto e botão centralizados
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, start_y))
        pygame.draw.rect(screen, (180, 220, 255), button_rect, border_radius=10)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Confetes caindo
        for confete in confetes:
            pygame.draw.circle(screen, confete["color"], (confete["x"], confete["y"]), 4)
            confete["y"] += 5
            if confete["y"] > SCREEN_HEIGHT:
                confete["y"] = random.randint(-100, 0)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos)):
                return

def show_defeat(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial Black", 54)
    button_font = pygame.font.SysFont("Arial", 28)

    # Texto e botão
    text = font.render("DERROTA!", True, (255, 80, 80))
    button_text = button_font.render("JOGAR DE NOVO", True, (255, 255, 255))

    # Cálculo de centralização
    total_height = text.get_height() + 40 + 60  # texto + espaço + botão
    start_y = (SCREEN_HEIGHT - total_height) // 2

    # Retângulo do botão
    button_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 130,
        start_y + text.get_height() + 40,
        260, 60
    )

    running = True
    while running:
        # Gradiente fundo
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            color = (30 + y // 10, 0, 0)
            pygame.draw.line(gradient, color, (0, y), (SCREEN_WIDTH, y))
        screen.blit(gradient, (0, 0))

        # Centraliza tudo
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, start_y))
        pygame.draw.rect(screen, (200, 80, 80), button_rect, border_radius=10)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos)):
                return
