"""Carregamento de imagens, sons e fontes do jogo.

Todas as funções de carregar têm um "plano B": se o arquivo ainda não
existir na pasta assets/, o jogo usa um retângulo colorido (imagens) ou
fica em silêncio (sons). Assim dá para programar e testar desde o
primeiro dia, antes de ter as imagens e os sons definitivos.
"""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import os
import random
import pygame
from config import LARGURA, ALTURA, CHAO_Y, PASTA_IMG, PASTA_SND, PASTA_FONT


def carregar_imagem(nome, tamanho, cor_reserva):
    """Carrega assets/img/<nome> no tamanho pedido.

    Se o arquivo não existir, devolve um retângulo da cor de reserva.
    """
    caminho = os.path.join(PASTA_IMG, nome)
    if os.path.exists(caminho):
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(imagem, tamanho)
    # Plano B: uma superfície transparente com um retângulo colorido dentro.
    imagem = pygame.Surface(tamanho, pygame.SRCALPHA)
    pygame.draw.rect(imagem, cor_reserva, imagem.get_rect(), border_radius=8)
    return imagem


# [NÍVEL: FÁCIL] — um for montando uma lista - M
def carregar_animacao(prefixo, quantidade, tamanho, cores_reserva):
    """Carrega os quadros <prefixo>0.png, <prefixo>1.png, ... numa lista."""
    quadros = []
    for i in range(quantidade):
        cor = cores_reserva[i % len(cores_reserva)]
        quadros.append(carregar_imagem(f'{prefixo}{i}.png', tamanho, cor))
    return quadros


# [NÍVEL: MÉDIO] — desenha prédios "aleatórios", mas sempre iguais (semente fixa).
def criar_predios_reserva(tamanho):
    """Desenha prédios cinzas simples para usar enquanto não há predios.png."""
    largura = tamanho[0]
    altura = tamanho[1]
    imagem = pygame.Surface(tamanho, pygame.SRCALPHA)
    sorteio = random.Random(42)  # semente fixa: o desenho sai igual toda vez
    x = 0
    while x < largura:
        largura_predio = sorteio.randint(60, 120)
        altura_predio = sorteio.randint(120, 320)
        tom = sorteio.randint(70, 110)
        predio = pygame.Rect(x, altura - altura_predio, largura_predio - 6, altura_predio)
        pygame.draw.rect(imagem, (tom, tom, tom + 10), predio)
        x += largura_predio
    return imagem


