"""Tela da partida: o loop principal do jogo."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import FPS, CHAO_Y, FASES, SAIR
from sprites import Jogador
from sprites import Fundo


# [NÍVEL: DIFÍCIL] — junta tudo: eventos, atualização, colisões e desenho.
def tela_jogo(tela, assets):
    """Roda uma partida e devolve (próximo estado, pontos)."""
    relogio = pygame.time.Clock()
    jogador = Jogador(assets)
    fundo_predios = Fundo(assets['predios'], 0.3, 0)
    fundo_rua = Fundo(assets['rua'], 1.0, CHAO_Y)
    velocidade = FASES[0]['velocidade']

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
        fundo_predios.update(velocidade)
        fundo_rua.update(velocidade)

        # ---------- 3. Colisões ----------

        # ---------- 4. Desenho ----------
        tela.fill(FASES[0]['ceu'])
        fundo_predios.desenhar(tela)
        fundo_rua.desenhar(tela)
        tela.blit(jogador.image, jogador.rect)
        pygame.display.update()
