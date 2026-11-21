"""Atrasado na Faria Lima — arquivo principal. Rode com: python main.py"""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import LARGURA, ALTURA, TITULO
from config import INICIO, INSTRUCOES, JOGANDO, GAME_OVER, SAIR
from assets import carregar_assets
from tela_jogo import tela_jogo
from tela_inicio import tela_inicio
from tela_instrucoes import tela_instrucoes
from tela_game_over import tela_game_over


# [NÍVEL: MÉDIO] — a máquina de estados das telas (como no jogo_v22).
def main():
    """Inicia o pygame, roda o jogo e fecha tudo no final."""
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        print('Sem som disponível: o jogo vai rodar mudo.')
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    assets = carregar_assets()  # só depois do set_mode (por causa do convert_alpha)

    estado = INICIO
    pontos = 0
    while estado != SAIR:
        if estado == INICIO:
            estado = tela_inicio(tela, assets)
        elif estado == INSTRUCOES:
            estado = tela_instrucoes(tela, assets)
        elif estado == JOGANDO:
            estado, pontos = tela_jogo(tela, assets)
        elif estado == GAME_OVER:
            estado = tela_game_over(tela, assets, pontos)

    pygame.quit()


# Só roda main() quando este arquivo é executado diretamente
# (e não quando é importado por outro arquivo).
if __name__ == '__main__':
    main()
