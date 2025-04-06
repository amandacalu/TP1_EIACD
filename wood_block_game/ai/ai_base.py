# ai/ai_base.py
class AIBase:
    def __init__(self, board, pieces, difficulty):
        self.board = board
        self.pieces = pieces
        self.difficulty = difficulty
        self.moves = []  # histórico de jogadas
        self.steps = 0

    def run(self):
        """
        Executa a IA até o fim do jogo.
        Deve ser implementado nas classes filhas.
        """
        raise NotImplementedError("Método run() deve ser implementado pela IA específica.")
