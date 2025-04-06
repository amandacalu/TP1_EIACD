# game/board.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import random

class Board:
    def __init__(self, rows, cols, cell_size, margin_top=100):
        self.empty_moves = 0
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.margin_top = margin_top
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.score = 0
        self.start_x = (800 - self.cols * self.cell_size) // 2  # ou use SCREEN_WIDTH se importar
        num_initial_blocks = random.randint(1, 6)
        for _ in range(num_initial_blocks):
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.grid[r][c] = 1

    def place(self, piece, row, col):
        for r, c in piece.shape:
            pr = row + r
            pc = col + c
            if 0 <= pr < self.rows and 0 <= pc < self.cols:
                self.grid[pr][pc] = piece.color



    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                start_x = (SCREEN_WIDTH - self.cols * self.cell_size) // 2
                x = col * self.cell_size + start_x
                y = row * self.cell_size + self.margin_top
                color = (230, 250, 255) if self.grid[row][col] == 0 else (100, 180, 255)
                pygame.draw.rect(screen, color, (x, y, self.cell_size - 2, self.cell_size - 2), border_radius=6)

    def can_place(self, piece, row, col):
        for r, c in piece.shape:
            r_pos = row + r
            c_pos = col + c
            if r_pos < 0 or r_pos >= self.rows or c_pos < 0 or c_pos >= self.cols:
                return False
            if self.grid[r_pos][c_pos] != 0:
                return False
        return True

    def place_piece(self, piece, row, col):
        if self.can_place(piece, row, col):
            points_before = self.score
            for r, c in piece.shape:
                self.grid[row + r][col + c] = 1
            self.check_and_clear_lines()
            if points_before == self.score:
                self.empty_moves += 1
            else:
                self.empty_moves = 0
            return True
        return False


    def check_and_clear_lines(self):
        full_rows = [i for i in range(self.rows) if all(self.grid[i])]
        full_cols = [j for j in range(self.cols) if all(self.grid[i][j] for i in range(self.rows))]

        for i in full_rows:
            self.grid[i] = [0] * self.cols
            self.score += 100

        for j in full_cols:
            for i in range(self.rows):
                self.grid[i][j] = 0
            self.score += 100

    def is_game_over(self, pieces):
        for piece in pieces:
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.can_place(piece, row, col):
                        return False
        return True
