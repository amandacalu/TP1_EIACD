from ai.ai_base import AIBase
import time
import pygame
from game.pieces import get_random_piece_set
from config import BG_COLOR, SCREEN_WIDTH
from game.draw_helpers import draw_available_pieces

class DFSAI(AIBase):
    def run(self):
        start_ns = time.perf_counter_ns()
        empty_turns = 0

        while True:
            move_found = False
            score_before = self.board.score

            for piece in self.pieces:
                for row in reversed(range(self.board.rows)):
                    for col in reversed(range(self.board.cols)):
                        if self.board.can_place(piece, row, col):
                            self.board.place(piece, row, col)
                            self.board.check_and_clear_lines()
                            self.steps += 1
                            move_found = True
                            break
                    if move_found:
                        break
                if move_found:
                    break

            if self.difficulty == "dificil":
                if self.board.score == score_before:
                    empty_turns += 1
                else:
                    empty_turns = 0

                if empty_turns >= 4:
                    break

            if self.board.score >= {"facil": 1000, "medio": 2000, "dificil": 3000}[self.difficulty]:
                break

            if not move_found:
                break

            self.pieces = get_random_piece_set(len(self.pieces), self.difficulty)

        end_ns = time.perf_counter_ns()
        duration = end_ns - start_ns
        tempo_segundos = duration / 1_000_000_000

        result = {
            "algoritmo": "DFS",
            "dificuldade": self.difficulty,  # ✅ Adicionado
            "pontuacao": self.board.score,
            "passos": self.steps,
            "tempo_ns": duration,
            "tempo_ms": round(duration / 1_000_000, 2),
            "tempo": tempo_segundos,
            "venceu": self.board.score >= {"facil": 1000, "medio": 2000, "dificil": 3000}[self.difficulty] and empty_turns < 4
        }

        from ai.report import save_report, save_summary
        save_report(result)
        save_summary(result)

        return result

    def run_visual(self, screen, clock):
        start_time = time.time()
        delay_ms = 300
        empty_turns = 0
        steps = 0

        while True:
            move_found = False
            score_before = self.board.score

            for piece in self.pieces:
                for row in reversed(range(self.board.rows)):
                    for col in reversed(range(self.board.cols)):
                        if self.board.can_place(piece, row, col):
                            self._draw_shadow(screen, piece, row, col)
                            draw_available_pieces(screen, self.pieces, self.board)
                            self._draw_ia_info(screen, steps, delay_ms)
                            pygame.display.flip()
                            pygame.time.delay(delay_ms)

                            self.board.place(piece, row, col)
                            self.board.check_and_clear_lines()

                            steps += 1
                            self.pieces = get_random_piece_set(len(self.pieces), self.difficulty)

                            screen.fill(BG_COLOR)
                            self.board.draw(screen)
                            draw_available_pieces(screen, self.pieces, self.board)
                            self._draw_ia_info(screen, steps, delay_ms)
                            pygame.display.flip()
                            pygame.time.delay(delay_ms)

                            move_found = True
                            break
                    if move_found:
                        break
                if move_found:
                    break

            if self.difficulty == "dificil":
                if self.board.score == score_before:
                    empty_turns += 1
                else:
                    empty_turns = 0

                if empty_turns >= 4:
                    break

            score_goal = {"facil": 1000, "medio": 2000, "dificil": 3000}[self.difficulty]
            if not move_found or self.board.is_game_over(self.pieces) or self.board.score >= score_goal:
                break

        return {
            "algoritmo": "DFS",
            "pontuacao": self.board.score,
            "passos": steps,
            "tempo": time.time() - start_time,
            "venceu": self.board.score >= score_goal and empty_turns < 4,
            "delay_ms": delay_ms
        }

    def _draw_shadow(self, screen, piece, row, col):
        screen.fill(BG_COLOR)
        self.board.draw(screen)

        for r, c in piece.shape:
            pr = row + r
            pc = col + c
            if 0 <= pr < self.board.rows and 0 <= pc < self.board.cols:
                x = self.board.start_x + pc * self.board.cell_size
                y = self.board.margin_top + pr * self.board.cell_size
                pygame.draw.rect(
                    screen,
                    (180, 220, 255),
                    (x, y, self.board.cell_size - 2, self.board.cell_size - 2),
                    border_radius=6
                )

    def _draw_ia_info(self, screen, steps, delay):
        font = pygame.font.SysFont('Arial', 22)
        info = f"IA: DFS   |   Steps: {steps}   |   Delay: {delay}ms"
        txt = font.render(info, True, (20, 60, 100))
        screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 20))
