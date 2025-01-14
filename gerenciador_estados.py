import pygame
import config as conf
import cores

class EstadoBase: #classe abstrata
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

    def processar_eventos(self, eventos):
        pass

    def atualizar(self):
        pass

    def desenhar(self, tela):
        pass


class MenuInicial(EstadoBase):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.fonte = pygame.font.SysFont("Arial", 48)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.gerenciador.sair_jogo()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.gerenciador.trocar_estado("fase")

    def desenhar(self, tela):
        tela.fill(cores.PRETO)
        titulo = self.fonte.render("Shooter Vertical", True, cores.BRANCO)
        instrucao = pygame.font.SysFont("Arial", 24).render("Pressione ENTER para jogar", True, cores.BRANCO)
        controles1 = pygame.font.SysFont("Arial", 24).render("Z - atirar", True, cores.BRANCO)
        controles2= pygame.font.SysFont("Arial", 24).render("SHIFT - focar", True, cores.BRANCO)
        controles3 = pygame.font.SysFont("Arial", 24).render("ESPAÇO (ou X) - bomba", True, cores.BRANCO)
        tela.blit(titulo, (conf.LARGURA_TELA // 2 - titulo.get_width() // 2, conf.ALTURA_TELA // 2 - 200))
        tela.blit(instrucao, (conf.LARGURA_TELA // 2 - instrucao.get_width() // 2, conf.ALTURA_TELA // 2 + 200))
        tela.blit(controles1, ((conf.LARGURA_TELA // 2 - instrucao.get_width() // 2), conf.ALTURA_TELA // 2 ))
        tela.blit(controles2, ((conf.LARGURA_TELA // 2 - instrucao.get_width() // 2), conf.ALTURA_TELA // 2 +30))
        tela.blit(controles3, ((conf.LARGURA_TELA // 2 - instrucao.get_width() // 2), conf.ALTURA_TELA // 2 +60))
        pygame.display.flip()


from nave import Nave
from gerenciador import GerenciadorObjetos
from inimigo import Inimigo

def reiniciar_jogo():
    """
    Reinicia o estado do jogo com os objetos necessários.
    Retorna um gerenciador de objetos e o jogador.
    """
    gerenciador_objetos = GerenciadorObjetos()
    jogador = Nave(gerenciador_objetos)
    gerenciador_objetos.adicionar_jogador(jogador)

    # Adiciona inimigos iniciais
    for i in range(5):
        inimigo = Inimigo()
        gerenciador_objetos.adicionar_inimigo(inimigo)

    return gerenciador_objetos, jogador

class Fase(EstadoBase):

    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.gerenciador_objetos, self.jogador = reiniciar_jogo()
        self.pontuacao = 0
        self.fundo = pygame.image.load("sprites/galaxy.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (conf.LARGURA_TELA, conf.ALTURA_TELA))

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.gerenciador.sair_jogo()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_p, pygame.K_ESCAPE]:
                    self.gerenciador.trocar_estado("pause")
                # if evento.key == pygame.K_r:
                #     self.gerenciador.trocar_estado("fase")

    def atualizar(self):
        self.gerenciador_objetos.atualizar()
        self.jogador.update()
        estado, pontos = self.gerenciador_objetos.verificar_colisoes()
        self.pontuacao += pontos
        if estado == "game_over":
            self.gerenciador.trocar_estado("game_over")

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))
        self.gerenciador_objetos.desenhar(tela)
        fonte = pygame.font.SysFont("Arial", 24)
        tela.blit(fonte.render(f"Pontuação: {self.pontuacao}", True, cores.VERMELHO), (10, 10))
        pygame.display.flip()


class TelaPause(EstadoBase):
    def __init__(self, gerenciador):
        super().__init__(gerenciador)
        self.fonte = pygame.font.SysFont("Arial", 48)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.gerenciador.sair_jogo()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_p, pygame.K_ESCAPE]:
                    self.gerenciador.trocar_estado("fase")
                if evento.key == pygame.K_r:
                    self.gerenciador.trocar_estado("fase")

    def desenhar(self, tela):
        tela.fill(cores.PRETO)
        texto_pausa = self.fonte.render("Jogo Pausado", True, cores.AZUL)
        instrucao = pygame.font.SysFont("Arial", 24).render("Pressione P ou ESC para continuar", True, cores.BRANCO)
        instrucao2 = pygame.font.SysFont("Arial", 24).render("Pressione R para reiniciar", True, cores.BRANCO)
        tela.blit(texto_pausa, (conf.LARGURA_TELA // 2 - texto_pausa.get_width() // 2, conf.ALTURA_TELA // 2 - 50))
        tela.blit(instrucao, (conf.LARGURA_TELA // 2 - instrucao.get_width() // 2, conf.ALTURA_TELA // 2 + 20))
        tela.blit(instrucao2, (conf.LARGURA_TELA // 2 - instrucao.get_width() // 2, conf.ALTURA_TELA // 2 + 50))
        pygame.display.flip()


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
                    self.gerenciador.trocar_estado("fase")

    def desenhar(self, tela):
        tela.fill(cores.PRETO)
        texto_game_over = self.fonte.render("Game Over", True, cores.VERMELHO)
        instrucao = pygame.font.SysFont("Arial", 24).render("Pressione R para reiniciar", True, cores.BRANCO)
        tela.blit(texto_game_over, (conf.LARGURA_TELA // 2 - texto_game_over.get_width() // 2, conf.ALTURA_TELA // 2 - 50))
        tela.blit(instrucao, (conf.LARGURA_TELA // 2 - instrucao.get_width() // 2, conf.ALTURA_TELA // 2 + 20))
        pygame.display.flip()


class GerenciadorEstados:
    def __init__(self):
        self.estados = {
            "menu": MenuInicial(self),
            "fase": Fase(self),
            "pause": TelaPause(self),
            "game_over": TelaGameOver(self)
        }
        self.estado_atual = self.estados["menu"]
        self.rodando = True

    def trocar_estado(self, novo_estado):
        if novo_estado in self.estados:
            if novo_estado == "fase":
                # Recria o estado "fase" ao trocar para ele
                self.estados["fase"] = Fase(self)
            self.estado_atual = self.estados[novo_estado]


    def sair_jogo(self):
        self.rodando = False

    def processar_eventos(self, eventos):
        self.estado_atual.processar_eventos(eventos)

    def atualizar(self):
        self.estado_atual.atualizar()

    def desenhar(self, tela):
        self.estado_atual.desenhar(tela)
