import pygame
import config as conf
# import cores
import random
from inimigo import Inimigo
from tiro import TiroInimigo
from hitbox import Hitbox

class Boss(Inimigo):
    def __init__(self,gerenciador):
        
        super().__init__()
        self.rect.x = 0.5*(conf.LARGURA_TELA - self.rect.width)
        self.rect.y = 20
        self.velocidade = 1
        
        self.hp_max = 100
        self.hp = self.hp_max

        self.gerenciador = gerenciador
        self.timer = 0

        self.hitbox = Hitbox(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        pass

    def update(self):
        """
        Atualiza a posição do inimigo e redefine-o quando sai da tela.
        """

        self.rect.y += self.velocidade/2
        self.rect.x += self.velocidade/2
        
        if self.rect.left > conf.LARGURA_TELA:
            # Reposiciona o inimigo acima da tela
            self.rect.x = 0
            self.rect.y = 0

        self.timer += 1

        if self.timer%100==0:
            self.flor(n=16)
            pass
        
        if self.timer%139==0:
            self.flor(360,3,200,random.randint(0,360))

        self.hitbox.rect.x = self.rect.x
        self.hitbox.rect.y = self.rect.y
        # print("boss x:", self.rect.x, "y:", self.rect.y)
        pass

    
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
