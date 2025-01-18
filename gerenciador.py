import pygame
from inimigo import Inimigo
from tiro import Tiro, TiroInimigo
from boss import Boss

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

        # Colisões: Tiros x Inimigos (usando hitboxes)
        status, pontos = self.verificar_colisao_tiros_inimigos()
        if status == "game_over":
            return status, pontos
        if status == "fase2":
            return status, pontos
        
        
        pontuacao += pontos

        # Colisões: Tiros dos inimigos x Jogador
        status, pontos = self.verificar_colisao_jogador_com_tiros_inimigos()
        if status == "game_over":
            return status, pontos

        # Colisões: Nave x Inimigos
        status, pontos = self.verificar_colisao_jogador_com_inimigos()
        if status == "game_over":
            return status, pontos

        return "jogando", pontuacao

    def verificar_colisao_tiros_inimigos(self):
        """Verifica colisões de tiros do jogador com inimigos e retorna a pontuação e status do jogo."""
        colisoes = []
        for tiro in self.tiros:
            for inimigo in self.inimigos:
                if tiro.hitbox.verificar_colisao(inimigo.hitbox):
                    colisoes.append((tiro, inimigo))

        pontuacao = 0
        for tiro, inimigo in colisoes:
            tiro = self.remover_objeto(tiro)
            # se for um BOSS
            if isinstance(inimigo, Boss): # É um BOSS!!!!
                # print("boss foi atingido!!")
                inimigo.dano()
                if inimigo.hp <= 0:
                    self.remover_objeto(inimigo)
                    pontuacao += 100
                    print("boss morreu!!")
                    for tiro in self.tiros_inimigos: #apagar todos os tiros inimigos
                        self.remover_objeto(tiro)
                    for inimigo in self.inimigos: #remover todos os inimigos também
                        self.remover_objeto(inimigo)

                    #mudar para fase2
                    return "fase2", pontuacao

                    # print(f"HP: {inimigo.hp}/ {inimigo.hp_max}")

                # Caso contrário, o boss segue vivo
                else:
                    pass
                    # print("boss continua vivo.") 
                    # print(f"HP: {inimigo.hp}/ {inimigo.hp_max}")

            else:  # Inimigo normal
                pontuacao += 1
                self.remover_objeto(tiro)
                self.remover_objeto(inimigo)
                novo_inimigo = Inimigo()
                self.adicionar_inimigo(novo_inimigo)
                break

        return "jogando", pontuacao

    def verificar_colisao_jogador_com_tiros_inimigos(self):
        """Verifica colisões do jogador com tiros dos inimigos."""
        if self.jogador:
            for tiro_inimigo in self.tiros_inimigos:
                if self.jogador.hitbox.verificar_colisao(tiro_inimigo.hitbox):
                    return "game_over", 0
        return "jogando", 0

    def verificar_colisao_jogador_com_inimigos(self):
        """Verifica colisões do jogador com inimigos."""
        if self.jogador:
            for inimigo in self.inimigos:
                if self.jogador.hitbox.verificar_colisao(inimigo.hitbox):
                    return "game_over", 0
        return "jogando", 0
