# game/pieces.py
import random

class Piece:
    def __init__(self, shape, color=(100, 180, 255)):
        self.shape = shape  # lista de coordenadas relativas [(0,0), (1,0), ...]
        self.color = color

def get_random_piece_set(quantity, level="facil"):
    base_pieces = [
        Piece([(0, 0), (1, 0)]),                     # I
        Piece([(0, 0), (0, 1)]),                     # -
        Piece([(0, 0), (1, 0), (1, 1)]),             # L
        Piece([(0, 0), (0, 1), (1, 0)]),             # L invertido
    ]

    if level in ["medio", "dificil"]:
        base_pieces += [
            Piece([(0, 1), (1, 0), (1, 1)]),         # Z
            Piece([(0, 1), (1, 0), (1, 1), (2, 1)])  # T (versão simplificada)
        ]

    return random.sample(base_pieces, quantity) 
