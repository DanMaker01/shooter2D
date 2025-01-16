import pygame
import config as conf
import random
from inimigo import Inimigo
from tiro import TiroInimigo
from hitbox import Hitbox
from rota import Rota

class Boss(Inimigo):
    def __init__(self, gerenciador):
        super().__init__()
        
        # Carrega a imagem do boss
        self.image = pygame.image.load("sprites/boss.png").convert_alpha()
        
        # Define a posição inicial usando floats para precisão
        self.x_pos = 0
        self.y_pos = 0
        
        # Inicializa o rect do boss
        self.rect.x = round(self.x_pos)
        self.rect.y = round(self.y_pos)

        self.velocidade = 1
        self.hp_max = 200
        self.hp = self.hp_max

        # Gerenciador de entidades e inicialização do timer
        self.gerenciador = gerenciador
        self.timer = 0

        # Controle de rota e movimento
        self.delta_x = 0
        self.delta_y = 0
        self.se_movendo_agora = False
        self.rota = Rota()

    def definir_rota(self, vetor_pos, vetor_tempo):
        """
        Define a rota do boss adicionando posições e tempos correspondentes.
        """
        for pos, tempo in zip(vetor_pos, vetor_tempo):
            self.rota.rota_add(pos, tempo)

    def update(self):
        """
        Atualiza a posição do boss com base na rota e realiza eventos baseados no tempo.
        """
        if self.rota.len_rota() > 0:  # Verifica se há itens na rota
            # print("update: self.timer = ", self.timer)
            if self.se_movendo_agora:
                # print("continuar movimento")
                self._continuar_movimento()
            else:
                # está começando atrasado em 1 tick @@@@@@@@@@@
                # começa a mover
                # print("iniciar NOVO movimento!")
                self._iniciar_movimento()

        # Atualiza as posições do rect e da hitbox
        self.rect.x = round(self.x_pos)
        self.rect.y = round(self.y_pos)
        self.hitbox.rect.x = self.rect.x
        self.hitbox.rect.y = self.rect.y

        # Eventos baseados no tempo
        self._executar_eventos_tempo()

        # Incrementa o timer
        self.timer += 1

    def _continuar_movimento(self):
        """
        Continua o movimento em direção ao próximo ponto da rota.
        """
        posicao_desejada, _ = self.rota.rota_get_item_atual()

        # Atualiza a posição com os deltas
        self.x_pos += self.delta_x
        self.y_pos += self.delta_y

        # Verifica se o boss chegou ao destino
        if abs(self.x_pos - posicao_desejada[0]) < 1 and abs(self.y_pos - posicao_desejada[1]) < 1:
            self.x_pos, self.y_pos = posicao_desejada
            self.delta_x = 0
            self.delta_y = 0
            self.se_movendo_agora = False
            self.rota.rota_avancar_item()  # Avança para o próximo ponto
            self.rect.x = round(self.x_pos)
            self.rect.y = round(self.y_pos)
            self.hitbox.rect.x = self.rect.x
            self.hitbox.rect.y = self.rect.y
            
            pass
        pass

    def _iniciar_movimento(self):
        """
        Calcula os deltas necessários para o próximo ponto da rota.
        """
        posicao_desejada, tempo_desejado = self.rota.rota_get_item_atual()
        posicao_atual = (self.x_pos, self.y_pos)
        
        # if self.timer == 198:
        #     print("_iniciar_movimento: self.timer = 198")
        # if self.timer == 199:
        #     print("_iniciar_movimento: self.timer = 199")
        # if self.timer == 200:
        #     print("_iniciar_movimento: self.timer = 200")
        # if self.timer == 201:
        #     print("_iniciar_movimento: self.timer = 201")
        print("VAI INICIAR MOVIMENTO!! posicao atual:", posicao_atual, "posicao desejada:", posicao_desejada, "tempo_atual", self.timer, "tempo_desejado", tempo_desejado)

        if tempo_desejado > 0:
            self.delta_x = (posicao_desejada[0] - posicao_atual[0]) / tempo_desejado
            self.delta_y = (posicao_desejada[1] - posicao_atual[1]) / tempo_desejado
        else:
            self.delta_x = self.delta_y = 0

        self.se_movendo_agora = True

    def _executar_eventos_tempo(self):
        """
        Executa eventos baseados no tempo.
        """
        fase = 3
        if self.timer != 0:

            if self.timer % 200 == 0:
                
                self.flor(n=16, v=320, a=1*fase)
                self.flor(n=16, v=300, a=2*fase)
                self.flor(n=16, v=280, a=3*fase)
                self.flor(n=16, v=260, a=4*fase)
                # self.flor(n=16, v=240, a=5*fase)
                print(f"Flor - Tempo: {self.timer}")
            
            if self.timer % 900 == 0:
                self.flor(n=16, v=320, a=1*fase)
                self.flor(n=16, v=300, a=2*fase)
                self.flor(n=16, v=280, a=3*fase)
                self.flor(n=16, v=260, a=4*fase)
                self.flor(n=16, v=240, a=5*fase)

                self.flor(n=16, v=220, a=-1*fase)
                self.flor(n=16, v=200, a=-2*fase)
                self.flor(n=16, v=180, a=-3*fase)
                self.flor(n=16, v=160, a=-4*fase)
                self.flor(n=16, v=140, a=-5*fase)
                print(f"Flor - Tempo: {self.timer}")
        
        # if self.timer % 150 == 0:
        #     self.flor(n=8,v=200)
        #     print(f"Flor - Tempo: {self.timer}")

    def atirar(self):
        """
        Atira um projétil básico.
        """
        tiro = TiroInimigo(self.rect.centerx, self.rect.bottom, 200, 270)
        self.gerenciador.adicionar_tiro_inimigo(tiro)

    def flor(self, r=360, n=36, v=200, a=0):
        """
        Dispara projéteis em padrão circular.
        """
        for i in range(n):
            angulo = (r / n) * i + a
            tiro = TiroInimigo(self.rect.centerx, self.rect.bottom, v, angulo)
            self.gerenciador.adicionar_tiro_inimigo(tiro)

    def dano(self):
        """
        Aplica dano ao boss.
        """
        self.hp -= 1
