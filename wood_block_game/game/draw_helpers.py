# game/draw_helpers.py

def draw_available_pieces(screen, pieces, board, highlight=None):
    import pygame

    total_width = len(pieces) * 100
    start_x = (800 - total_width) // 2
    y_offset = board.margin_top + board.rows * board.cell_size + 40

    for i, piece in enumerate(pieces):
        piece_x = start_x + i * 100
        for r, c in piece.shape:
            x = piece_x + c * 20
            y = y_offset + r * 20

            if piece == highlight:
                glow_rect = pygame.Rect(x - 2, y - 2, 22, 22)
                pygame.draw.rect(screen, (0, 255, 255), glow_rect, border_radius=6)

            pygame.draw.rect(screen, piece.color, (x, y, 18, 18), border_radius=4)
