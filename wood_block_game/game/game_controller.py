# game/game_controller.py
import pygame
import sys
import random
from game.board import Board
from game.pieces import get_random_piece_set
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR

class GameController:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.setup_difficulty()

        self.board = Board(self.board_size, self.board_size, self.cell_size)
        self.selected_piece = None
        self.selected_offset = (0, 0)
        self.pieces = get_random_piece_set(self.piece_count, self.difficulty)
        if self.difficulty == "dificil":
            self.empty_turns = 0
            self.last_score = 0
        self.font = pygame.font.SysFont('Arial', 28)
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.extra_small_font = pygame.font.SysFont('Arial', 16)
        self.last_score = 0
        self.back_button = pygame.Rect(SCREEN_WIDTH - 60, 10, 30, 30)

    def setup_difficulty(self):
        if self.difficulty == 'facil':
            self.board_size = 8
            self.piece_count = 4
            self.win_score = 1000
        elif self.difficulty == 'medio':
            self.board_size = 7
            self.piece_count = 3
            self.win_score = 2000
        elif self.difficulty == 'dificil':
            self.board_size = 6
            self.piece_count = 2
            self.win_score = 3000
        self.cell_size = 50

    def draw(self, screen):
        screen.fill(BG_COLOR)
        self.board.draw(screen)

        # Score
        score_text = self.font.render(f"Pontos: {self.board.score}", True, (30, 60, 90))
        screen.blit(score_text, (50, 20))

        # Meta abaixo da pontuação
        meta_text = self.small_font.render(f"Meta: {self.win_score}", True, (30, 60, 90))
        screen.blit(meta_text, (50, 55))

        # ⚠️ Aviso para o modo difícil
        if self.difficulty == "dificil":
            alert_font = pygame.font.SysFont('Arial', 20)
            pink = (255, 182, 193)
            counter_text = alert_font.render(f"Rodadas sem pontuar: {self.empty_turns} / 4", True, pink)
            screen.blit(counter_text, (50, 80))
            warning_text = alert_font.render("Atenção: no modo difícil, 4 rodadas sem pontuar = DERROTA!", True, pink)
            screen.blit(warning_text, (SCREEN_WIDTH // 2 - warning_text.get_width() // 2, SCREEN_HEIGHT - 40))

        # Peças disponíveis
        total_width = self.piece_count * 100
        start_x = (SCREEN_WIDTH - total_width) // 2
        y_offset = self.board.margin_top + self.board.rows * self.cell_size + 40

        for i, piece in enumerate(self.pieces):
            piece_x = start_x + i * 100
            for r, c in piece.shape:
                x = piece_x + c * 20
                y = y_offset + r * 20

                if piece == self.selected_piece:
                    neon_color = (0, 255, 255)
                    glow_rect = pygame.Rect(x - 2, y - 2, 22, 22)
                    pygame.draw.rect(screen, neon_color, glow_rect, border_radius=6)

                pygame.draw.rect(screen, piece.color, (x, y, 18, 18), border_radius=4)

        # Texto de regras — sempre no canto superior direito, abaixo da seta
        info_text = self.extra_small_font.render("Pressione 'R' para ler as regras", True, (90, 90, 90))
        screen.blit(info_text, (self.back_button.left - info_text.get_width() + 30, self.back_button.bottom + 5))

        # Sombra da peça selecionada
        if self.selected_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = (mouse_x - self.board.start_x) // self.cell_size
            grid_y = (mouse_y - self.board.margin_top) // self.cell_size

            origin_r, origin_c = self.selected_piece.shape[0]
            board_row = grid_y - origin_r
            board_col = grid_x - origin_c

            if self.board.can_place(self.selected_piece, board_row, board_col):
                for r, c in self.selected_piece.shape:
                    row = board_row + r
                    col = board_col + c
                    if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
                        x = self.board.start_x + col * self.cell_size
                        y = self.board.margin_top + row * self.cell_size
                        shadow_color = (180, 220, 255)
                        pygame.draw.rect(screen, shadow_color, (x, y, self.cell_size - 2, self.cell_size - 2), border_radius=6)

        # Seta de voltar
        pygame.draw.polygon(screen, (120, 120, 255), [
            (self.back_button.right, self.back_button.top + 5),
            (self.back_button.left, self.back_button.centery),
            (self.back_button.right, self.back_button.bottom - 5)
        ], 0)

        pygame.display.flip()

    def handle_click(self, pos):
        if self.back_button.collidepoint(pos):
            self.__init__(self.difficulty)
            return "menu"

        total_width = self.piece_count * 100
        start_x = (SCREEN_WIDTH - total_width) // 2
        y_offset = self.board.margin_top + self.board.rows * self.cell_size + 40

        for i, piece in enumerate(self.pieces):
            piece_x = start_x + i * 100
            piece_rects = [(piece_x + c * 20, y_offset + r * 20, 18, 18) for r, c in piece.shape]
            for rect in piece_rects:
                if pygame.Rect(rect).collidepoint(pos):
                    self.selected_piece = piece
                    return

        if self.selected_piece:
            mouse_x, mouse_y = pos
            grid_x = (mouse_x - self.board.start_x) // self.cell_size
            grid_y = (mouse_y - self.board.margin_top) // self.cell_size

            origin_r, origin_c = self.selected_piece.shape[0]
            board_row = grid_y - origin_r
            board_col = grid_x - origin_c

            if self.board.can_place(self.selected_piece, board_row, board_col):
                self.board.place_piece(self.selected_piece, board_row, board_col)
                self.board.check_and_clear_lines()
                if self.difficulty == "dificil":
                    if self.board.score == self.last_score:
                        self.empty_turns += 1
                    else:
                        self.empty_turns = 0
                    self.last_score = self.board.score
                self.pieces.remove(self.selected_piece)
                if len(self.pieces) == 0:
                    self.pieces = get_random_piece_set(self.piece_count, self.difficulty)
                self.selected_piece = None

    def check_victory(self):
        return self.board.score >= self.win_score

    def check_game_over(self):
        if self.difficulty == "dificil" and self.empty_turns >= 4:
            return True
        return self.board.is_game_over(self.pieces)
