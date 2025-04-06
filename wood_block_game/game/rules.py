# game/rules.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR

def show_rules(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    big_font = pygame.font.SysFont("Arial Black", 30)

    rules_text = [
        "REGRAS DO JOGO:",
        "- Clique em uma peça abaixo para selecioná-la.",
        "- Mire no tabuleiro para ver a sombra da peça.",
        "- Clique novamente para posicionar a peça.",
        "- Preencha linhas ou colunas inteiras para ganhar pontos.",
        "- Ao atingir a pontuação alvo, você vence!",
        "- Se não houver mais movimentos possíveis, é derrota.",
    ]

    back_button = pygame.Rect(20, 20, 40, 40)

    while True:
        screen.fill(BG_COLOR)

        # Título
        title = big_font.render("Regras", True, (255, 182, 193))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        # Texto das regras
        for i, line in enumerate(rules_text):
            rendered = font.render(line, True, (30, 30, 30))
            screen.blit(rendered, (80, 120 + i * 40))

        # Desenhar a seta
        pygame.draw.polygon(screen, (120, 120, 255), [
            (back_button.right, back_button.top),
            (back_button.left, back_button.centery),
            (back_button.right, back_button.bottom)
], 0)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
