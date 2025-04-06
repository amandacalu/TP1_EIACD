# ai/astar_ai.py
from ai.ai_base import AIBase
import heapq
import time
import pygame
from itertools import count
from copy import deepcopy
from game.pieces import get_random_piece_set
from config import BG_COLOR
from game.draw_helpers import draw_available_pieces

class AStarAI(AIBase):
    def __init__(self, board, pieces, difficulty):
        super().__init__(board, pieces, difficulty)
        self.delay_ms = 300
        self.active_heuristics = [
            self.h1_clear_lines,
            self.h2_center_bias,
            self.h3_adjacent_bonus,
            #self.h4_penalize_useless_moves
        ]

    def run(self):
        start_ns = time.perf_counter_ns()
        while True:
            move = self.best_move()
            if move is None:
                break
            piece, row, col = move
            self.board.place(piece, row, col)
            self.board.check_and_clear_lines()
            self.steps += 1

            if self.board.score >= self.target_score() or self.board.empty_moves >= 4:
                break

            self.pieces = get_random_piece_set(len(self.pieces), self.difficulty)

        end_ns = time.perf_counter_ns()
        duration = end_ns - start_ns
        tempo_segundos = duration / 1_000_000_000

        result = {
            "algoritmo": "astar",  # <-- Corrigido para salvar com nome do arquivo compatível
            "heuristicas": self.get_heuristics_names(short=True),
            "dificuldade": self.difficulty,
            "pontuacao": self.board.score,
            "passos": self.steps,
            "tempo_ns": duration,
            "tempo_ms": round(duration / 1_000_000, 2),
            "tempo": tempo_segundos,
            "venceu": self.board.score >= self.target_score()
        }

        from ai.report import save_report, save_summary
        save_report(result)
        save_summary(result)

        return result

    def run_visual(self, screen, clock):
        start = time.time()
        passos = 0
        delay = self.delay_ms

        while True:
            move = self.best_move()
            if move is None:
                break

            piece, row, col = move
            self._draw_shadow(screen, piece, row, col)
            draw_available_pieces(screen, self.pieces, self.board)
            self._draw_ia_info(screen, passos, delay)
            self._draw_heuristics_description(screen)
            pygame.display.flip()
            pygame.time.delay(delay)

            self.board.place(piece, row, col)
            self.board.check_and_clear_lines()
            passos += 1

            screen.fill(BG_COLOR)
            self.board.draw(screen)
            draw_available_pieces(screen, self.pieces, self.board)
            self._draw_ia_info(screen, passos, delay)
            self._draw_heuristics_description(screen)
            pygame.display.flip()
            pygame.time.delay(delay)

            if self.board.score >= self.target_score() or self.board.empty_moves >= 4:
                break

            self.pieces = get_random_piece_set(len(self.pieces), self.difficulty)

        return {
            "algoritmo": "astar",  # <-- Corrigido aqui também
            "heuristicas": self.get_heuristics_names(short=True),
            "pontuacao": self.board.score,
            "passos": passos,
            "tempo": time.time() - start,
            "venceu": self.board.score >= self.target_score(),
            "delay_ms": delay
        }

    def best_move(self):
        heap = []
        counter = count()
        for piece in self.pieces:
            for row in range(self.board.rows):
                for col in range(self.board.cols):
                    if self.board.can_place(piece, row, col):
                        new_board = deepcopy(self.board)
                        points_before = new_board.score
                        new_board.place(piece, row, col)
                        new_board.check_and_clear_lines()
                        gained = new_board.score - points_before
                        h = self.evaluate(new_board, gained)
                        heapq.heappush(heap, (h, next(counter), (piece, row, col)))
        if heap:
            return heapq.heappop(heap)[2]
        return None

    def evaluate(self, board, gained):
        h_total = 0
        for h_func in self.active_heuristics:
            h_total += h_func(board, gained)
        return -h_total

    def get_heuristics_names(self, short=False):
        names = []
        for h in self.active_heuristics:
            if h == self.h1_clear_lines:
                names.append("h1" if short else "h1_clear_lines")
            elif h == self.h2_center_bias:
                names.append("h2" if short else "h2_center_bias")
            elif h == self.h3_adjacent_bonus:
                names.append("h3" if short else "h3_adjacent_bonus")
            elif h == self.h4_penalize_useless_moves:
                names.append("h4" if short else "h4_penalize_useless_moves")
        return names

    def _draw_shadow(self, screen, piece, row, col):
        screen.fill(BG_COLOR)
        self.board.draw(screen)
        for r, c in piece.shape:
            pr = row + r
            pc = col + c
            if 0 <= pr < self.board.rows and 0 <= pc < self.board.cols:
                x = self.board.start_x + pc * self.board.cell_size
                y = self.board.margin_top + pr * self.board.cell_size
                pygame.draw.rect(screen, (180, 220, 255), (x, y, self.board.cell_size - 2, self.board.cell_size - 2), border_radius=6)

    def _draw_ia_info(self, screen, passos, delay):
        font = pygame.font.SysFont('Arial', 22)
        info = f"IA: A*   |   Jogadas: {passos}   |   Delay: {delay}ms"
        txt = font.render(info, True, (20, 60, 100))
        screen.blit(txt, (screen.get_width() // 2 - txt.get_width() // 2, 20))

    def _draw_heuristics_description(self, screen):
        font = pygame.font.SysFont('Arial', 15)
        y = screen.get_height() - 100
        for h in self.get_heuristics_names():
            desc = self._describe_heuristic(h)
            txt = font.render(desc, True, (60, 60, 90))
            screen.blit(txt, (screen.get_width() // 2 - txt.get_width() // 2, y))
            y += 18

    def _describe_heuristic(self, name):
        descriptions = {
            "h1_clear_lines": "Heurística 1: Prefere jogadas que limpam linhas/colunas. (h1)",
            "h2_center_bias": "Heurística 2: Prefere peças mais próximas ao centro. (h2)",
            "h3_adjacent_bonus": "Heurística 3: Prefere peças encostadas a outras. (h3)",
            "h4_penalize_useless_moves": "Heurística 4: Penaliza jogadas que não pontuam (modo difícil). (h4)"
        }
        return descriptions.get(name, name)

    def target_score(self):
        return {"facil": 1000, "medio": 2000, "dificil": 3000}[self.difficulty]

    def h1_clear_lines(self, board, gained):
        return gained

    def h2_center_bias(self, board, gained):
        center_r = board.rows / 2
        center_c = board.cols / 2
        total = 0
        for r in range(board.rows):
            for c in range(board.cols):
                if board.grid[r][c]:
                    dist = abs(r - center_r) + abs(c - center_c)
                    total += (10 - dist)
        return total

    def h3_adjacent_bonus(self, board, gained):
        bonus = 0
        for r in range(board.rows):
            for c in range(board.cols):
                if board.grid[r][c]:
                    neighbors = [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]
                    for nr, nc in neighbors:
                        if 0 <= nr < board.rows and 0 <= nc < board.cols:
                            if board.grid[nr][nc]:
                                bonus += 1
        return bonus

    def h4_penalize_useless_moves(self, board, gained):
        return gained if gained > 0 else -50
