"""Tela da partida: o loop principal do jogo."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import FPS, CHAO_Y, FASES, SAIR
from config import LARGURA, PIXELS_POR_METRO, BRANCO, GAME_OVER
from config import PONTOS_CAFE
from config import ALTURA, ACELERACAO_NOITE, AMARELO
from sprites import Jogador
from sprites import Fundo
from sprites import Explosao
from gerador import Gerador
from utils import desenhar_texto


# [NÍVEL: MÉDIO] — percorre a lista de fases e guarda a última que já começou.
def fase_atual(distancia):
    """Devolve o dicionário da fase em que o jogador está."""
    fase = FASES[0]
    for f in FASES:
        if distancia >= f['inicio']:
            fase = f
    return fase


# [NÍVEL: MÉDIO]
def velocidade_atual(fase, distancia):
    """Velocidade do mundo. Na NOITE, aumenta a cada 500 m."""
    velocidade = fase['velocidade']
    if fase['nome'] == 'NOITE':
        velocidade += (distancia - fase['inicio']) // 500 * ACELERACAO_NOITE
    return velocidade


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
    grupos = {
        'todos': pygame.sprite.Group(),       # tudo que anda e é desenhado
        'obstaculos': pygame.sprite.Group(),  # o que machuca
        'itens': pygame.sprite.Group(),       # o que dá pra pegar
    }
    gerador = Gerador(assets)
    fase = FASES[0]
    distancia_px = 0
    pontos = 0
    cafes = 0
    aviso_fase_ate = pygame.time.get_ticks() + 2000
    fim_em = None

    while True:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()

        # ---------- 1. Eventos ----------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR, pontos
        # get_pressed() diz quais teclas estão APERTADAS AGORA (segurando).
        teclas = pygame.key.get_pressed()
        jogador.voando = teclas[pygame.K_SPACE]

        # ---------- 2. Atualização ----------
        distancia = distancia_px // PIXELS_POR_METRO
        nova_fase = fase_atual(distancia)
        if nova_fase is not fase:
            fase = nova_fase
            aviso_fase_ate = agora + 2000  # mostra o nome da fase por 2 s
        velocidade = velocidade_atual(fase, distancia)
        distancia_px += velocidade
        jogador.update()
        fundo_predios.update(velocidade)
        fundo_rua.update(velocidade)
        gerador.atualizar(fase, jogador, grupos)
        grupos['todos'].update(velocidade)

        # ---------- 3. Colisões ----------
        # True = o item some do jogo ao ser pego.
        pegos = pygame.sprite.spritecollide(jogador, grupos['itens'], True, pygame.sprite.collide_mask)
        for item in pegos:
            if item.tipo == 'cafe':
                cafes += 1
            if item.tipo == 'capacete':
                jogador.escudo = True
        pontos = distancia + cafes * PONTOS_CAFE
        # False = o obstáculo não some sozinho; decidimos abaixo.
        batidas = pygame.sprite.spritecollide(jogador, grupos['obstaculos'], False, pygame.sprite.collide_mask)
        for obstaculo in batidas:
            if jogador.levar_dano():
                obstaculo.kill()
                grupos['todos'].add(Explosao(assets['explosao'], obstaculo.rect.center))
        if jogador.vidas == 0 and fim_em is None:
            fim_em = agora + 1200  # espera 1,2 s para a explosão aparecer
        if fim_em is not None and agora >= fim_em:
            return GAME_OVER, pontos

        # ---------- 4. Desenho ----------
        tela.fill(fase['ceu'])
        fundo_predios.desenhar(tela)
        fundo_rua.desenhar(tela)
        grupos['todos'].draw(tela)
        if jogador.vidas > 0:
            tela.blit(jogador.image, jogador.rect)
        if jogador.escudo:
            raio = max(jogador.rect.width, jogador.rect.height) // 2 + 8
            pygame.draw.circle(tela, AMARELO, jogador.rect.center, raio, 3)
        desenhar_hud(tela, assets, jogador, distancia, pontos)
        if agora < aviso_fase_ate:
            desenhar_texto(tela, assets['fonte_grande'], fase['nome'] + '!', AMARELO, (LARGURA // 2, ALTURA // 3))
        pygame.display.update()
