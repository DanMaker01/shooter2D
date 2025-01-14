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
        # self.image = pygame.transform.scale(imagem_original, (64, 20))  # Ajuste para o tamanho desejado
        self.image = imagem_original
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, conf.LARGURA_TELA - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.hitbox = Hitbox(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.velocidade = random.randint(2, 6)

    def update(self):
        """
        Atualiza a posição do inimigo e redefine-o quando sai da tela.
        """
        self.hitbox.rect.x = self.rect.x
        self.hitbox.rect.y = self.rect.y
        
        self.rect.y += self.velocidade
        if self.rect.top > conf.ALTURA_TELA:
            # Reposiciona o inimigo acima da tela
            self.rect.x = random.randint(0, conf.LARGURA_TELA - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidade = random.randint(2, 8)


# IMPLEMENTAR @@@@
    # def atirar(self):
    #     tiro = TiroInimigo(self.rect.centerx, self.rect.top, 20, 270)
    #     self.gerenciador.adicionar_tiro_inimigo(tiro)