import pygame
from inimigo import Inimigo
from tiro import Tiro

class GerenciadorObjetos:
    def __init__(self):
        self.todos_sprites = pygame.sprite.Group()  # Todos os objetos
        self.tiros = pygame.sprite.Group()         # Apenas os projéteis
        self.inimigos = pygame.sprite.Group()      # Apenas os inimigos
        self.jogador = None                        # Referência ao jogador

    def adicionar_jogador(self, jogador):
        """Adiciona o jogador ao gerenciador."""
        self.jogador = jogador
        self.todos_sprites.add(jogador)

    def adicionar_tiro(self, tiro):
        """Adiciona um projétil ao jogo."""
        self.tiros.add(tiro)
        self.todos_sprites.add(tiro)

    def adicionar_inimigo(self, inimigo):
        """Adiciona um inimigo ao jogo."""
        self.inimigos.add(inimigo)
        self.todos_sprites.add(inimigo)

    def remover_objeto(self, objeto):
        """Remove qualquer objeto do jogo."""
        self.todos_sprites.remove(objeto)
        if isinstance(objeto, Tiro):
            self.tiros.remove(objeto)
        elif isinstance(objeto, Inimigo):
            self.inimigos.remove(objeto)

    def atualizar(self):
        """Atualiza todos os objetos gerenciados."""
        self.todos_sprites.update()

    def desenhar(self, tela):
        """Desenha todos os objetos na tela."""
        self.todos_sprites.draw(tela)

    def verificar_colisoes(self):
        """Verifica colisões entre tiros e inimigos, e nave com inimigos."""
        pontuacao = 0

        # Colisões: Tiros x Inimigos
        colisoes = pygame.sprite.groupcollide(self.inimigos, self.tiros, True, True)
        for colisao in colisoes:
            pontuacao += 1
            # Adiciona um novo inimigo (ou qualquer outra lógica de reposição)
            novo_inimigo = Inimigo()
            self.adicionar_inimigo(novo_inimigo)

        # Colisões: Nave x Inimigos
        if self.jogador and pygame.sprite.spritecollide(self.jogador, self.inimigos, False):
            return "game_over", pontuacao

        return "jogando", pontuacao
