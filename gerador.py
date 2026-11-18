"""Gerador: decide quando cada obstáculo e item aparece."""
# Código gerado com IA (Claude, da Anthropic) — ver a seção "Uso de IA" no README.
import random
import pygame
from sprites import Drone


# [NÍVEL: DIFÍCIL] — temporizadores com get_ticks() (mesma ideia do limite
# de tiros do jogo_v16 do tutorial), agora para vários tipos de objeto.
class Gerador:
    """Guarda o instante em que cada tipo de objeto deve nascer."""

    def __init__(self, assets):
        """Marca os primeiros horários de nascimento (em milissegundos)."""
        self.assets = assets
        agora = pygame.time.get_ticks()
        self.proximo_drone = agora + 1500

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
