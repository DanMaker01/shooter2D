import pygame
import config as conf
from tiro import Tiro
from hitbox import Hitbox

class Nave(pygame.sprite.Sprite):
    def __init__(self, gerenciador):
        super().__init__()
        # Carregar a imagem da nave
        imagem_original = pygame.image.load("sprites/nave.png").convert_alpha()
        self.image = imagem_original
        
        self.rect = self.image.get_rect()
        self.rect.x = conf.LARGURA_TELA // 2
        self.rect.y = conf.ALTURA_TELA - 100
        
        # Variáveis de posição flutuante
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y
        
        # Definir hitbox centralizada
        proporcao = 0.50
        self.hitbox = Hitbox(
            self.rect.x + (self.rect.width / 2),
            self.rect.y + (self.rect.height / 2),
            self.rect.width * proporcao,
            self.rect.height * proporcao)

        self.velocidade = 2000
        self.velocidade_focado = 500
        self.gerenciador = gerenciador  # Referência ao GerenciadorObjetos
        
        self.tempo_recarga = 0  # Tempo para controlar a taxa de tiro
        self.tempo_recarga_max = 20
        
        self.tempo_recarga_bomba = 0  # Tempo para controlar o cooldown da bomba
        self.tempo_recarga_bomba_max = 100  # Tempo máximo de cooldown para a bomba
        
        self.focado = False

    def update(self):
        """
        Atualiza o movimento da nave e gerencia os tiros.
        """
        # super().update()
        keys = pygame.key.get_pressed()
        
        # MOVIMENTO (utilizando x_pos e y_pos para movimento suave)
        if keys[pygame.K_LEFT] and self.x_pos > 0:
            if self.focado:
                self.x_pos -= self.velocidade_focado / 1000
            else:
                self.x_pos -= self.velocidade / 1000

        if keys[pygame.K_RIGHT] and self.x_pos < conf.LARGURA_TELA:
            if self.focado:
                self.x_pos += self.velocidade_focado / 1000
            else:
                self.x_pos += self.velocidade / 1000
        
        # Atualiza o rect.x com base na posição flutuante
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)

        # Atualiza a hitbox
        self.hitbox.rect.x = self.rect.x + self.rect.width * 0.25
        self.hitbox.rect.y = self.rect.y + self.rect.height * 0.25

        # BOMBA!!! (controle de cooldown da bomba)
        if keys[pygame.K_x] or keys[pygame.K_SPACE]:
            if self.tempo_recarga_bomba == 0:
                for vel in [300, 400, 500, 580, 660]:  # Distâncias das bombas
                    self.bomba(velocidade=vel)

                # Define o cooldown da bomba
                self.tempo_recarga_bomba = self.tempo_recarga_bomba_max
            else:
                pass
            
        # ATIRAR continuamente enquanto o SPACE está pressionado
        if keys[pygame.K_z]:
            self.atirar()  # Atirar

        # Focar/desfocar
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.focar()
        else:
            self.desfocar()

        # Atualiza o tempo de recarga
        if self.tempo_recarga > 0:
            self.tempo_recarga -= 1

        # Atualiza o cooldown da bomba
        if self.tempo_recarga_bomba > 0:
            self.tempo_recarga_bomba -= 1

    def desenhar_hitbox(self, tela):
        """Desenha a hitbox com uma cor para visualização."""
        pygame.draw.rect(tela, (255, 0, 0), self.hitbox.rect, 4)  # Desenha a hitbox em vermelho (2px de espessura)        

    def atirar(self):
        """
        Gera tiros no gerenciador, com uma taxa de disparo controlada.
        """
        if self.tempo_recarga == 0:  # Só atira se a recarga estiver zerada
            if not self.focado:  # Focado
                for i in range(5):
                    tiro = Tiro(self.rect.centerx, self.rect.top, 2000, 180 - 45 * i)
                    self.gerenciador.adicionar_tiro(tiro)
                    
                self.tempo_recarga = 3 * self.tempo_recarga_max  # Ajuste para definir a taxa de disparo
            else:
                for i in range(2):
                    tiro = Tiro(self.rect.centerx, self.rect.top, 1000, 90 + 2 * i)
                    self.gerenciador.adicionar_tiro(tiro)
                    tiro = Tiro(self.rect.centerx, self.rect.top, 1000, 90 - 2 * i)
                    self.gerenciador.adicionar_tiro(tiro)

                self.tempo_recarga = self.tempo_recarga_max  # Ajuste para definir a taxa de disparo

    def bomba(self, qtd=36, velocidade=2000, fase=0):
        """
        Gera tiros em todas as direções (bomba), com cooldown.
        """
        for i in range(qtd):
            tiro = Tiro(self.rect.centerx, self.rect.top, velocidade, i * (360 / qtd) + fase)
            self.gerenciador.adicionar_tiro(tiro)
        
    def focar(self):
        self.focado = True

    def desfocar(self):
        self.focado = False
