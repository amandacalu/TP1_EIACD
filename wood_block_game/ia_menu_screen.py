# ia_menu_screen.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from game.ui_elements import Button
from ia_mode import select_ia, run_ai_mode
from relatorios.relatorio_menu_screen import relatorio_menu_screen

def ia_menu_screen(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 32)

    jogar_button = Button("Jogar", (SCREEN_WIDTH // 2, 260), font, action="jogar")
    relatorios_button = Button("Ver Relatórios", (SCREEN_WIDTH // 2, 340), font, action="relatorios")
    voltar_button = Button("Voltar ao Menu", (SCREEN_WIDTH // 2, 420), font, action="voltar")

    buttons = [jogar_button, relatorios_button, voltar_button]

    while True:
        screen.fill(BG_COLOR)

        # Título
        title_font = pygame.font.SysFont('Arial Black', 46, bold=True)
        title_surface = title_font.render("Modo IA", True, (255, 182, 193))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        if button.action == "jogar":
                            algoritmo = select_ia(screen)
                            run_ai_mode(screen, algoritmo)
                        elif button.action == "relatorios":
                            relatorio_menu_screen(screen)
                        elif button.action == "voltar":
                            return  # volta para o main_menu
