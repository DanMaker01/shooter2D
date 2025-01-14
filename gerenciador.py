import pygame
from inimigo import Inimigo
from tiro import Tiro, TiroInimigo

class GerenciadorObjetos:
    def __init__(self):
        self.todos_sprites = pygame.sprite.Group()  # Todos os objetos
        self.tiros = pygame.sprite.Group()         # Apenas os projéteis do jogador
        self.tiros_inimigos = pygame.sprite.Group()  # Apenas os projéteis dos inimigos
        self.inimigos = pygame.sprite.Group()      # Apenas os inimigos
        self.jogador = None                        # Referência ao jogador

    def adicionar_jogador(self, jogador):
        """Adiciona o jogador ao gerenciador."""
        self.jogador = jogador
        self.todos_sprites.add(jogador)

    def adicionar_tiro(self, tiro):
        """Adiciona um projétil do jogador ao jogo."""
        self.tiros.add(tiro)
        self.todos_sprites.add(tiro)

    def adicionar_tiro_inimigo(self, tiro_inimigo):
        """Adiciona um projétil do inimigo ao jogo."""
        self.tiros_inimigos.add(tiro_inimigo)
        self.todos_sprites.add(tiro_inimigo)

    def adicionar_inimigo(self, inimigo):
        """Adiciona um inimigo ao jogo."""
        self.inimigos.add(inimigo)
        self.todos_sprites.add(inimigo)

    def remover_objeto(self, objeto):
        """Remove qualquer objeto do jogo."""
        self.todos_sprites.remove(objeto)
        if isinstance(objeto, Tiro):
            self.tiros.remove(objeto)
        elif isinstance(objeto, TiroInimigo):
            self.tiros_inimigos.remove(objeto)
        elif isinstance(objeto, Inimigo):
            self.inimigos.remove(objeto)

    def atualizar(self):
        """Atualiza todos os objetos gerenciados."""
        self.todos_sprites.update()

    def desenhar(self, tela):
        """Desenha todos os objetos na tela."""
        self.todos_sprites.draw(tela)

        if self.jogador:
            self.jogador.desenhar_hitbox(tela)

    def verificar_colisoes(self):
        """Verifica colisões entre hitboxes de tiros e inimigos, e do jogador com inimigos e tiros inimigos."""
        pontuacao = 0

        # Colisões: TirosInimigos x Jogador (usando hitboxes)
        if self.jogador:
            for tiro_inimigo in self.tiros_inimigos:
                if self.jogador.hitbox.verificar_colisao(tiro_inimigo.hitbox):
                    return "game_over", pontuacao

        # Colisões: Tiros x Inimigos (usando hitboxes)
        colisoes = pygame.sprite.groupcollide(self.inimigos, self.tiros, True, True)
        for colisao in colisoes:
            pontuacao += 1
            # Adiciona um novo inimigo (ou qualquer outra lógica de reposição)
            novo_inimigo = Inimigo()
            self.adicionar_inimigo(novo_inimigo)

        # Colisões: Tiros dos inimigos x Jogador (usando hitboxes)
        if self.jogador:
            for tiro_inimigo in self.tiros_inimigos:
                if self.jogador.hitbox.verificar_colisao(tiro_inimigo.hitbox):
                    return "game_over", pontuacao

        # Colisões: Nave x Inimigos (usando hitboxes)
        if self.jogador:
            for inimigo in self.inimigos:
                if self.jogador.hitbox.verificar_colisao(inimigo.hitbox):
                    return "game_over", pontuacao

        return "jogando", pontuacao
