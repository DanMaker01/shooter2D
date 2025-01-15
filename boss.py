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
        self.x_pos = (3 / 4) * conf.LARGURA_TELA
        self.y_pos = (1 / 8) * conf.ALTURA_TELA
        
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
            if self.se_movendo_agora:
                self._continuar_movimento()
            else:
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

    def _iniciar_movimento(self):
        """
        Calcula os deltas necessários para o próximo ponto da rota.
        """
        posicao_desejada, tempo_desejado = self.rota.rota_get_item_atual()
        posicao_atual = (self.x_pos, self.y_pos)

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
        if self.timer % 100 == 0:
            self.flor(n=16)
            print(f"Flor - Tempo: {self.timer}")

        if self.timer % 139 == 0:
            self.flor(r=360, n=5, v=200, a=random.randint(0, 360))

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
