# ia/execution_mode.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS
from game.ui_elements import Button

def select_execution_mode(screen):
    font = pygame.font.SysFont('Arial', 36)
    clock = pygame.time.Clock()

    title = font.render("Como a IA deve jogar?", True, (255, 182, 193))

    buttons = [
        Button("Modo Eficiência", (SCREEN_WIDTH // 2, 260), font, action="eficiencia"),
        Button("Modo Visual", (SCREEN_WIDTH // 2, 340), font, action="visual"),
    ]

    while True:
        screen.fill(BG_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 140))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.action
