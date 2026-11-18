"""Atrasado na Faria Lima — arquivo principal. Rode com: python main.py"""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import LARGURA, ALTURA, TITULO
from assets import carregar_assets
from tela_jogo import tela_jogo


# [NÍVEL: FÁCIL]
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

    estado, pontos = tela_jogo(tela, assets)
    print(f'Fim! Estado: {estado} | Pontos: {pontos}')

    pygame.quit()


# Só roda main() quando este arquivo é executado diretamente
# (e não quando é importado por outro arquivo).
if __name__ == '__main__':
    main()
