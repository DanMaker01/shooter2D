import pygame
import cores


# Classe do Tiro
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade_magnitude, angulo):
        """
        Inicializa o tiro.
        :param x: Posição x inicial.
        :param y: Posição y inicial.
        :param velocidade_magnitude: Magnitude da velocidade (intensidade).
        :param angulo: Ângulo em graus (direção do tiro).
        """
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(cores.BRANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Define a velocidade como um vetor 2D com base na magnitude e ângulo
        self.velocidade = pygame.math.Vector2()
        self.velocidade.from_polar((velocidade_magnitude, angulo))  # Vetor a partir da magnitude e do ângulo

    def update(self):
        """
        Atualiza a posição do tiro de acordo com sua velocidade.
        """
        # Move o tiro com base na velocidade
        self.rect.x += self.velocidade.x
        self.rect.y -= self.velocidade.y

        # Remove o tiro se sair da tela
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height() \
                or self.rect.left > pygame.display.get_surface().get_width() or self.rect.right < 0:
            self.kill()
