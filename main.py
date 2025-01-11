import pygame
import logging
import config as conf
import cores
from nave import Nave
from gerenciador import GerenciadorObjetos
from inimigo import Inimigo


def inicializar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((conf.LARGURA_TELA, conf.ALTURA_TELA))
    pygame.display.set_caption("Shooter Vertical")
    clock = pygame.time.Clock()

    # Carregando a imagem de fundo
    fundo = pygame.image.load("sprites/galaxy.png").convert()  # Substitua pelo caminho correto
    fundo = pygame.transform.scale(fundo, (conf.LARGURA_TELA, conf.ALTURA_TELA))
    
    return tela, clock, fundo

def reiniciar_jogo():
    gerenciador = GerenciadorObjetos()
    jogador = Nave(gerenciador)
    gerenciador.adicionar_jogador(jogador)
    for _ in range(5):
        gerenciador.adicionar_inimigo(Inimigo())
    return gerenciador, jogador


def processar_eventos(eventos, jogador, estado, gerenciador, pontuacao):
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return False, estado, pontuacao, gerenciador, jogador

        # jogador.processar_evento_teclado(evento)
        
        if estado == "game_over" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                novo_gerenciador, novo_jogador = reiniciar_jogo()
                return True, "jogando", 0, novo_gerenciador, novo_jogador
    return True, estado, pontuacao, gerenciador, jogador


def desenhar_tela(tela, gerenciador, pontuacao, estado, fps_atual, fundo):
    tela.blit(fundo, (0, 0))  # Desenhe o fundo primeiro
    gerenciador.desenhar(tela)
    
    fonte = pygame.font.SysFont("Arial", 24)
    tela.blit(fonte.render(f"Pontuação: {pontuacao}", True, cores.VERMELHO), (10, 10))
    tela.blit(fonte.render(f"FPS: {fps_atual}", True, cores.VERMELHO), (conf.LARGURA_TELA - 100, 10))
    tela.blit(fonte.render(f"Projéteis: {len(gerenciador.tiros)}", True, cores.VERMELHO), (10, 40))
    
    if estado == "game_over":
        fonte_game_over = pygame.font.SysFont("Arial", 48)
        tela.blit(fonte_game_over.render("Game Over", True, cores.VERMELHO),
                  (conf.LARGURA_TELA // 2 - 150, conf.ALTURA_TELA // 2 - 50))
        tela.blit(fonte.render("Pressione R para reiniciar", True, cores.BRANCO),
                  (conf.LARGURA_TELA // 2 - 150, conf.ALTURA_TELA // 2 + 10))
    pygame.display.flip()


#
def main():
    logging.basicConfig(level=logging.INFO)
    tela, clock, fundo = inicializar_jogo()  # Adicionado fundo
    gerenciador, jogador = reiniciar_jogo()
    jogando, estado, pontuacao = True, "jogando", 0

    while jogando:
        eventos = pygame.event.get()
        jogando, estado, pontuacao, gerenciador, jogador = processar_eventos(eventos, jogador, estado, gerenciador, pontuacao)
        
        if estado == "jogando":
            gerenciador.atualizar()
            jogador.update()
            estado, pontos = gerenciador.verificar_colisoes()
            pontuacao += pontos

        desenhar_tela(tela, gerenciador, pontuacao, estado, int(clock.get_fps()), fundo)  # Passando fundo
        clock.tick(conf.FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
