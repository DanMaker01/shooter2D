import pygame


class Hitbox:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)

    def verificar_colisao(self, outra_hitbox):
        """Verifica se essa hitbox colide com outra hitbox."""
        return self.rect.colliderect(outra_hitbox.rect)
