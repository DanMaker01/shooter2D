import pygame
import config as conf
# import cores
import random
from inimigo import Inimigo
from tiro import TiroInimigo
from hitbox import Hitbox
class Boss(Inimigo):
    def __init__(self, gerenciador):
        super().__init__()
        
        # Carrega a imagem de Boss
        self.image = pygame.image.load("sprites/boss.png").convert_alpha()
        # Posição inicial usando floats
        self.x = 0.5 * (conf.LARGURA_TELA - self.rect.width)
        self.y = 0
        
        # Atribuição inicial ao rect
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        self.velocidade = 1
        self.hp_max = 300
        self.hp = self.hp_max

        self.gerenciador = gerenciador
        self.timer = 0

    def update(self):
        """
        Atualiza a posição do boss e redefine-o quando sai da tela.
        """
        # Atualiza as posições com floats
        self.x += self.velocidade / 2
        self.y += self.velocidade / 9

        # Atualiza o rect com valores arredondados
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        # Reseta a posição se sair da tela
        if self.rect.left > conf.LARGURA_TELA:
            self.x = 0-self.rect.width  # Usar variável float
            self.rect.x = round(self.x - self.rect.width)

        self.timer += 1

        if self.timer % 100 == 0:
            self.flor(n=16)

        if self.timer % 139 == 0:
            self.flor(360, 5, 200, random.randint(0, 360))

        # Atualiza a hitbox
        self.hitbox.rect.x = self.rect.x
        self.hitbox.rect.y = self.rect.y

    
    def atirar(self):
        tiro = TiroInimigo(self.rect.centerx, self.rect.bottom, 200, 270)
        self.gerenciador.adicionar_tiro_inimigo(tiro)

    def flor(self, r=360, n=36, v=200, a=0):
        for i in range(n):
            tiro = TiroInimigo(self.rect.centerx, self.rect.bottom, v, (r/n)*i + a) ## IMPLEMENTAR, formato do feixe
            self.gerenciador.adicionar_tiro_inimigo(tiro)
    def dano(self):
        self.hp -= 1
        pass
