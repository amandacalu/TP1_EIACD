# game/human_mode.py
import pygame
import sys
from game.ui_elements import Button
from game.game_controller import GameController
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from game.rules import show_rules
from game.animations import show_victory, show_defeat

def select_difficulty(screen):
    font = pygame.font.SysFont('Arial', 36)
    clock = pygame.time.Clock()

    buttons = [
        Button("Fácil", (SCREEN_WIDTH // 2, 200), font, action="facil"),
        Button("Médio", (SCREEN_WIDTH // 2, 300), font, action="medio"),
        Button("Difícil", (SCREEN_WIDTH // 2, 400), font, action="dificil"),
    ]

    while True:
        screen.fill(BG_COLOR)

        title = font.render("Escolha a dificuldade", True, (255, 182, 193))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.action
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    show_rules(screen)  # ✅ mostra regras mesmo antes de escolher a dificuldade

def run_human_mode(screen):
    clock = pygame.time.Clock()
    difficulty = select_difficulty(screen)
    game = GameController(difficulty)

    while True:
        clock.tick(FPS)
        game.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                result = game.handle_click(event.pos)
                if result == "menu":
                    return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    show_rules(screen)  # ✅ mostra popup com regras durante o jogo também

        if game.check_victory():
            show_victory(screen)
            return
        elif game.check_game_over():
            show_defeat(screen)
            return
        
def human_mode_choice(screen):
    font = pygame.font.SysFont('Arial', 36)
    clock = pygame.time.Clock()

    buttons = [
        Button("Sem Dicas", (SCREEN_WIDTH // 2, 250), font, action="sem"),
        Button("Com Dicas", (SCREEN_WIDTH // 2, 350), font, action="com"),
    ]

    while True:
        screen.fill(BG_COLOR)
        title = font.render("Modo Humano", True, (255, 182, 193))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        if button.action == "sem":
                            run_human_mode(screen)
                        elif button.action == "com":
                            from game.hint_mode import run_hint_mode
                            run_hint_mode(screen)

