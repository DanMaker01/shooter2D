import math
import pygame
from config import *
import cores

from nave import Nave
from gerenciador import GerenciadorObjetos
from inimigo import Inimigo
from boss import Boss

# ---------------------------------------------------------------------------------------------------------
class EstadoBase: #classe abstrata
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.timer = 0

    def processar_eventos(self, eventos):
        pass

    def atualizar(self):
        pass

    def desenhar(self, tela):
        pass
# ---------------------------------------------------------------------------------------------------------

class MenuInicial(EstadoBase):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.fonte = pygame.font.SysFont("Arial", 48)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.gerenciador.sair_jogo()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                # self.gerenciador.trocar_estado("fase1")
                self.gerenciador.trocar_estado("fase2")

    def desenhar(self, tela):
        tela.fill(cores.PRETO)
        titulo = self.fonte.render("Shooter Vertical", True, cores.BRANCO)
        instrucao = pygame.font.SysFont("Arial", 24).render("Pressione ENTER para jogar", True, cores.BRANCO)
        controles1 = pygame.font.SysFont("Arial", 24).render("Z - atirar", True, cores.BRANCO)
        controles2= pygame.font.SysFont("Arial", 24).render("SHIFT - focar", True, cores.BRANCO)
        controles3 = pygame.font.SysFont("Arial", 24).render("ESPAÇO (ou X) - bomba", True, cores.BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 2 - 200))
        tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, ALTURA_TELA // 2 + 300))
        tela.blit(controles1, ((LARGURA_TELA // 2 - instrucao.get_width() // 2), ALTURA_TELA // 2 ))
        tela.blit(controles2, ((LARGURA_TELA // 2 - instrucao.get_width() // 2), ALTURA_TELA // 2 +30))
        tela.blit(controles3, ((LARGURA_TELA // 2 - instrucao.get_width() // 2), ALTURA_TELA // 2 +60))
        pygame.display.flip()

# ---------------------------------------------------------------------------------------------------------

class Fase1(EstadoBase):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        print("fase 1 iniciando, vai reinicar agora")
        self.gerenciador_objetos, self.jogador = self.reiniciar_jogo()
        self.pontuacao = 0
        self.fundo = pygame.image.load("sprites/galaxy.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA_TELA, ALTURA_TELA))

        
    def reiniciar_jogo(self):
        """
        Reinicia o estado do jogo com os objetos necessários.
        Retorna um gerenciador de objetos e o jogador.
        """
        # --------------------------------------------------------
        gerenciador_objetos = GerenciadorObjetos()

        # --------------------------------------------------------
        jogador = Nave(gerenciador_objetos)
        gerenciador_objetos.adicionar_jogador(jogador)

        # --------------------------------------------------------
        boss = Boss(gerenciador_objetos)
        boss.mudar_posicao((1 / 2) * LARGURA_TELA -boss.rect.width/2 , (0/4)* ALTURA_TELA -boss.rect.height/2) #posicao inicial
        # boss.mudar_posicao((3 / 4) * conf.LARGURA_TELA , (1 / 8) * conf.ALTURA_TELA) #posicao inicial
        # --------------------------------------------------------
        # Rota 
        rota_entrada = [ (256,96)]
        rota_entrada_tempo =[ 200] #alguns 199 porque ele tá atrasando movimento

        
        # rota_pos = [ (128,96), (128,288), (384,288), (384,96),
        #             (233,34), (98,169), (278,350), (414,215), (384,96)] #retangulo
        # rota_tempo = [ 99, 99, 99, 99, 99,99,99,99,99]
        # boss.definir_rota(rota_pos, rota_tempo)
        
        
        # adicionar (-boss.rect.width/2, -boss.rect.height/2) em cada elemento
        rota_entrada_centralizada = [(x - boss.rect.width/2, y - boss.rect.height/2) for x, y in rota_entrada]

        boss.definir_rota(rota_entrada_centralizada, rota_entrada_tempo)
        # boss.definir_rota(rota_entrada, rota_entrada_tempo)
        gerenciador_objetos.adicionar_inimigo(boss)


        # --------------------------------------------------------
        # Adiciona inimigos iniciais
        # for i in range(3):
        #     inimigo = Inimigo()
        #     gerenciador_objetos.adicionar_inimigo(inimigo)

        # --------------------------------------------------------

        return gerenciador_objetos, jogador
    
    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.gerenciador.sair_jogo()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_p, pygame.K_ESCAPE]:
                    self.gerenciador.trocar_estado("pause")
                if evento.key == pygame.K_r:
                    self.gerenciador.trocar_estado("fase1")
                

    def atualizar(self):
        self.jogador.update()
        self.gerenciador_objetos.atualizar()
        # self.boss.update() # já é atualizado nos objetos
        estado, pontos = self.gerenciador_objetos.verificar_colisoes()
        self.pontuacao += pontos
        if estado == "fase2":
            self.gerenciador.trocar_estado("fase2")
        if estado == "game_over":
            self.gerenciador.trocar_estado("game_over")

    def desenhar(self, tela):
        #fundo branco
        tela.blit(self.fundo, (0, 0))
        #objetos
        self.gerenciador_objetos.desenhar(tela)
        
        #desenhar HUD
        # Fonte para o texto
        fonte = pygame.font.SysFont("Arial", 24)
        # Exibindo a pontuação
        tela.blit(fonte.render(f"Pontuação: {self.pontuacao}", True, cores.VERMELHO), (10, 10))
        # Exibindo o FPS
        fps = str(int(self.gerenciador.fps))  # Usa o FPS armazenado no gerenciador
        tela.blit(fonte.render(f"FPS: {fps}", True, cores.VERMELHO), (10, 40))
        # Exibindo o número de tiros
        num_tiros = len(self.gerenciador_objetos.tiros)  # Número de tiros do jogador
        tela.blit(fonte.render(f"Tiros: {num_tiros}", True, cores.VERMELHO), (10, 70))
        # Exibindo o número de tiros dos inimigos
        num_inimigos = len(self.gerenciador_objetos.inimigos)  # Número de tiros dos inimigos
        tela.blit(fonte.render(f"Inimigos: {num_inimigos}", True, cores.VERMELHO), (10, 100))
        # Exibindo o número de tiros dos inimigos
        num_tiros_inimigos = len(self.gerenciador_objetos.tiros_inimigos)  # Número de tiros dos inimigos
        tela.blit(fonte.render(f"Tiros Inimigos: {num_tiros_inimigos}", True, cores.VERMELHO), (10, 130))
        
        #exibindo a vida do boss
        if len(self.gerenciador_objetos.inimigos) > 0:
            #verifica se o tipo é Boss ou Inimigo
            if isinstance(self.gerenciador_objetos.inimigos.sprites()[0], Boss):
                inimigo = self.gerenciador_objetos.inimigos.sprites()[0]
                vida_boss = inimigo.hp
                vida_boss_max = inimigo.hp_max
                tela.blit(fonte.render(f"Vida Boss: {vida_boss}/{vida_boss_max}", True, cores.VERMELHO), (10, 160))
                pass
            else:
                
                # inimigo = self.gerenciador_objetos.inimigos.sprites()[0]
                # vida_boss = inimigo.hp
                # vida_boss_max = inimigo.hp_max
                # tela.blit(fonte.render(f"Vida Boss: {vida_boss}/{vida_boss_max}", True, cores.VERMELHO), (10, 160))
                pass
            pass
        
        # Atualizando a tela
        pygame.display.flip()
# ---------------------------------------------------------------------------------------------------------

class Fase2(EstadoBase):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.gerenciador_objetos = None
        self.jogador = None
        self.pontuacao = 0
        self.fundo = pygame.image.load("sprites/galaxy.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA_TELA, ALTURA_TELA))
        self.boss = None
        self.gerenciador_objetos, self.jogador = self.reiniciar_jogo()
        
    def reiniciar_jogo(self):
        """
        Reinicia o estado do jogo com os objetos necessários.
        Retorna um gerenciador de objetos e o jogador.
        """
        # --------------------------------------------------------
        gerenciador_objetos = GerenciadorObjetos()

        # --------------------------------------------------------
        jogador = Nave(gerenciador_objetos)
        gerenciador_objetos.adicionar_jogador(jogador)
        print("criando o boss")
        # --------------------------------------------------------
        self.boss = Boss(gerenciador_objetos)
        self.boss.mudar_posicao(384-self.boss.rect.width/2 , 192) #posicao inicial
        print("boss pos inicial:", self.boss.rect.x, self.boss.rect.y)
        # boss.mudar_posicao((3 / 4) * conf.LARGURA_TELA , (1 / 8) * conf.ALTURA_TELA) #posicao inicial
        # --------------------------------------------------------
        # Rota 
        rota_entrada = []
        # cria os pontos de um circulo de raio 96 com centro em (256, 192) dividido em 16 pontos
        r = 96
        qtd = 16
        vel_entre_cada = 16
        rota_entrada = [(math.cos(2 * math.pi / qtd * i) * r + 256, math.sin(2 * math.pi / qtd * i) * r + 192) for i in range(qtd)]
        # print(rota_entrada)

        # -------------------------------------------------------------------------
        # tempo
        rota_entrada_tempo = []
        for i in range(len(rota_entrada)):
            rota_entrada_tempo.append(vel_entre_cada) 
        
        # posicao centralizada
        # adicionar (-boss.rect.width/2, -boss.rect.height/2) em cada elemento
        rota_entrada_centralizada = [(x - self.boss.rect.width/2, y - self.boss.rect.height/2) for x, y in rota_entrada]

        # -------------------------------------------------------------------------
        # definir rota para o boss fazer
        self.boss.definir_rota(rota_entrada_centralizada, rota_entrada_tempo)
        # boss.definir_rota(rota_entrada, rota_entrada_tempo)
        gerenciador_objetos.adicionar_inimigo(self.boss)


        # --------------------------------------------------------
        # Adiciona inimigos iniciais
        # for i in range(3):
        #     inimigo = Inimigo()
        #     gerenciador_objetos.adicionar_inimigo(inimigo)

        # --------------------------------------------------------

        return gerenciador_objetos, jogador
    
    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.gerenciador.sair_jogo()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_p, pygame.K_ESCAPE]:
                    self.gerenciador.trocar_estado("pause")
                if evento.key == pygame.K_r:
                    self.gerenciador.trocar_estado("fase2")
                

    def atualizar(self):
        self.jogador.update()
        self.gerenciador_objetos.atualizar()
        
        TEMPO_FASE_2 = 1280
        # -------------------------------------------------------------------------------------
        # executar eventos de tempo
        if self.timer != 0:
            add_angulo_fase = 3

            if self.boss.hp/self.boss.hp_max > 1/3:
                
                if self.timer % 160 == 0:       
                    self.boss.flor(n=16, v=320, a=1*add_angulo_fase)
                    self.boss.flor(n=16, v=300, a=2*add_angulo_fase)
                    self.boss.flor(n=16, v=280, a=3*add_angulo_fase)
                    self.boss.flor(n=16, v=260, a=4*add_angulo_fase)
                    print(f"Flor - Tempo: {self.timer}, Posicao: {self.boss.rect.centerx}, {self.boss.rect.bottom}")
                
                if self.timer % 1280 == 0:
                    self.boss.flor(n=16, v=320, a=1*add_angulo_fase)
                    self.boss.flor(n=16, v=300, a=2*add_angulo_fase)
                    self.boss.flor(n=16, v=280, a=3*add_angulo_fase)
                    self.boss.flor(n=16, v=260, a=4*add_angulo_fase)
                    self.boss.flor(n=16, v=240, a=5*add_angulo_fase)

                    self.boss.flor(n=16, v=220, a=-1*add_angulo_fase)
                    self.boss.flor(n=16, v=200, a=-2*add_angulo_fase)
                    self.boss.flor(n=16, v=180, a=-3*add_angulo_fase)
                    self.boss.flor(n=16, v=160, a=-4*add_angulo_fase)
                    self.boss.flor(n=16, v=140, a=-5*add_angulo_fase)
                    print(f"Florzão - Tempo: {self.timer} Posicao: {self.boss.rect.centerx}, {self.boss.rect.bottom}" )
                
                
            else:

                if self.timer % 200 == 0:    
                    #flor monstruosa   
                    self.boss.flor(n=16, v=320, a=1*add_angulo_fase)
                    self.boss.flor(n=16, v=300, a=2*add_angulo_fase)
                    self.boss.flor(n=16, v=280, a=3*add_angulo_fase)
                    self.boss.flor(n=16, v=260, a=4*add_angulo_fase)
                    self.boss.flor(n=16, v=240, a=5*add_angulo_fase)

                    self.boss.flor(n=16, v=220, a=-1*add_angulo_fase)
                    self.boss.flor(n=16, v=200, a=-2*add_angulo_fase)
                    self.boss.flor(n=16, v=180, a=-3*add_angulo_fase)
                    self.boss.flor(n=16, v=160, a=-4*add_angulo_fase)
                    self.boss.flor(n=16, v=140, a=-5*add_angulo_fase)
                    print(f"Florzão Fase2 - Tempo: {self.timer}")

                    
        
        # ------------------------------------------------------------------------------------
        if self.boss.hp/self.boss.hp_max <= 1/3 :
            print("self.timer = ", self.timer,". boss com pouca vida, troca para estrategia 2" )
            rota_pos = [ (128,96),(128,96), (128,288), (384,288), (384,96), (256,96)]
            rota_tempo =[ 99,99, 199, 199, 199, 99] #alguns 199 porque ele tá atrasando movimento
            
            
            rota_centralizada = [(x - self.boss.rect.width/2, y - self.boss.rect.height/2) for x, y in rota_pos]

            self.boss.definir_rota(rota_centralizada, rota_tempo)
        

        # ------------------------------------------------------------------------------------

        # if self.timer % 150 == 0:
        #     self.flor(n=8,v=200)
        #     print(f"Flor - Tempo: {self.timer}")
        # self.boss.update() # já é atualizado nos objetos

        self.timer+=1
        # ------------------------------------------------------------------------------------

        estado, pontos = self.gerenciador_objetos.verificar_colisoes()
        self.pontuacao += pontos
        if self.boss.hp <= 0:
            estado = "fase1"
        # ------------------------------------------------------------------------------------
        if estado == "fase1":
            self.gerenciador.trocar_estado("fase1")
        if estado == "game_over":
            self.gerenciador.trocar_estado("game_over")

    def desenhar(self, tela):
        #fundo branco
        tela.blit(self.fundo, (0, 0))
        #objetos
        self.gerenciador_objetos.desenhar(tela)
        
        #desenhar HUD
        # Fonte para o texto
        fonte = pygame.font.SysFont("Arial", 24)
        # Exibindo a pontuação
        tela.blit(fonte.render(f"Pontuação: {self.pontuacao}", True, cores.VERMELHO), (10, 10))
        # Exibindo o FPS
        fps = str(int(self.gerenciador.fps))  # Usa o FPS armazenado no gerenciador
        tela.blit(fonte.render(f"FPS: {fps}", True, cores.VERMELHO), (10, 40))
        # Exibindo o número de tiros
        num_tiros = len(self.gerenciador_objetos.tiros)  # Número de tiros do jogador
        tela.blit(fonte.render(f"Tiros: {num_tiros}", True, cores.VERMELHO), (10, 70))
        # Exibindo o número de tiros dos inimigos
        num_inimigos = len(self.gerenciador_objetos.inimigos)  # Número de tiros dos inimigos
        tela.blit(fonte.render(f"Inimigos: {num_inimigos}", True, cores.VERMELHO), (10, 100))
        # Exibindo o número de tiros dos inimigos
        num_tiros_inimigos = len(self.gerenciador_objetos.tiros_inimigos)  # Número de tiros dos inimigos
        tela.blit(fonte.render(f"Tiros Inimigos: {num_tiros_inimigos}", True, cores.VERMELHO), (10, 130))
        
        #exibindo a vida do boss
        if len(self.gerenciador_objetos.inimigos) > 0:
            #verifica se o tipo é Boss ou Inimigo
            if isinstance(self.gerenciador_objetos.inimigos.sprites()[0], Boss):
                inimigo = self.gerenciador_objetos.inimigos.sprites()[0]
                vida_boss = inimigo.hp
                vida_boss_max = inimigo.hp_max
                tela.blit(fonte.render(f"Vida Boss: {vida_boss}/{vida_boss_max}", True, cores.VERMELHO), (10, 160))
                pass
            else:
                
                # inimigo = self.gerenciador_objetos.inimigos.sprites()[0]
                # vida_boss = inimigo.hp
                # vida_boss_max = inimigo.hp_max
                # tela.blit(fonte.render(f"Vida Boss: {vida_boss}/{vida_boss_max}", True, cores.VERMELHO), (10, 160))
                pass
            pass
        
        # Atualizando a tela
        pygame.display.flip()

# --------
class TelaGameOver(EstadoBase):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.fonte = pygame.font.SysFont("Arial", 48)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.gerenciador.sair_jogo()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    self.gerenciador.trocar_estado("menu")

    def desenhar(self, tela):
        # tela.fill(())
        texto_game_over = self.fonte.render("Game Over", True, cores.VERMELHO)
        instrucao = pygame.font.SysFont("Arial", 24).render("Pressione R para reiniciar", True, cores.BRANCO)
        tela.blit(texto_game_over, (LARGURA_TELA // 2 - texto_game_over.get_width() // 2, ALTURA_TELA // 2 - 50))
        tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, ALTURA_TELA // 2 + 20))
        pygame.display.flip()


class GerenciadorEstados:
    def __init__(self):
        self.estados = {
            "menu": MenuInicial(self),
            "fase1": Fase1(self),  # Esse estado já é criado na inicialização
            "fase2": Fase2(self),  # Esse estado já é criado na inicialização
            "game_over": TelaGameOver(self)
        }
        self.estado_atual = self.estados["menu"]
        self.rodando = True
        self.fps = 0  # Adiciona um atributo para armazenar o FPS

    def trocar_estado(self, novo_estado):
        if novo_estado in self.estados:
            print("Tentando trocar para o estado:", novo_estado)
            if novo_estado == "fase1" :
                # Recria o estado "fase" ao trocar para ele apenas se não for a fase atual
                self.estados["fase1"] = Fase1(self)
            elif novo_estado == "fase2":
                # Recria o estado "fase" ao trocar para ele apenas se não for a fase atual
                self.estados["fase2"] = Fase2(self)
            else:
                pass

            self.estado_atual = self.estados[novo_estado]
            pass

    def sair_jogo(self):
        self.rodando = False

    def processar_eventos(self, eventos):
        self.estado_atual.processar_eventos(eventos)

    def atualizar(self):
        self.estado_atual.atualizar()

    def desenhar(self, tela):
        self.estado_atual.desenhar(tela)

    def set_fps(self, fps):
        self.fps = fps
