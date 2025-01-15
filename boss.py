import pygame
import config as conf
# import cores
import random
from inimigo import Inimigo
from tiro import TiroInimigo
from hitbox import Hitbox
from rota import Rota

class Boss(Inimigo):
    def __init__(self, gerenciador):
        super().__init__()
        
        # Carrega a imagem de Boss
        self.image = pygame.image.load("sprites/boss.png").convert_alpha()
        # self.x = 0.5 * (conf.LARGURA_TELA - self.rect.width)
        # self.y = 50

        # Posição inicial usando floats
        self.x_pos = (3/4)*conf.LARGURA_TELA #- self.rect.width/2
        self.y_pos = (1/8)*conf.ALTURA_TELA #- self.rect.height/2
        
        # Atribuição inicial ao rect
        self.rect.x = round(self.x_pos)
        self.rect.y = round(self.y_pos)

        self.velocidade = 1
        self.hp_max = 150
        self.hp = self.hp_max

        self.gerenciador = gerenciador
        self.timer = 0


        self.delta_x = 0
        self.delta_y = 0
        self.se_movendo_agora = False
        self.rota = Rota()
        pass

    def definir_rota(self,vetor_pos, vetor_tempo):
        for i in range(len(vetor_pos)):
            self.rota.rota_add(vetor_pos[i],vetor_tempo[i])
        pass

    def update(self):
        """
        Atualiza a posição do boss de acordo com a rota e redefine-o se sair da tela.
        """
        # ------------------------------------------------------------------------
        # Mover na rota
        if self.rota.len_rota() != 0:  # Verifica se a rota não está vazia
            if self.se_movendo_agora:
                # Continua movendo
                posicao_desejada, tempo_desejado = self.rota.rota_get_item_atual()
                posicao_atual = (self.x_pos, self.y_pos)

                # Atualiza a posição com delta
                self.x_pos += self.delta_x
                self.y_pos += self.delta_y

                # Verifica se chegou ao destino (com tolerância de 1 pixel)
                if abs(self.x_pos - posicao_desejada[0]) < 1 and abs(self.y_pos - posicao_desejada[1]) < 1:
                    self.x_pos, self.y_pos = posicao_desejada  # Garante que atinja a posição exata
                    self.delta_x = 0
                    self.delta_y = 0
                    self.se_movendo_agora = False
                    self.rota.rota_avancar_item()  # Pega o próximo item da rota
            else:
                # Inicia movimento para o próximo ponto da rota
                posicao_desejada, tempo_desejado = self.rota.rota_get_item_atual()
                posicao_atual = (self.x_pos, self.y_pos)

                # Calcula a velocidade necessária para atingir a posição no tempo desejado
                if tempo_desejado > 0:
                    self.delta_x = (posicao_desejada[0] - posicao_atual[0]) / tempo_desejado
                    self.delta_y = (posicao_desejada[1] - posicao_atual[1]) / tempo_desejado
                else:
                    self.delta_x = self.delta_y = 0  # Evita divisão por zero

                self.se_movendo_agora = True

        # ------------------------------------------------------------------------
        # ------------------------------------------------------------------------
        # Atualiza o rect com valores arredondados
        self.rect.x = round(self.x_pos)
        self.rect.y = round(self.y_pos)
        # Atualiza a hitbox baseada no rect da classe sprite
        self.hitbox.rect.x = self.rect.x
        self.hitbox.rect.y = self.rect.y
        # ------------------------------------------------------------------------
        # Executa eventos baseados no timer
        if self.timer % 100 == 0:
            self.flor(n=16)

        if self.timer % 139 == 0:
            self.flor(360, 5, 200, random.randint(0, 360))

        # ------------------------------------------------------------------------
        # Controle de tempo
        self.timer += 1

    
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
