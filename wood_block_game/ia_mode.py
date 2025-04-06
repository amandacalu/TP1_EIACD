# ia_mode.py
import pygame
import time
from game.ui_elements import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from game.pieces import get_random_piece_set
from game.board import Board
from ai.bfs_ai import BFSAI
from ai.dfs_ai import DFSAI
from ai.astar_ai import AStarAI
from ai.report import save_report
from ai.execution_mode import select_execution_mode

def select_ia(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 36)

    title = font.render("Escolha o Algoritmo da IA", True, (255, 182, 193))

    spacing = 100
    first_button_y = 200

    buttons = [
        Button("BFS", (SCREEN_WIDTH // 2, first_button_y), font, action="bfs"),
        Button("DFS", (SCREEN_WIDTH // 2, first_button_y + spacing), font, action="dfs"),
        Button("A*",  (SCREEN_WIDTH // 2, first_button_y + 2 * spacing), font, action="astar"),
    ]

    while True:
        screen.fill(BG_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.action

def run_ai_mode(screen, algoritmo_escolhido):
    clock = pygame.time.Clock()

    # Escolha de dificuldade
    font = pygame.font.SysFont('Arial', 36)
    title = font.render("Escolha a dificuldade", True, (255, 182, 193))
    buttons = [
        Button("Fácil", (SCREEN_WIDTH // 2, 220), font, action="facil"),
        Button("Médio", (SCREEN_WIDTH // 2, 300), font, action="medio"),
        Button("Difícil", (SCREEN_WIDTH // 2, 380), font, action="dificil"),
    ]

    difficulty = None
    while difficulty is None:
        screen.fill(BG_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
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
                        difficulty = button.action

    # Criar tabuleiro e peças iniciais
    size = {"facil": 8, "medio": 7, "dificil": 6}[difficulty]
    board = Board(size, size, 40, margin_top=100)
    pieces = get_random_piece_set(3, difficulty)

    # Escolher IA
    if algoritmo_escolhido == "bfs":
        ia = BFSAI(board, pieces, difficulty)
    elif algoritmo_escolhido == "dfs":
        ia = DFSAI(board, pieces, difficulty)
    elif algoritmo_escolhido == "astar":
        ia = AStarAI(board, pieces, difficulty)

    modo = select_execution_mode(screen)

    if modo == "eficiencia":
        result = ia.run()
        show_ia_result(screen, result)
    elif modo == "visual":
        result = ia.run_visual(screen, clock)
        show_ia_result(screen, result)

def show_ia_result(screen, result):
    font = pygame.font.SysFont('Arial', 30)
    clock = pygame.time.Clock()

    title = font.render("RELATÓRIO DA IA", True, (255, 182, 193))
    lines = [
        f"Algoritmo: {result['algoritmo']}",
        f"Heurísticas usadas: {', '.join(result.get('heuristicas', ['Nenhuma']))}",
        f"Pontuação: {result['pontuacao']}",
        f"Passos: {result['passos']}",
        f"Tempo: {result.get('tempo_ms', round(result.get('tempo', 0), 2))} ms",
        f"Resultado: {'VITÓRIA' if result['venceu'] else 'DERROTA'}"
    ]

    button_font = pygame.font.SysFont('Arial', 28)
    back_button = Button("Voltar ao Menu", (SCREEN_WIDTH // 2, 520), button_font, action="menu")

    while True:
        screen.fill(BG_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        for i, line in enumerate(lines):
            rendered = font.render(line, True, (30, 60, 90))
            screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, 180 + i * 50))

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return
