from math import sin
import math
import pygame
import config as conf
from tiro import Tiro
from hitbox import Hitbox
import random

class Nave(pygame.sprite.Sprite):
    def __init__(self, gerenciador):
        super().__init__()
        # Carregar a imagem da nave
        imagem_original = pygame.image.load("sprites/nave.png").convert_alpha()
        self.image = imagem_original
        
        # Definir o retangulo da nave
        self.rect = self.image.get_rect()
        self.rect.x = conf.LARGURA_TELA // 2
        self.rect.y = conf.ALTURA_TELA - 100
        
        # Variáveis de posição flutuante (ações são feitas nas posições flutuantes, 
        # para depois serem convertidas em inteiros para serem aceitos por rect.x e rect.y)----------------------------------
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y

        # Definir hitbox centralizada reduzida-----------------------------
        self.hitbox_escala = 0.10
        self.hitbox = Hitbox(0,0, self.rect.width*self.hitbox_escala, self.rect.height*self.hitbox_escala)

        # Variáveis de movimento -------------------------------------------
        self.velocidade = 1500
        self.velocidade_focado = 300
        self.gerenciador = gerenciador  # Referência ao GerenciadorObjetos
        
        # Controle de tiros ------------------------------------------------
        self.tempo_recarga = 0  # Tempo para controlar a taxa de tiro
        self.tempo_recarga_max = 25
        
        self.tempo_recarga_bomba = 0  # Tempo para controlar o cooldown da bomba
        self.tempo_recarga_bomba_max = 500  # Tempo máximo de cooldown para a bomba
        
        self.focado = False

        pass

    def update(self):
        """
        Atualiza o movimento da nave e gerencia os tiros.
        """
        # super().update()
        keys = pygame.key.get_pressed()
        
        # MOVIMENTO (utilizando x_pos e y_pos para movimento suave)-----------
        if keys[pygame.K_LEFT] and self.x_pos > 0:
            if self.focado:
                self.x_pos -= self.velocidade_focado / 1000
            else:
                self.x_pos -= self.velocidade / 1000

        if keys[pygame.K_RIGHT] and self.x_pos < conf.LARGURA_TELA-self.rect.width:
            if self.focado:
                self.x_pos += self.velocidade_focado / 1000
            else:
                self.x_pos += self.velocidade / 1000
        
        # Atualiza o rect.x e rect.y com base na posição flutuante
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)
        # Atualiza a hitbox
        self.hitbox.rect.x = self.rect.x + ( self.rect.width * (1-self.hitbox_escala) / 2)
        self.hitbox.rect.y = self.rect.y + ( self.rect.height * (1-self.hitbox_escala) / 2)

        # BOMBA!!! (controle de cooldown da bomba)------------------------------------------
        if keys[pygame.K_x] or keys[pygame.K_SPACE]:
            if self.tempo_recarga_bomba == 0:
                #gera as 5 flores, cada uma com sua velocidade inicial
                velocidades = [300, 400, 500, 580, 660]
                for vel in velocidades:  # Distâncias das bombas
                    self.bomba(velocidade=vel, fase=(vel/velocidades[-1])*360)

                # Define o cooldown da bomba
                self.tempo_recarga_bomba = self.tempo_recarga_bomba_max
            else:
                pass # Se ainda estiver recarregando a bomba, não faz nada.
            
        # ATIRAR continuamente enquanto o "Z" está pressionado
        if keys[pygame.K_z]:
            self.atirar()  # Atirar

        # Focar/desfocar---------------------------------------------------------
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
        
        # -----------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------
        pass

    def desenhar_hitbox(self, tela):
        """Desenha a hitbox com uma cor para visualização."""
        pygame.draw.rect(tela, (255, 0, 0), self.hitbox.rect, 4)  # Desenha a hitbox em vermelho (2px de espessura)        
        pass
    
    from math import sin
    
    def atirar(self):
        """
        Gera tiros no gerenciador, com uma taxa de disparo controlada.
        """
        if self.tempo_recarga == 0:  # Só atira se a recarga estiver zerada
            if not self.focado:  # Desfocado
                ranges = 9
                for i in range(ranges):
                    tiro = Tiro(self.rect.centerx, self.rect.top, 
                                1000+2000*sin(math.radians(180/(ranges-1) * i)),    # velocidade
                                180 - (180/(ranges-1)) * i+21)                         # angulo
                    self.gerenciador.adicionar_tiro(tiro)
                    
                    tiro = Tiro(self.rect.centerx, self.rect.top, 
                                1000+2000*sin(math.radians(180/(ranges-1) * i)),    # velocidade
                                180 - (180/(ranges-1)) * i-21)                         # angulo
                    self.gerenciador.adicionar_tiro(tiro)
                    
                self.tempo_recarga = 3 * self.tempo_recarga_max  # Ajuste para definir a taxa de disparo 
            else: # Focado
                for i in range(2):
                    tiro = Tiro(self.rect.centerx, self.rect.top, 1000-200*i, 90 + 2 * i)
                    self.gerenciador.adicionar_tiro(tiro)
                    tiro = Tiro(self.rect.centerx, self.rect.top, 1000-200*i, 90 - 2 * i)
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
