import pygame
import config as conf
# import cores
import random

from tiro import TiroInimigo
from hitbox import Hitbox
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carregar a imagem do inimigo
        imagem_original = pygame.image.load("sprites/inimigo.png").convert_alpha()
        self.image = imagem_original

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, conf.LARGURA_TELA - self.rect.width)
        self.rect.y = random.randint(-100, -40)

        self.hitbox = Hitbox(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        
        # Velocidade
        self.velocidade = random.randint(2, 6)
        # hp inimigo
        self.hp = 1

        # Variáveis de posição float
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y

    def update(self):
        """
        Atualiza a posição do inimigo e redefine-o quando sai da tela.
        """
        self.y_pos += self.velocidade

        if self.rect.top > conf.ALTURA_TELA:
            # Reposiciona o inimigo acima da tela
            self.x_pos = random.randint(0, conf.LARGURA_TELA - self.rect.width)
            self.y_pos = random.randint(-100, -40)
            self.velocidade = random.randint(2, 8)

        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

        self.hitbox.rect.x = self.rect.x
        self.hitbox.rect.y = self.rect.y

    def mudar_posicao(self, nova_x, nova_y):
        """
        Altera a posição do inimigo para as coordenadas especificadas e atualiza rect e hitbox.

        :param nova_x: Nova coordenada X
        :param nova_y: Nova coordenada Y
        """
        # Atualiza as posições internas
        self.x_pos = nova_x
        self.y_pos = nova_y

        # Atualiza o rect com os novos valores
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

        # Atualiza a hitbox com os novos valores
        self.hitbox.rect.x = self.rect.x
        self.hitbox.rect.y = self.rect.y
