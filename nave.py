import pygame
import config as conf
from tiro import Tiro
import cores


# Classe da Nave
class Nave(pygame.sprite.Sprite):
    def __init__(self, gerenciador):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(cores.AZUL)
        self.rect = self.image.get_rect()
        self.rect.centerx = conf.LARGURA_TELA // 2
        self.rect.bottom = conf.ALTURA_TELA - 10
        self.velocidade = 4
        self.gerenciador = gerenciador  # Referência ao GerenciadorObjetos

    def processar_evento_teclado(self, evento):
        """
        Processa eventos relacionados às teclas pressionadas.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                self.atirar()

    def update(self):
        """
        Atualiza o movimento da nave com base nas teclas pressionadas.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.right < conf.LARGURA_TELA:
            self.rect.x += self.velocidade

    def atirar(self):
        """
        Chamado quando o jogador pressiona espaço.
        Gera tiros no gerenciador.
        """
        qtd = 3  # Quantidade de tiros, melhor que seja impar
        for i in range(qtd):
            x_ajuste = i - (qtd / 2)
            tiro = Tiro(self.rect.centerx + x_ajuste, self.rect.top)
            self.gerenciador.adicionar_tiro(tiro)
