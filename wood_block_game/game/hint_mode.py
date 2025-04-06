# game/hint_mode.py
import pygame
import sys
from game.ui_elements import Button
from game.game_controller import GameController
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from game.rules import show_rules
from game.animations import show_victory, show_defeat
from game.pieces import get_random_piece_set
from game.human_mode import select_difficulty

class HintAI:
    def __init__(self, board, pieces):
        self.board = board
        self.pieces = pieces

    def find_best_move(self):
        best_score = -1
        best_move = None

        for piece in self.pieces:
            for row in range(self.board.rows):
                for col in range(self.board.cols):
                    if self.board.can_place(piece, row, col):
                        temp_board = [r[:] for r in self.board.grid]
                        for r, c in piece.shape:
                            temp_board[row + r][col + c] = 1
                        score = self._simulate_score(temp_board)
                        if score > best_score:
                            best_score = score
                            best_move = (piece, row, col)
        return best_move

    def _simulate_score(self, grid):
        full_rows = sum(1 for row in grid if all(cell != 0 for cell in row))
        full_cols = sum(1 for col in zip(*grid) if all(cell != 0 for cell in col))
        return (full_rows + full_cols) * 100

def run_hint_mode(screen):
    clock = pygame.time.Clock()
    difficulty = select_difficulty(screen)
    game = GameController(difficulty)
    hint = None

    small_font = pygame.font.SysFont('Arial', 20)
    extra_small_font = pygame.font.SysFont('Arial', 16)

    back_button = pygame.Rect(SCREEN_WIDTH - 60, 10, 30, 30)

    while True:
        clock.tick(FPS)
        game.draw(screen)

        # Dica verde pastel
        if hint:
            piece, row, col = hint
            pastel_green = (144, 238, 144)
            for r, c in piece.shape:
                pr = row + r
                pc = col + c
                if 0 <= pr < game.board.rows and 0 <= pc < game.board.cols:
                    x = game.board.start_x + pc * game.board.cell_size
                    y = game.board.margin_top + pr * game.board.cell_size
                    pygame.draw.rect(screen, pastel_green, (x, y, game.board.cell_size - 2, game.board.cell_size - 2), border_radius=6)

        # Seta de voltar
        pygame.draw.polygon(screen, (120, 120, 255), [
            (back_button.right, back_button.top + 5),
            (back_button.left, back_button.centery),
            (back_button.right, back_button.bottom - 5)
        ], 0)

        # Texto de ajuda
        r_text = extra_small_font.render("Pressione 'R' para ler as regras", True, (90, 90, 90))
        d_text = extra_small_font.render("Pressione 'D' para dicas", True, (90, 90, 90))
        screen.blit(r_text, (back_button.left - r_text.get_width() + 30, back_button.bottom + 5))
        screen.blit(d_text, (back_button.left - d_text.get_width() + 30, back_button.bottom + 25))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                game.handle_click(event.pos)
                hint = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    show_rules(screen)
                elif event.key == pygame.K_d:
                    ai = HintAI(game.board, game.pieces)
                    hint = ai.find_best_move()

        if game.check_victory():
            show_victory(screen)
            return
        elif game.check_game_over():
            show_defeat(screen)
            return
