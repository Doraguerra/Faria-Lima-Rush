"""Leitura e gravação do recorde num arquivo de texto."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import os
from config import ARQUIVO_RECORDE


# [NÍVEL: FÁCIL] — open/read, como na aula de arquivos.
def ler_recorde():
    """Devolve o recorde salvo, ou 0 se ainda não houver arquivo."""
    if not os.path.exists(ARQUIVO_RECORDE):
        return 0
    with open(ARQUIVO_RECORDE, 'r') as arquivo:
        conteudo = arquivo.read().strip()
    if conteudo.isdigit():
        return int(conteudo)
    return 0  # arquivo vazio ou estragado


# [NÍVEL: FÁCIL]
def salvar_recorde(pontos):
    """Grava o novo recorde no arquivo (apaga o anterior)."""
    with open(ARQUIVO_RECORDE, 'w') as arquivo:
        arquivo.write(str(pontos))
