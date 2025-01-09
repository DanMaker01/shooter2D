import pygame
import config as conf
from tiro import Tiro
#import cores


class Nave(pygame.sprite.Sprite):
    def __init__(self, gerenciador):
        super().__init__()
        # Carregar a imagem da nave
        imagem_original = pygame.image.load("sprites/nave.png").convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (50, 40))  # Ajuste para o tamanho desejado
        
        self.rect = self.image.get_rect()
        self.rect.centerx = conf.LARGURA_TELA // 2
        self.rect.bottom = conf.ALTURA_TELA - 10
        self.velocidade = 4
        self.gerenciador = gerenciador  # Referência ao GerenciadorObjetos
        self.tempo_recarga = 0  # Tempo para controlar a taxa de tiro
        self.tempo_recarga_max = 20

    def update(self):
        """
        Atualiza o movimento da nave e gerencia os tiros.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.right < conf.LARGURA_TELA:
            self.rect.x += self.velocidade

        # Atirar continuamente enquanto o SPACE está pressionado
        if keys[pygame.K_SPACE]:
            self.atirar()

        # Atualiza o tempo de recarga
        if self.tempo_recarga > 0:
            self.tempo_recarga -= 1

    def atirar(self):
        """
        Gera tiros no gerenciador, com uma taxa de disparo controlada.
        """
        if self.tempo_recarga == 0:  # Só atira se a recarga estiver zerada
            qtd = 5  # Quantidade de tiros, melhor que seja impar
            for i in range(qtd):
                x_ajuste = 11 * (i - (qtd / 2))
                tiro = Tiro(self.rect.centerx + x_ajuste, self.rect.top)
                self.gerenciador.adicionar_tiro(tiro)
            self.tempo_recarga = self.tempo_recarga_max  # Ajuste para definir a taxa de disparo
