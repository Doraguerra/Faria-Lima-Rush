"""Tela da partida: o loop principal do jogo."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import FPS, CHAO_Y, FASES, SAIR
from config import LARGURA, ALTURA, CINZA
from sprites import Jogador


# [NÍVEL: DIFÍCIL] — junta tudo: eventos, atualização, colisões e desenho.
def tela_jogo(tela, assets):
    """Roda uma partida e devolve (próximo estado, pontos)."""
    relogio = pygame.time.Clock()
    jogador = Jogador(assets)

    while True:
        relogio.tick(FPS)

        # ---------- 1. Eventos ----------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR, 0
        # get_pressed() diz quais teclas estão APERTADAS AGORA (segurando).
        teclas = pygame.key.get_pressed()
        jogador.voando = teclas[pygame.K_SPACE]

        # ---------- 2. Atualização ----------
        jogador.update()

        # ---------- 3. Colisões ----------

        # ---------- 4. Desenho ----------
        tela.fill(FASES[0]['ceu'])
        pygame.draw.rect(tela, CINZA, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
        tela.blit(jogador.image, jogador.rect)
        pygame.display.update()
