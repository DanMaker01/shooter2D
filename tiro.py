import pygame
import cores
import math

class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade, angulo):
        """
        Inicializa o tiro.
        :param x: Posição x inicial do tiro.
        :param y: Posição y inicial do tiro.
        :param velocidade: Velocidade escalar do tiro.
        :param angulo: Direção do tiro em graus.
        """
        super().__init__()
        # Criação do sprite do tiro
        self.image = pygame.Surface((10, 10))  # Tamanho do tiro
        self.image.fill(cores.BRANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Define a posição inicial

        # Vetor de posição
        self.posicao = pygame.math.Vector2(x, y)
        
        # Vetor de velocidade
        radiano = math.radians(angulo)
        self.velocidade = pygame.math.Vector2(
            velocidade * math.cos(radiano),
            -velocidade * math.sin(radiano)  # Negativo para mover para cima
        )

    def update(self):
        """
        Atualiza a posição do tiro com base em sua velocidade.
        """
        # Atualiza a posição do tiro
        self.posicao += self.velocidade

        # Atualiza a posição do rect com base no vetor de posição
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))

        # Remove o tiro se sair da tela
        largura_tela = pygame.display.get_surface().get_width()
        altura_tela = pygame.display.get_surface().get_height()
        if (self.rect.right < 0 or self.rect.left > largura_tela or 
            self.rect.bottom < 0 or self.rect.top > altura_tela):
            self.kill()
