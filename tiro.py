import pygame
import cores


# Classe do Tiro

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(cores.BRANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidade = -20

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()
