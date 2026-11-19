"""Gerador: decide quando cada obstáculo e item aparece."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import random
import pygame
from config import LARGURA, TETO_Y, CHAO_Y
from sprites import Drone
from sprites import Item


# [NÍVEL: DIFÍCIL] — temporizadores com get_ticks() (mesma ideia do limite
# de tiros do jogo_v16 do tutorial), agora para vários tipos de objeto.
class Gerador:
    """Guarda o instante em que cada tipo de objeto deve nascer."""

    def __init__(self, assets):
        """Marca os primeiros horários de nascimento (em milissegundos)."""
        self.assets = assets
        agora = pygame.time.get_ticks()
        self.proximo_drone = agora + 1500
        self.proximo_cafe = agora + 2500

    def atualizar(self, fase, jogador, grupos):
        """Cria os objetos cujo horário chegou e sorteia o próximo horário."""
        agora = pygame.time.get_ticks()
        if agora >= self.proximo_drone:
            movel = fase['drones_moveis'] and random.random() < 0.5
            drone = Drone(self.assets['drone'], movel)
            grupos['todos'].add(drone)
            grupos['obstaculos'].add(drone)
            minimo, maximo = fase['intervalo_drone']
            self.proximo_drone = agora + random.randint(minimo, maximo)
        if agora >= self.proximo_cafe:
            self.criar_fileira_de_cafes(grupos)
            self.proximo_cafe = agora + random.randint(3000, 5000)

    def criar_fileira_de_cafes(self, grupos):
        """Cria 5 cafés em fila, numa altura sorteada."""
        y = random.randint(TETO_Y + 20, CHAO_Y - 60)
        for i in range(5):
            cafe = Item(self.assets['cafe'], 'cafe', LARGURA + i * 50, y)
            grupos['todos'].add(cafe)
            grupos['itens'].add(cafe)
