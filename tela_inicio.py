"""Tela inicial (menu)."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import FPS, LARGURA, CHAO_Y, FASES, BRANCO, AMARELO, PRETO
from config import JOGANDO, INSTRUCOES, SAIR
from sprites import Fundo
from recorde import ler_recorde
from utils import desenhar_texto


# [NÍVEL: FÁCIL] — um loop pequeno que espera uma tecla.
def tela_inicio(tela, assets):
    """Mostra o menu e devolve o próximo estado (JOGANDO, INSTRUCOES ou SAIR)."""
    relogio = pygame.time.Clock()
    recorde = ler_recorde()
    fundo_predios = Fundo(assets['predios'], 0.3, 0)
    fundo_rua = Fundo(assets['rua'], 1.0, CHAO_Y)
    centro_x = LARGURA // 2

    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return JOGANDO
                if evento.key == pygame.K_i:
                    return INSTRUCOES
                if evento.key == pygame.K_ESCAPE:
                    return SAIR

        # O cenário anda devagar no menu, só para dar vida à tela.
        fundo_predios.update(2)
        fundo_rua.update(2)

        tela.fill(FASES[0]['ceu'])
        fundo_predios.desenhar(tela)
        fundo_rua.desenhar(tela)
        desenhar_texto(tela, assets['fonte_grande'], 'FARIA LIMA', PRETO, (centro_x + 3, 103))
        desenhar_texto(tela, assets['fonte_grande'], 'FARIA LIMA', AMARELO, (centro_x, 100))
        desenhar_texto(tela, assets['fonte_grande'], 'RUSH', PRETO, (centro_x + 3, 153))
        desenhar_texto(tela, assets['fonte_grande'], 'RUSH', AMARELO, (centro_x, 150))
        # Painel escuro semitransparente para o texto ficar legível.
        # O 4º número da cor (150) é a transparência: 0 = invisível, 255 = opaco.
        painel = pygame.Surface((600, 160), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 150))
        tela.blit(painel, (centro_x - 300, 220))
        desenhar_texto(tela, assets['fonte_media'], 'ENTER para jogar', BRANCO, (centro_x, 260))
        desenhar_texto(tela, assets['fonte_pequena'], 'I para instrucoes   ESC para sair', BRANCO, (centro_x, 300))
        desenhar_texto(tela, assets['fonte_pequena'], f'Recorde: {recorde} pontos', AMARELO, (centro_x, 340))
        pygame.display.update()
