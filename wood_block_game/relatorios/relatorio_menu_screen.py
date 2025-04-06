# relatorios/relatorio_menu_screen.py

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS
from game.ui_elements import Button
from relatorios.relatorio_individual_screen import relatorio_individual_screen
from relatorios.relatorio_comparativo_screen import relatorio_comparativo_screen

def relatorio_menu_screen(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 32)

    bfs_button = Button("Relatório - BFS", (SCREEN_WIDTH // 2, 220), font, action="bfs")
    dfs_button = Button("Relatório - DFS", (SCREEN_WIDTH // 2, 300), font, action="dfs")
    astar_button = Button("Relatório - A*", (SCREEN_WIDTH // 2, 380), font, action="astar")
    tabela_button = Button("Comparação IAs", (SCREEN_WIDTH // 2, 460), font, action="tabela")
    voltar_button = Button("Voltar", (SCREEN_WIDTH // 2, 540), font, action="voltar")

    buttons = [bfs_button, dfs_button, astar_button, tabela_button, voltar_button]

    while True:
        screen.fill(BG_COLOR)

        # Título
        title_font = pygame.font.SysFont('Arial Black', 44, bold=True)
        title_surface = title_font.render("Relatórios da IA", True, (255, 182, 193))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

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
                        if button.action in ["bfs", "dfs", "astar"]:
                            relatorio_individual_screen(screen, button.action)
                        elif button.action == "tabela":
                            relatorio_comparativo_screen(screen)
                        elif button.action == "voltar": 
                            return
