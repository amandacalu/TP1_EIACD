import pygame
import pandas as pd
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS, TEXT_COLOR
from game.ui_elements import Button

def relatorio_comparativo_screen(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)
    title_font = pygame.font.SysFont('Arial Black', 34, bold=True)
    small_font = pygame.font.SysFont('Arial', 16)

    voltar_button = Button("Voltar", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40), font)

    caminhos = {
        "BFS": "relatorios/bfs_resumo.csv",
        "DFS": "relatorios/dfs_resumo.csv",
        "A*": "relatorios/astar_resumo.csv"
    }

    dificuldades = ["facil", "medio", "dificil"]
    resultados = {}

    for nome, caminho in caminhos.items():
        if os.path.exists(caminho) and os.path.getsize(caminho) > 0:
            try:
                df = pd.read_csv(caminho)

                # Corrige parsing da coluna venceu
                df["venceu"] = df["venceu"].astype(str).str.strip().str.lower().map({"true": True, "false": False})

                info = {}
                for dif in dificuldades:
                    sub = df[df["modo"] == dif]
                    vitorias = sub[sub["venceu"] == True]
                    derrotas = sub[sub["venceu"] == False]

                    info[dif] = {
                        "v": len(vitorias),
                        "d": len(derrotas),
                        "tv": round(vitorias["tempo_ms"].mean() if not vitorias.empty else 0, 2),
                        "td": round(derrotas["tempo_ms"].mean() if not derrotas.empty else 0, 2)
                    }

                vitorias_total = df[df["venceu"] == True]
                derrotas_total = df[df["venceu"] == False]
                info["total"] = {
                    "v": len(vitorias_total),
                    "d": len(derrotas_total),
                    "tv": round(vitorias_total["tempo_ms"].mean() if not vitorias_total.empty else 0, 2),
                    "td": round(derrotas_total["tempo_ms"].mean() if not derrotas_total.empty else 0, 2)
                }

                resultados[nome] = info
            except Exception as e:
                print(f"Erro ao processar {nome}: {e}")

    rodando = True
    while rodando:
        screen.fill(BG_COLOR)
        title = title_font.render("Comparativo das IAs", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

        colunas = list(caminhos.keys())
        x0 = 140
        dx = 200
        y0 = 100

        for i, nome in enumerate(colunas):
            head = font.render(nome, True, TEXT_COLOR)
            screen.blit(head, (x0 + i * dx + 40, y0))

        y = y0 + 30
        for dif in dificuldades + ["total"]:
            nome_dif = dif.upper() if dif != "total" else "TOTAL"
            screen.blit(font.render(nome_dif, True, TEXT_COLOR), (40, y))

            for i, nome in enumerate(colunas):
                if nome in resultados and dif in resultados[nome]:
                    r = resultados[nome][dif]
                    linha = f"V:{r['v']}  D:{r['d']}  TV:{r['tv']}ms  TD:{r['td']}ms"
                else:
                    linha = "Sem dados"
                screen.blit(small_font.render(linha, True, TEXT_COLOR), (x0 + i * dx, y))
            y += 30

        voltar_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_button.is_clicked(event.pos):
                    return