# [NÍVEL: FÁCIL] — um retângulo cinza e faixas brancas. - M e C
def criar_rua_reserva(tamanho):
    """Desenha uma rua cinza com faixas, para usar enquanto não há rua.png."""
    largura = tamanho[0]
    altura = tamanho[1]
    imagem = pygame.Surface(tamanho)
    imagem.fill((50, 50, 55))
    for x in range(0, largura, 80):
        pygame.draw.rect(imagem, (230, 230, 230), (x, altura // 2 - 3, 40, 6))
    return imagem


# [NÍVEL: FÁCIL] — círculos cada vez maiores. - M
def criar_explosao_reserva():
    """Cria 6 quadros de explosão (círculos laranja crescendo)."""
    quadros = []
    for i in range(6):
        imagem = pygame.Surface((80, 80), pygame.SRCALPHA)
        raio = 10 + i * 6
        pygame.draw.circle(imagem, (255, 140 + i * 15, 0), (40, 40), raio)
        quadros.append(imagem)
    return quadros


# [NÍVEL: FÁCIL]
def carregar_fundo(nome, tamanho, funcao_reserva):
    """Carrega uma imagem de fundo ou, se não existir, desenha a de reserva."""
    caminho = os.path.join(PASTA_IMG, nome)
    if os.path.exists(caminho):
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(imagem, tamanho)
    return funcao_reserva(tamanho)


# [NÍVEL: MÉDIO] — testa várias extensões e o caso de não haver som.
def carregar_som(nome, volume=0.5):
    """Carrega assets/snd/<nome>.ogg ou .wav. Devolve None se não houver."""
    if pygame.mixer.get_init() is None:  # computador sem som
        return None
    for extensao in ['.ogg', '.wav']:
        caminho = os.path.join(PASTA_SND, nome + extensao)
        if os.path.exists(caminho):
            som = pygame.mixer.Sound(caminho)
            som.set_volume(volume)
            return som
    return None


# [NÍVEL: FÁCIL] - M
def tocar(som):
    """Toca um som, se ele existir (se for None, não faz nada)."""
    if som is not None:
        som.play()


# [NÍVEL: FÁCIL]
def tocar_musica(volume=0.4):
    """Toca a música de fundo em loop (-1 = repetir para sempre)."""
    if pygame.mixer.get_init() is None:
        return
    for extensao in ['.ogg', '.mp3', '.wav']:
        caminho = os.path.join(PASTA_SND, 'musica' + extensao)
        if os.path.exists(caminho):
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            return


# [NÍVEL: FÁCIL]
def parar_musica():
    """Para a música de fundo."""
    if pygame.mixer.get_init() is not None:
        pygame.mixer.music.stop()


# [NÍVEL: FÁCIL]
def carregar_fonte(nome, tamanho):
    """Carrega a fonte do jogo ou, se não existir, a fonte padrão do pygame."""
    caminho = os.path.join(PASTA_FONT, nome)
    if os.path.exists(caminho):
        return pygame.font.Font(caminho, tamanho)
    return pygame.font.Font(None, int(tamanho * 1.6))  # a padrão é menor


# [NÍVEL: FÁCIL] — igual ao load_assets() do tutorial (jogo_v20).
def carregar_assets():
    """Carrega tudo e devolve um dicionário com imagens, sons e fontes."""
    assets = {}
    # Imagens (nome do arquivo, tamanho em pixels, cor de reserva)
    assets['jogador_correndo'] = carregar_animacao(
        'jogador_corre', 2, (48, 64), [(230, 120, 40), (200, 100, 30)])
    assets['jogador_voando'] = carregar_animacao(
        'jogador_voa', 2, (48, 64), [(240, 160, 40), (255, 190, 70)])
    assets['drone'] = carregar_imagem('drone.png', (64, 40), (90, 90, 100))
    assets['pombo'] = carregar_animacao(
        'pombo', 2, (64, 40), [(150, 150, 160), (120, 120, 130)])
    assets['aviso'] = carregar_imagem('aviso.png', (48, 48), (230, 40, 40))
    assets['cafe'] = carregar_imagem('cafe.png', (32, 32), (120, 70, 30))
    assets['capacete'] = carregar_imagem('capacete.png', (40, 40), (250, 210, 0))
    assets['vida'] = carregar_imagem('vida.png', (28, 28), (220, 40, 60))
    assets['predios'] = carregar_fundo('predios.png', (LARGURA, CHAO_Y), criar_predios_reserva)
    assets['rua'] = carregar_fundo('rua.png', (LARGURA, ALTURA - CHAO_Y), criar_rua_reserva)
    if os.path.exists(os.path.join(PASTA_IMG, 'explosao0.png')):
        assets['explosao'] = carregar_animacao('explosao', 6, (80, 80), [(255, 140, 0)])
    else:
        assets['explosao'] = criar_explosao_reserva()
    # Sons (None quando o arquivo ainda não existe)
    assets['som_jetpack'] = carregar_som('jetpack', 0.3)
    assets['som_cafe'] = carregar_som('cafe')
    assets['som_batida'] = carregar_som('batida')
    assets['som_escudo'] = carregar_som('escudo')
    assets['som_aviso'] = carregar_som('aviso')
    assets['som_game_over'] = carregar_som('game_over')
    # Fontes
    assets['fonte_grande'] = carregar_fonte('PressStart2P-Regular.ttf', 32)
    assets['fonte_media'] = carregar_fonte('PressStart2P-Regular.ttf', 18)
    assets['fonte_pequena'] = carregar_fonte('PressStart2P-Regular.ttf', 12)
    return assets
