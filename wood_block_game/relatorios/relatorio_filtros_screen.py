import pygame
import csv
import os
from datetime import datetime, timedelta
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS
from game.ui_elements import Button

def relatorio_filtros_screen(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)
    title_font = pygame.font.SysFont('Arial Black', 34)

    dias_opcoes = [1, 3, 5, 7, 10, 30]
    botoes = []
    for i, dias in enumerate(dias_opcoes):
        btn = Button(f"Últimos {dias} dias", (SCREEN_WIDTH // 2, 130 + i * 60), font, action=dias)
        botoes.append(btn)

    voltar_button = Button("Voltar", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40), pygame.font.SysFont('Arial', 26))

    while True:
        screen.fill(BG_COLOR)

        title = title_font.render("Filtro por Período", True, (255, 182, 193))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        for btn in botoes:
            btn.draw(screen)

        voltar_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in botoes:
                    if btn.is_clicked(event.pos):
                        mostrar_resumo_periodo(screen, btn.action)
                if voltar_button.is_clicked(event.pos):
                    return

def mostrar_resumo_periodo(screen, dias):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)
    title_font = pygame.font.SysFont('Arial Black', 30)
    voltar_button = Button("Voltar", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40), pygame.font.SysFont('Arial', 26))

    algoritmos = ["bfs", "dfs", "astar"]
    hoje = datetime.today()
    inicio = hoje - timedelta(days=dias)

    resultados = {}

    for algoritmo in algoritmos:
        caminho = os.path.join("relatorios", f"{algoritmo}_resumo.csv")
        jogos = 0
        if os.path.exists(caminho):
            with open(caminho, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data_str = row.get("data", "")
                    try:
                        data_jogo = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                        if data_jogo >= inicio:
                            jogos += 1
                    except:
                        continue
        resultados[algoritmo.upper()] = jogos

    while True:
        screen.fill(BG_COLOR)

        titulo = title_font.render(f"Jogos nos últimos {dias} dias", True, (240, 200, 240))
        screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 40))

        y = 110
        for ia, total in resultados.items():
            txt = font.render(f"{ia}: {total} jogos", True, (240, 240, 240))
            screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, y))
            y += 40

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
