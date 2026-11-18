"""Tela da partida: o loop principal do jogo."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import FPS, CHAO_Y, FASES, SAIR
from config import LARGURA, PIXELS_POR_METRO, BRANCO, GAME_OVER
from sprites import Jogador
from sprites import Fundo
from gerador import Gerador
from utils import desenhar_texto


# [NÍVEL: FÁCIL]
def desenhar_hud(tela, assets, jogador, distancia, pontos):
    """Desenha vidas, distância e pontos no topo da tela (o "HUD")."""
    for i in range(jogador.vidas):
        tela.blit(assets['vida'], (20 + i * 36, 18))
    fonte = assets['fonte_pequena']
    desenhar_texto(tela, fonte, f'{distancia} m', BRANCO, (LARGURA - 260, 20), False)
    desenhar_texto(tela, fonte, f'Pontos: {pontos}', BRANCO, (LARGURA - 260, 44), False)


# [NÍVEL: DIFÍCIL] — junta tudo: eventos, atualização, colisões e desenho.
def tela_jogo(tela, assets):
    """Roda uma partida e devolve (próximo estado, pontos)."""
    relogio = pygame.time.Clock()
    jogador = Jogador(assets)
    fundo_predios = Fundo(assets['predios'], 0.3, 0)
    fundo_rua = Fundo(assets['rua'], 1.0, CHAO_Y)
    velocidade = FASES[0]['velocidade']
    grupos = {
        'todos': pygame.sprite.Group(),       # tudo que anda e é desenhado
        'obstaculos': pygame.sprite.Group(),  # o que machuca
        'itens': pygame.sprite.Group(),       # o que dá pra pegar
    }
    gerador = Gerador(assets)
    fase = FASES[0]
    distancia_px = 0
    pontos = 0

    while True:
        relogio.tick(FPS)

        # ---------- 1. Eventos ----------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR, pontos
        # get_pressed() diz quais teclas estão APERTADAS AGORA (segurando).
        teclas = pygame.key.get_pressed()
        jogador.voando = teclas[pygame.K_SPACE]

        # ---------- 2. Atualização ----------
        distancia = distancia_px // PIXELS_POR_METRO
        distancia_px += velocidade
        jogador.update()
        fundo_predios.update(velocidade)
        fundo_rua.update(velocidade)
        gerador.atualizar(fase, jogador, grupos)
        grupos['todos'].update(velocidade)

        # ---------- 3. Colisões ----------
        pontos = distancia
        # False = o obstáculo não some sozinho; decidimos abaixo.
        batidas = pygame.sprite.spritecollide(jogador, grupos['obstaculos'], False, pygame.sprite.collide_mask)
        for obstaculo in batidas:
            if jogador.levar_dano():
                obstaculo.kill()
        if jogador.vidas == 0:
            return GAME_OVER, pontos

        # ---------- 4. Desenho ----------
        tela.fill(FASES[0]['ceu'])
        fundo_predios.desenhar(tela)
        fundo_rua.desenhar(tela)
        grupos['todos'].draw(tela)
        tela.blit(jogador.image, jogador.rect)
        desenhar_hud(tela, assets, jogador, distancia, pontos)
        pygame.display.update()
