import pygame
import config as conf
from gerenciador_estados import GerenciadorEstados

# -------------------------------------------------------------------------------------
# TO-DO
# -------------------------------------------------------------------------------------
#  
#  - melhorar as mortes
#  - atirar() na classe Inimigo
#  - Fazer um arquivo chamado roteiro.txt que diz a ordem das fases e padrões dos boss
#  - 
# 
# -------------------------------------------------------------------------------------




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
