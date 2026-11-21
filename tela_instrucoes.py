"""Tela de instruções (como jogar)."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import pygame
from config import FPS, LARGURA, BRANCO, AMARELO, CINZA, INICIO, SAIR
from utils import desenhar_texto


# [NÍVEL: FÁCIL]
def tela_instrucoes(tela, assets):
    """Mostra como jogar. ENTER ou ESC voltam ao menu."""
    relogio = pygame.time.Clock()
    # Cada linha: (imagem ao lado ou None, texto)
    linhas = [
        (None, 'Segure ESPACO para voar. Solte para cair.'),
        (assets['cafe'], 'Cafe: +10 pontos'),
        (assets['capacete'], 'Capacete: aguenta uma batida'),
        (assets['drone'], 'Drone: desvie!'),
        (assets['aviso'], 'Aviso: um pombo-missil vem ai!'),
        (None, 'P pausa   ESC volta ao menu'),
    ]

    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return INICIO

        tela.fill(CINZA)
        desenhar_texto(tela, assets['fonte_grande'], 'COMO JOGAR', AMARELO, (LARGURA // 2, 60))
        y = 130
        for imagem, texto in linhas:
            if imagem is not None:
                retangulo = imagem.get_rect()
                retangulo.center = (190, y + 8)
                tela.blit(imagem, retangulo)
            desenhar_texto(tela, assets['fonte_pequena'], texto, BRANCO, (250, y), False)
            y += 55
        desenhar_texto(tela, assets['fonte_pequena'], 'ENTER para voltar', AMARELO, (LARGURA // 2, 500))
        pygame.display.update()
