import pygame
import config as conf
# import cores

from nave import Nave
from gerenciador import GerenciadorObjetos
from inimigo import Inimigo
from gerenciador_estados import GerenciadorEstados




def main():
    pygame.init()
    tela = pygame.display.set_mode((conf.LARGURA_TELA, conf.ALTURA_TELA))
    pygame.display.set_caption("Shooter Vertical")
    clock = pygame.time.Clock()
    gerenciador = GerenciadorEstados()

    while gerenciador.rodando:
        eventos = pygame.event.get()
        gerenciador.processar_eventos(eventos)
        gerenciador.atualizar()
        gerenciador.set_fps(clock.get_fps())  # Define o FPS no gerenciador
        gerenciador.desenhar(tela)
        clock.tick(conf.FPS)  # Controla o FPS da tela
    pygame.quit()








if __name__ == "__main__":
    main()
