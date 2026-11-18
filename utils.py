"""Funções de apoio usadas por várias telas."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.


# [NÍVEL: FÁCIL] — mesma ideia do jogo_v3 do tutorial (font.render + blit).
def desenhar_texto(tela, fonte, texto, cor, posicao, centralizado=True):
    """Desenha um texto na tela.

    Se centralizado=True, 'posicao' é o centro do texto.
    Se centralizado=False, 'posicao' é o canto superior esquerdo.
    """
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()
    if centralizado:
        retangulo.center = posicao
    else:
        retangulo.topleft = posicao
    tela.blit(imagem, retangulo)
