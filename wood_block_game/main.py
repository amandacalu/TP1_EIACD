# main.py
import pygame
import sys
from game.ui_elements import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from game.human_mode import run_human_mode

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wood Block Game - Menu")
clock = pygame.time.Clock()

# Font padrão
font = pygame.font.SysFont('Arial', 36)

# Botões do menu
buttons = [
    Button("Modo Humano", (SCREEN_WIDTH // 2, 250), font, action="human"),
    Button("Modo IA", (SCREEN_WIDTH // 2, 350), font, action="ai"),
    Button("Sair", (SCREEN_WIDTH // 2, 450), font, action="exit"),
]

def draw_menu():
    screen.fill(BG_COLOR)
    title_font = pygame.font.SysFont('Arial Black', 60, bold=True)
    title_surface = title_font.render("Wood Block Game", True, (255, 182, 193))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surface, title_rect)

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

def main_menu():
    while True:
        clock.tick(FPS)
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        if button.action == "exit":
                            pygame.quit()
                            sys.exit()
                        elif button.action == "human":
                            from game.human_mode import human_mode_choice
                            human_mode_choice(screen)
                        elif button.action == "ai":
                            from ia_menu_screen import ia_menu_screen  # ✅ import local evita circular import
                            ia_menu_screen(screen)  # ✅ chama a nova tela

if __name__ == "__main__":
    main_menu()
