"""Constantes do jogo.
"""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.

import os

# Janela 
LARGURA = 960
ALTURA = 540
FPS = 60
TITULO = 'Faria Lima Rush'

#Pastas e arquivos
# os.path.dirname(__file__) = a pasta onde este arquivo está.
# Assim o jogo acha os assets mesmo se for aberto a partir de outra pasta.
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_IMG = os.path.join(PASTA_BASE, 'assets', 'img')
PASTA_SND = os.path.join(PASTA_BASE, 'assets', 'snd')
PASTA_FONT = os.path.join(PASTA_BASE, 'assets', 'font')
ARQUIVO_RECORDE = os.path.join(PASTA_BASE, 'recorde.txt')

# Cores (R, G, B) 
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AMARELO = (255, 210, 0)
VERMELHO = (220, 40, 40)
CINZA = (60, 60, 70)

# Física do jogador
GRAVIDADE = 0.5      # quanto a velocidade para baixo aumenta a cada quadro
EMPURRAO = 0.9       # quanto o jetpack empurra para cima a cada quadro
VEL_MAX = 10         # velocidade vertical máxima (para cima ou para baixo)
CHAO_Y = ALTURA - 60  # altura (y) do chão
TETO_Y = 20          # altura (y) do teto
JOGADOR_X = 150      # o jogador fica sempre nesta posição x

#  Regras 
VIDAS_INICIAIS = 3
TEMPO_INVENCIVEL = 1500   # milissegundos piscando depois de uma batida (jogador fica imune a qualqer coisa)
PIXELS_POR_METRO = 20     # quantos pixels andados valem 1 metro
PONTOS_CAFE = 10
TEMPO_AVISO_MISSIL = 1000  # milissegundos de aviso antes do pombo-míssil
VEL_MISSIL = 12            # velocidade extra do pombo-míssil
ACELERACAO_NOITE = 1       # na noite(fase 3), +1 de velocidade a cada 500 m

#  Fases 
# Cada fase é um dicionário. 'inicio' = a partir de quantos metros ela começa.
FASES = [
    {'nome': 'MANHÃ', 'inicio': 0, 'velocidade': 6, 'ceu': (135, 206, 235),
     'misseis': False, 'drones_moveis': False, 'intervalo_drone': (1200, 2000)},
    {'nome': 'TARDE', 'inicio': 500, 'velocidade': 8, 'ceu': (245, 165, 95),
     'misseis': True, 'drones_moveis': False, 'intervalo_drone': (1000, 1700)},
    {'nome': 'NOITE', 'inicio': 1500, 'velocidade': 10, 'ceu': (25, 25, 60),
     'misseis': True, 'drones_moveis': True, 'intervalo_drone': (800, 1400)},
]

# Estados (telas)
INICIO = 'inicio'
INSTRUCOES = 'instrucoes'
JOGANDO = 'jogando'
GAME_OVER = 'game_over'
SAIR = 'sair'

# ---------- Patinete ----------
VEL_PATINETE = 5               # velocidade extra do patinete (o pombo usa 12)
FAIXA_PATINETE = CHAO_Y - 56   # abaixo desta altura é a calçada: só patinetes passam ali
