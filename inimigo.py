
import pygame

import config as conf
import cores
import random

# Classe do Inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(cores.VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, conf.LARGURA_TELA - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = random.randint(2, 6)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > conf.ALTURA_TELA:
            self.rect.x = random.randint(0, conf.LARGURA_TELA - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidade = random.randint(2, 6)