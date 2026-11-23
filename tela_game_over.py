"""Tela de fim de jogo."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import FPS, LARGURA, BRANCO, AMARELO, VERMELHO, JOGANDO, INICIO, SAIR
from recorde import ler_recorde, salvar_recorde
from utils import desenhar_texto


# [NÍVEL: FÁCIL]
def tela_game_over(tela, assets, pontos):
    """Mostra os pontos, salva o recorde e devolve o próximo estado."""
    relogio = pygame.time.Clock()
    recorde = ler_recorde()
    novo_recorde = pontos > recorde
    if novo_recorde:
        salvar_recorde(pontos)
        recorde = pontos
    centro_x = LARGURA // 2

    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return JOGANDO
                if evento.key == pygame.K_ESCAPE:
                    return INICIO

        tela.fill((20, 20, 35))
        desenhar_texto(tela, assets['fonte_grande'], 'FIM DE JOGO', VERMELHO, (centro_x, 110))
        desenhar_texto(tela, assets['fonte_pequena'], 'Voce chegou atrasado no trabalho!', BRANCO, (centro_x, 170))
        desenhar_texto(tela, assets['fonte_media'], f'Pontos: {pontos}', BRANCO, (centro_x, 250))
        desenhar_texto(tela, assets['fonte_media'], f'Recorde: {recorde}', AMARELO, (centro_x, 300))
        # Pisca a cada meio segundo (500 ms ligado, 500 ms desligado).
        if novo_recorde and (pygame.time.get_ticks() // 500) % 2 == 0:
            desenhar_texto(tela, assets['fonte_media'], 'NOVO RECORDE!', AMARELO, (centro_x, 360))
        desenhar_texto(tela, assets['fonte_pequena'], 'ENTER jogar de novo     ESC menu', BRANCO, (centro_x, 460))
        pygame.display.update()
