import pygame
import csv
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS
from game.ui_elements import Button

def relatorio_individual_screen(screen, algoritmo):
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont('Arial Black', 36)
    header_font = pygame.font.SysFont('Arial', 18)
    cell_font = pygame.font.SysFont('Arial', 15)
    voltar_button = Button("Voltar", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40), pygame.font.SysFont('Arial', 24))

    # Cores
    header_color = (10, 40, 120)
    default_cell_color = (15, 60, 150)
    green_color = (0, 120, 0)
    red_color = (180, 0, 0)

    # Caminho absoluto do CSV
    base_path = os.path.dirname(__file__)
    caminho_csv = os.path.join(base_path, f"{algoritmo}_resumo.csv")
    dados = []

    if os.path.exists(caminho_csv):
        with open(caminho_csv, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dados.append(row)

    scroll_y = 0
    scroll_speed = 20

    while True:
        screen.fill(BG_COLOR)

        # Título
        titulo = f"Relatório: {algoritmo.upper()}"
        title_surface = title_font.render(titulo, True, (255, 182, 193))
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 20))

        # Cabeçalhos
        headers = ["Data/Hora", "Modo", "Venceu", "Pontos", "Passos", "Tempo (ms)"]
        col_x = [30, 170, 290, 400, 500, 610]  # espaçamentos ajustados!
        for i, h in enumerate(headers):
            header_surface = header_font.render(h, True, header_color)
            screen.blit(header_surface, (col_x[i], 80))

        # Dados
        base_y = 110 - scroll_y
        for row in dados:
            try:
                tempo_ms = round(float(row.get("tempo_ms", 0) or 0), 2)
            except:
                tempo_ms = 0.0

            venceu_raw = row.get("venceu", "--")
            venceu_str = str(venceu_raw)

            values = [
                row.get("data", ""),
                row.get("modo", "--"),
                venceu_str,
                row.get("pontuacao", "--"),
                row.get("passos", "--"),
                str(tempo_ms)
            ]

            for i, v in enumerate(values):
                if i == 2:  # coluna "Venceu"
                    cor = green_color if v == "True" else red_color if v == "False" else default_cell_color
                else:
                    cor = default_cell_color

                val_surface = cell_font.render(str(v), True, cor)
                screen.blit(val_surface, (col_x[i], base_y))
            base_y += 26

        voltar_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_button.is_clicked(event.pos):
                    return
            elif event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * scroll_speed
                scroll_y = max(0, scroll_y)
